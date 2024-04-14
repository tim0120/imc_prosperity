import pandas as pd
from tqdm import tqdm
import numpy as np


# importing all data
df_prev2 = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_-2_nn.csv', delimiter=';')
df_prev1 = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_-1_nn.csv', delimiter=';')
df_prev0 = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_0_nn.csv', delimiter=';')
last_timestamp_day0 = df_prev2['timestamp'].iloc[-1]  
last_timestamp_day1 = df_prev1['timestamp'].iloc[-1] + last_timestamp_day0 + 1 
df_prev1['timestamp'] += last_timestamp_day0 + 1
df_prev0['timestamp'] += last_timestamp_day1 + 1
all_trades = pd.concat([df_prev2, df_prev1, df_prev0], ignore_index=True)
df_starfruit = all_trades[all_trades['symbol']=='STARFRUIT']
df_starfruit = df_starfruit.groupby('timestamp').last().reset_index()
df_starfruit.to_csv('starfruit_all_trades.csv',index=False)

def df_to_windowed_df(dataframe, first_timestamp, last_timestamp, n=20):
    # Ensure the dataframe is sorted by timestamp
    dataframe = dataframe.sort_values('timestamp')
    
    # Convert timestamps to integers if they are not already
    dataframe['timestamp'] = dataframe['timestamp'].astype(int)

    # Initialize lists to hold the input features (X) and target values (Y)
    X, Y = [], []

    for i in tqdm(range(first_timestamp, last_timestamp+1)):
        # Get the subset of dataframe up to the current timestamp
        df_subset = dataframe[dataframe['timestamp'] <= i].tail(n+1)

        if len(df_subset) != n+1:
            print(f'Error: Window of size {n} is too large for timestamp {i}')
            return

        # Get the 'price' values as numpy array
        values = df_subset['price'].to_numpy()
        x, y = values[:-1], values[-1]

        # Append the features and target to their respective lists
        X.append(x)
        Y.append(y)

        # If we've reached the last timestamp, exit the loop
        if i == last_timestamp:
            break

    # Convert the lists to a pandas DataFrame
    ret_df = pd.DataFrame(X, columns=[f'Timestamp-{n-i}' for i in range(n)])
    ret_df['Target'] = Y
    ret_df['Target Timestamp'] = range(first_timestamp + n, last_timestamp + 1)

    return ret_df

windowed_df = df_to_windowed_df(df_starfruit, 7100, 2999102, n=20)

print(windowed_df.head())
