import math
from logger import get_logger
from binance_client import BinanceFuturesClient
logger = get_logger()

def run_grid(symbol, lower, upper, steps, client_cfg):
    symbol = symbol.upper()
    if lower <= 0 or upper <= 0 or upper <= lower:
        raise ValueError('Invalid price bounds')
    if steps < 1:
        raise ValueError('steps must be >=1')
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    gap = (upper - lower) / steps
    grid = []
    logger.info(f'Creating grid from {lower} to {upper} in {steps} steps (gap {gap})')
    for i in range(steps):
        buy_price = lower + i*gap
        sell_price = buy_price + gap
        grid.append({'buy': buy_price, 'sell': sell_price})
    # Simulation: log grid; real implementation would place OCO/limit orders and manage lifecycle
    logger.info(f'Grid plan: {grid}')
    return {'status':'simulated','grid':grid}
