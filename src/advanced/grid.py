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

def validate_price(price):
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be positive.")
        return p
    except ValueError:
        raise ValueError("Invalid price. Must be a number.")

def place_grid_orders(api_key, api_secret, symbol, base_price, grid_levels, quantity_per_level):
    client = Client(api_key, api_secret)
    for i in range(grid_levels):
        buy_price = base_price * (1 - 0.01 * (i + 1))  # Example: 1% lower each level
        sell_price = base_price * (1 + 0.01 * (i + 1))  # Example: 1% higher each level
        try:
            # Place buy limit order
            buy_order = client.futures_create_order(
                symbol=symbol,
                side='BUY',
                type='LIMIT',
                quantity=quantity_per_level,
                price=buy_price,
                timeInForce='GTC'
            )
            logging.info(f"Grid buy order {i+1} placed: {buy_order}")
            print(f"Grid buy order {i+1} placed: {buy_order}")

            # Place sell limit order
            sell_order = client.futures_create_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                quantity=quantity_per_level,
                price=sell_price,
                timeInForce='GTC'
            )
            logging.info(f"Grid sell order {i+1} placed: {sell_order}")
            print(f"Grid sell order {i+1} placed: {sell_order}")
        except BinanceAPIException as e:
            logging.error(f"Error placing grid order {i+1}: {e}")
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Place grid orders on Binance Futures.')
    parser.add_argument('symbol', help='Trading pair, e.g., BTCUSDT')
    parser.add_argument('base_price', help='Base price for grid')
    parser.add_argument('grid_levels', help='Number of grid levels')
    parser.add_argument('quantity_per_level', help='Quantity per grid level')

    args = parser.parse_args()

    # Validate inputs
    validate_symbol(args.symbol)
    base_price = validate_price(args.base_price)
    grid_levels = int(args.grid_levels)
    if grid_levels <= 0:
        raise ValueError("Grid levels must be positive.")
    quantity_per_level = validate_quantity(args.quantity_per_level)

    # Get API keys
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    place_grid_orders(api_key, api_secret, args.symbol, base_price, grid_levels, quantity_per_level)

if __name__ == '__main__':
    main()
