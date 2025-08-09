
import argparse
import sys
from market_orders import place_market_order
from limit_orders import place_limit_order
from advanced.stop_limit import place_stop_limit
from advanced.oco import place_oco
from advanced.twap import run_twap
from advanced.grid import run_grid
from logger import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(prog='binance-bot', description='Binance USDT-M Futures CLI bot')
    parser.add_argument('--api-key', help='Binance API key')
    parser.add_argument('--api-secret', help='Binance API secret')
    parser.add_argument('--dry-run', action='store_true', help='Do not send orders to Binance; simulate only')

    subparsers = parser.add_subparsers(dest='command', required=True)

    p_market = subparsers.add_parser('market', help='Place market order')
    p_market.add_argument('symbol')
    p_market.add_argument('side', choices=['BUY','SELL'])
    p_market.add_argument('quantity', type=float)

    p_limit = subparsers.add_parser('limit', help='Place limit order')
    p_limit.add_argument('symbol')
    p_limit.add_argument('side', choices=['BUY','SELL'])
    p_limit.add_argument('quantity', type=float)
    p_limit.add_argument('price', type=float)

    p_stop = subparsers.add_parser('stop_limit', help='Place stop-limit order')
    p_stop.add_argument('symbol')
    p_stop.add_argument('side', choices=['BUY','SELL'])
    p_stop.add_argument('quantity', type=float)
    p_stop.add_argument('stop_price', type=float)
    p_stop.add_argument('limit_price', type=float)

    p_oco = subparsers.add_parser('oco', help='Place OCO: take-profit + stop-loss')
    p_oco.add_argument('symbol')
    p_oco.add_argument('side', choices=['BUY','SELL'])
    p_oco.add_argument('quantity', type=float)
    p_oco.add_argument('take_profit', type=float)
    p_oco.add_argument('stop_price', type=float)
    p_oco.add_argument('stop_limit_price', type=float)

    p_twap = subparsers.add_parser('twap', help='Run TWAP: split order over time')
    p_twap.add_argument('symbol')
    p_twap.add_argument('side', choices=['BUY','SELL'])
    p_twap.add_argument('quantity', type=float)
    p_twap.add_argument('--slices', type=int, default=5, help='Number of slices')
    p_twap.add_argument('--interval', type=float, default=1.0, help='Seconds between slices')

    p_grid = subparsers.add_parser('grid', help='Run Grid strategy (simulated)')
    p_grid.add_argument('symbol')
    p_grid.add_argument('lower', type=float)
    p_grid.add_argument('upper', type=float)
    p_grid.add_argument('steps', type=int)

    args = parser.parse_args()
    client_cfg = {'api_key': args.api_key, 'api_secret': args.api_secret, 'dry_run': args.dry_run}

    try:
        if args.command == 'market':
            place_market_order(args.symbol, args.side, args.quantity, client_cfg)
        elif args.command == 'limit':
            place_limit_order(args.symbol, args.side, args.quantity, args.price, client_cfg)
        elif args.command == 'stop_limit':
            place_stop_limit(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price, client_cfg)
        elif args.command == 'oco':
            place_oco(args.symbol, args.side, args.quantity, args.take_profit, args.stop_price, args.stop_limit_price, client_cfg)
        elif args.command == 'twap':
            run_twap(args.symbol, args.side, args.quantity, slices=args.slices, interval=args.interval, client_cfg=client_cfg)
        elif args.command == 'grid':
            run_grid(args.symbol, args.lower, args.upper, args.steps, client_cfg)
        else:
            parser.print_help()
    except Exception as e:
        logger.exception('Fatal error running command')
        sys.exit(1)

if __name__ == '__main__':
    main()
