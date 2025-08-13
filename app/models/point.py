# app/models/point.py
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class POI(Base):
    __tablename__ = 'pois'  # Nome da tabela no banco

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    # Restrições para garantir apenas valores positivos
    __table_args__ = (
        CheckConstraint('x >= 0', name='check_x_positive'),
        CheckConstraint('y >= 0', name='check_y_positive'),
    )

    def __repr__(self):
        return f"<POI(id={self.id}, name='{self.name}', x={self.x}, y={self.y})>"