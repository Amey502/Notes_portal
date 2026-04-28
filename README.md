# Notes Sharing Portal with build in AI-Summarizers and Chatbot

## Overview

This project is an AI-powered collaborative learning platform built using Django. It allows users to create teams, share notes and PDFs, interact through comments and likes, and leverage AI features such as automatic summarization and a context-aware chatbot.

The system integrates Natural Language Processing (NLP) techniques and a locally hosted Large Language Model (LLM) to enhance learning and collaboration.

---

## Features

### Team Management

* Create and join teams
* Each team acts as a private workspace

### Posts & Content Sharing

* Create posts with text and optional PDF uploads
* View and download PDFs
* Edit and delete posts

### Interaction

* Like posts
* Comment on posts

### AI Summarization

* Automatically generates summaries for posts
* Extracts text from:

  * Normal PDFs
  * Scanned PDFs (using OCR)
* Handles large text using chunking

### Chatbot (AI Assistant)

* Ask questions related to team content
* Uses context from recent posts
* Powered by a locally running LLM via Ollama

### Search & Sorting

* Search posts by title or user
* Sort posts by likes or latest

### Admin Panel

* Manage teams, posts, and comments
* Filter and search functionality

---

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (default Django DB)
* **AI/NLP:**

  * Transformers (Hugging Face)
  * PyTorch
* **PDF Processing:**

  * PyMuPDF (fitz)
* **OCR:**

  * Tesseract OCR
* **LLM Integration:**

  * Ollama (local model inference)

---

## Installation & Setup

### 1️. Clone the repository

```bash
git clone <your-repo-link>
cd <project-folder>
```

---

### 2️. Create and activate conda environment

```bash
conda create -n ai_project python=3.10
conda activate ai_project
```

---

### 3️. Install required libraries

```bash
pip install -r libraries.txt
```

---

### 4️. Install Tesseract OCR (Manual Step)

Tesseract is **not available via pip**, so install it manually:

#### Windows:

1. Download from: https://github.com/tesseract-ocr/tesseract
2. Install it (default path recommended):

   ```
   C:\Program Files\Tesseract-OCR\
   ```
3. Add this in your Python code (already done in project):

   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\TesseractOCR\\tesseract.exe"
   ```

---

### 5️. Install and Run Ollama

#### Install Ollama:

  https://ollama.com

#### Pull model:

```bash
ollama run llama3
```

#### Start Ollama server:

```bash
ollama serve
```

---

### 6️. Run Django Server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## How It Works

### AI Summarization Flow

1. User uploads post/PDF
2. Text is extracted (OCR if needed)
3. Text is cleaned and split into chunks
4. Transformer model generates summaries
5. Final summary is stored and displayed

---

### Chatbot Flow

1. User asks a question
2. Backend fetches relevant team posts
3. Context is built
4. Sent to local LLM via Ollama
5. Response returned to UI

---

## Notes

* Ensure **Ollama is running** before using chatbot
* Large PDFs may take time to process
* OCR is used only for scanned documents

---

## Future Improvements

* Add embeddings for better context retrieval (RAG)
* Improve chatbot UI
* Deploy using cloud infrastructure

---

## Author

Ameya Singh
