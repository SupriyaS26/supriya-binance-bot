from logger import get_logger
from binance_client import BinanceFuturesClient
logger = get_logger()

def validate_price(p):
    if p <= 0:
        raise ValueError('Price must be > 0')
    return float(p)

def place_limit_order(symbol, side, quantity, price, client_cfg):
    symbol = symbol.upper()
    price = validate_price(price)
    if quantity <= 0:
        raise ValueError('Quantity must be > 0')
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    resp = client.place_limit_order(symbol, side, quantity, price)
    logger.info(f'Limit order response: {resp}')
    return resp
