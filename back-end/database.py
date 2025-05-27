from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)  # 'user' ou 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Cria o banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)
