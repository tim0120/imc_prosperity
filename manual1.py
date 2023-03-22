T = [
    [1, 0.5, 1.45, 0.75],
    [1.95, 1, 3.1, 1.49],
    [0.67, 0.31, 1, 0.48],
    [1.34, 0.64, 1.98, 1]
]

scores = {}
num_trades = 6
def possible_trades(curr, n):
    if n == 0:
        return curr
    trades = []
    for i in range(len(T)):
        p = possible_trades(curr[:] + [i], n-1)
        if type(p[0]) == int:
            trades.append(p)
        else:
            trades += p
            
    return trades

def ratio(trade):
    r = 1
    for (j, i) in zip(trade[:-1], trade[1:]):
        r *= T[j][i]
    return r

trades = possible_trades([3], num_trades-2)
best_trade = None
best_ratio = 0
for trade in trades: 
    trade = trade + [3]
    r = ratio(trade)
    if r > best_ratio:
        best_ratio = r
        best_trade = trade

print(best_trade)
print(best_ratio)
