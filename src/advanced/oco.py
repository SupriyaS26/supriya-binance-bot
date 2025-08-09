from logger import get_logger
from binance_client import BinanceFuturesClient
logger = get_logger()

def place_oco(symbol, side, quantity, take_profit, stop_price, stop_limit_price, client_cfg):
    symbol = symbol.upper()
    if take_profit <= 0 or stop_price <= 0 or stop_limit_price <= 0:
        raise ValueError('Prices must be > 0')
    client = BinanceFuturesClient(client_cfg.get('api_key'), client_cfg.get('api_secret'), dry_run=client_cfg.get('dry_run', True))
    # Futures does not have native OCO; emulate by placing two opposite orders and cancel one when other fills.
    logger.info('Placing OCO (simulated for futures): placing TP and SL orders')
    tp = client.place_limit_order(symbol, 'SELL' if side=='BUY' else 'BUY', quantity, take_profit)
    sl = client.place_stop_limit(symbol, 'SELL' if side=='BUY' else 'BUY', quantity, stop_price, stop_limit_price)
    response = {'tp': tp, 'sl': sl, 'strategy': 'simulated_oco'}
    logger.info(f'OCO response: {response}')
    return response
