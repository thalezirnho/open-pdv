from sqlalchemy import Column, DateTime, Float, Integer, JSON, String
from datetime import datetime
from zoneinfo import ZoneInfo
from app.core.database import Base

class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, nullable=False)
    cliente_telefone = Column(String, nullable=True)
    origem = Column(String, nullable=False)
    tipo_consumo = Column(String, nullable=False)    
    forma_pagamento = Column(String, nullable=False) 
    endereco_entrega = Column(String, nullable=True)  
    status = Column(String, default="Pendente", nullable=False)
    itens = Column(JSON, nullable=False)             
    valor_total = Column(Float, nullable=False)
    
    # Força a geração do timestamp no fuso horário correto do Brasil
    data_criacao = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo"))
    )