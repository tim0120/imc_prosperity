import numpy as np

num_reserve_samples = 1000
min_bid, max_bid = 900, 1000
reserve_sample = np.random.triangular(min_bid, max_bid, max_bid, num_reserve_samples)

best_return = 0
best_range = None
for min_bid_i in range(min_bid, max_bid+1, 1):
    for max_bid_i in range(min_bid_i, max_bid+1, 1):
        will_buy = reserve_sample > max_bid_i
        buying_reserves = reserve_sample[will_buy]
        buy_i = np.mean(np.where(
            min_bid_i > buying_reserves,
            min_bid_i,
            max_bid_i
        ))
        avg_return = max_bid - buy_i
        if avg_return > best_return:
            best_return = avg_return
            best_range = (min_bid_i, max_bid_i)

print(best_return)
print(best_range)
