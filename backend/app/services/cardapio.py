from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.cardapio import CategoriaModel, ProdutoModel
from app.schemas.cardapio import CategoriaCreate, ProdutoCreate

class CardapioService:
    # --- Métodos de Categoria ---
    @staticmethod
    def criar_categoria(db: Session, cat_data: CategoriaCreate) -> CategoriaModel:
        db_cat = CategoriaModel(nome=cat_data.nome)
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)
        return db_cat

    @staticmethod
    def listar_categorias(db: Session) -> List[CategoriaModel]:
        return db.query(CategoriaModel).order_by(CategoriaModel.nome.asc()).all()

    # --- Métodos de Produto ---
    @staticmethod
    def criar_produto(db: Session, prod_data: ProdutoCreate) -> ProdutoModel:
        db_prod = ProdutoModel(**prod_data.model_dump())
        db.add(db_prod)
        db.commit()
        db.refresh(db_prod)
        return db_prod

    @staticmethod
    def listar_produtos(db: Session) -> List[ProdutoModel]:
        return db.query(ProdutoModel).order_by(ProdutoModel.nome.asc()).all()

    @staticmethod
    def atualizar_produto(db: Session, prod_id: int, prod_data: ProdutoCreate) -> Optional[ProdutoModel]:
        db_prod = db.query(ProdutoModel).filter(ProdutoModel.id == prod_id).first()
        if db_prod:
            for key, value in prod_data.model_dump().items():
                setattr(db_prod, key, value)
            db.commit()
            db.refresh(db_prod)
        return db_prod