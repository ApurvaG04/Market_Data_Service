from fastapi import APIRouter
from app.schemas.price import PriceResponse, PollRequest
from app.services.market_data import get_latest_price, start_polling


router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_price(symbol: str, provider: str = "yfinance"):
    return await get_latest_price(symbol, provider)

@router.post("/prices/poll", status_code=202)
async def poll_prices(req: PollRequest):
    return await start_polling(req)