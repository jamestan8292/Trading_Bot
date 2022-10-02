import pandas as pd
from dotenv import load_dotenv
import os
import p2_FMP_Requests as fmp
from pathlib import Path


# load api key for financialmodelingprep.com from .env file
load_dotenv()
apikey = os.getenv("FMP_API_KEY")

ticker = 'NVDA'
num_periods = "1000"

response = fmp.get_historical_stock_price_5min(ticker, apikey)
df = pd.DataFrame(response).set_index('date')
file = (ticker + '_data_5minutes.csv')
filepath = Path("./Resources/" + file)   
df.to_csv(filepath)

"""""
# get historical daily stock price for NVDA
ticker = 'NVDA'
num_days = "1000"

NVDA_hist_price_response = fmp.get_historial_daily_stock_price_last_x_days(ticker, num_days, apikey)
NVDA_hist_price_df = pd.DataFrame(NVDA_hist_price_response['historical']).drop('label', axis=1).set_index('date')

# NVDA_hist_dcf_response = fmp.get_historical_dcf(ticker, num_days, apikey)
# NVDA_hist_dcf_df = pd.DataFrame(NVDA_hist_dcf_response).drop('symbol', axis=1).set_index('date')

# NVDA_hist_market_cap_response =fmp.get_historical_market_cap(ticker, num_days, apikey)
# NVDA_hist_market_cap_df = pd.DataFrame(NVDA_hist_market_cap_response).drop('symbol', axis=1).set_index('date')

# NVDA_df = pd.concat([NVDA_hist_price_df, NVDA_hist_market_cap_df, NVDA_hist_dcf_df],  axis = 1)


NVDA_df = NVDA_hist_price_df.sort_index(ascending=True)
NVDA_df = NVDA_df.drop(['unadjustedVolume', 'adjClose', 'change', 'changePercent', 'changeOverTime'], axis=1)

filepath = Path('Resources/NVDA_data.csv')   
NVDA_df.to_csv(filepath)


# get historical daily stock price for AMD
ticker = 'AMD'
num_days = "1000"

AMD_hist_price_response = fmp.get_historial_daily_stock_price_last_x_days(ticker, num_days, apikey)
AMD_hist_price_df = pd.DataFrame(AMD_hist_price_response['historical']).drop('label', axis=1).set_index('date')

# AMD_hist_dcf_response = fmp.get_historical_dcf(ticker, num_days, apikey)
# AMD_hist_dcf_df = pd.DataFrame(AMD_hist_dcf_response).drop('symbol', axis=1).set_index('date')

# AMD_hist_market_cap_response =fmp.get_historical_market_cap(ticker, num_days, apikey)
# AMD_hist_market_cap_df = pd.DataFrame(AMD_hist_market_cap_response).drop('symbol', axis=1).set_index('date')

# AMD_df = pd.concat([AMD_hist_price_df, AMD_hist_market_cap_df, AMD_hist_dcf_df],  axis = 1)

AMD_df = AMD_hist_price_df.sort_index(ascending=True)
AMD_df = AMD_df.drop(['unadjustedVolume', 'adjClose', 'change', 'changePercent', 'changeOverTime'], axis=1)

filepath = Path('Resources/AMD_data.csv')   
AMD_df.to_csv(filepath)


"""