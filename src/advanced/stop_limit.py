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

def validate_price(price):
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be positive.")
        return p
    except ValueError:
        raise ValueError("Invalid price. Must be a number.")

def place_stop_limit_order(api_key, api_secret, symbol, side, quantity, stop_price, limit_price):
    client = Client(api_key, api_secret)
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='STOP',
            quantity=quantity,
            stopPrice=stop_price,
            price=limit_price,
            timeInForce='GTC'
        )
        logging.info(f"Stop-limit order placed: {order}")
        print(f"Stop-limit order placed: {order}")
    except BinanceAPIException as e:
        logging.error(f"Error placing stop-limit order: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Place a stop-limit order on Binance Futures.')
    parser.add_argument('symbol', help='Trading pair, e.g., BTCUSDT')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', help='Order quantity')
    parser.add_argument('stop_price', help='Stop price')
    parser.add_argument('limit_price', help='Limit price')

    args = parser.parse_args()

    # Validate inputs
    validate_symbol(args.symbol)
    quantity = validate_quantity(args.quantity)
    stop_price = validate_price(args.stop_price)
    limit_price = validate_price(args.limit_price)

    # Get API keys
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    place_stop_limit_order(api_key, api_secret, args.symbol, args.side, quantity, stop_price, limit_price)

if __name__ == '__main__':
    main()
