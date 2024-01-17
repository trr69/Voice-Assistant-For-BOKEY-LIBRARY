import requests
import config
import pyttsx3
from query_data import user_ask


def ask_gpt(prompt: str):
    try:
        output = user_ask(prompt)
        pyttsx3.speak(output)
    except Exception as e:
        print(f"errorGPT: {e}")

