# app/services/finder.py

from typing import List
from app.models.point import POI
from app.database.pgsql import SessionLocal
import math

# Função ára encontrar POIs próximos a (x,y) dentro da distância máxima.
def find_nearby_pois(x: int, y: int, max_distance: int) -> List[POI]:
    """
    Retorna uma lista de POIs cuja distância até (x, y) seja menor ou igual à distância máxima.
    """
    session = SessionLocal()
    try:
        # Primeiro busca todos os POIs
        all_pois = session.query(POI).all()
        
        # Filtra localmente (alternativa: poderia usar funções do banco para filtrar)
        nearby = []
        for poi in all_pois:
            distance = math.sqrt((poi.x - x)**2 + (poi.y - y)**2)
            if distance <= max_distance:
                nearby.append(poi)
        return nearby
    finally:
        session.close()

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
        return session.query(POI).all()
        # for poi in pois:
        #     print(poi)           
    finally:
        session.close()

# Função para buscar POI por nome
def find_pois(name: str):
    session = SessionLocal()
    try:
        pois = session.query(POI).filter(POI.name.ilike(f"%{name}%")).all()
        return pois
    finally:
        session.close()

# Função para atualizar POI
def update_poi(poi_id: int, update_data: dict):
    """Atualiza um POI existente"""
    session = SessionLocal()
    try:
        # Busca o POI pelo ID
        poi = session.query(POI).filter(POI.id == poi_id).first()
        if not poi:
            return None
        
        # Aplica as atualizações
        for field, value in update_data.items():
            if value is not None:  # Só atualiza campos que foram fornecidos
                setattr(poi, field, value)
        
        session.commit()
        session.refresh(poi)
        return poi
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar POI: {str(e)}")
        return None
    finally:
        session.close()

# Função para deletar POI
def delete_poi(poi_id: int)-> bool:
    """Remove um POI do banco de dados
    
    Args:
        poi_id: ID do POI a ser removido
        
    Returns:
        bool: True se foi deletado, False se não encontrado
    """
    session = SessionLocal()
    try:
        poi = session.query(POI).filter(POI.id == poi_id).first()
        if not poi:
            return False
        
        session.delete(poi)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar POI: {str(e)}")
        return False
    finally:
        session.close()
