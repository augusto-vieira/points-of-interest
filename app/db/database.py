from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Cria o engine do SQLAlchemy para conectar ao banco
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definição dos modelos ORM
Base = declarative_base()

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