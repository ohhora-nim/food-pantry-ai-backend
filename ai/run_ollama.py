import os
from ollama import Client

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

client = Client(host=f"{OLLAMA_HOST}:11434")
AI_MODEL = "gemma4:e2b"


def run_ai(prompt, options):
    response = client.chat(
        model=f'{AI_MODEL}',
        messages=[{"role": "user", "content": prompt}],
        options=options
    )

    return clean_json(response["message"]["content"])


# =========================================
# Helpers
# =========================================


def clean_json(s):
    return s.replace('```json', '').replace('```', '')



# =========================================
# Clean Text
# =========================================

def clean_text(text):
    if not text:
        return ""

    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    text = " ".join(text.split())

    return text.strip()