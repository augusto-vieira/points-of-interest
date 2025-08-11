# app/models/point.py

class POI:
    """
    Representa um Ponto de Interesse (POI) com nome e coordenadas (x, y).
    """

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    def to_dict(self) -> dict:
        """
        Converte o objeto POI em um dicionário para retorno na API.
        """
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
        }