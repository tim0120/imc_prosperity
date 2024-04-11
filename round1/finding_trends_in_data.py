import pandas as pd

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

# splitting up the data into amethyst and starfruit
# dictionaries will take the form --> [(timestamp, price, quantity)]
# amethyst = [] 
# starfruit = []

# for index, row in all_days_trades.iterrows():
#     timestamp = row['timestamp']
#     price = row['price']
#     symbol = row['symbol']
#     quantity = row['quantity']
#     if symbol == 'STARFRUIT':
#         starfruit.append((timestamp, price, quantity))