from pydantic import BaseModel
from typing import Optional

# Schemas de Categoria
class CategoriaCreate(BaseModel):
    nome: str

class CategoriaResponse(CategoriaCreate):
    id: int
    class Config:
        from_attributes = True

# Schemas de Produto
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    categoria_id: int
    disponivel: bool = True

class ProdutoResponse(BaseModel): # Modificado para herdar direto do BaseModel
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    categoria_id: int
    disponivel: bool
    imagem_url: Optional[str] = None # <-- Adicionado explicitamente aqui!

    class Config:
        from_attributes = True