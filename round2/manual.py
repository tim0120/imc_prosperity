# Let's represent the exchanges as a dictionary as the user requested
exchange_rates_dict = {
    ('Pizza Slice', 'Wasabi Root'): 0.48,
    ('Pizza Slice', 'Snowball'): 1.52,
    ('Pizza Slice', 'Shells'): 0.71,
    ('Wasabi Root', 'Pizza Slice'): 2.05,
    ('Wasabi Root', 'Snowball'): 3.26,
    ('Wasabi Root', 'Shells'): 1.56,
    ('Snowball', 'Pizza Slice'): 0.64,
    ('Snowball', 'Wasabi Root'): 0.3,
    ('Snowball', 'Shells'): 0.46,
    ('Shells', 'Pizza Slice'): 1.41,
    ('Shells', 'Wasabi Root'): 0.61,
    ('Shells', 'Snowball'): 2.08
}

# Define a function to find the best trade sequence with path using the new dictionary representation
def find_best_trade_sequence_dict(trades_dict, start_currency, trades_left, capital, path=[]):
    # Base case: If no trades left, return the current capital and path if back to Shells
    if trades_left == 0:
        return (capital, path) if start_currency == 'Shells' else (0, [])
    
    best_trade_value = 0
    best_trade_path = []
    # Try trading the start currency to each of the other currencies
    for (from_currency, to_currency), rate in trades_dict.items():
        if from_currency == start_currency:
            # Calculate the capital after the trade
            new_capital = capital * rate
            # Recursively find the best trade sequence after the current trade
            trade_value, trade_path = find_best_trade_sequence_dict(
                trades_dict, to_currency, trades_left - 1, new_capital, path + [(from_currency, to_currency, rate)]
            )
            if trade_value > best_trade_value:
                best_trade_value = trade_value
                best_trade_path = trade_path
    
    return best_trade_value, best_trade_path

max_trades = 5
initial_capital = 2000000
# Start the recursive function from Shells with 5 trades left
best_strategy_value_dict, best_strategy_path_dict = find_best_trade_sequence_dict(
    exchange_rates_dict, 'Shells', max_trades, initial_capital
)

print(best_strategy_value_dict, best_strategy_path_dict)
# AFTER TRADE 1: 2,820,000 Pizza slices
# AFTER TRADE 2: 1,353,600 Wasabi Root
# AFTER TRADE 3: 2,111,616 Shells
# AFTER TRADE 4: 2,977,378.56 Pizza Slices
# AFTER TRADE 5: 2,113,938.78 Shells