import argparse
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_symbol(symbol):
    if not symbol.isupper() or not symbol.endswith('USDT'):
        raise ValueError("Invalid symbol. Must be uppercase and end with USDT.")

def validate_quantity(quantity):
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        return qty
    except ValueError:
        raise ValueError("Invalid quantity. Must be a number.")

def place_market_order(api_key, api_secret, symbol, side, quantity):
    client = Client(api_key, api_secret)
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )
        logging.info(f"Market order placed: {order}")
        print(f"Market order placed: {order}")
    except BinanceAPIException as e:
        logging.error(f"Error placing market order: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Place a market order on Binance Futures.')
    parser.add_argument('symbol', help='Trading pair, e.g., BTCUSDT')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', help='Order quantity')

    args = parser.parse_args()

    # Validate inputs
    validate_symbol(args.symbol)
    quantity = validate_quantity(args.quantity)

    # Get API keys
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    place_market_order(api_key, api_secret, args.symbol, args.side, quantity)

if __name__ == '__main__':
    main()
