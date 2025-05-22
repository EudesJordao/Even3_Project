from google.generativeai import GenerativeModel
from config import MODEL_NAME

# Instancia o modelo generativo
model = GenerativeModel(MODEL_NAME)

# Cria uma sessão de chat persistente
chat_session = model.start_chat(history=[])

def generate_response(user_input: str) -> str:
    response = chat_session.send_message(user_input)
    return response.text
