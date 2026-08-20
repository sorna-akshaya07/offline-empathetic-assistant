from pydoc import text
from unittest import result
import wave
import json
import queue
import ollama
import sounddevice as sd
import time
import config
import uuid
from datetime import datetime

from safetyvalidator import validate_response
from safetyvalidator import is_unsafe
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
from playsound import playsound

# ---------------------------------------------------------
# STEP 1: Load Piper Voice (Offline TTS)
# ---------------------------------------------------------

voice = PiperVoice.load(config.VOICE_MODEL_PATH)

# ---------------------------------------------------------
# STEP 2: Load Offline Speech Recognition (Vosk)
# ---------------------------------------------------------

model = Model(config.VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetWords(True)
audio_queue = queue.Queue()

# ---------------------------------------------------------
# STEP 3: Initialize Session and Conversation Memory
# ---------------------------------------------------------

session_id = str(uuid.uuid4())
session_history = []
conversation_history = []
turn_index = 0

# ---------------------------------------------------------
# STEP 4: Microphone Audio Callback
# ---------------------------------------------------------

def callback(indata, frames, time, status):
    if status:
        print(status)

    audio_queue.put(bytes(indata))
# ---------------------------------------------------------
# STEP 5: Capture Speech Using Vosk with Confidence Checking
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

                # Get word-level confidence
                words = result.get("result", [])

                if words:
                    confidence = sum(
                        word.get("conf", 0)
                        for word in words
                    ) / len(words)
                else:
                    confidence = 0.0

                # STT confidence check
                if confidence < config.STT_CONFIDENCE_THRESHOLD:
                    print("⚠️ Speech was unclear. Please repeat.")
                    continue

                if text:
                    print(f"You: {text}")
                    return text

            

# ---------------------------------------------------------
# STEP 6: Get Response from Local LLM
# ---------------------------------------------------------

def get_llm_response(user_text: str) -> str:
    """Generate an empathetic response using the local LLM."""

    global turn_index

    # ---------------------------------------------------------
    # Check User Input for Unsafe Requests
    # ---------------------------------------------------------

    if is_unsafe(user_text):
        safe_response = (
            "I'm sorry, but I can't help with that. "
            "I'm here to support you in a safe way."
        )

        print(f"Sundae: {safe_response}")
        return safe_response


    turn_index += 1

    # ---------------------------------------------------------
    # Store User Turn in Session History
    # ---------------------------------------------------------

    session_history.append({
        "session_id": session_id,
        "turn_index": turn_index,
        "timestamp": datetime.now().isoformat(),
        "speaker": "user",
        "content": user_text
    })

    # ---------------------------------------------------------
    # Add User Message to Conversation History
    # ---------------------------------------------------------

    conversation_history.append({
        "role": "user",
        "content": user_text
    })

    # ---------------------------------------------------------
    # Generate Response Using the Configured Local LLM
    # ---------------------------------------------------------

    response = ollama.chat(
        model=config.LOCAL_MODEL_NAME,
        messages=[
            {"role": "system", "content": config.SYSTEM_PROMPT},
            *conversation_history
        ],
        options={
            "temperature": config.TEMPERATURE,
            "top_p": config.TOP_P,
            "top_k": config.TOP_K,
            "num_ctx": config.NUM_CTX,
            "num_predict": config.NUM_PREDICT,
        }
    )

    reply = response["message"]["content"].strip()

    # ---------------------------------------------------------
    # Validate Generated Response Using SafetyValidator
    # ---------------------------------------------------------

    reply = validate_response(reply)

    # ---------------------------------------------------------
    # Store Assistant Turn in Session History
    # ---------------------------------------------------------

    turn_index += 1

    session_history.append({
        "session_id": session_id,
        "turn_index": turn_index,
        "timestamp": datetime.now().isoformat(),
        "speaker": "assistant",
        "content": reply
    })

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })


    # ---------------------------------------------------------
    # Keep Only the Most Recent Conversation Messages
    # ---------------------------------------------------------

    if len(conversation_history) > config.MAX_HISTORY_MESSAGES:
        conversation_history[:] = conversation_history[
            -config.MAX_HISTORY_MESSAGES:
        ]

    print(f"Sundae: {reply}")

    return reply
# ---------------------------------------------------------
# STEP 7: Convert LLM Response to Speech Using Piper
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
# STEP 8: Run the Complete Offline Conversation Pipeline
# ---------------------------------------------------------

def sundae_respond(output_path: str = "response.wav"):
    global turn_index

    # Listen through microphone
    user_text = listen()

    # Handle Empty Speech Input
    if not user_text:
        return True
    
    # Reset Session When the User Starts a New Conversation
    if user_text.lower() in ["new conversation", "start over","reset conversation"]:
        conversation_history.clear()
        session_history.clear()
        turn_index = 0
        print("New Conversation started")
        return True
    
    # Exit the Application Using a Voice Command
    if user_text.lower() in ["exit", "quit", "goodbye", "stop"]:
        print("Goodbye! Take care.")
        return False

    # Measure Local LLM Response Latency
    start_time = time.time()
    reply_text = get_llm_response(user_text)
    end_time = time.time()
    latency = end_time - start_time
    print(f"LLM Latency: {latency:.2f}seconds")

    # Validate Response Before Sending It to TTS
    if not reply_text or not reply_text.strip():
        print("No valid response generated by the LLM. Waiting for the next input...")
        return True

    # Convert Response to Speech and Play Audio
    speak(reply_text, output_path)

    # Automatically play the generated audio
    print("🔊 Playing response...\n")
    playsound(output_path)

    return True


# ---------------------------------------------------------
# STEP 9: Start the Sundae Doll Offline AI Companion
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("      Sundae Doll - Offline AI Companion")
    print("=" * 60)
    print("🎤 Speak through the microphone.")
    print(f"🦙 Local LLM : {config.LOCAL_MODEL_NAME}")
    print("🗣️ Piper TTS")
    print("🔊 Audio Playback : Automatic")
    print("🌐 Internet : Not Required")
    print("Say 'exit' or 'quit' to stop.\n")


    # Generate Unique Output File Names for Each Response
    counter = 1

    while True:

        model_name = config.LOCAL_MODEL_NAME.replace(":", "_")
        output_file = f"sundae_offline_{model_name}_{counter}.wav"
        

        continue_chat = sundae_respond(output_file)

        if not continue_chat:
            break

        counter += 1