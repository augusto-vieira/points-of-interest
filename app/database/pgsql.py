# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis do ambiente pelo arquivo .env
load_dotenv(override=True)

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL') 

# Cria o engine do SQLAlchemy para conectar ao banco
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(bind=engine)

# # Base para definição dos modelos ORM
# Base = declarative_base()

def get_db():
    """
    Dependência do FastAPI para obter uma sessão de banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()