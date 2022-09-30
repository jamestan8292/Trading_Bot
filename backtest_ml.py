# USing Finta for trading signals - ML Version back testing.
# OUTPUTS: 
#  Evaluate the model's ability to predict the trading signal for the testing data using a classification report
#  Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns


### Build X & Y Datasets

import numpy as np
import pandas as pd
import hvplot.pandas
from pathlib import Path

# Setting these options will allow for reviewing more of the DataFrames
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 1000)
# Import the finta Python library and the TA module
from finta import TA
# ## Import the CSV file and create the Pandas DataFrame
# Read in CSV file in from the resources folder into a Pandas DataFrame
# Set the date as the DateTimeIndex
df = pd.read_csv(
    Path("../Resources/amd_data.csv"),
    index_col = "date", 
    parse_dates = True, 
    infer_datetime_format = True
)
# Use the pct_change function to generate the returns from "close"
df["actual_returns"] = df["close"].pct_change()
# Drop all NaN values from the DataFrame
df = df.dropna()
# Generate the Input Features, X
# Create a simple moving average (SMA) using a window size of 4. 
# Assign this to a column called `sma_fast`
short_window = 4
df['sma_fast'] = TA.SMA(df, 4)
# Create a simple moving average (SMA) using a window size of 100. 
# Assign this to a column called `sma_slow`
long_window = 100
df['sma_slow'] = df['close'].rolling(window=long_window).mean()
# Create additional technical indicators
df["ssma"] = TA.SSMA(df)
df["ema"] = TA.EMA(df, 50)
df["dema"] = TA.DEMA(df)
df["tema"] = TA.TEMA(df)
df["trima"] = TA.TRIMA(df)
# Drop the NaNs using dropna()
df = df.dropna()
# Assign a copy of the technical variable columns to a new DataFrame called `X` and lag it.
X = df[['sma_fast', 'sma_slow', 'ssma', 'ema', 'dema', 'tema', 'trima']].shift().dropna().copy()
# Initialize the new `Signal` column
df['signal'] = 0.0
# Generate signal to buy stock long
df.loc[(df['actual_returns'] >= 0), 'signal'] = 1
# Generate signal to sell stock short
df.loc[(df['actual_returns'] < 0), 'signal'] = -1
df.tail(3)
# Copy the new "signal" column to a new Series called `y`.
y = df['signal']
display(X.head(1))
display(y.head(2))

### Split the data into Training and test datasets

# Import the neccessary Date function
from pandas.tseries.offsets import DateOffset

# Use the following code to select the start of the training period: `training_begin = X.index.min()`
training_begin = X.index.min()
print(training_begin)

# Use the following code to select the ending period for the training data: `training_end = X.index.min() + DateOffset(months=3)`
training_end = X.index.min() + DateOffset(months=6)
print(training_end)

# Generate the X_train and y_train DataFrames using loc to select the rows from `training_begin` up to `training_end`
# Hint: Use `loc[training_begin:training_end]` for X_train and y_train
X_train = X.loc[training_begin:training_end]
y_train = y.loc[training_begin:training_end]

# Generate the X_test and y_test DataFrames using loc to select from `training_end` to the last row in the DataFrame.
# Hint: Use `loc[training_end:]` for X_test and y_test
X_test = X.loc[training_end:]
y_test = y.loc[training_end:]

# Use StandardScaler to scale the X_train and X_test data.
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaler = scaler.fit(X_train)
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

from imblearn.over_sampling import RandomOverSampler
# Use RandomOverSampler to resample the datase using random_state=1
ros = RandomOverSampler(random_state=1)
X_resampled, y_resampled = ros.fit_resample(X_train_scaled, y_train)

### Train and Generate Trade Predictions

# Create the classifier model.
from sklearn.svm import SVC
model = SVC()
 
# Fit the model to the data using X_train_scaled and y_train
model = model.fit(X_resampled, y_resampled)

# Use the trained model to predict the trading signals for the training data.
training_signal_predictions = model.predict(X_resampled)

# Evaluate the model using a classification report
from sklearn.metrics import classification_report
training_report = classification_report(y_resampled, training_signal_predictions)
print(training_report)

# Use the trained model to predict the trading signals for the testing data.
testing_signal_predictions = model.predict(X_test_scaled)

# Evaluate the model's ability to predict the trading signal for the testing data using a classification report
training_report = classification_report(y_test, testing_signal_predictions)
print(training_report)

# Create a new empty predictions DataFrame using code provided below.
predictions_df = pd.DataFrame(index=X_test.index)
predictions_df['predicted_returns'] = testing_signal_predictions
predictions_df['predicted_returns'].value_counts()

# Add in actual returns and calculate trading returns
predictions_df['actual_returns'] = df['actual_returns']
predictions_df['trading_algorithm_returns'] = predictions_df['actual_returns'] * predictions_df['predicted_returns']
predictions_df.head(20)

# Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns`
(1 + predictions_df[['actual_returns', 'trading_algorithm_returns']]).cumprod().plot()