## Overview

This project is an offline AI companion prototype for the Sundae Doll. It integrates multiple local Large Language Models (Llama 3.2 3B, Gemma 2B, Qwen 2.5 3B, and Phi-3 Mini), offline speech recognition using Vosk, and Piper Text-to-Speech (TTS) to provide natural, empathetic, and safe voice interactions without requiring an internet connection.

## Features

- Fully offline AI companion
- Supports Llama 3.2 3B, Gemma 2B, Qwen 2.5 3B, and Phi-3 Mini via Ollama
- Offline Speech-to-Text using Vosk
- Offline Text-to-Speech using Piper
- Automatic audio playback
- Empathetic conversational responses
- Minimal session memory for follow-up conversations
- Improved safety handling for harmful requests
- Automatic latency measurement
- Automatic voice response generation

## Work Flow
Microphone
      ↓
Vosk Speech Recognition
      ↓
Local LLM (Llama / Gemma / Qwen / Phi)
      ↓
Safety Validation
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
python test_qwen.py
python test_phi.py
python offline_llms_runner.py
```

---
## Output Files

sundae_offline_gemma.wav 
sundae_offline_llama.wav 
sundae_offline_qwen.wav 
sundae_offline_phi.wav 

## Switching Between Local LLM Models

The offline_llms_runner.py file is a common runner for all four local LLMs (Llama 3.2 3B, Gemma 2B, Qwen 2.5 3B, and Phi-3 Mini). The model can be switched by changing only the LOCAL_MODEL_NAME value in this file. The remaining conversation, safety, memory, and TTS logic remains unchanged.



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

## Recent Improvements

### High Priority
- Improved prompt engineering
- Added minimal session memory
- Improved safety handling

### Medium Priority
- Consolidated repeated logic
- Replaced model-specific scripts
- Added better response validation

### Low Priority
- Added realistic conversation testing
- Extended prompt comparison
- Expanded model comparison process

## Evaluation Report

The repository includes the following evaluation documents:

- 📄 Local LLM Performance Comparison for Offline Empathetic Assistant.pdf
- 📄 Piper Offline Empathetic Assistant Recordings.pdf

These documents include:

- 22 conversation scenario evaluations
- Model-wise response comparisons
- Latency measurements
- Failure and degradation observations
- Audio recording references
- Final performance analysis

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

