import pandas as pd
import numpy as np

def gain_loss(df):

    # Add the trade_type column to track buys and sells
    df['trade_type'] = np.nan
    
    # Initialize a cost/proceeds column for recording trade metrics
    df["cost/proceeds"] = np.nan
    
    # Initialize share size and accumulated shares
    share_size = 100
    accumulated_shares = 0
    bought = False
    initial_investment = 0
    
    # Loop through the Pandas DataFrame and initiate a trade at each iteration
    for index, row in df.iterrows():
    
        # buy if the previous_price is 0, in other words, buy on the first day
        if row["Entry/Exit"] == 1:
            df.loc[index, "trade_type"] = "buy"
        
            bought = True  # indicate stock has been bought
        
            if initial_investment == 0:
                initial_investment = row["Close"] * share_size
        
            # calculate the cost of the trade by multiplying the current day's price
            # by the share_size, or number of shares purchased
            df.loc[index, "cost/proceeds"] = -(row["Close"] * share_size)
        
            # add the number of shares purchased to the accumulated shares
            accumulated_shares += share_size
        
        # buy if the current day's price is less than the previous day's price
        elif row["Entry/Exit"] == -1 and bought: #able to sell only when stock has first been bought
            df.loc[index, "trade_type"] = "sell"
        
            # calculate the cost of the trade by multiplying the current day's price
            # by the share_size, or number of shares purchased
            df.loc[index, "cost/proceeds"] = (row["Close"] * share_size)
        
            # add the number of shares purchased to the accumulated shares
            accumulated_shares -= share_size
        
        # hold if the current day's price is equal to the previous day's price
        else:
            df.loc[index, "trade_type"] = "hold"
        
    # if the index is the last index of the DataFrame and there is still accumulated stock, sell the remaining holding
    if index == df.index[-1] and accumulated_shares !=0:
        df.loc[index, "trade_type"] = "sell"
    
        # calculate the proceeds by multiplying the last day's price by the accumulated shares
        df.loc[index, "cost/proceeds"] = row["Close"] * accumulated_shares
    
        accumulated_shares = 0
        
    return df, initial_investment, accumulated_shares