from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    
    # Relacionamento para conseguir puxar os produtos de uma categoria facilmente
    produtos = relationship("ProdutoModel", back_populates="categoria", cascade="all, delete-orphan")

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True, nullable=False)
    imagem_url = Column(String, nullable=True)
    
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("CategoriaModel", back_populates="produtos")