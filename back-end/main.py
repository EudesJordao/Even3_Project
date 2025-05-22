from fastapi import FastAPI
from pydantic import BaseModel
from model import generate_response

app = FastAPI()

class UserMessage(BaseModel):
    message: str

system_prompt = (
    "Você é uma IA especializada em orientar alunos na criação de TCCs. "
    "Sempre evite plágio e ajude o aluno passo a passo, como se ele nunca tivesse feito um TCC. "
    "Peça o tema, área de estudo, e ajude com introdução, problema, objetivo, justificativa, etc."
)

# Rota de teste da API
@app.get("/")
def root():
    return {"message": "API da IA Mentora de TCC"}

# Rota principal do chat
@app.post("/chat")
async def chat(user_msg: UserMessage):
    try:
        full_input = f"{system_prompt}\nUsuário: {user_msg.message}"
        response = generate_response(full_input)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
