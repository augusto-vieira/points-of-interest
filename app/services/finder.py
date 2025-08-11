# app/services/finder.py

from typing import List
from app.models.point import POI
import math

def find_nearby_pois(pois: List[POI], x: int, y: int, max_distance: int) -> List[dict]:
    """
    Retorna uma lista de POIs cuja distância até (x, y) seja menor ou igual à distância máxima.
    """

    nearby = []

    for poi in pois:
        # Distância Euclidiana entre os pontos
        distance = math.sqrt((poi.x - x) ** 2 + (poi.y - y) ** 2)

        if distance <= max_distance:
            nearby.append(poi.to_dict())

    return nearby