from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.database import engine, SessionLocal
from app.models import currency  # importar el modelo para que Base lo registre
from app.database import Base
from app.routers.currency_router import router as currency_router
from app.seed import seed_currencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    # Seed inicial
    db = SessionLocal()
    try:
        seed_currencies(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Currency Converter API",
    description=(
        "prueba tecnica API REST para conversión de divisas. Permite registrar monedas con sus tasas de cambio, "
        "consultar y modificar tasas, agregar o eliminar divisas, y convertir cantidades entre monedas."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Rutas API
app.include_router(currency_router)

# Servir frontend estático
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
