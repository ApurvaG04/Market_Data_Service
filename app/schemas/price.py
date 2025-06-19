from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel


class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    provider: str

class PollRequest(BaseModel):
    symbols: List[str]
    interval: int  # in seconds
    provider: Literal["yfinance", "alpha_vantage", "finnhub"] = "yfinance"