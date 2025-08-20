# 📍 Points of Interest API

Este projeto implementa uma API REST para cadastro e consulta de **Pontos de Interesse (POIs)** com base em coordenadas geográficas. Desenvolvido para o desafio proposto pela XY Inc.

## 🚀 Funcionalidades

- ✅ Cadastrar POIs com nome e coordenadas (x, y)
- ✅ Listar todos os POIs cadastrados
- ✅ Listar POIs por proximidade de um ponto de referência (x, y) com distância máxima (d-max)

📝 Requisitos para ser atendidos:

negativas.
- [x] Listar os **POIs por proximidade**. Este serviço receberá uma coordenada **X** e uma coordenada **Y**, especificando um ponto de referência, bem como uma distância **máxima (d-max)** em metros. O serviço deverá **retornar todos os POIs** da base de dados que estejam a uma distância menor ou igual a d-max a partir do ponto de referência.
- [x] **Listar** todos os POIs cadastrados
- [x] **Cadastrar POIs** com **nome** e coordenadas **(x, y)** inteiras não 
- [x] Os POIs devem ser **armazenados** em uma **base de dados.**

📝 Novas funcionalidades:
- [x] **Atualizar** um POIs
- [x] **Deletar*** um POIs
- [x] **Encontrar** um POIs **por nome**

## 📦 Tecnologias

- Python 3.8+
- FastAPI
- Uvicorn
- Gerenciador de dependências: [uv](https://github.com/astral-sh/uv)

## ▶️ Como rodar
**Criar o ambiente virtual**
```bash
uv pip install fastapi uvicorn
uvicorn app.main:app --reload
```

**Instalar o Projeto com .toml**
```bash
uv pip install .     # Instalação normal
uv pip install -e .  # Modo desenvolvimento (editable)
```

**Acesse a documentação interativa:**
```yaml
Swagger: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
```
--
## Exemplo de uso da API
**Requisição:**
```json
POST /search HTTP/1.1
Content-Type: application/json

{
  "x": 20,
  "y": 10,
  "max_distance": 10
}
```

**Resposta:**
```json
{
  "results": [
    {
      "name": "Lanchonete",
      "x": 27,
      "y": 12
    },
    {
      "name": "Joalheria",
      "x": 15,
      "y": 12
    },
    {
      "name": "Pub",
      "x": 12,
      "y": 8
    },
    {
      "name": "Supermercado",
      "x": 23,
      "y": 6
    }
  ]
}
```

**Testes com curl**
```bash
# Listar todos 
curl http://localhost:8000/api/list

# Procurar por nome
curl "http://localhost:8000/api/pois/by-name?name=Casa"

# Excluir por id
curl -X DELETE http://localhost:8000/api/pois/2   

# Atualizar POI
curl -X PUT "http://localhost:8000/api/pois/123" \
  -H "Content-Type: application/json" \
  -d '{"name": "Novo Nome", "x": 23, "y": 33}'

# Encontrar um POI por distância
curl -s -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"x": 20, "y": 21, "max_distance": 25}'
```

**Clone do projeto**
```bash
git clone https://github.com/augusto-vieira/points-of-interest.git
cd points-of-interest/
```