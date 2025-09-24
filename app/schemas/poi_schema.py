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
    id: int
    name: str
    x: int
    y: int

class POISearchResponse(BaseModel):
    """
    Modelo de resposta da API: lista de POIs encontrados.
    """
    results: List[POIItem]

###
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

class POIUpdateRequest(BaseModel):
    """Modelo para atualização de POI"""
    name: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Novo Nome",
                "x": 30,
                "y": 40
            }
        }

class POIDeleteResponse(BaseModel):
    """Modelo de resposta para deleção de POI"""
    success: bool
    message: str
    deleted_id: Optional[int] = None