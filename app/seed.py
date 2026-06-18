from sqlalchemy.orm import Session
from app.models.currency import Currency


INITIAL_CURRENCIES = [
    {"code": "USD", "name": "Dólar Estadounidense",    "symbol": "$",    "rate_to_usd": 1.0},
    {"code": "COP", "name": "Peso Colombiano",          "symbol": "$",    "rate_to_usd": 4150.0},
    {"code": "EUR", "name": "Euro",                     "symbol": "€",    "rate_to_usd": 0.92},
    {"code": "BRL", "name": "Real Brasileño",           "symbol": "R$",   "rate_to_usd": 5.05},
    {"code": "MXN", "name": "Peso Mexicano",            "symbol": "$",    "rate_to_usd": 17.15},
    {"code": "GBP", "name": "Libra Esterlina",          "symbol": "£",    "rate_to_usd": 0.79},
    {"code": "JPY", "name": "Yen Japonés",              "symbol": "¥",    "rate_to_usd": 149.50},
    {"code": "CAD", "name": "Dólar Canadiense",         "symbol": "CA$",  "rate_to_usd": 1.36},
    {"code": "ARS", "name": "Peso Argentino",           "symbol": "$",    "rate_to_usd": 870.0},
    {"code": "CLP", "name": "Peso Chileno",             "symbol": "$",    "rate_to_usd": 950.0},
    {"code": "PEN", "name": "Sol Peruano",              "symbol": "S/.",  "rate_to_usd": 3.75},
    {"code": "CNY", "name": "Yuan Chino",               "symbol": "¥",    "rate_to_usd": 7.24},
]


def seed_currencies(db: Session):
    """Inserta las divisas iniciales si la tabla está vacía."""
    count = db.query(Currency).count()
    if count == 0:
        for data in INITIAL_CURRENCIES:
            db.add(Currency(**data))
        db.commit()
        print(f"[Seed] {len(INITIAL_CURRENCIES)} divisas registradas.")
    else:
        print(f"[Seed] Ya existen {count} divisas, se omite el seed.")
