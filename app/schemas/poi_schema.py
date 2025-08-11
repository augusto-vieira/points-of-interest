# app/schemas/poi_schema.py

from pydantic import BaseModel
from typing import List

class POISearchRequest(BaseModel):
    """
    Modelo de entrada da API: coordenadas e distância máxima.
    """
    x: int
    y: int
    max_distance: int

class POIItem(BaseModel):
    """
    Representa um POI no retorno da API.
    """
    name: str
    x: int
    y: int

class POISearchResponse(BaseModel):
    """
    Modelo de resposta da API: lista de POIs encontrados.
    """
    results: List[POIItem]