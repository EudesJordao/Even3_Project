import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

# Pegando a chave da variável de ambiente
api_key = os.getenv("GEMINI_API_KEY")

# Verifica se a chave existe
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

# Configura o SDK com a chave
genai.configure(api_key=api_key)

# Nome do modelo
MODEL_NAME = "gemini-1.5-flash"
