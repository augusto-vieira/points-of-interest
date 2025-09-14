import pytest
from fastapi.testclient import TestClient
from app.main import app # importa minha aplicação

client = TestClient(app)

def test_create_poi():
    """Testa criação de POI via endpoint POST."""
    payload = {"name": "POI Teste", "x": 10, "y": 20}
    response = client.post("/api/pois/", json=payload)
    
    # Verifica se a resposta é 200 (sucesso na criação)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["poi"]["name"] == "POI Teste"
    assert data["poi"]["x"] == 10.0
    assert data["poi"]["y"] == 20.0
    return data["poi"]

def test_list_pois():
    """Testa listagem de POIs via endpoint GET."""
    response = client.get("/api/pois/")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)

def test_search_pois_by_name():
    """Testa busca de POI por nome via endpoint GET."""
    client.post("/api/pois/", json={"name": "BuscaNome", "x": 1, "y": 2})
    response = client.get("/api/pois/by-name?name=BuscaNome")
    assert response.status_code == 200
    data = response.json()
    assert any(poi["name"] == "BuscaNome" for poi in data.get("results", []))

def test_search_pois_nearby():
    """Testa busca de POIs próximos via endpoint POST."""
    client.post("/api/pois/", json={"name": "NearbyPOI", "x": 5, "y": 5})
    payload = {"x": 5, "y": 5, "max_distance": 10}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert any(poi["name"] == "NearbyPOI" for poi in data.get("results", []))

def test_update_poi():
    """Testa atualização de POI via endpoint PUT."""
    create_resp = client.post("/api/pois/", json={"name": "AtualizarPOI", "x": 7, "y": 8})
    poi_id = create_resp.json()["poi"]["id"]
    update_payload = {"name": "POI Atualizado", "x": 9, "y": 10}
    response = client.put(f"/api/pois/{poi_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["poi"]["name"] == "POI Atualizado"

def test_delete_poi():
    """Testa remoção de POI via endpoint DELETE."""
    create_resp = client.post("/api/pois/", json={"name": "DeletarPOI", "x": 11, "y": 12})
    poi_id = create_resp.json()["poi"]["id"]
    response = client.delete(f"/api/pois/{poi_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

# Teste rápido para inspecionar as rotas
def test_list_routes():
    print("=== Rotas disponíveis no app ===")
    for r in app.routes:
        print(r.path, r.methods)

    # Garante que a rota de criação existe
    paths = [r.path for r in app.routes]
    assert "/create" in paths
    assert "/list" in paths
    assert "/search" in paths

def test_debug_create_poi():
    payload = {"name": "POI Teste", "x": 10, "y": 20}
    response = client.post("/create", json=payload)
    print("Status Code:", response.status_code)
    try:
        print("JSON:", response.json())
    except Exception as e:
        print("Erro ao decodificar JSON:", e)
        print("Texto da resposta:", response.text)