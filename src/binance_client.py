# binance_client.py
from binance.client import Client
from binance.exceptions import BinanceAPIException

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, dry_run=True):
        self.dry_run = dry_run
        self.client = Client(api_key, api_secret)
        self.client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'  # testnet URL

    def place_market_order(self, symbol, side, quantity):
        if self.dry_run:
            return {'dry_run': True, 'symbol': symbol, 'side': side, 'quantity': quantity, 'type': 'MARKET'}
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            return order
        except BinanceAPIException as e:
            return {'error': str(e)}

    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        if self.dry_run:
            return {'dry_run': True, 'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'type': 'LIMIT'}
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            return order
        except BinanceAPIException as e:
            return {'error': str(e)}

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price, time_in_force='GTC'):
        if self.dry_run:
            return {
                'dry_run': True,
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'stopPrice': stop_price,
                'price': limit_price,
                'type': 'STOP_MARKET'
            }
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_MARKET',  # for stop-limit orders on futures testnet
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce=time_in_force
            )
            return order
        except BinanceAPIException as e:
            return {'error': str(e)}
