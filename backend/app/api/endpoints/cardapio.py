import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.cardapio import CategoriaCreate, CategoriaResponse, ProdutoResponse
from app.services.cardapio import CardapioService
from app.models.cardapio import ProdutoModel

router = APIRouter(tags=["Cardápio"])

# ==========================================
# ROTAS DE CATEGORIA (JSON normal)
# ==========================================
@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return CardapioService.criar_categoria(db, payload)

@router.get("/categorias", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return CardapioService.listar_categorias(db)


# ==========================================
# ROTAS DE PRODUTO (Form Data para fotos e arquivos)
# ==========================================
@router.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return CardapioService.listar_produtos(db)

@router.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(
    nome: str = Form(...),
    descricao: str | None = Form(None),
    preco: float = Form(...),
    categoria_id: int = Form(...),
    disponivel: bool = Form(True),
    imagem: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    imagem_url = None
    if imagem and imagem.filename:
        if not os.path.exists("static"):
            os.makedirs("static")
        file_path = f"static/{imagem.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)
        imagem_url = f"/{file_path}"

    db_prod = ProdutoModel(
        nome=nome, 
        descricao=descricao, 
        preco=preco,
        categoria_id=categoria_id, 
        disponivel=disponivel, 
        imagem_url=imagem_url
    )
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
async def editar_produto(
    produto_id: int,
    nome: str = Form(...),
    descricao: str | None = Form(None),
    preco: float = Form(...),
    categoria_id: int = Form(...),
    disponivel: bool = Form(True),
    imagem: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    db_prod = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if imagem and imagem.filename:
        if not os.path.exists("static"):
            os.makedirs("static")
        file_path = f"static/{imagem.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)
        db_prod.imagem_url = f"/{file_path}"

    db_prod.nome = nome
    db_prod.descricao = descricao
    db_prod.preco = preco
    db_prod.categoria_id = categoria_id
    db_prod.disponivel = disponivel

    db.commit()
    db.refresh(db_prod)
    return db_prod

# --- NOVA ROTA: Alternar status com um clique ---
@router.patch("/produtos/{produto_id}/toggle", response_model=ProdutoResponse)
def alternar_status_produto(produto_id: int, db: Session = Depends(get_db)):
    db_prod = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Inverte o booleano de disponibilidade
    db_prod.disponivel = not db_prod.disponivel
    db.commit()
    db.refresh(db_prod)
    return db_prod