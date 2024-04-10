import numpy as np
from tqdm import tqdm

num_reserve_samples = 10000
min_bid, max_bid = 900, 1000

epochs = 250
best_ranges = []
for _ in tqdm(range(epochs)):
    reserve_sample = np.random.triangular(min_bid, max_bid, max_bid, num_reserve_samples)
    best_return = 0
    best_range = None
    for min_bid_i in range(min_bid, max_bid, 1):
        for max_bid_i in range(min_bid_i, max_bid+1, 1):
            buying_reserves = reserve_sample[reserve_sample < max_bid_i]
            buy_i = np.sum(np.where(
                min_bid_i > buying_reserves,
                min_bid_i,
                max_bid_i
            ))
            return_i = max_bid * len(buying_reserves) - buy_i
            if return_i > best_return:
                best_return = return_i
                best_range = [min_bid_i, max_bid_i]
    best_ranges.append(best_range)

# print(best_ranges)
best_best_range = np.mean(np.array(best_ranges), axis=0)
print(best_best_range)