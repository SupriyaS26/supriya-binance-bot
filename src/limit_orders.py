# limit_orders.py
from logger import get_logger
from binance_client import BinanceFuturesClient

logger = get_logger()

def validate_symbol(symbol):
    if not symbol.isalnum():
        raise ValueError('Invalid symbol')
    return symbol.upper()

def validate_quantity(q):
    if q <= 0:
        raise ValueError('Quantity must be > 0')
    return float(q)

def validate_price(p):
    if p <= 0:
        raise ValueError('Price must be > 0')
    return float(p)


def place_limit_order(symbol, side, quantity, price, client_cfg):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    price = validate_price(price)

    client = BinanceFuturesClient(
        client_cfg.get('api_key'),
        client_cfg.get('api_secret'),
        dry_run=client_cfg.get('dry_run', True)
    )
    resp = client.place_limit_order(symbol, side, quantity, price)
    logger.info(f'Limit order response: {resp}')
    return resp
def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price, client_cfg):
    # validate inputs...
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    resp = client.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    logger.info(f'Stop-limit order response: {resp}')
    return resp