1. Clone the repository

git clone https://github.com/SupriyaS26/supriya-binance-bot.git

cd supriya-binance-bot

2. Create and activate a virtual environment
In Windows Powershell:
python -m venv venv
.\venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

To test:
To run the Bot CLI
In Windows Powershell run:
To place a market order
python src/cli.py --dry-run market BTCUSDT BUY 0.001
Limit order
python src/cli.py --dry-run limit BTCUSDT SELL 0.001 30000
Stop-Limit order
python src/cli.py --dry-run stop-limit BTCUSDT BUY 0.001 30500 30000
