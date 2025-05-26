from fastapi import FastAPI
from pydantic import BaseModel
from model import generate_content

app = FastAPI()

class UserMessage(BaseModel):
    message: str

chat_history = []

@app.get("/")
def read_root():
    return {"status": "API está rodando"}

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

@app.post("/chat")
async def chat_with_ia(user_msg: UserMessage):
    print("Recebido:", user_msg.message)

    system_prompt = (
        "Você é uma IA especializada em orientar alunos na criação de TCCs. "
        "Sempre evite plágio e ajude o aluno passo a passo, como se ele nunca tivesse feito um TCC. "
        "Peça o tema, área de estudo, e ajude com introdução, problema, objetivo, justificativa, etc."
    )

    if not chat_history:
        chat_history.append(system_prompt)

    chat_history.append(user_msg.message)

    try:
        ia_text = generate_content(chat_history)
        chat_history.append(ia_text)
        return {"response": ia_text}
    except Exception as e:
        return {"error": str(e)}
