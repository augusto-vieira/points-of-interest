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

-- Listar fixa de POIs do desafio:
INSERT INTO pois (name, x, y) VALUES
    ('Lanchonete', 27, 12),
    ('Posto', 31, 18),
    ('Joalheria', 15, 12),
    ('Floricultura', 19, 21),
    ('Pub', 12, 8),
    ('Supermercado', 23, 6),
    ('Churrascaria', 28, 2);