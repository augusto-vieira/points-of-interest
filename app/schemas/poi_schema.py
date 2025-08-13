# app/schemas/poi_schema.py
from pydantic import BaseModel
from typing import List, Optional

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

###
class POINameSearchRequest(BaseModel):
    """Modelo de requisição para busca de POIs por nome.
    
    Atributos:
        name (str): Nome ou parte do nome do POI que será buscado.
                    A busca é case-insensitive e permite pesquisa parcial.
    """
    name: str

class POICreateRequest(BaseModel):
    """Modelo de requisição para criação de um novo POI"""
    name: str
    x: int
    y: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Padaria do Zé",
                "x": 23,
                "y": 42
            }
        }

class POICreateResponse(BaseModel):
    """Modelo de resposta para criação de POI"""
    success: bool
    message: str
    poi: Optional[POIItem] = None