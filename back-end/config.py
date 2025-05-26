import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não está definida no .env")

client = OpenAI(api_key=api_key)

MODEL_NAME = "gpt-4"  # corrigido, sem o 'oadwe'
