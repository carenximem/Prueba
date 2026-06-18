import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SERVER   = os.getenv("DB_SERVER",   "localhost\\SQLEXPRESS")
DATABASE = os.getenv("DB_NAME",     "PRUEBATECNICA")
DRIVER   = os.getenv("DB_DRIVER",   "ODBC Driver 17 for SQL Server")

# Trusted_Connection=yes → Autenticación Windows (usuario caren\cmala)
DATABASE_URL = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER.replace(' ', '+')}"
    f"&Trusted_Connection=yes"
)

engine = create_engine(DATABASE_URL, fast_executemany=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()