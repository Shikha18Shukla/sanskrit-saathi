\# 🪷 Sanskrit Saathi



> An AI-powered Sanskrit study companion built for BAMS students.



Sanskrit Saathi helps students understand Sanskrit text through simple English and Hindi explanations, accurate IAST transliteration, word-by-word breakdowns, and interactive quizzes.



It includes a dedicated \*\*BAMS Sanskrit mode\*\* that provides Ayurveda-focused context when relevant.



\## ✨ Features



\- 📜 Sanskrit text explanation

\- 🔤 Accurate IAST transliteration

\- 🇬🇧 Simple English meaning

\- 🇮🇳 Simple Hindi meaning

\- 🧩 Word-by-word breakdown

\- 📚 Context and usage

\- 🪷 BAMS Sanskrit study mode

\- 🌿 General Sanskrit study mode

\- 🧠 AI-generated quizzes

\- 🔒 Local AI inference using an open-weight model



\## 🤖 AI



Sanskrit Saathi uses \*\*Gemma 3 4B\*\* through \*\*Ollama\*\*.



The AI model runs locally on the user's computer rather than sending Sanskrit text to a cloud AI service.



\## 🛠️ Tech Stack



\- Python

\- Flask

\- HTML

\- CSS

\- JavaScript

\- Ollama

\- Gemma 3 4B

\- indic-transliteration



\## 🚀 Run Locally



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd sanskrit-saathi



2\. Create a virtual environment

python -m venv venv

3\. Activate the virtual environment



Windows:



.\\venv\\Scripts\\activate

4\. Install dependencies

pip install -r requirements.txt

5\. Install Ollama



Install Ollama and make sure it is running.



Then download Gemma 3 4B:



ollama pull gemma3:4b

6\. Start Sanskrit Saathi

python app.py



Open the application at:



http://127.0.0.1:5000

🏗️ Architecture

User

&#x20; ↓

Sanskrit Saathi Web UI

&#x20; ↓

Flask Backend

&#x20; ↓

Ollama

&#x20; ↓

Gemma 3 4B

&#x20; ↓

Flask

&#x20; ↓

Explanation / Quiz



IAST transliteration is generated using the indic-transliteration library.



🌱 Why Local AI?



Sanskrit Saathi uses an open-weight model locally through Ollama.



This makes it possible to:



Learn without depending on a paid AI API

Keep submitted Sanskrit text on the user's computer

Experiment with different open models

Run the application without sending requests to a hosted AI provider

💡 Why I Built It



Sanskrit can be a difficult part of BAMS for students who do not have a strong Sanskrit background.



Sanskrit Saathi was built for a friend studying BAMS who struggled with understanding Sanskrit course material.



The goal was simple:



Make Sanskrit easier to understand while keeping the learning experience beginner-friendly and relevant to BAMS.



⚠️ Disclaimer



Sanskrit Saathi is a language-learning tool and not a substitute for a Sanskrit teacher, textbook, or qualified medical professional.



Ayurvedic context provided by the application should be verified with appropriate academic sources and teachers.



📌 Project Status



MVP completed and tested with a BAMS student.





After pasting and saving it, run:



```powershell

git status

