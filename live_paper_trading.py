# LIVE PAPER TRADING USING ALPACA MARKETS

# Initial imports
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load .env environment variables
load_dotenv()



API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"

# Create a connection to the API 
api = tradeapi.REST(API_KEY, API_SECRET, ALPACA_API_BASE_URL, api_version="v2")

# Set signal variable
signal = 1 # Generate signals from technical indicators algorithm or trahined machine learning model

# Create buy signal, num shares and ticker
if signal == 1:
    orderSide = "buy"
else:
    orderSide = "sell"

# Get final closing price
prices = api.get_barset(ticker, "1Min").df
limit_amount = prices["NVDA"]["close"][-1]

# Submit order
api.submit_order(
    symbol="TSLA", 
    qty=number_of_shares, 
    side=orderSide, 
    time_in_force="gtc", 
    type="limit", 
    limit_price=limit_amount
)