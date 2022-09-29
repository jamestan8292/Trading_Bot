try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import pandas as pd

base_string = "https://financialmodelingprep.com/api/v3/"
api_string = "?apikey="

# code provided by financialmodelingprep.com
def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

# get ticker company profile
def get_profile(ticker, apikey):
    url = (base_string + "profile/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

# get ticker income statment
def get_income_statement(ticker, limit, apikey):
    url = (base_string + "income-statement/" + ticker + "?limit=" + limit + "&apikey=" + apikey)
    return get_jsonparsed_data(url)

# get ticker balance sheet
def get_balance_sheet(ticker, limit, apikey):
    url = (base_string + "balance-sheet-statement/" + ticker + "?limit=" + limit + "&apikey=" + apikey)
    return get_jsonparsed_data(url)

def get_cash_flow_statement(ticker, apikey):
    url = (base_string + "cash-flow-statement/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_ratios_ttm(ticker, apikey):
    url = (base_string + "ratios-ttm/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_enterprise_values(ticker, apikey):
    url = (base_string + "enterprise-values/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_key_metrics(ticker, limit, apikey):
    url = (base_string + "key-metrics/" + ticker + "?limit=" + limit + "&apikey=" + apikey)
    return get_jsonparsed_data(url)

def get_sp500_constituent(apikey):
    url = (base_string + "sp500_constituent/" + api_string + apikey)
    return get_jsonparsed_data(url)

def get_stock_hist_daily_prices(ticker, start_date, end_date, apikey):
    url = (base_string + "historical-price-full/" + ticker + "?from=" + start_date + "&to=" + end_date + "&apikey=" + apikey)
    response = get_jsonparsed_data(url)
    response_df = pd.DataFrame(response['historical'])
    return response_df

def get_sp500_hist_daily_prices(start_date, end_date, apikey):
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/%5EGSPC?from=" + start_date + "&to=" + end_date + "&apikey=" + apikey)
    # url = (base_string + "historical-price-full/" + ticker + "?from=" + start_date + "&to=" + end_date + "&apikey=" + apikey)
    response = get_jsonparsed_data(url)
    response_df = pd.DataFrame(response['historical'])
    return response_df

def get_current_stock_price(ticker, apikey):
    url = (base_string + "quote-short/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_stock_price_1min(ticker, apikey):
    url = (base_string + "historical-chart/1min/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_stock_price_5min(ticker, apikey):
    url = (base_string + "historical-chart/5min/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_stock_price_15min(ticker, apikey):
    url = (base_string + "historical-chart/15min/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_stock_price_30min(ticker, apikey):
    url = (base_string + "historical-chart/30min/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_stock_price_1hour(ticker, apikey):
    url = (base_string + "historical-chart/1hour/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historial_daily_stock_price_start_end(ticker, start_date, end_date, apikey):
    url = (base_string + "historical-price-full/" + ticker +"?from=" +start_date + "&to" + end_date + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historial_daily_stock_price_last_x_days(ticker, num_days, apikey):
    url = (base_string + "historical-price-full/" + ticker +"?timeseries=" + num_days + "&apikey=" + apikey)
    return get_jsonparsed_data(url)

def get_tradable_symbol_list(apikey):
    url = (base_string + "available-traded/list" + api_string + apikey)
    return get_jsonparsed_data(url)

def get_stock_list(apikey):
    url = (base_string + "stock/list" + api_string + apikey)
    return get_jsonparsed_data(url)

def get_financial_growth(ticker, apikey):
    url = (base_string + "financial-growth/" + ticker + api_string + apikey)
    return get_jsonparsed_data(url)

def get_historical_dcf(ticker, limit, apikey):
    url = (base_string + "historical-daily-discounted-cash-flow/"+ ticker +"?limit=" + limit + "&apikey=" + apikey)
    return get_jsonparsed_data(url)

def get_historical_market_cap(ticker, limit, apikey):
    url = (base_string + "historical-market-capitalization/"+ ticker +"?limit=" + limit + "&apikey=" + apikey)
    return get_jsonparsed_data(url)


