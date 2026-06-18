from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate, CurrencyUpdate, ConversionRequest, ConversionResponse, ConversionResult


class CurrencyService:

    @staticmethod
    def get_all(db: Session) -> List[Currency]:
        return db.query(Currency).all()

    @staticmethod
    def get_by_id(db: Session, currency_id: int) -> Currency:
        currency = db.query(Currency).filter(Currency.id == currency_id).first()
        if not currency:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Divisa con id={currency_id} no encontrada")
        return currency

    @staticmethod
    def get_by_code(db: Session, code: str) -> Currency:
        currency = db.query(Currency).filter(Currency.code == code.upper()).first()
        if not currency:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Divisa con código '{code}' no encontrada")
        return currency

    @staticmethod
    def create(db: Session, data: CurrencyCreate) -> Currency:
        existing = db.query(Currency).filter(Currency.code == data.code.upper()).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Ya existe una divisa con código '{data.code}'")
        currency = Currency(
            code=data.code.upper(),
            name=data.name,
            symbol=data.symbol,
            rate_to_usd=data.rate_to_usd
        )
        db.add(currency)
        db.commit()
        db.refresh(currency)
        return currency

    @staticmethod
    def update(db: Session, currency_id: int, data: CurrencyUpdate) -> Currency:
        currency = CurrencyService.get_by_id(db, currency_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(currency, field, value)
        db.commit()
        db.refresh(currency)
        return currency

    @staticmethod
    def update_rate(db: Session, code: str, new_rate: float) -> Currency:
        currency = CurrencyService.get_by_code(db, code)
        currency.rate_to_usd = new_rate
        db.commit()
        db.refresh(currency)
        return currency

    @staticmethod
    def delete(db: Session, currency_id: int) -> dict:
        currency = CurrencyService.get_by_id(db, currency_id)
        db.delete(currency)
        db.commit()
        return {"message": f"Divisa '{currency.code}' eliminada exitosamente"}

    @staticmethod
    def convert(db: Session, request: ConversionRequest) -> ConversionResponse:
        # Obtener moneda de partida
        from_currency = CurrencyService.get_by_code(db, request.from_currency)

        # Convertir cantidad a USD primero (moneda base)
        amount_in_usd = request.amount / from_currency.rate_to_usd

        results = []
        for target_code in request.to_currencies:
            target = CurrencyService.get_by_code(db, target_code)
            converted = amount_in_usd * target.rate_to_usd
            results.append(ConversionResult(
                currency_code=target.code,
                currency_name=target.name,
                symbol=target.symbol,
                converted_amount=round(converted, 6),
                rate_to_usd=target.rate_to_usd
            ))

        return ConversionResponse(
            amount=request.amount,
            from_currency=from_currency.code,
            results=results
        )
