import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import pedidos
from app.core.database import Base, engine
from app.models import pedido, cardapio  
from app.api.endpoints import pedidos, cardapio as rotas_cardapio

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles

# Cria de forma automática as tabelas se elas não existirem no banco de dados.
# Em produção avanzada, substitui-se isso pelas migrações do Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gerenciador de Restaurante API",
    description="Backend centralizado para gestão de pedidos originados de Totens e Web",
    version="1.0.0"
)

# Liberação de CORS para permitir requisições de outros domínios (Frontend Web / Android)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina explicitamente os domínios permitidos
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- TRATAMENTO DE ERRO PERSONALIZADO ---
# Isto impede o UnicodeDecodeError e mostra o erro real do formulário
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    erros_limpos = []
    for error in exc.errors():
        erros_limpos.append({
            "localizacao": error.get("loc"),
            "mensagem": error.get("msg"),
            "tipo": error.get("type")
        })
    
    # Imprime diretamente no terminal do Docker para facilitar a leitura
    print("\n!!! ERRO DE VALIDAÇÃO NO FORMULÁRIO !!!")
    print(erros_limpos)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    
    return JSONResponse(
        status_code=422,
        content={"detail": erros_limpos}
    )
# ----------------------------------------


# Cria a pasta 'static' caso ela não exista
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclui o grupo de rotas configurado para os pedidos
app.include_router(pedidos.router, prefix="/api")


# Registro do novo roteador do cardápio
app.include_router(pedidos.router, prefix="/api")
app.include_router(rotas_cardapio.router, prefix="/api")


@app.get("/healthcheck", tags=["Health"])
def verificar_saude():
    return {"status": "healthy"}