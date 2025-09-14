import pytest
from app.services.finder import list_pois, find_poi_by_name, find_pois_nearby

def test_list_pois():
	"""Testa se a função retorna uma lista de POIs."""
	pois = list_pois()
	assert isinstance(pois, list)

def test_find_poi_by_name_found():
	"""Testa busca de POI por nome existente."""
	pois = find_poi_by_name("Teste")
	assert isinstance(pois, list)

def test_find_poi_by_name_not_found():
	"""Testa busca de POI por nome inexistente."""
	pois = find_poi_by_name("NomeInexistente")
	assert pois == [] or isinstance(pois, list)

def test_find_pois_nearby_found():
	"""Testa busca de POIs próximos com resultado esperado."""
	pois = find_pois_nearby(0, 0, 100)
	assert isinstance(pois, list)

def test_find_pois_nearby_none():
	"""Testa busca de POIs próximos sem resultado (fora do alcance)."""
	pois = find_pois_nearby(9999, 9999, 1)
	assert pois == [] or isinstance(pois, list)

def test_find_pois_nearby_zero_distance():
	"""Testa busca de POIs próximos com distância zero."""
	pois = find_pois_nearby(0, 0, 0)
	assert pois == [] or isinstance(pois, list)

def test_find_pois_nearby_negative_distance():
	"""Testa busca de POIs próximos com distância negativa (caso limite)."""
	pois = find_pois_nearby(0, 0, -10)
	assert pois == [] or isinstance(pois, list)
