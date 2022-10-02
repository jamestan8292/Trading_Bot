# Imports
import pandas as pd


# CCI (Commodity Channel Index)
def CCI (data, period):
    TP = (data['High'] + data['Low'] + data['Close']) / 3
    CCI = pd.Series((TP - TP.rolling(window=period).mean()) / (0.015 * TP.rolling(window=period).std()), name = 'CCI')
    data = pd.concat([data, CCI], axis=1)
    return data

# EVM (Ease of Movement)
def EVM (data, period):
    dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
    br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
    EVM = dm / br 
    EVM_MA = pd.Series(EVM.rolling(window=period).mean(), name = 'EVM')
    data = pd.concat([data, EVM_MA], axis=1)
    return data


# SMA (Simple Moving Average)
def SMA(data, period): 
    close = data['Close']
    sma = pd.Series(close.rolling(window=period).mean(), name = ('SMA_' + str(period)))
    data = pd.concat([data, sma], axis=1)
    return data


# EWMA (Exponentially Weighted Moving Average)
def EWMA(data, period):
    close = data['Close']
    ema = pd.Series(close.ewm(span = period, min_periods = (period - 1)).mean(), name = 'EWMA_' + str(period))
    data = pd.concat([data, ema], axis=1)
    return data

# ROC (price Rate Of Change)
def ROC(data, period): 
    N = data['Close'].diff(period)
    D = data['Close'].shift(period)
    roc = pd.Series(N/D,name='ROC')
    data = pd.concat([data, roc], axis=1)
    return data

# Bolinger Bands
def BBands(data, period): 
    MA = data.Close.rolling(window=period).mean()
    SD = data.Close.rolling(window=period).std()
    data['UpperBB'] = MA + (2 * SD) 
    data['LowerBB'] = MA - (2 * SD)
    return data

# Force Index
def FI(data, period):
    FI = pd.Series(data['Close'].diff(period) * data['Volume'], name = 'ForceIndex') 
    data = data = pd.concat([data, FI], axis=1)
    return data

# SMA & EWMA
def SMA_EWMA(data, period_list):
    for period in period_list:
        data = SMA(data, period)
        data = EWMA(data, period)
    return data
