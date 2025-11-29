from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base


class Cliente(Base):
    """
    Modelo de dados para Cliente na fila
    """
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(20), nullable=False)
    tipo_atendimento = Column(String(1), nullable=False)  # N = Normal, P = Prioritário
    posicao = Column(Integer, nullable=False)
    data_chegada = Column(DateTime, default=datetime.now, nullable=False)
    atendido = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', posicao={self.posicao}, tipo='{self.tipo_atendimento}')>"

