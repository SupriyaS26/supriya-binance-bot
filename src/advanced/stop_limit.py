from logger import get_logger
from binance_client import BinanceFuturesClient
logger = get_logger()

def place_stop_limit(symbol, side, quantity, stop_price, limit_price, client_cfg):
    symbol = symbol.upper()
    if stop_price <= 0 or limit_price <= 0:
        raise ValueError('Prices must be > 0')
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    resp = client.place_stop_limit(symbol, side, quantity, stop_price, limit_price)
    logger.info(f'Stop-limit response: {resp}')
    return resp
