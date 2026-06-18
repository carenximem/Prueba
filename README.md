# 💱 Currency Converter API

API REST para conversión de divisas — Prueba Técnica OATI · UD  
**Punto #2:** Servicio de conversión de divisas

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Base de datos | **SQL Server** (mssql+pyodbc) |
| Validación | Pydantic v2 |
| Servidor | Uvicorn (ASGI) |
| Frontend | HTML + CSS + JS vanilla |

---

## Estructura del Proyecto

```
currency-api/
├── main.py                        # Punto de entrada FastAPI
├── requirements.txt
├── README.md
├── .env.example                   # Variables de entorno de ejemplo
├── app/
│   ├── database.py                # Configuración SQLAlchemy → SQL Server
│   ├── seed.py                    # Datos iniciales (12 divisas)
│   ├── models/
│   │   └── currency.py            # Entidad única: Currency
│   ├── schemas/
│   │   └── currency.py            # Schemas Pydantic (request/response)
│   ├── services/
│   │   └── currency_service.py    # Lógica de negocio
│   └── routers/
│       └── currency_router.py     # Endpoints REST
└── static/
    └── index.html                 # Frontend SPA
```

---

## Modelo de Datos (SQL Server)

Entidad **única**, tal como especifica el enunciado:

```sql
CREATE TABLE currencies (
    id           INT           PRIMARY KEY IDENTITY(1,1),
    code         VARCHAR(10)   NOT NULL UNIQUE,   -- "COP", "EUR"
    name         VARCHAR(100)  NOT NULL,           -- "Peso Colombiano"
    symbol       VARCHAR(10)   NOT NULL,           -- "$", "€"
    rate_to_usd  FLOAT         NOT NULL,           -- tasa vs USD (base)
    created_at   DATETIME      DEFAULT GETDATE(),
    updated_at   DATETIME
);
```

**Lógica de conversión:**  
Todas las tasas se almacenan relativas al USD.  
Para convertir de A → B: `(amount / rate_A) × rate_B`

---

## Instrucciones de Ejecución

### 1. Pre-requisitos
- **SQL Server** instalado (Express, Developer o superior)
- **ODBC Driver 17 for SQL Server** instalado  
  → Descargar: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Python 3.11+

### 2. Crear la base de datos en SQL Server
```sql
CREATE DATABASE currency_db;
```

### 3. Configurar variables de entorno
Crea un archivo `.env` (o exporta las variables) con:
```env
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=currency_db
DB_USER=sa
DB_PASSWORD=TuPassword123!
DB_DRIVER=ODBC Driver 17 for SQL Server
```

O edita directamente `app/database.py` con tus credenciales.

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Iniciar el servidor
```bash
uvicorn main:app --reload
```

### 6. Acceder
- **Frontend:** http://localhost:8000  
- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc

Al iniciar, SQLAlchemy crea la tabla automáticamente y carga **12 divisas** de ejemplo.

---

## Endpoints REST

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/currencies/` | Listar todas las divisas |
| GET | `/api/currencies/{id}` | Obtener divisa por ID |
| GET | `/api/currencies/code/{code}` | Obtener divisa por código |
| POST | `/api/currencies/` | Registrar nueva divisa |
| PUT | `/api/currencies/{id}` | Actualizar divisa |
| PATCH | `/api/currencies/code/{code}/rate` | Actualizar sólo la tasa |
| DELETE | `/api/currencies/{id}` | Eliminar divisa |
| POST | `/api/currencies/convert` | Convertir entre divisas |

### Ejemplo: Conversión
```http
POST /api/currencies/convert
Content-Type: application/json

{
  "amount": 1000.0,
  "from_currency": "USD",
  "to_currencies": ["COP", "EUR", "BRL"]
}
```

**Respuesta:**
```json
{
  "amount": 1000.0,
  "from_currency": "USD",
  "results": [
    { "currency_code": "COP", "converted_amount": 4150000.0, "symbol": "$" },
    { "currency_code": "EUR", "converted_amount": 920.0,     "symbol": "€" },
    { "currency_code": "BRL", "converted_amount": 5050.0,    "symbol": "R$" }
  ]
}
```

---

## Divisas Precargadas (12)

USD · COP · EUR · BRL · MXN · GBP · JPY · CAD · ARS · CLP · PEN · CNY

---

## Buenas Prácticas Aplicadas

- Separación de capas: models / schemas / services / routers
- Manejo de excepciones con HTTPException y códigos HTTP correctos
- Validación de datos con Pydantic v2
- Lógica de negocio desacoplada de los routers (patrón Service)
- Seed automático sin duplicación en arranques repetidos
- Configuración por variables de entorno (sin credenciales hardcodeadas)
