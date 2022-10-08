# Imports
import warnings
warnings.filterwarnings('ignore')

import os
import json
import pandas as pd
from dotenv import load_dotenv
import joblib
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import pytz

import logging
from time import sleep
import streamlit as st

import alpaca_trade_api as tradeapi

#---------------------------
# Change main variables here
#---------------------------

# Set ticker
ticker = 'NVDA'

# Set # shares
share_size = 100

#---------------------------
# Set up Alpaca API
#---------------------------

# load .env file. File must be in the same directory as this application
load_dotenv()


# Initialize Alpaca API
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"

# Create a connection to the API 
api = tradeapi.REST(API_KEY, API_SECRET, ALPACA_API_BASE_URL, api_version="v2")


#--------------------------------
# Set up date format and timezone
#--------------------------------

# Set date/time format
date_format='%m/%d/%Y %H:%M:%S %Z'

# Set timezone
my_timezone=timezone('US/Pacific')


#----------
# Functions
#----------

# Return date/time in pacific timezone
def datetime_now():
    now = datetime.now()
    now = my_timezone.localize(now)
    now = now.astimezone(my_timezone)
    return now

# Convert given seconds to hours, minutes, second and return result in one string
def convert_seconds_hhmmss(s):
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return str(round(hours)) + ':' + str(round(minutes)) + ':' + str(round(seconds))

# Calculates how many minutes are left until the market close
# Check this so as not to execute any new orders just before the market closes
# Intention is not to carry any trades overnight
def minutes_to_market_close():
    clock = api.get_clock()
    closing = clock.next_close - clock.timestamp
    return round(closing.total_seconds() / 60)

# Wait for market to open
def wait_for_market_open():
    dt_now = st.empty() # current date/time streamlit placeholder
    tto = st.empty()    # time to open streamlit placeholder
    clock = api.get_clock()
    while not clock.is_open:
        clock = api.get_clock()
        time_to_open = (clock.next_open - clock.timestamp).total_seconds()
        now = datetime_now()
        dt_now.markdown('Date/time now: ' + now.strftime(date_format))
        hhmmss = convert_seconds_hhmmss(time_to_open)
        tto.markdown('Time to market open (hh:mm:ss) ' + hhmmss)
        sleep(1)

# Send order. First check to see if there is 10 minuites left before market closes
def send_order(ticker, direction, share_size):
    if minutes_to_market_close() > 10:

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

def get_position(ticker):

    try:
        position = api.get_position(ticker)
        position_qty = int(position.qty)
        bought = True
    except:
        position_qty = 0
        bought = False
    return position_qty, bought

# ----------------
# Initializations
# ----------------

# Title shown on Streamlit webpage
st.title('Trading Bot')

# Log error messsages
logging.basicConfig(
	filename='errlog.log',
	level=logging.WARNING,
	format='%(asctime)s:%(levelname)s:%(message)s',
)

# Cancel any open orders
api.cancel_all_orders()

# Set flags
next_trade = True
order_submitted = False
done_for_the_day = False

# Check if stock has been bought before
# If it has been bought before, set share_size to position quantity
position_qty, bought = get_position(ticker)
st.text('Current Position of {} is {}'.format(ticker, position_qty))

# Load 'trained' scaler
filepath_scaler= ('./Resources/' + ticker + '_xgb_5mins_scaler.sav')
with open(filepath_scaler, 'rb') as f: 
    X_scaler = joblib.load(f)

# Load trained model
filepath_model= ('./Resources/' + ticker + '_xgb_5mins_model.sav')
with open(filepath_model, 'rb') as f: 
    model = joblib.load(f)


# ----------------
# Main loop
# ----------------

while True:

    try:

        wait_for_market_open()

        # wait 6 mins for next data to be available
        clock = api.get_clock()
        st.markdown('Market is open. Waiting 6 minutes for data ...')
        sleep(360 - clock.timestamp.second)

        # Get live stock data, scale data, and generate trading signal using trained machine learning model
        new_data_df = yf.download(ticker, period='1d', interval='5m')
        new_data_df.drop(columns=['Adj Close'], axis=1, inplace=True)
        df = new_data_df.take([-2])
        print('df = ', df)
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
            now = datetime_now()
            st.markdown('Date/time now: ' + now.strftime(date_format))
            st.markdown(now.strftime("%Y-%m-%d %H:%M:%S") + ' Bought')

        elif signal==0 and bought==True:
            order_submitted, done_for_the_day = send_order(ticker, 'sell', share_size)
            bought = False
            next_trade = False
            now = datetime_now()
            st.markdown('Date/time now: ' + now.strftime(date_format))
            st.markdown(now.strftime(date_format) + ' Sold')
        else:
            now = datetime_now()
            st.markdown(now.strftime(date_format) + ' Hold')

    except Exception as e:
	    logging.exception(e)