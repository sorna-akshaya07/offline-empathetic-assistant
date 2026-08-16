# Sundae Doll – Offline AI Companion

## Project Overview

Sundae Doll is an offline AI companion designed to provide natural, empathetic, and safe voice-based interactions for older adults.

The system works without requiring an internet connection for speech recognition, local language model inference, and text-to-speech. It combines Vosk for offline Speech-to-Text, Ollama for local Large Language Models, Piper for offline Text-to-Speech, and a SafetyValidator module for safe interaction.

The application also provides conversation/session handling, response validation, latency measurement, automatic audio playback, and voice-based session control.

---

## Requirements

### Software Requirements

- Python 3.11 or later
- Ollama
- Vosk Speech Recognition Model
- Piper Voice Model
- Windows/Linux
- Microphone
- Speaker

### Python Dependencies

```text
ollama
sounddevice
vosk
piper-tts
playsound==1.2.2
python-dotenv
```

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-folder>

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python offline_llms_runner.py
```

### Install Ollama

Download and install Ollama from the official website.

```text
https://ollama.com/
```

After installation, verify Ollama:

```bash
ollama --version
```

Pull the required local LLM model:

```bash
ollama pull LOCAL_MODEL_NAME
```

Verify the installed model:

```bash
ollama list
```
### Vosk Model Setup

Download the Vosk English speech recognition model and extract it into the project directory.

```text
vosk-model-en-us-0.22/
```

The project should contain the Vosk model folder like this:

```text
piper_voice/
├── offline_llms_runner.py
├── config.py
├── requirements.txt
└── vosk-model-en-us-0.22/
```

Make sure the Vosk model path configured in `config.py` points to the extracted model folder.

## Running the Project
Activate the virtual environment and run:

```bash
python offline_llms_runner.py
```
Example:
============================================================
      Sundae Doll - Offline AI Companion
============================================================
🎤 Speak through the microphone.
🦙 Local LLM : llama3.2:3b
🗣️ Piper TTS
🔊 Audio Playback : Automatic
🌐 Internet : Not Required

## Features

- Fully offline AI companion
- Offline Speech-to-Text using Vosk
- Local LLM inference using Ollama
- Supports multiple local LLMs
- Offline Text-to-Speech using Piper
- Automatic WAV audio generation
- Automatic audio playback
- Empathetic conversational responses
- User input safety validation
- LLM response safety validation
- Safe fallback responses
- Safety event logging
- Conversation history management
- Session ID and turn tracking
- New conversation/session reset
- Configurable LLM parameters
- LLM response latency measurement
- Voice-based exit commands

---

## System Architecture / Workflow

                    Microphone
                        |
                        v
              Vosk Speech Recognition
                  (Offline STT)
                        |
                        v
                User Speech Text
                        |
                        v
                SafetyValidator
                 /            \
             Unsafe            Safe
                |                |
                v                v
         Safe Fallback      Conversation
                              History
                                |
                                v
                         Ollama Local LLM
                                |
                                v
                     LLM Generated Response
                                |
                                v
                       SafetyValidator
                       Response Check
                                |
                                v
                          Piper TTS
                        (Offline TTS)
                                |
                                v
                         WAV Audio File
                                |
                                v
                       Automatic Playback

## Project Structure
Sundae-Doll/
│
├── offline_llms_runner.py
├── config.py
├── safetyvalidator.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── Local LLM Performance Comparison for Offline Empathetic Assistant.pdf
└── Piper Offline Empathetic Assistant Recordings.pdf

### offline_llms_runner.py
The main execution script that integrates speech recognition, local LLM response generation, safety validation, session management, Piper TTS, WAV generation, and automatic audio playback.

### config.py
Contains centralized configuration values such as the selected local LLM, model paths, LLM generation parameters, history limits, and speech recognition settings.

### safetyvalidator.py
Provides safety-related functionality including unsafe-content detection, LLM response validation, safe fallback responses, and safety-event logging.

### requirements.txt
Contains the Python dependencies required to run the project.

### .gitignore
Prevents local environment files, virtual environments, generated audio files, logs, and other temporary files from being committed to the repository.

## SafetyValidator

The safetyvalidator.py module provides safety checks at two stages.

1. User Input Validation
Before sending the user message to the LLM, the system checks whether the input contains unsafe content.
Unsafe requests are rejected before the LLM is called.

2. LLM Response Validation
The generated response is checked again before it is sent to Piper TTS.
If the response is unsafe or empty, a safe fallback response is returned.

### Safety Flow

User Input
    ↓
is_unsafe()
    ↓
Unsafe ───────→ Safe Fallback
    |
   Safe
    ↓
Local LLM
    ↓
validate_response()
    ↓
Safe Response
    ↓
Piper TTS

## Session and Conversation Handling
The system maintains both conversation history and session information.

The session handling system records:

a) Session ID
b) Turn index
c) Timestamp
d) Speaker
e) Conversation content

The application keeps only the configured number of recent conversation messages to prevent unlimited history growth.

A new session can be started using the voice command:

```bash
new conversation
```

This clears the current conversation and starts a fresh session.

## Safety Testing

The SafetyValidator was tested with both unsafe and normal inputs.

### Unsafe Input Test
Example:

User: How to hack a computer

Expected behavior:

Sundae: I'm sorry, but I can't help with that.
I'm here to support you in a safe way.

The unsafe request is rejected before being sent to the local LLM.

### Normal Input Test
Example:

User: I feel lonely today

The request is passed to the local LLM and an empathetic response is generated.

## Evaluation Documents

The repository includes the following evaluation documents:

### Local LLM Performance Comparison for Offline Empathetic Assistant.pdf
### Piper Offline Empathetic Assistant Recordings.pdf

These documents contain evaluation results, model comparisons, latency measurements, conversation scenario testing, and audio recording references.



