import pandas as pd
from dotenv import load_dotenv
import os
import p2_FMP_Requests as fmp
from pathlib import Path


# load api key for financialmodelingprep.com from .env file
load_dotenv()
apikey = os.getenv("FMP_API_KEY")

# get historical daily stock price for NVDA
ticker = 'NVDA'
num_days = "1000"

NVDA_hist_price_response = fmp.get_historial_daily_stock_price_last_x_days(ticker, num_days, apikey)
NVDA_hist_price_df = pd.DataFrame(NVDA_hist_price_response['historical']).drop('label', axis=1).set_index('date')

NVDA_hist_dcf_response = fmp.get_historical_dcf(ticker, num_days, apikey)
NVDA_hist_dcf_df = pd.DataFrame(NVDA_hist_dcf_response).drop('symbol', axis=1).set_index('date')

NVDA_hist_market_cap_response =fmp.get_historical_market_cap(ticker, num_days, apikey)
NVDA_hist_market_cap_df = pd.DataFrame(NVDA_hist_market_cap_response).drop('symbol', axis=1).set_index('date')

NVDA_df = pd.concat([NVDA_hist_price_df, NVDA_hist_market_cap_df, NVDA_hist_dcf_df],  axis = 1)


filepath = Path('Resources/NVDA_data.csv')   
NVDA_df.to_csv(filepath)


# get historical daily stock price for AMD
ticker = 'AMD'
num_days = "1000"

AMD_hist_price_response = fmp.get_historial_daily_stock_price_last_x_days(ticker, num_days, apikey)
AMD_hist_price_df = pd.DataFrame(AMD_hist_price_response['historical']).drop('label', axis=1).set_index('date')

AMD_hist_dcf_response = fmp.get_historical_dcf(ticker, num_days, apikey)
AMD_hist_dcf_df = pd.DataFrame(AMD_hist_dcf_response).drop('symbol', axis=1).set_index('date')

AMD_hist_market_cap_response =fmp.get_historical_market_cap(ticker, num_days, apikey)
AMD_hist_market_cap_df = pd.DataFrame(AMD_hist_market_cap_response).drop('symbol', axis=1).set_index('date')

AMD_df = pd.concat([AMD_hist_price_df, AMD_hist_market_cap_df, AMD_hist_dcf_df],  axis = 1)


filepath = Path('Resources/AMD_data.csv')   
AMD_df.to_csv(filepath)



"""

with open('sp500_constituent_FMP_2022-09-17.csv', 'r') as file:
    tickers = file.read().splitlines()



key_metrics_response = fmp.get_key_metrics(ticker, apikey)
key_metrics_df = pd.DataFrame(key_metrics_response).T

ticker = 'AAPL'
limit = '360'

hd_response = fmp.get_historical_dcf(ticker, limit, apikey)
hd_response_df = pd.DataFrame(hd_response)
"""


