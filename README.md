

## Overview

This project is an offline AI companion prototype for the Sundae Doll. It combines a local Large Language Model (LLM) with Piper Text-to-Speech (TTS) to generate empathetic responses and convert them into speech without requiring an internet connection.

---

## Features

- Fully offline conversation
- Local LLM using Gemma 2 (2B) via Ollama
- Offline speech synthesis using Piper TTS
- Generates empathetic responses
- Converts responses into speech (.wav)

---

## Project Workflow

```
User Input
      ↓
Gemma 2 (2B) - Ollama
      ↓
Empathetic Text Response
      ↓
Piper TTS
      ↓
Speech Output (.wav)
```

---

## Technologies Used

- Python 3.11
- Ollama
- Gemma 2 (2B)
- Piper TTS
- Hugging Face (Piper Voice Model)

---

## Requirements

- Python 3.11 or later
- Ollama
- Piper Voice Model
- Windows/Linux

---

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

---

## Install Ollama

Download and install Ollama from

https://ollama.com/download

Download the Gemma model

```bash
ollama pull gemma2:2b
```

---

## Download Piper Voice

Download the following files from the Hugging Face Piper Voices repository.

- en_US-amy-medium.onnx
- en_US-amy-medium.onnx.json

Place both files inside the project folder.

---

## Running the Project

Start the Ollama server

```bash
ollama serve
```

Open another terminal

```bash
python test.py
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
sundae_offline_response_1.wav
```

---

## Current Limitation

- Piper voice sounds robotic.
- It does not express emotions such as happiness, sadness, empathy, or concern.
- Future work includes exploring emotional speech synthesis and fine-tuning Piper for more natural speech.

---

## Future Improvements

- Emotional voice generation
- Fine-tuned Piper models
- Voice cloning
- Microphone input (Speech-to-Text)
- Real-time conversation
- Emotion detection from user input

---

