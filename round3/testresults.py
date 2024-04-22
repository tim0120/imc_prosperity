import pandas as pd

df = pd.read_csv('/Users/stevenhenry/Documents/imc_prosperity/54674385-34f5-44cf-abd6-99b545e85258.csv',delimiter=';')
total_pnl = df['profit_and_loss'].sum()
print(total_pnl)