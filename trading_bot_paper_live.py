# Imports
import warnings
warnings.filterwarnings('ignore')

import os
import json
import pandas as pd
from dotenv import load_dotenv
import joblib
import yfinance as yf

import logging
from time import sleep

import alpaca_trade_api as tradeapi

# Load .env environment variables
load_dotenv()

ticker = 'NVDA'

# Initialize Alpaca API
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"

# Create a connection to the API 
api = tradeapi.REST(API_KEY, API_SECRET, ALPACA_API_BASE_URL, api_version="v2")

# Log error messsages
logging.basicConfig(
	filename='errlog.log',
	level=logging.WARNING,
	format='%(asctime)s:%(levelname)s:%(message)s',
)

# Cancel any open orders
api.cancel_all_orders()

# Set # shares
share_size = 10

# Set flags
next_trade = True
order_submitted = False
done_for_the_day = False

# Check if stock has been bought before
# If it has been bought before, set share_size to position quantity
try:
    position = api.get_position(ticker)
    position_qty = int(position.qty)
except:
    position_qty = 0
    
if position_qty == share_size:
    bought = True
    share_size = position_qty


# Load 'trained' scaler
filepath_scaler= ('./Resources/' + ticker + '_xgb_scaler.sav')
with open(filepath_scaler, 'rb') as f: 
    X_scaler = joblib.load(f)

# Load trained model
filepath_model= ('./Resources/' + ticker + '_xgb_model.sav')
with open(filepath_model, 'rb') as f: 
    model = joblib.load(f)


# calculates how many minutes are left until the market close
# Check this so as not to execute any new orders just before the market closes
# Intention is not to carry any trades overnight
def time_to_market_close():
    clock = api.get_clock()
    closing = clock.next_close - clock.timestamp
    return round(closing.total_seconds() / 60)

# Wait for market to open
def wait_for_market_open():
	clock = api.get_clock()
	if not clock.is_open:
		time_to_open = (clock.next_open - clock.timestamp).total_seconds()
		sleep(round(time_to_open))

# Send order. First check to see if there is 10 minuites left before market closes
def send_order(ticker, direction, share_size):
    if time_to_market_close() > 10:

        api.submit_order(
            symbol=ticker, 
            qty=share_size, 
            side=direction, 
            time_in_force="gtc", 
            type="market")
        order_sent = True
        done_for_the_day = False

    else:
        order_sent = False
        done_for_the_day = True
        
    return order_sent, done_for_the_day

# main loop

while True:

    try:

        while True:

            wait_for_market_open()

            # wait 6 mins for next data to be available
            clock = api.get_clock()
            sleep(360 - clock.timestamp.second)

            # Get live stock data, scale data, and generate trading signal using trained machine learning model
            new_data_df = yf.download(ticker, period='1d', interval='5m')
            new_data_df.drop(columns=['Adj Close'], axis=1, inplace=True)
            df = new_data_df.take([-2])
            new_data_scaled = X_scaler.transform(df)
            signal = model.predict(new_data_scaled)
            signal = signal[0]

            # Set limit amount
            # limit_amount = df['Close'].values[0]
            # limit_amount
            
            # Buy if stock has not been already bought
            # Sell if stock has already been bought
            # Do nothing if stock has been bought and signal is 1, or if stock is already sold and signal is 0
            # Logic will not allow stock to be bought or sold multiple times
            if signal==1 and bought==False:  
                 order_submitted, done_for_the_day = send_order(ticker, 'buy', share_size)
                 bought = True
                 next_trade = False

            elif signal==0 and bought==True:
                order_submitted, done_for_the_day = send_order(ticker, 'sell', share_size)
                bought = False
                next_trade = False

            # Check if order has been fully filled, exit loop only if order is fully filled (order_submitted = False)
            # while order_submitted:
            #     sleep(1)
            #     position = api.get_position(ticker)
            #     if int(position.qty) == share_size:
            #         order_submitted = False
            #         sleep(300)  # wait 5 mins before next trade

            # If done_for_the_day flag is true, sleep until market opens
            # while done_for_the_day:
            #     clock = api.get_clock()
            #     next_market_open = clock.next_open - clock.timestamp

            #     # Cancel any open orders
            #     api.cancel_all_orders()

            #     sleep(next_market_open.total_seconds())
            #     next_trade = True

    except Exception as e:
	    logging.exception(e)