from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class RawPriceData(SQLModel, table=True):
    symbol: str = Field(primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        primary_key=True)
    price: float
    source: str
    raw_response: str
    