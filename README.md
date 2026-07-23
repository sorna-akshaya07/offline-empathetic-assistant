## Overview

This project is an offline AI companion prototype for the Sundae Doll. It integrates local Large Language Models (Llama 3.2 3B and Gemma 2B), offline speech recognition using Vosk, and Piper Text-to-Speech (TTS) to provide natural and empathetic voice interactions without requiring an internet connection.

## Features

- Fully offline AI companion
- Supports Llama 3.2 3B and Gemma 2B via Ollama
- Offline Speech-to-Text using Vosk
- Offline Text-to-Speech using Piper
- Automatic audio playback
- Empathetic conversational responses
- Safe handling of harmful requests
- Automatic voice response generation

## Project Workflow

Microphone
      ↓
Vosk Speech Recognition
      ↓
Llama 3.2 3B / Gemma 2B
      ↓
Empathetic Response
      ↓
Piper TTS
      ↓
Automatic Audio Playback

## Technologies Used

- Python 3.11
- Ollama
- Llama 3.2 3B
- Gemma 2B
- Piper TTS
- Vosk Speech Recognition
- Hugging Face (Piper Voice Model)

## Requirements

- Python 3.11 or later
- Ollama
- Piper Voice Model
- Windows/Linux
- Vosk Speech Recognition Model

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Install Ollama

Download and install Ollama from

https://ollama.com/download

Download the Gemma model

```bash
ollama pull gemma2:2b
ollama pull llama3.2:3b
pip install ollama piper-tts vosk sounddevice playsound==1.2.2
```

## Download Piper Voice

Download the following files from the Hugging Face Piper Voices repository.

- en_US-amy-medium.onnx
- en_US-amy-medium.onnx.json

Place both files inside the project folder.


## Download Vosk 

vosk-model-small-en-us-0.22

Extract the folder and place it inside:

C:\piper_voice\

## Running the Project

Start the Ollama server

```bash
ollama serve
```

Open another terminal

```bash
python test_llama.py
python test_gemma.py
```

---

## Example

Input

```
You: I am feeling sad today.
```

Output

```
Sundae:
I'm sorry you're feeling sad. I'm here with you. Tomorrow is a new day.
```

A speech file will also be generated.

```
sundae_offline_gemma_1.wav
sundae_offline_llama_1.wav
```

---

## Current Limitation

- Piper voice sounds little robotic.
- The prototype currently supports English only.



## Future Improvements

- Better speech recognition
- Higher quality emotional voices
- Additional local LLM comparison
- Conversation memory
- Emotion-aware responses

