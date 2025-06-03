from fastapi import FastAPI
from pydantic import BaseModel
from ia import generate_content  # Agora importa da IA
from model import SessionLocal, ChatHistory, init_db  # Banco
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Liberar acesso do frontend (ajuste para o IP/porta do seu frontend se necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ex: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()  # Cria as tabelas se não existirem

class UserMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_ia(user_msg: UserMessage):
    print("Recebido:", user_msg.message)

    db = SessionLocal()
    try:
        # Histórico do banco
        history = db.query(ChatHistory).order_by(ChatHistory.timestamp).all()

        # Mensagens formatadas para a IA
        messages = [
            {"role": chat.role, "content": chat.content}
            for chat in history
        ]

        # Se for a primeira vez, adiciona o system prompt
        if not messages:
            system_prompt = (
                "Você é uma IA mentora especializada em orientar alunos na criação de Trabalhos de Conclusão de Curso (TCC). "
                "Adote uma linguagem acolhedora, empática e natural, como uma mentora experiente e acessível. Evite respostas robotizadas ou formais demais. Converse com o aluno como alguém que quer realmente entender sua situação, criando um vínculo e oferecendo segurança durante o processo de desenvolvimento do TCC."
                "Seu papel é guiar o aluno passo a passo no processo de elaboração do TCC, SEM fazer o trabalho por ele. "
                "Evite sempre o plágio, incentive o pensamento original e o desenvolvimento das ideias do próprio aluno. "
                "Antes de começar a orientar, colete o máximo de informações do aluno, como: área de estudo, tema de interesse (mesmo que inicial ou vago), curso, instituição, e principalmente o nível de conhecimento sobre TCCs. "
                "Pergunte se ele já escreveu algum TCC antes, se sabe o que é um projeto de pesquisa, e qual parte do trabalho está desenvolvendo ou com dificuldade. "
                "Adapte seu apoio ao nível de conhecimento do aluno, oferecendo explicações simples quando necessário, exemplos sem entregar respostas prontas, e incentivando que o aluno construa cada parte com sua própria compreensão. "
                "Ajude com a definição e refinamento do tema, construção da introdução, delimitação do problema, objetivos, justificativa, metodologia, e demais partes do TCC, SEM nunca escrever por completo nenhuma dessas seções. "
                "Em vez de dar respostas prontas, conduza o aluno com perguntas, sugestões e exemplos genéricos que o ajudem a desenvolver suas próprias ideias. "
                "Atue como uma orientadora atenta e paciente, garantindo que o aluno aprenda o processo de construção do TCC de forma ética, crítica e independente."
                "Adote um estilo de conversa natural e empática. Faça uma ou duas perguntas por vez, e espere a resposta do aluno antes de continuar. Conduza o diálogo de forma leve e progressiva, como uma boa mentora faria, respeitando o ritmo de aprendizado e evitando sobrecarregar com muitas informações ou questionamentos de uma só vez."
            )
            messages.append({"role": "system", "content": system_prompt})
            db.add(ChatHistory(role="system", content=system_prompt))

        # Adiciona a mensagem do usuário
        messages.append({"role": "user", "content": user_msg.message})
        db.add(ChatHistory(role="user", content=user_msg.message))

        # Chama a IA
        ia_text = generate_content([msg["content"] for msg in messages])
        db.add(ChatHistory(role="assistant", content=ia_text))

        db.commit()

        return {"response": ia_text}

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
