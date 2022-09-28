# Initial imports
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load .env environment variables 
load_dotenv()

# Set api keys and base url
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"

# Instancize api

api = tradeapi.REST(API_KEY, API_SECRET, ALPACA_API_BASE_URL, api_version="v2")


# Buying function
def buy(q, s):
    api.submit_order(
        symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

# Selling function
def sell(q, s):
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

# Set ticker and quantity of sale.
ticker = "NVDA"
quantity = 10

held = False 


signal = [] # Placeholder for data imported from another module

while True:
    print("Working.")

    if signal == 1 and not held: 
        print(f"Purchasing {quantity} of {ticker}")
        buy(quantity, ticker)
        held=True
    
    elif signal == -1 and held:
        print(f"Selling {quantity} of {ticker}")
        held=False

