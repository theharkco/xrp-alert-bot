"""
FastAPI server for XRP Price Alert Bot
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import Optional, list

from src.main import XRPPriceService, AIPriceAnalyzer, PriceAlert

app = FastAPI(
    title="XRP Price Alert Bot",
    description="Real-time XRP price monitoring with AI-powered analysis",
    version="1.0.0"
)

# Global service instance
price_service = XRPPriceService()


class AlertConfig(BaseModel):
    """Alert configuration request"""
    symbol: str = "xrpusd"
    threshold: float
    condition: str  # "greater_than" or "less_than"
    enabled: bool = True


class AlertResponse(BaseModel):
    """Alert configuration response"""
    success: bool
    alert: PriceAlert
    message: str


class PriceResponse(BaseModel):
    """Current price response"""
    price: float
    timestamp: str
    trend: Optional[str] = None
    analysis: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    global price_service
    # Setup default alerts
    price_service.alerts = [
        PriceAlert(symbol="xrpusd", threshold=2.50, condition="greater_than", enabled=True),
        PriceAlert(symbol="xrpusd", threshold=2.00, condition="less_than", enabled=True),
    ]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "XRP Price Alert Bot",
        "status": "running",
        "endpoints": [
            "/alerts",
            "/price",
            "/analyze",
            "/health"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "current_price": price_service.current_price,
        "alerts_active": len([a for a in price_service.alerts if a.enabled])
    }


@app.post("/alerts", response_model=AlertResponse)
async def configure_alert(alert_config: AlertConfig):
    """Add or update a price alert"""
    try:
        # Validate condition
        if alert_config.condition not in ["greater_than", "less_than"]:
            raise HTTPException(status_code=400, detail="Invalid condition")
        
        # Create alert
        alert = PriceAlert(
            symbol=alert_config.symbol,
            threshold=alert_config.threshold,
            condition=alert_config.condition,
            enabled=alert_config.enabled
        )
        
        # Add to service
        price_service.alerts.append(alert)
        
        return AlertResponse(
            success=True,
            alert=alert,
            message=f"Alert configured: XRP {alert.condition} ${alert.threshold}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts")
async def list_alerts():
    """List all active alerts"""
    return {
        "alerts": [
            {
                "symbol": alert.symbol,
                "threshold": alert.threshold,
                "condition": alert.condition,
                "enabled": alert.enabled
            }
            for alert in price_service.alerts
        ],
        "total": len(price_service.alerts)
    }


@app.delete("/alerts/{alert_index}")
async def delete_alert(alert_index: int):
    """Delete an alert by index"""
    if alert_index < 0 or alert_index >= len(price_service.alerts):
        raise HTTPException(status_code=404, detail="Alert not found")
    
    deleted = price_service.alerts.pop(alert_index)
    return {
        "success": True,
        "message": f"Alert deleted: {deleted.symbol} {deleted.condition} ${deleted.threshold}"
    }


@app.get("/price", response_model=PriceResponse)
async def get_price():
    """Get current XRP price"""
    async with aiohttp.ClientSession() as session:
        price = await price_service.get_historical_price(session)
        
        if not price:
            raise HTTPException(status_code=500, detail="Failed to fetch price")
        
        return PriceResponse(
            price=price,
            timestamp=datetime.now().isoformat()
        )


@app.post("/analyze", response_model=dict)
async def analyze_price():
    """Analyze current price trend"""
    async with aiohttp.ClientSession() as session:
        price = await price_service.get_historical_price(session)
        
        if not price:
            raise HTTPException(status_code=500, detail="Failed to fetch price")
        
        # Simulate price history for analysis
        prices = [price * (1 + (i - 50) * 0.001) for i in range(100)]
        
        analysis = await AIPriceAnalyzer.analyze_price_trend(prices)
        
        return analysis


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)