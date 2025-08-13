# app/services/finder.py

from typing import List
from app.models.point import POI
from app.database.pgsql import SessionLocal
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

# Função para adicionar um POI
def add_poi(name: str, x: int, y: int):
    session = SessionLocal()
    try:
        poi = POI(name=name, x=x, y=y)
        session.add(poi)
        session.commit()
        # print(f"POI '{name}' adicionado com sucesso!")
        session.refresh(poi)     
        return poi 
    except Exception as e:
        session.rollback()
        print("Erro ao adicionar POI:", e)
        return None      
    finally:
        session.close()

# Função para listar todos os POIs
def list_pois():
    session = SessionLocal()
    try:
        pois = session.query(POI).all()
        for poi in pois:
            print(poi)           
    finally:
        session.close()

# Função para buscar POI por nome
def find_poi(name: str):
    session = SessionLocal()
    try:
        pois = session.query(POI).filter(POI.name.ilike(f"%{name}%")).all()
        return pois
    finally:
        session.close()

# Função para atualizar POI
def update_poi(poi_id: int, new_name: str, new_x: int, new_y: int):
    session = SessionLocal()
    try:
        poi = session.query(POI).get(poi_id)
        if poi:
            poi.name = new_name
            poi.x = new_x
            poi.y = new_y
            session.commit()
            print("POI atualizado com sucesso!")
        else:
            print("POI não encontrado!")
    finally:
        session.close()

# Função para deletar POI
def delete_poi(poi_id: int):
    session = SessionLocal()
    try:
        poi = session.query(POI).get(poi_id)
        if poi:
            session.delete(poi)
            session.commit()
            print("POI removido com sucesso!")
        else:
            print("POI não encontrado!")
    finally:
        session.close()
