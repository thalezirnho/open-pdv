from sqlalchemy.orm import Session
from typing import Optional
from app.models.pedido import PedidoModel
from app.schemas.pedido import PedidoCreate, PedidoUpdateDados

class PedidoService:
    @staticmethod
    def criar_pedido(db: Session, pedido_data: PedidoCreate) -> PedidoModel:
        db_pedido = PedidoModel(
            cliente_nome=pedido_data.cliente_nome,
            cliente_telefone=pedido_data.cliente_telefone,
            endereco_entrega=pedido_data.endereco_entrega,  # <-- Deve ser idêntico ao modelo
            origem=pedido_data.origem,
            tipo_consumo=pedido_data.tipo_consumo,
            forma_pagamento=pedido_data.forma_pagamento,
            itens=[item.model_dump() for item in pedido_data.itens],
            valor_total=pedido_data.valor_total,
            status="Pendente"
        )
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido

    @staticmethod
    def listar_todos(db: Session) -> list[PedidoModel]:
        return db.query(PedidoModel).order_by(PedidoModel.data_criacao.asc()).all()

    @staticmethod
    def atualizar_status(db: Session, pedido_id: int, novo_status: str) -> Optional[PedidoModel]:
        db_pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()
        if db_pedido:
            db_pedido.status = novo_status
            db.commit()
            db.refresh(db_pedido)
        return db_pedido

    @staticmethod
    def editar_dados_pedido(db: Session, pedido_id: int, dados: PedidoUpdateDados) -> Optional[PedidoModel]:
        db_pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()
        if db_pedido:
            db_pedido.tipo_consumo = dados.tipo_consumo
            db_pedido.forma_pagamento = dados.forma_pagamento
            db_pedido.endereco_entrega = dados.endereco_entrega if dados.tipo_consumo == "Delivery" else None
            db.commit()
            db.refresh(db_pedido)
        return db_pedido