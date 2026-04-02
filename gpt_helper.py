# gpt_helper.py
# Groq AI Helper

import requests
import os


def _load_env_file(path=".env"):
    if not os.path.isfile(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        pass


# Groq API Endpoint
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Load environment variables
_load_env_file()


def _get_headers(api_key=None):
    key = api_key or os.getenv("GROQ_API_KEY")

    if not key:
        return None

    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }


def ask_gpt(prompt, api_key=None):

    headers = _get_headers(api_key)

    if headers is None:
        return "GROQ_API_KEY not found. Add it to .env file."

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt + "\n\nGive a short helpful answer."
            }
        ],
        "temperature": 0.3,
        "max_tokens": 200
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return f"Groq API error: HTTP {response.status_code} - {response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "Groq API timeout. Try again."

    except Exception as e:
        return f"Groq API error: {str(e)}"