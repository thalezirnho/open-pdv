from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int
    nome_produto: str
    preco_unitario: float
    observacao: Optional[str] = None 

class PedidoCreate(BaseModel):
    cliente_nome: str
    cliente_telefone: Optional[str] = None
    endereco_entrega: Optional[str] = None # NOVO CAMPO
    origem: str = Field(..., description="'totem', 'site' ou 'balcao'")
    tipo_consumo: str = Field(..., description="'Comer no local', 'Retirada', 'Delivery'")
    forma_pagamento: str = Field(..., description="'Pix', 'Cartão de Crédito', 'Cartão de Débito', 'Dinheiro'")
    itens: List[ItemPedido]
    valor_total: float

class PedidoUpdateStatus(BaseModel):
    status: str

# SCHEMA PARA A EDIÇÃO VIA KANBAN
class PedidoUpdateDados(BaseModel):
    tipo_consumo: str
    forma_pagamento: str
    endereco_entrega: Optional[str] = None

class PedidoResponse(PedidoCreate):
    id: int
    status: str
    data_criacao: datetime

    class Config:
        from_attributes = True