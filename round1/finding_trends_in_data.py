import pandas as pd
import matplotlib.pyplot as plt


# importing all data
day0_trades = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_0_nn.csv', delimiter=';')
day1_trades = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_-1_nn.csv', delimiter=';')
day2_trades = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/round1/trades_round_1_day_-2_nn.csv', delimiter=';')

# splitting up the data into amethyst and starfruit
# dictionaries will take the form --> [(timestamp, price, quantity)]
amethyst = [] 
starfruit = []

for index, row in day0_trades.iterrows():
    timestamp = row['timestamp']
    price = row['price']
    symbol = row['symbol']
    quantity = row['quantity']
    if symbol == 'STARFRUIT':
        starfruit.append((timestamp, price, quantity))
    else:
        amethyst.append((timestamp, price, quantity))

# plotting graphs
# Assuming 'amethyst' and 'starfruit' are your lists of tuples with (timestamp, price, quantity)
amethyst_df = pd.DataFrame(amethyst, columns=['timestamp', 'price', 'quantity'])
starfruit_df = pd.DataFrame(starfruit, columns=['timestamp', 'price', 'quantity'])

