from fastapi import FastAPI, Body, HTTPException
from app.schemas.poi_schema import POISearchRequest, POISearchResponse, POIItem
from app.services.finder import find_nearby_pois
from app.models.point import POI

# Instancia a aplicação FastAPI
app = FastAPI(title="Points of Interest")

# Lista fixa de POIs (Points of Interest)
pois = [
    POI(name="Lanchonete", x=27, y=12),
    POI(name="Posto", x=31, y=18),
    POI(name="Joalheria", x=15, y=12),
    POI(name="Floricultura", x=19, y=21),
    POI(name="Pub", x=12, y=8),
    POI(name="Supermercado", x=23, y=6),
    POI(name="Churrascaria", x=28, y=2),
]


@app.get("/list", response_model=POISearchResponse)
def list_pois():
    """
    Retorna todos os POIs cadastrados.
    """
    return POISearchResponse(results=[poi.to_dict() for poi in pois])

@app.post("/search", response_model=POISearchResponse)
def search_pois(request: POISearchRequest):
    """
    Rota para buscar POIs próximos a um ponto (x, y), dentro de uma distância máxima.
    """
    result = find_nearby_pois(pois, x=request.x, y=request.y, max_distance=request.max_distance)
    return POISearchResponse(results=result)

@app.post("/create", response_model=POIItem)
def create_poi(poi: POIItem = Body(...)):
    """
    Cadastra um novo POI com nome e coordenadas inteiras não negativas.
    """
    if poi.x < 0 or poi.y < 0:
        raise HTTPException(status_code=400, detail="Coordenadas devem ser inteiras não negativas.")
    
    new_poi = POI(name=poi.name, x=poi.x, y=poi.y)
    pois.append(new_poi)
    return poi