"""
###################################################
###### Get Income Tax Statements for screened tickers

with open('tickers_3045.csv', 'r') as file:
    tickers = file.read().splitlines()

# ticker = "AIRTP"
# tickers = ['AAPL', 'BA']
limit = "20"   # years
    
i = 1
income_statements_df = pd.DataFrame()
balance_sheet_df = pd.DataFrame()
key_metrics_df = pd.DataFrame()
magic_formula_df = pd.DataFrame()
for ticker in tickers:

    # income statement
    is_response = fmp.get_income_statement(ticker, limit, apikey)
    is_df = pd.DataFrame(is_response)
    if is_df.empty:
        continue

    # balance_sheet
    bs_response = fmp.get_balance_sheet(ticker, limit, apikey)
    bs_df = pd.DataFrame(bs_response)
    if bs_df.empty:
        continue

    # key metrics
    km_response = fmp.get_key_metrics(ticker, limit, apikey)
    km_df = pd.DataFrame(km_response)
    if km_df.empty:
        continue


    # income statement
    year = is_df['date'].str[:4]   # get year from date string
    year_df=pd.DataFrame(year)  # convert list to dataframe
    year_df.rename(columns={ 'date': 'year' }, inplace = True)
    is_df1 = pd.concat([year_df, is_df], axis=1)
    income_statements_df = pd.concat([income_statements_df, is_df1], axis = 0)
    
    is_slice_df = is_df1[['symbol', 'year', 'incomeBeforeTax']]
    

    # balance_sheet
    year = bs_df['date'].str[:4]   # get year from date string
    year_df=pd.DataFrame(year)  # convert list to dataframe
    year_df.rename(columns={ 'date': 'year' }, inplace = True)
    bs_df1 = pd.concat([year_df, bs_df], axis=1)
    balance_sheet_df = pd.concat([balance_sheet_df, bs_df1], axis = 0)
    
    bs_slice_df = bs_df1[['netReceivables', 'inventory', 'accountPayables', 'propertyPlantEquipmentNet']]
    

    # key metrics
    year = km_df['date'].str[:4]   # get year from date string
    year_df=pd.DataFrame(year)  # convert list to dataframe
    year_df.rename(columns={ 'date': 'year' }, inplace = True)
    km_df1 = pd.concat([year_df, km_df], axis=1)
    key_metrics_df = pd.concat([key_metrics_df, km_df1], axis = 0)
    
    km_slice_df = km_df1[['marketCap', 'enterpriseValue', 'peRatio', 'dividendYield']]
    
    
    
    # combined dataframe slices
    mf_df = pd.concat([is_slice_df,
                       bs_slice_df, 
                       km_slice_df], axis=1)
    
    mf_df['earnings_yield'] = mf_df['incomeBeforeTax'] / mf_df['enterpriseValue']
    mf_df['return_on_capital'] = mf_df['incomeBeforeTax'] / (mf_df['netReceivables'] 
                                                             + mf_df['inventory'] 
                                                             - mf_df['accountPayables'] 
                                                             + mf_df['propertyPlantEquipmentNet'])
    
    magic_formula_df = pd.concat([magic_formula_df, mf_df], axis = 0)
    
    print("Downloaded and Processed ", i, " tickers - ", ticker)
    i = i + 1
          
    
filepath = Path('magic_formula_data1.csv')   
magic_formula_df.to_csv(filepath)

filepath = Path('income_statements1.csv')   
income_statements_df.to_csv(filepath)

filepath = Path('balance_sheets1.csv')   
balance_sheet_df.to_csv(filepath)

filepath = Path('key_metrics1.csv')   
key_metrics_df.to_csv(filepath)

# mf_ba_year_df = magic_formula_df[magic_formula_df['year'] == '2013']





# aapl = income_statements_df[income_statements_df['symbol']=='AAPL']


###################################################



###################################################
###### load 8081 tickers from tickers_8081.csv
with open('tickers_8081.csv', 'r') as file:
    tickers = file.read().splitlines()

# tickers = ['AAPL', 'BA']

#### Get profile of all tickers
count=0
stocks_profile_df = pd.DataFrame()
for ticker in tickers:
    response = fmp.get_profile(ticker, apikey)
    ticker_profile_df = pd.DataFrame(response)
    stocks_profile_df = pd.concat([stocks_profile_df, ticker_profile_df], axis=0)
    count=count+1
    # time.sleep(0.2)
    if count % 10 == 0:
        print ('Downloaded ', count, ' stock profiles')
    
filepath = Path('stocks_profile.csv')  
stocks_profile_df.to_csv(filepath)
###################################################



#### Full stock list
# # get all stocks including etf and funds and store dataframe into csv file
# response = fmp.get_stock_list(apikey)
# stock_list_raw_df = pd.DataFrame(response)
# filepath = Path('stock_list_raw.csv')  
# stock_list_raw_df.to_csv(filepath)

# # filter out non-stocks and store dataframe into csv file
# stock_list_local_df = stock_list_raw_df[(stock_list_raw_df['exchangeShortName'] == 'NASDAQ') | (stock_list_raw_df['exchangeShortName'] == 'NYSE')]
# stock_list_df = stock_list_local_df[stock_list_local_df['type'] == 'stock']
# filepath = Path('stock_list.csv')  
# stock_list_df.to_csv(filepath)



#### Get financial growth of a stock
# response = fmp.get_financial_growth(ticker, apikey)
# financial_growth_df = pd.DataFrame(response)


#### Get financial growth of a stock
# ticker = 'AAPL'
# response = fmp.get_stock_list(ticker, apikey)

#### Tradable Stock List
# response = fmp.get_tradable_symbol_list(apikey)
# tradable_list_raw_df = pd.DataFrame(response)
# filepath = Path('tradable_list_raw.csv')  
# stock_list_df.to_csv(filepath)


### Graham Intrinisic Value Calculation
# variables
# ticker = 'AAPL'
# basic_eps = 5.11
# growth = 17.93
# current_aaa_bond_yield = 2.57

# # Constants
# pe_no_growth = 7
# num_growth = 1
# ave_aaa_bond_yield = 4.4




# intrinsic_value = (eps * (pe_no_growth + (num_growth * growth)) * ave_aaa_bond_yield) / current_aaa_bond_yield 



# key_metrics_response = fmp.get_key_metrics(ticker, apikey)
# key_metrics_df = pd.DataFrame(key_metrics_response).T

# ratios_ttm_response = fmp.get_ratios_ttm(ticker, apikey)
# ratios_ttm_df = pd.DataFrame(ratios_ttm_response).T

"""
