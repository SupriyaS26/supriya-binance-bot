import argparse

def handle_market(args):
    client_cfg = {'dry_run': args.dry_run}
    from market_orders import place_market_order
    resp = place_market_order(args.symbol, args.side, args.quantity, client_cfg)
    print(resp)

def handle_limit(args):
    client_cfg = {'dry_run': args.dry_run}
    from limit_orders import place_limit_order
    resp = place_limit_order(args.symbol, args.side, args.quantity, args.price, client_cfg)
    print(resp)

def handle_stop_limit(args):
    client_cfg = {'dry_run': args.dry_run}
    from limit_orders import place_stop_limit_order
    resp = place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price, client_cfg)
    print(resp)


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--dry-run", action="store_true", help="Simulate orders without sending to API")

    subparsers = parser.add_subparsers(dest="command")

    # Market order
    market_parser = subparsers.add_parser("market", help="Place a market order")
    market_parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g. BTCUSDT)")
    market_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    market_parser.add_argument("quantity", type=float, help="Order quantity")
    market_parser.set_defaults(func=handle_market)

    # Limit order
    limit_parser = subparsers.add_parser("limit", help="Place a limit order")
    limit_parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g. BTCUSDT)")
    limit_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    limit_parser.add_argument("quantity", type=float, help="Order quantity")
    limit_parser.add_argument("price", type=float, help="Order price")
    limit_parser.set_defaults(func=handle_limit)

    # Stop-Limit order
    stop_limit_parser = subparsers.add_parser("stop-limit", help="Place a stop-limit order")
    stop_limit_parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g. BTCUSDT)")
    stop_limit_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    stop_limit_parser.add_argument("quantity", type=float, help="Order quantity")
    stop_limit_parser.add_argument("stop_price", type=float, help="Stop price")
    stop_limit_parser.add_argument("limit_price", type=float, help="Limit price")
    stop_limit_parser.set_defaults(func=handle_stop_limit)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
