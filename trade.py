import pandas as pd
import numpy as np

def gain_loss(df, share_size):

    # Add the trade_type column to track buys and sells
    df['trade_type'] = np.nan
    
    # Initialize a cost/proceeds column for recording trade metrics
    df["cost/proceeds"] = np.nan
    
    # Initialize share size and accumulated shares
    accumulated_shares = 0
    bought = False
    
    # Loop through the Pandas DataFrame and initiate a trade at each iteration
    for index, row in df.iterrows():
    
        # buy if the previous_price is 0, in other words, buy on the first day
        if row["Entry/Exit"] == 1:
            df.loc[index, "trade_type"] = "buy"
        
            bought = True  # indicate stock has been bought
        
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
        
        
    return df, accumulated_shares




def calc_portfolio_value(df, share_size, initial_capital):
    
    
    df["Position"] = share_size * df["Signal"]
    
    # Find the points in time where share position is bought or sold
    df["Entry/Exit Position"] = df["Position"].diff()
    
    # Multiply share price by entry/exit positions and get the cumulatively sum
    df["Portfolio Holdings"] = (
        df["Close"] * df["Entry/Exit Position"].cumsum()
    )
    
    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    df["Portfolio Cash"] = (
        initial_capital - (df["Close"] * df["Entry/Exit Position"]).cumsum()
    )
    
    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    df["Portfolio Total"] = (
        df["Portfolio Cash"] + df["Portfolio Holdings"]
    )
    
    # Calculate the portfolio daily returns
    df["Portfolio Daily Returns"] = df["Portfolio Total"].pct_change()
    
    # Calculate the cumulative returns
    df["Portfolio Cumulative Returns"] = (
        1 + df["Portfolio Daily Returns"]
    ).cumprod() - 1
    
    return df

def portfolio_metrics(df, initial_capital):
    
    # Create the list of the metric names
    metrics = [
        'Annualized Return',
        'Cumulative Returns',
        'Annual Volatility',
        'Sharpe Ratio',
        'Sortino Ratio'
    ]
    
    # Create a list that holds the column name
    columns = ['Backtest']
    
    # Initialize the DataFrame with index set to evaluation metrics and columns 
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)
    
    # Calculate the Annualized return metric: CAGR = ([(Ending Value / Beginning Value) ^ (1 / (# trading days/252))] - 1)
    total_profit_loss = df["cost/proceeds"].sum()
    portfolio_evaluation_df.loc['Annualized Return'] = ((initial_capital+total_profit_loss)/initial_capital)**(365/df.shape[0]) - 1

    
    # Calculate the Cumulative returns metric
    portfolio_evaluation_df.loc['Cumulative Returns'] = total_profit_loss / initial_capital
    
    # Calculate the Annual volatility metric
    portfolio_evaluation_df.loc['Annual Volatility'] = (
        df['Portfolio Daily Returns'].std() * np.sqrt(252)
    )
    
    # Calculate the Sharpe ratio
    portfolio_evaluation_df.loc['Sharpe Ratio'] = (
        df['Portfolio Daily Returns'].mean() * 252) / (
        df['Portfolio Daily Returns'].std() * np.sqrt(252)
    )
    
    # Calculate the Sortino ratio
    # Start by calculating the downside return values
    
    # Create a DataFrame that contains the Portfolio Daily Returns column
    sortino_ratio_df = df[['Portfolio Daily Returns']].copy()
    
    # Create a column to hold downside return values
    sortino_ratio_df.loc[:,'Downside Returns'] = 0
    
    # Find Portfolio Daily Returns values less than 0, 
    # square those values, and add them to the Downside Returns column
    sortino_ratio_df.loc[sortino_ratio_df['Portfolio Daily Returns'] < 0, 
                         'Downside Returns'] = sortino_ratio_df['Portfolio Daily Returns']**2
    
    # Calculate the annualized return value
    annualized_return = sortino_ratio_df['Portfolio Daily Returns'].mean() * 252
    
    # Calculate the annualized downside standard deviation value
    downside_standard_deviation = np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252)
    
    # Divide the annualized return value by the downside standard deviation value
    sortino_ratio = annualized_return/downside_standard_deviation
    
    # Add the Sortino ratio to the evaluation DataFrame
    portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio
    
    return portfolio_evaluation_df