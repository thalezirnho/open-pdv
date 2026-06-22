from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdateStatus, PedidoUpdateDados
from app.services.pedido import PedidoService

# CORREÇÃO: Adicionado o prefix="/pedidos" novamente aqui
router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def receber_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return PedidoService.criar_pedido(db=db, pedido_data=pedido)

@router.get("/", response_model=List[PedidoResponse])
async def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoService.listar_todos(db=db)

@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
async def mudar_status_pedido(pedido_id: int, payload: PedidoUpdateStatus, db: Session = Depends(get_db)):
    pedido_atualizado = PedidoService.atualizar_status(db=db, pedido_id=pedido_id, novo_status=payload.status)
    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido_atualizado

@router.put("/{pedido_id}/dados", response_model=PedidoResponse)
async def editar_dados_pedido(pedido_id: int, payload: PedidoUpdateDados, db: Session = Depends(get_db)):
    pedido_atualizado = PedidoService.editar_dados_pedido(db=db, pedido_id=pedido_id, dados=payload)
    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido_atualizado