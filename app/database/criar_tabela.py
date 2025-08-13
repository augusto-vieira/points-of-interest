# criar_tabela.py
from  .pgsql import engine
from  app.models.point import Base

# Isso criará TODAS as tabelas definidas por modelos que herdam de Base
Base.metadata.create_all(engine)

# Execute no terminal:
# python -m app.database.criar_tabela
