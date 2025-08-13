-- Listar Bancos de Dados:
SELECT datname FROM pg_database;

-- Listar Tabelas de um Banco de Dados:
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'; -- Para listar apenas as tabelas no schema público

-- Listar Colunas de uma Tabela:
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'pois';

-- Selecionando todas as colunas:
SELECT * FROM pois;

-- Inserindo dados em todas as colunas:
INSERT INTO pois (name, x, y)
VALUES ('Casa', 19, 13);

-- Inserindo dados em algumas colunas:
INSERT INTO pois (name)
VALUES ('CasaNova');  -- vai retornar erro, não aceita valor vazio.