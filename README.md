# Binance Futures Order Bot

A CLI-based trading bot for Binance USDT-M Futures supporting market, limit, and advanced orders like stop-limit, OCO, TWAP, and grid.

## Features

- **Core Orders**: Market and Limit orders
- **Advanced Orders**: Stop-Limit, OCO, TWAP, Grid
- **Validation**: Input validation for symbol, quantity, prices
- **Logging**: All actions logged to `bot.log` with timestamps

## Setup

1. Clone or download the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Obtain Binance API key and secret from [Binance](https://www.binance.com/en/my/settings/api-management).
4. Set environment variables:
   - `BINANCE_API_KEY`: Your API key
   - `BINANCE_API_SECRET`: Your API secret
   - For testnet: Use testnet API keys and set `testnet=True` in client initialization (modify code accordingly).

## Usage

### Market Order

```
python src/market_orders.py BTCUSDT BUY 0.01
```

### Limit Order

```
python src/limit_orders.py BTCUSDT BUY 0.01 50000
```

### Stop-Limit Order

```
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 49000 48000
```

### OCO Order

```
python src/advanced/oco.py BTCUSDT BUY 0.01 51000 49000 48500
```

### TWAP Order

```
python src/advanced/twap.py BTCUSDT BUY 0.01 10 60
```

### Grid Orders

```
python src/advanced/grid.py BTCUSDT 50000 5 0.002
```

## File Structure

```
[project_root]/
├── src/
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── advanced/
│   │   ├── stop_limit.py
│   │   ├── oco.py
│   │   ├── twap.py
│   │   └── grid.py
│   └── __init__.py
├── bot.log
├── requirements.txt
└── README.md
```

## Notes

- Use testnet for testing to avoid real trades.
- Logs are saved in `bot.log`.
- Ensure sufficient balance and permissions for futures trading.

## Resources

- [Binance Futures API Docs](https://binance-docs.github.io/apidocs/futures/en/)
- Historical Data: [Link](https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view)
- Fear & Greed Index: [Link](https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view)
