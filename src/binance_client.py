"""Wrapper for Binance Futures client.
If python-binance is not installed or API keys are absent, runs in simulation (dry-run) mode.
"""
from typing import Optional
try:
    from binance import Client
    from binance.enums import *
    BINANCE_AVAILABLE = True
except Exception:
    BINANCE_AVAILABLE = False

from logger import get_logger
logger = get_logger()

class BinanceFuturesClient:
    def __init__(self, api_key: Optional[str], api_secret: Optional[str], dry_run: bool=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.dry_run = dry_run or (api_key is None or api_secret is None)
        if not BINANCE_AVAILABLE and not self.dry_run:
            logger.warning('python-binance not available; switching to dry-run mode')
            self.dry_run = True
        if not self.dry_run:
            self.client = Client(api_key, api_secret)
        else:
            self.client = None

    def place_market_order(self, symbol, side, quantity):
        logger.info(f'place_market_order called: {symbol} {side} {quantity}')
        if self.dry_run:
            return {'status':'simulated','symbol':symbol,'side':side,'quantity':quantity}
        order = self.client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
        return order

    def place_limit_order(self, symbol, side, quantity, price, timeInForce='GTC'):
        logger.info(f'place_limit_order called: {symbol} {side} {quantity} @ {price}')
        if self.dry_run:
            return {'status':'simulated','symbol':symbol,'side':side,'quantity':quantity,'price':price}
        order = self.client.futures_create_order(symbol=symbol, side=side, type='LIMIT', quantity=quantity, price=str(price), timeInForce=timeInForce)
        return order

    def place_stop_limit(self, symbol, side, quantity, stop_price, limit_price):
        logger.info(f'place_stop_limit called: {symbol} {side} {quantity} stop:{stop_price} limit:{limit_price}')
        if self.dry_run:
            return {'status':'simulated','symbol':symbol,'side':side,'quantity':quantity,'stop_price':stop_price,'limit_price':limit_price}
        params = {'symbol':symbol,'side':side,'type':'STOP_MARKET','stopPrice':str(stop_price),'closePosition':False,'quantity':quantity}
        # For USDT-M futures, STOP or STOP_MARKET types exist; adjust as needed.
        order = self.client.futures_create_order(**params)
        return order

    def cancel_order(self, symbol, orderId):
        logger.info(f'cancel_order called: {symbol} {orderId}')
        if self.dry_run:
            return {'status':'simulated','symbol':symbol,'orderId':orderId}
        return self.client.futures_cancel_order(symbol=symbol, orderId=orderId)
