from flask import Flask, render_template, request, jsonify
import requests

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def get_study_mode(data):
    mode = data.get("study_mode", "general")

    if not isinstance(mode, str):
        return "general"

    mode = mode.strip().lower()

    if mode not in ["general", "bams"]:
        mode = "general"

    return mode


def get_mode_instructions(mode):
    if mode == "bams":
        return """
Study mode: BAMS Sanskrit.

The learner is studying Sanskrit as part of a BAMS course.

When the provided Sanskrit text clearly relates to Ayurveda or
BAMS, explain the relevant context in a beginner-friendly way.

IMPORTANT:
- Do not invent Ayurvedic meanings.
- Do not give medical advice.
- Do not make unsupported claims about diseases, treatments,
  medicines, or health effects.
- Keep the Sanskrit meaning separate from Ayurvedic interpretation.
- If the Ayurvedic context is uncertain, clearly say so.
"""

    return """
Study mode: General Sanskrit.

Focus on general Sanskrit learning:
- Direct meaning
- Vocabulary
- Word-by-word understanding
- Basic context

Do not add unsupported Ayurvedic, philosophical, or spiritual
interpretations.
"""


def get_iast(text):
    try:
        return transliterate(
            text,
            sanscript.DEVANAGARI,
            sanscript.IAST
        )
    except Exception:
        return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/explain", methods=["POST"])
def explain():
    data = request.get_json() or {}

    text = data.get("text", "").strip()
    study_mode = get_study_mode(data)

    if not text:
        return jsonify({
            "error": "Please enter some Sanskrit text."
        }), 400

    iast = get_iast(text)
    mode_instructions = get_mode_instructions(study_mode)

    prompt = f"""
You are Sanskrit Saathi, a careful Sanskrit learning assistant
for a beginner BAMS student.

{mode_instructions}

Analyze ONLY this Sanskrit text:

{text}

A deterministic Sanskrit transliteration system has already
generated this IAST transliteration:

{iast}

Do NOT change, reinterpret, or regenerate this transliteration.

Provide ONLY these sections:

3. Simple English meaning
4. Simple Hindi meaning
5. Word-by-word breakdown
6. Context or usage
7. Important note about uncertainty

STRICT ACCURACY RULES:

- Do not invent Sanskrit meanings.
- Do not invent grammar rules.
- Do not invent etymologies.
- Do not invent historical claims.
- Do not invent Ayurvedic, philosophical, or spiritual claims.
- Distinguish literal meaning from contextual meaning.
- If the text is a single word, focus primarily on its direct meaning.
- Do not treat visarga (ः), anusvara (ं), vowel signs, or other
  orthographic/grammatical markers as separate words.
- Do not describe visarga as an emphatic vowel, sandhi vowel,
  ending particle, or stress marker unless there is a specific
  grammatical reason and you are certain.
- Do not invent a grammatical analysis simply because the input
  is a single word.
- For word-by-word breakdown, only explain actual lexical words
  present in the input.
- If a grammatical detail is uncertain, say:
  "I am not certain about this grammatical detail."
- Never guess.

Keep the explanation beginner-friendly and concise.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        answer = response.json()["response"]

        final_answer = f"""1. Original Sanskrit:
{text}

2. Transliteration (IAST):
{iast}

{answer}"""

        return jsonify({
            "answer": final_answer
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Could not connect to Ollama: {e}"
        }), 500


@app.route("/api/quiz", methods=["POST"])
def quiz():
    data = request.get_json() or {}

    text = data.get("text", "").strip()
    study_mode = get_study_mode(data)

    if not text:
        return jsonify({
            "error": "Please enter some Sanskrit text."
        }), 400

    mode_instructions = get_mode_instructions(study_mode)

    prompt = f"""
You are Sanskrit Saathi, a cautious Sanskrit learning assistant
for a beginner BAMS student.

{mode_instructions}

Sanskrit text:
{text}

Create exactly 5 beginner-level multiple-choice questions using
ONLY facts that can be directly established from the Sanskrit text
and its basic meaning.

IMPORTANT:

- If the input contains only a single Sanskrit word, do not invent
  grammar, sentence usage, etymology, pronunciation rules, syllable
  information, cultural claims, Ayurvedic claims, or example phrases.
- Questions may test direct English meaning, direct Hindi meaning,
  vocabulary, or recognition of the Sanskrit word.
- Do not invent example sentences.
- Do not introduce unrelated Sanskrit words.
- Do not invent grammatical properties.
- Do not invent Ayurvedic or philosophical interpretations.
- Every question must have one clearly correct answer.
- Keep explanations to one sentence.
- Never guess.

For each question use exactly:

Question:
A.
B.
C.
D.
Correct Answer:
Explanation:

Return ONLY the questions.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return jsonify({
            "quiz": response.json()["response"]
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Could not connect to Ollama: {e}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)