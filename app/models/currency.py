from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Currency(Base):
    """
    Entidad única que registra todo lo relacionado a divisas.
    Almacena la moneda, su tasa de cambio respecto al USD y metadata.
    Compatible con SQL Server (mssql+pyodbc).
    """
    __tablename__ = "currencies"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code         = Column(String(10),  unique=True, nullable=False, index=True)   # ej: "COP"
    name         = Column(String(100), nullable=False)                             # ej: "Peso Colombiano"
    symbol       = Column(String(10),  nullable=False)                             # ej: "$"
    rate_to_usd  = Column(Float,       nullable=False)                             # tasa vs USD
    created_at   = Column(DateTime, server_default=func.now())
    updated_at   = Column(DateTime, onupdate=func.now())
