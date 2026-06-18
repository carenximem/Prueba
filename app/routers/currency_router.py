from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.currency import (
    CurrencyCreate, CurrencyUpdate, CurrencyResponse,
    ConversionRequest, ConversionResponse
)
from app.services.currency_service import CurrencyService

router = APIRouter(prefix="/api/currencies", tags=["Divisas"])


@router.get("/", response_model=List[CurrencyResponse], summary="Listar todas las divisas")
def list_currencies(db: Session = Depends(get_db)):
    """Retorna el listado completo de divisas registradas con sus tasas de cambio."""
    return CurrencyService.get_all(db)


@router.get("/{currency_id}", response_model=CurrencyResponse, summary="Obtener divisa por ID")
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    """Retorna los datos de una divisa específica por su ID."""
    return CurrencyService.get_by_id(db, currency_id)


@router.get("/code/{code}", response_model=CurrencyResponse, summary="Obtener divisa por código")
def get_currency_by_code(code: str, db: Session = Depends(get_db)):
    """Retorna los datos de una divisa específica por su código (ej: USD, COP)."""
    return CurrencyService.get_by_code(db, code)


@router.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED,
             summary="Registrar nueva divisa")
def create_currency(data: CurrencyCreate, db: Session = Depends(get_db)):
    """Registra una nueva divisa con su tasa de cambio respecto al USD."""
    return CurrencyService.create(db, data)


@router.put("/{currency_id}", response_model=CurrencyResponse, summary="Actualizar divisa")
def update_currency(currency_id: int, data: CurrencyUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de una divisa existente (nombre, símbolo o tasa de cambio)."""
    return CurrencyService.update(db, currency_id, data)


@router.patch("/code/{code}/rate", response_model=CurrencyResponse, summary="Actualizar tasa de cambio")
def update_rate(code: str, new_rate: float, db: Session = Depends(get_db)):
    """Actualiza únicamente la tasa de cambio de una divisa por su código."""
    return CurrencyService.update_rate(db, code, new_rate)


@router.delete("/{currency_id}", summary="Eliminar divisa")
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    """Elimina una divisa del sistema."""
    return CurrencyService.delete(db, currency_id)


@router.post("/convert", response_model=ConversionResponse, summary="Convertir divisas")
def convert_currency(request: ConversionRequest, db: Session = Depends(get_db)):
    """
    Convierte una cantidad de dinero desde una moneda de partida
    hacia uno o más monedas de llegada seleccionadas por el usuario.
    """
    return CurrencyService.convert(db, request)
