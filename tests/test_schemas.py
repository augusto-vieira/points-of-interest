import pytest
from app.schemas.poi_schema import POICreateRequest, POIUpdateRequest, POIItem, POISearchResponse

def test_poi_create_schema():
	"""Testa criação de POI válido via schema."""
	data = {"name": "Teste", "x": 10.0, "y": 20.0}
	poi = POICreateRequest(**data)
	assert poi.name == "Teste"
	assert poi.x == 10.0
	assert poi.y == 20.0

def test_poi_create_schema_invalid():
	"""Testa criação de POI inválido via schema (tipos errados)."""
	with pytest.raises(Exception):
		POICreateRequest(name="Teste", x="abc", y=None)

def test_poi_update_schema_partial():
	"""Testa atualização parcial de POI via schema."""
	poi = POIUpdateRequest(name="NovoNome")
	assert poi.name == "NovoNome"
	assert poi.x is None
	assert poi.y is None

def test_poi_update_schema_full():
	"""Testa atualização completa de POI via schema."""
	poi = POIUpdateRequest(name="Nome", x=1.1, y=2.2)
	assert poi.name == "Nome"
	assert poi.x == 1.1
	assert poi.y == 2.2

def test_poi_item_schema():
	"""Testa criação de POIItem via schema."""
	poi = POIItem(id=1, name="Item", x=3.3, y=4.4)
	assert poi.id == 1
	assert poi.name == "Item"
	assert poi.x == 3.3
	assert poi.y == 4.4

def test_poi_search_response():
	"""Testa resposta de busca de POIs via schema."""
	items = [POIItem(id=1, name="A", x=1, y=2), POIItem(id=2, name="B", x=3, y=4)]
	resp = POISearchResponse(results=items)
	assert len(resp.results) == 2
	assert resp.results[0].name == "A"

def test_poi_create_schema_negative():
	"""Testa criação de POI com coordenadas negativas."""
	poi = POICreateRequest(name="Negativo", x=-10, y=-20)
	assert poi.x == -10
	assert poi.y == -20

def test_poi_update_schema_empty():
	"""Testa atualização de POI sem dados (todos campos None)."""
	poi = POIUpdateRequest()
	assert poi.name is None
	assert poi.x is None
	assert poi.y is None

def test_poi_item_schema_repr():
	"""Testa representação textual de POIItem."""
	poi = POIItem(id=99, name="Repr", x=0, y=0)
	assert "POIItem" in repr(poi)
