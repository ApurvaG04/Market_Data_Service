import asyncio
import yfinance as yf
from datetime import datetime
from app.schemas.price import PriceResponse, PollRequest
from app.services.producer import publish_price_event
from uuid import uuid4

async def get_latest_price(symbol: str, provider: str) -> PriceResponse:
    if provider == "yfinance":
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            raise ValueError(f"No data for {symbol}")
        latest = data.iloc[-1]
        price_response = PriceResponse(
            symbol=symbol,
            price=round(latest["Close"], 2),
            timestamp=latest.name.to_pydatetime(),
            provider=provider
        )
        event_data = {
            "symbol": price_response.symbol,
            "price": price_response.price,
            "timestamp": price_response.timestamp.isoformat(),
            "source": price_response.provider,
            "raw_response": "{}" 
        }        
        publish_price_event(event_data)        
        return price_response
    else:
        raise NotImplementedError(f"Provider '{provider}' is not supported yet")

async def start_polling(req: PollRequest) -> dict:
    job_id = f"poll_{uuid4().hex[:8]}"
    
    async def poll_symbol(symbol: str, interval: int):
        while True:
            try:
                await get_latest_price(symbol, "yfinance")
    
            except Exception as e:
                print(f"Polling error for {symbol}: {e}")
            await asyncio.sleep(interval)
    
    for sym in req.symbols:
        asyncio.create_task(poll_symbol(sym, req.interval))
    
    return {
        "job_id": job_id,
        "status": "accepted",
        "config": {
            "symbols": req.symbols,
            "interval": req.interval
        }
    }