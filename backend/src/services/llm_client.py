import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini OpenAI-compatible endpoint
)

def get_gemini_client():
    return client

def get_chatbot_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash", # Using the correct model name for Gemini 2.5 Flash
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from LLM: {e}"
