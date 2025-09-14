import pytest
from app.models.point import POI

def test_poi_creation():
    """Testa criação de POI com valores válidos."""
    poi = POI(id=1, name="Teste", x=10.0, y=20.0)
    assert poi.id == 1
    assert poi.name == "Teste"
    assert poi.x == 10.0
    assert poi.y == 20.0

def test_poi_negative_coordinates():
    """Testa POI com coordenadas negativas."""
    poi = POI(id=2, name="Negativo", x=-5.5, y=-7.2)
    assert poi.x == -5.5
    assert poi.y == -7.2

def test_poi_zero_coordinates():
    """Testa POI com coordenadas zero."""
    poi = POI(id=3, name="Zero", x=0.0, y=0.0)
    assert poi.x == 0.0
    assert poi.y == 0.0

def test_poi_update():
    """Testa atualização dos atributos de POI."""
    poi = POI(id=4, name="Original", x=1.0, y=2.0)
    poi.name = "Atualizado"
    poi.x = 3.3
    poi.y = 4.4
    assert poi.name == "Atualizado"
    assert poi.x == 3.3
    assert poi.y == 4.4

def test_poi_equality():
    """Testa igualdade entre dois objetos POI."""
    poi1 = POI(id=5, name="Igual", x=1.1, y=2.2)
    poi2 = POI(id=5, name="Igual", x=1.1, y=2.2)
    assert poi1 == poi2

def test_poi_repr():
    """Testa representação textual de POI."""
    poi = POI(id=6, name="Repr", x=9.9, y=8.8)
    rep = repr(poi)
    assert "POI" in rep
    assert "Repr" in rep

def test_poi_invalid_types():
    """Testa criação de POI com tipos inválidos (deve falhar)."""
    with pytest.raises(TypeError):
        POI(id="abc", name=123, x="x", y=None)