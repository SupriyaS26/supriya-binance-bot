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

def place_market_order(symbol, side, quantity, client_cfg):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    resp = client.place_market_order(symbol, side, quantity)
    logger.info(f'Market order response: {resp}')
    return resp
