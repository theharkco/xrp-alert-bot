# 🚀 XRP Price Alert Bot

Real-time XRP price monitoring with AI-powered analysis and configurable alerts.

## Features

- ⚡ **Real-time Price Monitoring**: WebSocket connection to XRP Ledger
- 🤖 **AI-Powered Analysis**: Trend detection and market analysis
- 🔔 **Configurable Alerts**: Set price thresholds for greater_than/less_than
- 📊 **REST API**: FastAPI endpoints for integration
- 💎 **XRP Ledger Integration**: Direct connection to Ripple data stream

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Async**: aiohttp, websockets
- **Data**: Pydantic models
- **Deployment**: Coolify with nixpacks

## Quick Start

### Local Development

```bash
# Clone repo
git clone https://github.com/theharkco/xrp-alert-bot
cd xrp-alert-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python src/main.py

# Or run the API server
python src/api.py
```

### API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `GET /alerts` - List all alerts
- `POST /alerts` - Create new alert
- `DELETE /alerts/{index}` - Delete alert
- `GET /price` - Current XRP price
- `POST /analyze` - AI price analysis

### Example: Create Alert

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"symbol": "xrpusd", "threshold": 3.00, "condition": "greater_than"}'
```

## Deployment to Coolify

This app is configured for Coolify deployment using nixpacks:

1. **Repository**: https://github.com/theharkco/xrp-alert-bot
2. **Build Command**: `echo 'No build needed for Python app'`
3. **Start Command**: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `PORT`: 8000 (default)

### nixpacks Configuration

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'No build needed for Python app'"]

[options]
path = "."
```

## Alert Configuration

Default alerts on startup:
- XRP > $2.50 (bullish alert)
- XRP < $2.00 (bearish alert)

Add custom alerts via API:
```json
{
  "symbol": "xrpusd",
  "threshold": 2.75,
  "condition": "greater_than",
  "enabled": true
}
```

## AI Analysis

The bot uses heuristic-based AI analysis to detect:
- **Bullish trends**: Price increases > 2%
- **Bearish trends**: Price decreases > 2%
- **Neutral**: Consolidation period

Analysis includes:
- Trend direction
- Confidence score
- Percentage change
- Volatility metrics
- Human-readable summary

## Security Notes

⚠️ **Important**: For production:
- Use environment variables for configuration
- Add authentication to API endpoints
- Implement rate limiting
- Set up proper logging and monitoring

## License

MIT

---

Built with ❤️ by minihark 🎭