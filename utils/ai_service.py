import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def analyze_image(image, prompt):
    """Analyze a construction site image using Gemini."""

    if client is None:
        return "Gemini API key not found. Please check your .env file."

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[prompt, image],
        )
        return response.text or "No analysis was returned."

    except Exception as error:
        return f"AI analysis failed: {error}"

def ask_construction_assistant(question, weather):
    """Answer construction questions using Gemini text input."""

    if client is None:
        return "Gemini API key not found. Please check your .env file."

    prompt = f"""
    You are a construction information assistant.

    Current weather condition: {weather}
    User question: {question}

    Provide clear, practical, safety-conscious guidance.
    Recommend consulting a qualified site engineer when necessary.
    Do not invent site-specific facts.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text or "No response was returned."

    except Exception as error:
        return f"AI assistant failed: {error}"
