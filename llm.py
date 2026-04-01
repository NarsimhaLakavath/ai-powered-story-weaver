import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please add it to the .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)


def _generate_text(prompt: str, temperature: float = 0.8, max_tokens: int = 400) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text.strip()


def generate_opening_story(prompt: str, temperature: float = 0.8) -> str:
    return _generate_text(prompt, temperature=temperature, max_tokens=350)


def continue_story_with_ai(prompt: str, temperature: float = 0.8) -> str:
    return _generate_text(prompt, temperature=temperature, max_tokens=400)


def generate_story_choices(prompt: str, temperature: float = 0.8) -> str:
    text = _generate_text(prompt, temperature=temperature, max_tokens=300)

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) < 3:
        return "1. Investigate the file deeper.\n2. Question the receptionist.\n3. Leave the building immediately."

    return text
