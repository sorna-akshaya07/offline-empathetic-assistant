import wave
import ollama
from piper import PiperVoice

# ---------------------------------------------------------
# STEP 1: Load the Piper voice (runs fully offline)
# ---------------------------------------------------------
VOICE_MODEL_PATH = "en_US-amy-medium.onnx"
voice = PiperVoice.load(VOICE_MODEL_PATH)

# ---------------------------------------------------------
# STEP 2: Local LLM settings (runs fully offline via Ollama)
# ---------------------------------------------------------
LOCAL_MODEL_NAME = "gemma2:2b"  # small Google Gemma 2 model, good for offline/on-device use

SYSTEM_PROMPT = (
    "You are Sundae, a warm, caring companion doll for an older adult. "
    "Always respond with short, gentle, empathetic sentences. "
    "If the user expresses sadness, pain, or distress, respond with comfort "
    "and reassurance, like a caring friend. Keep responses to 1-2 sentences."
)


def get_llm_response(user_text: str) -> str:
    """Get an empathetic reply from the LOCAL LLM (no internet needed)."""
    response = ollama.chat(
        model=LOCAL_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return response["message"]["content"].strip()


# ---------------------------------------------------------
# STEP 3: Convert the LLM's reply into speech using Piper (offline)
# ---------------------------------------------------------
def speak(text: str, output_path: str = "response.wav"):
    """Generate a .wav voice file from text using the Piper voice."""
    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(voice.config.sample_rate)

        for audio_chunk in voice.synthesize(text):
            wav_file.writeframes(audio_chunk.audio_int16_bytes)

    print(f"Voice saved to: {output_path}")


# ---------------------------------------------------------
# STEP 4: Full offline pipeline
# ---------------------------------------------------------
def sundae_respond(user_text: str, output_path: str = "response.wav"):
    print(f"User said: {user_text}")
    reply_text = get_llm_response(user_text)
    print(f"Sundae's reply: {reply_text}")
    speak(reply_text, output_path)
    return reply_text


# ---------------------------------------------------------
# Interactive mode - type your own messages, works with NO internet
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== Sundae Doll - OFFLINE Interactive Mode ===")
    print("(No internet needed - LLM and voice both run locally)")
    print("Type how you're feeling, and Sundae will respond with voice.")
    print("Type 'exit' or 'quit' to stop.\n")

    counter = 1
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye! Take care.")
            break

        if not user_input:
            continue

        output_file = f"sundae_offline_response_{counter}.wav"
        sundae_respond(user_input, output_path=output_file)
        print()
        counter += 1