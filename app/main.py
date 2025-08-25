from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.poi_schema import POISearchRequest, POISearchResponse, POIItem, POICreateResponse, POICreateRequest, POIUpdateRequest, POIDeleteResponse
from app.services.finder import find_nearby_pois, find_pois, add_poi, list_pois, update_poi, delete_poi
from app.models.point import POI

# Instancia a aplicação FastAPI
app = FastAPI(title="Points of Interest")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (em desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os headers
)


@app.get("/api/list", response_model=POISearchResponse)
def list_pois_endpoint():
    """
    Retorna todos os POIs cadastrados.
    """

    # Chama a função de listar os POIs no banco de dados
    pois = list_pois()

    # Converta os objetos ORM para POIItem
    poi_items = [POIItem(name=poi.name, x=poi.x, y=poi.y) for poi in pois]

    # Retorna a resposta no formato esperado pelo cliente
    return POISearchResponse(results=poi_items)

@app.post("/api/{search}", response_model=POISearchResponse)
def search_pois(request: POISearchRequest):
    """
    Rota para buscar POIs próximos a um ponto (x, y), dentro de uma distância máxima (d-max).
    """

    nearby_pois = find_nearby_pois(
        x=request.x,
        y=request.y,
        max_distance=request.max_distance
    )

    # Converte para POIItem
    poi_items = [
        POIItem(name=poi.name, x=poi.x, y=poi.y) 
        for poi in nearby_pois
    ]

    return POISearchResponse(results=poi_items)

@app.get("/api/pois/{by_name}", response_model=POISearchResponse)
def search_pois_by_name(name: str):   
    """
    Rota para buscar POIs por nome.
    """

    # Chama a função de busca no banco de dados
    pois = find_pois(name=name)

    # Converta os objetos ORM para POIItem
    # Isso é necessário para garantir a serialização correta na resposta
    poi_items = [POIItem(name=poi.name, x=poi.x, y=poi.y) for poi in pois]

    # Retorna a resposta no formato esperado pelo cliente
    return POISearchResponse(results=poi_items)

@app.post("/api/pois/", response_model=POICreateResponse)
def create_poi(poi_data: POICreateRequest):
    """
    Rota para cadastrar um POI.
    """
    try:
            # Adiciona o POI ao banco de dados
            success = add_poi(name=poi_data.name, x=poi_data.x, y=poi_data.y)
            
            if success:
                # Se necessário, poderia buscar o POI recém-criado para retornar seus dados
                return POICreateResponse(
                    success=True,
                    message=f"POI '{poi_data.name}' criado com sucesso",
                    poi=POIItem(name=poi_data.name, x=poi_data.x, y=poi_data.y)
                )
            else:
                return POICreateResponse(
                    success=False,
                    message="Falha ao criar POI - verifique os dados informados"
                )
                
    except Exception as e:
        # Log detalhado do erro (em produção, usar logging)
        print(f"Erro inesperado ao criar POI: {str(e)}")
        return POICreateResponse(
            success=False,
            message="Ocorreu um erro interno ao processar sua requisição"
        )

@app.put("/api/pois/{poi_id}", response_model=POICreateResponse)
def update_poi_endpoint(
    poi_id: int, 
    update_data: POIUpdateRequest
):
    """
    Atualiza um POI existente
    
    Args:
        poi_id: ID do POI a ser atualizado
        update_data: Campos a serem atualizados (nome, x, y)
        
    Returns:
        Resposta com o POI atualizado ou mensagem de erro
    """
    # Converte o Pydantic model para dict, removendo campos não informados (None)
    update_dict = update_data.model_dump(exclude_unset=True)
    
    updated_poi = update_poi(poi_id, update_dict)
    
    if not updated_poi:
        return POICreateResponse(
            success=False,
            message=f"POI com ID {poi_id} não encontrado"
        )
    
    return POICreateResponse(
        success=True,
        message="POI atualizado com sucesso",
        poi=POIItem(
            name=updated_poi.name,
            x=updated_poi.x,
            y=updated_poi.y
        )
    )

@app.delete("/api/pois/{poi_id}", response_model=POIDeleteResponse)
def delete_poi_endpoint(poi_id: int):
    """
    Remove um POI pelo ID
    
    Args:
        poi_id: ID do POI a ser removido
        
    Returns:
        POIDeleteResponse: Resposta indicando sucesso/falha
    """
    success = delete_poi(poi_id)
    
    if success:
        return POIDeleteResponse(
            success=True,
            message=f"POI {poi_id} removido com sucesso",
            deleted_id=poi_id
        )
    else:
        return POIDeleteResponse(
            success=False,
            message=f"POI {poi_id} não encontrado"
        )