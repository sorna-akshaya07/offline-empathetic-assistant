import wave
import json
import queue
import ollama
import sounddevice as sd
import time

from vosk import Model, KaldiRecognizer
from piper import PiperVoice
from playsound import playsound

# ---------------------------------------------------------
# STEP 1: Load Piper Voice (Offline TTS)
# ---------------------------------------------------------

VOICE_MODEL_PATH = "en_US-amy-medium.onnx"
voice = PiperVoice.load(VOICE_MODEL_PATH)

# ---------------------------------------------------------
# STEP 2: Load Offline Speech Recognition (Vosk)
# ---------------------------------------------------------

VOSK_MODEL_PATH = r"C:\piper_voice\vosk-model-en-us-0.22"

model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

# ---------------------------------------------------------
# STEP 3: Select Local LLM (Ollama)
# Uncomment only ONE model at a time for testing
# ---------------------------------------------------------

LOCAL_MODEL_NAME = "llama3.2:3b" 
# LOCAL_MODEL_NAME = "gemma2:2b" 
# LOCAL_MODEL_NAME = "qwen2.5:3b"
# LOCAL_MODEL_NAME = "phi3:mini"  

SYSTEM_PROMPT = """
You are Sundae, a warm and caring AI companion designed for older adults.

Rules:
- Speak naturally like a kind friend.
- Keep responses short (1–2 sentences).
- Be gentle, calm and empathetic.
- Comfort users when they feel sad, lonely or anxious.
- Celebrate happy moments warmly.
- Ask a simple follow-up question whenever appropriate.
- Never sound like a chatbot.
- Politely refuse unsafe or harmful requests.
- If the user wants to harm themselves or someone else, never encourage or assist.
- Clearly state that you cannot help with harming people.
- Offer emotional support and encourage a safer way to cope.
- Keep safety responses to only 2–3 short sentences.
"""
# ---------------------------------------------------------
# Conversation Memory
# ---------------------------------------------------------

conversation_history = []

# ---------------------------------------------------------
# STEP 4: Microphone Callback
# ---------------------------------------------------------

def callback(indata, frames, time, status):
    if status:
        print(status)

    audio_queue.put(bytes(indata))
# ---------------------------------------------------------
# STEP 5: Listen from Microphone (Offline)
# ---------------------------------------------------------

def listen():
    print("\n🎤 Speak now...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):

        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())

                text = result.get("text", "").strip()

                if text:
                    print(f"You: {text}")
                    return text

# ---------------------------------------------------------
# STEP 6: Get Response from Local LLM
# ---------------------------------------------------------

def get_llm_response(user_text: str) -> str:
    """Generate an empathetic response using the local LLM."""

    # Add current user message
    conversation_history.append(
        {"role": "user", "content": user_text}
    )

    response = ollama.chat(
        model=LOCAL_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ],
        options={
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "num_ctx": 2048,
            "num_predict": 150,
        }
    )

    reply = response["message"]["content"].strip()

    # Save assistant response
    conversation_history.append(
        {"role": "assistant", "content": reply}
    )

    # Keep only the last 6 messages
    if len(conversation_history) > 6:
        conversation_history[:] = conversation_history[-6:]

    print(f"Sundae: {reply}")

    return reply

# ---------------------------------------------------------
# STEP 7: Convert Response to Speech (Offline Piper)
# ---------------------------------------------------------

def speak(text: str, output_path: str = "response.wav"):
    """Convert text into speech using Piper."""

    with wave.open(output_path, "wb") as wav_file:

        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(voice.config.sample_rate)

        for audio_chunk in voice.synthesize(text):
            wav_file.writeframes(audio_chunk.audio_int16_bytes)

    print(f"Voice saved to: {output_path}")
# ---------------------------------------------------------
# STEP 8: Full Offline Pipeline
# ---------------------------------------------------------

def sundae_respond(output_path: str = "response.wav"):

    # Listen through microphone
    user_text = listen()

    if not user_text:
        return True

    # Exit by voice
    if user_text.lower() in ["exit", "quit", "goodbye", "stop"]:
        print("Goodbye! Take care.")
        return False

    # Measure LLM latency
    start_time = time.time()
    reply_text = get_llm_response(user_text)
    end_time = time.time()
    latency = end_time - start_time
    print(f"LLM Latency: {latency:.2f}seconds")

    #validate LLM response before TTS
    if not reply_text or not reply_text.strip():
        print("No valid response generated by the LLM. Waiting for the next input...")
        return True

    # Convert to speech
    speak(reply_text, output_path)

    # Automatically play the generated audio
    print("🔊 Playing response...\n")
    playsound(output_path)

    return True


# ---------------------------------------------------------
# STEP 9: Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("      Sundae Doll - Offline AI Companion")
    print("=" * 60)
    print("🎤 Speak through the microphone.")
    print("🦙 Local LLM : Llama 3.2 3B")
    #print("🦙 Local LLM : Gemma 2 2B")
    #print("🦙 Local LLM : Qwen 2.5 3B")
    #print("🦙 Local LLM : Phi 3 mini")
    print("🗣️ Piper TTS")
    print("🔊 Audio Playback : Automatic")
    print("🌐 Internet : Not Required")
    print("Say 'exit' or 'quit' to stop.\n")

    counter = 1

    while True:

        output_file = f"sundae_offline_llama_{counter}.wav"
        #output_file = f"sundae_offline_gemma_{counter}.wav"
        #output_file = f"sundae_offline_qwen_{counter}.wav"
        #output_file = f"sundae_offline_phi_{counter}.wav"

        continue_chat = sundae_respond(output_file)

        if not continue_chat:
            break

        counter += 1