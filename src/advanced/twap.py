import argparse
import logging
import time
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

def validate_positive_int(value):
    try:
        val = int(value)
        if val <= 0:
            raise ValueError("Must be positive integer.")
        return val
    except ValueError:
        raise ValueError("Invalid integer. Must be a number.")

def place_twap_order(api_key, api_secret, symbol, side, total_quantity, num_orders, interval_seconds):
    client = Client(api_key, api_secret)
    quantity_per_order = total_quantity / num_orders
    for i in range(num_orders):
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity_per_order
            )
            logging.info(f"TWAP order {i+1}/{num_orders} placed: {order}")
            print(f"TWAP order {i+1}/{num_orders} placed: {order}")
        except BinanceAPIException as e:
            logging.error(f"Error placing TWAP order {i+1}: {e}")
            print(f"Error: {e}")
        if i < num_orders - 1:
            time.sleep(interval_seconds)

def main():
    parser = argparse.ArgumentParser(description='Place a TWAP order on Binance Futures.')
    parser.add_argument('symbol', help='Trading pair, e.g., BTCUSDT')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('total_quantity', help='Total order quantity')
    parser.add_argument('num_orders', help='Number of orders to split into')
    parser.add_argument('interval_seconds', help='Interval between orders in seconds')

    args = parser.parse_args()

    # Validate inputs
    validate_symbol(args.symbol)
    total_quantity = validate_quantity(args.total_quantity)
    num_orders = validate_positive_int(args.num_orders)
    interval_seconds = validate_positive_int(args.interval_seconds)

    # Get API keys
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    place_twap_order(api_key, api_secret, args.symbol, args.side, total_quantity, num_orders, interval_seconds)

if __name__ == '__main__':
    main()
