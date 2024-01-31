from query_data import GPTQuery
from silero import TTSModel

gpt = GPTQuery()

def ask_gpt(prompt: str):
    try:
        output = gpt.user_ask(prompt)
        t = TTSModel()
        t(output)
    except Exception as e:
        print(f"errorGPT: {e}")
