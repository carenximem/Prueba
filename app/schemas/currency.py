from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CurrencyBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=10, description="Código ISO de la moneda (ej: USD, COP)")
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo de la moneda")
    symbol: str = Field(..., min_length=1, max_length=10, description="Símbolo de la moneda")
    rate_to_usd: float = Field(..., gt=0, description="Tasa de cambio respecto al USD")


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    symbol: Optional[str] = Field(None, min_length=1, max_length=10)
    rate_to_usd: Optional[float] = Field(None, gt=0)


class CurrencyResponse(CurrencyBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Schemas para conversión
class ConversionRequest(BaseModel):
    amount: float = Field(..., description="Cantidad de dinero a convertir (doble precisión)")
    from_currency: str = Field(..., description="Código de la moneda de partida")
    to_currencies: List[str] = Field(..., min_length=1, description="Lista de monedas de llegada")


class ConversionResult(BaseModel):
    currency_code: str
    currency_name: str
    symbol: str
    converted_amount: float
    rate_to_usd: float


class ConversionResponse(BaseModel):
    amount: float
    from_currency: str
    results: List[ConversionResult]
