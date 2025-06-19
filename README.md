# 📈 Market Data Service

A FastAPI-based microservice for polling, storing, and publishing market price data using Kafka. Data providers like Yahoo Finance (`yfinance`) are supported. Price events are pushed to Kafka for downstream processing.

---

## 📚 Overview

This service allows you to:

- Fetch the latest price for a symbol from a data provider.
- Start polling for price updates at a configurable interval.
- Publish real-time price updates to a Kafka topic (`price-events`).
- Store data in a PostgreSQL database via SQLModel.
- Support future expansion (multiple providers, consumers, analytics).

---

## ⚙️ Setup & Installation

### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) with WSL 2 backend on Windows
- Python 3.11+ (for local debugging)
- `docker-compose`
- Kafka + Zookeeper (included via Docker)

### 2. Clone the Repository

```bash
git clone https://github.com/yourname/market-data-service.git
cd market-data-service
```

### 3. Start the Services

```bash
docker-compose up --build
```

> This starts:
>
> - FastAPI app on `localhost:8000`
> - PostgreSQL on port `5432`
> - Kafka (via Zookeeper) on port `9092`
> - Adminer DB GUI at `localhost:8080`

---

## 🧪 API Documentation

Once running, access:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

#### GET `/prices/latest`

Query the most recent price.

```http
GET /prices/latest?symbol=AAPL&provider=yfinance
```

#### POST `/prices/poll`

Start polling prices for a list of symbols.
```http
POST /prices/poll
```
```json
{
  "symbols": ["AAPL", "GOOG"],
  "interval": 60
}
```

---

## 🧱 Architecture Overview

```
Client ──────┐
            ▼
       [ FastAPI ]
            │
  ┌───────────────────────────────┐
  │         ▼             │
  │   SQLModel + DB       │
  │         │             ▼
  │  Kafka Producer ──▶ [ price-events topic ]
  ▼                       ▲
 Swagger UI         (future consumers)
```

- **Framework**: FastAPI
- **DB Layer**: SQLModel + Alembic
- **Messaging**: Kafka
- **Data Provider**: yfinance (Yahoo Finance)
- **Schema**: Pydantic

---

## 👨‍💼 Local Development

### Enter API container shell

```bash
docker exec -it <container_name> bash
```

### Run alembic migrations

```bash
alembic upgrade head
```

### Format code

```bash
black app/
```

### Install extra Python dependencies

```bash
pip install <package>
```

---

## 💠 Troubleshooting

| Problem                      | Solution                                                      |
| ---------------------------- | ------------------------------------------------------------- |
| `ModuleNotFoundError`        | Make sure you rebuild containers: `docker-compose up --build` |
| `Kafka connect ECONNREFUSED` | Ensure Kafka container is running and port `9092` is exposed  |
| `WSL 2 not found` (Windows)  | Install and enable WSL 2, restart Docker Desktop              |
| Database errors              | Check `DATABASE_URL` in your `.env` and docker-compose config |

---

## 🔮 Future Improvements

- Kafka consumer to persist prices to DB
- Prometheus + Grafana for monitoring
- More price providers (e.g., Alpha Vantage)
- Authentication & rate limiting

---

## 📄 License

MIT License

