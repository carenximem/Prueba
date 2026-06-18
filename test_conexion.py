from app.database import engine

try:
    with engine.connect() as conn:
        print(" Conexión exitosa a SQL Server")
except Exception as e:
    print(f" Error de conexión: {e}")
