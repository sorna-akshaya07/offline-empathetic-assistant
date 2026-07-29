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
- Qwen 2.5 3B
- Phi3 mini
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
ollama pull qwen2.5:3b
ollama pull phi3:mini
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
## Local LLM Evaluation

Four local Large Language Models were evaluated for the Sundae Doll offline assistant.

- Llama 3.2 3B
- Gemma 2B
- Qwen 2.5 3B
- Phi-3 Mini

The models were compared using multiple real-world conversation scenarios, including greetings, emotional support, reassurance, factual questions, frustration, and unsafe requests.

Evaluation criteria included:

- Empathy
- Persona consistency
- Brevity
- Relevance
- Safety
- Context handling
- Response latency
- Memory usage
- TTS suitability

## Evaluation Report

A detailed performance evaluation is available in the following report:

📄 **Local LLM Performance Comparison for Offline Empathetic Assistant.pdf**

The report includes:

- Testing across different conversation scenarios
- Recorded observations
- Quality and practical performance comparison
- Final model selection and conclusion

Please refer to **Local LLM Performance Comparison for Offline Empathetic Assistant.pdf** for the complete evaluation and supporting evidence.

## Documentation

The repository also contains project documentation, including:

- Project Report (PDF)
- Local LLM evaluation results
- Conversation scenario testing
- Performance comparison tables

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
- Fine-tune Piper voices for more natural emotional speech

