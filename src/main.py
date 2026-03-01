"""
XRP Price Alert Bot
Real-time XRP price monitoring with AI-powered analysis
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional

import aiohttp
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PriceAlert(BaseModel):
    """Price alert configuration"""
    symbol: str = Field(default="xrpusd", description="Trading pair")
    threshold: float = Field(description="Price threshold for alert")
    condition: str = Field(description="greater_than or less_than")
    enabled: bool = Field(default=True)


class XRPPriceService:
    """XRP price monitoring service"""
    
    def __init__(self):
        self.ws_url = "wss://data.ripple.com/data/stream"
        self.rest_url = "https://data.ripple.com/v2/exchanges/Binance/charts"
        self.alerts: list[PriceAlert] = []
        self.current_price: Optional[float] = None
    
    async def connect(self, session: aiohttp.ClientSession):
        """Connect to WebSocket stream"""
        try:
            ws = await session.ws_connect(self.ws_url)
            await ws.send_str(json.dumps({
                "type": "subscribe",
                "streams": ["trade", "book", "ledger"]
            }))
            logger.info("Connected to XRP WebSocket")
            return ws
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return None
    
    async def get_historical_price(self, session: aiohttp.ClientSession) -> Optional[float]:
        """Get current XRP price from REST API"""
        try:
            async with session.get(
                f"{self.rest_url}/xrpusd",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        self.current_price = data[0]["price"]
                        return self.current_price
        except Exception as e:
            logger.error(f"Price fetch error: {e}")
        return None
    
    def check_alerts(self, price: float) -> list[dict]:
        """Check if any alerts should be triggered"""
        triggered = []
        for alert in self.alerts:
            if not alert.enabled:
                continue
            
            if alert.condition == "greater_than" and price > alert.threshold:
                triggered.append({
                    "type": "alert",
                    "message": f"🚨 XRP price crossed ${alert.threshold} (CURRENT: ${price:.4f})",
                    "price": price,
                    "threshold": alert.threshold,
                    "timestamp": datetime.now().isoformat()
                })
            elif alert.condition == "less_than" and price < alert.threshold:
                triggered.append({
                    "type": "alert",
                    "message": f"🚨 XRP price dropped below ${alert.threshold} (CURRENT: ${price:.4f})",
                    "price": price,
                    "threshold": alert.threshold,
                    "timestamp": datetime.now().isoformat()
                })
        return triggered


class AIPriceAnalyzer:
    """AI-powered price analysis"""
    
    @staticmethod
    async def analyze_price_trend(
        prices: list[float],
        timeframe: str = "1h"
    ) -> dict:
        """Analyze price trend using simple AI heuristics"""
        if len(prices) < 2:
            return {"trend": "unknown", "confidence": 0.0}
        
        # Calculate simple metrics
        change = prices[-1] - prices[0]
        change_pct = (change / prices[0]) * 100
        volatility = max(prices) - min(prices)
        
        # Simple trend detection
        if change_pct > 2:
            trend = "bullish"
            confidence = min(0.5 + (change_pct / 10), 0.95)
        elif change_pct < -2:
            trend = "bearish"
            confidence = min(0.5 + (abs(change_pct) / 10), 0.95)
        else:
            trend = "neutral"
            confidence = 0.7
        
        return {
            "trend": trend,
            "confidence": confidence,
            "change_pct": change_pct,
            "volatility": volatility,
            "timeframe": timeframe,
            "analysis": AIPriceAnalyzer._generate_summary(trend, change_pct, volatility)
        }
    
    @staticmethod
    def _generate_summary(trend: str, change_pct: float, volatility: float) -> str:
        """Generate human-readable AI summary"""
        summaries = {
            "bullish": f"📈 XRP is showing bullish momentum with {abs(change_pct):.2f}% gain. Volatility: {volatility:.4f}",
            "bearish": f"📉 XRP is trending bearish with {abs(change_pct):.2f}% decline. Volatility: {volatility:.4f}",
            "neutral": f"⚖️ XRP is consolidating with minimal movement ({change_pct:.2f}%). Low volatility environment."
        }
        return summaries.get(trend, "Market analysis pending")


def get_initial_price() -> Optional[float]:
    """Synchronous price fetch for API startup"""
    import aiohttp
    
    ws_url = "wss://data.ripple.com/data/stream"
    rest_url = "https://data.ripple.com/v2/exchanges/Binance/charts"
    
    async def fetch():
        async with aiohttp.ClientSession() as session:
            return await XRPPriceService().get_historical_price(session)
    
    return asyncio.run(fetch())


if __name__ == "__main__":
    # For standalone monitoring mode
    logger.info("Running in standalone monitoring mode - WebSocket connection disabled")