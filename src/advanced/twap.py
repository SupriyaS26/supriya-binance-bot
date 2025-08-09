import time
from logger import get_logger
from binance_client import BinanceFuturesClient
logger = get_logger()

def run_twap(symbol, side, quantity, slices=5, interval=1.0, client_cfg=None):
    symbol = symbol.upper()
    if slices <= 0:
        raise ValueError('slices must be > 0')
    slice_qty = float(quantity) / slices
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    results = []
    logger.info(f'Starting TWAP: {slices} slices, {interval}s interval, {slice_qty} per slice')
    for i in range(slices):
        res = client.place_market_order(symbol, side, slice_qty)
        results.append(res)
        logger.info(f'TWAP slice {i+1}/{slices} result: {res}')
        time.sleep(interval)
    return results
