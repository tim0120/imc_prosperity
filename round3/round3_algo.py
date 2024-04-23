from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    def __init__(self) -> None:
        self.max_positions = {'STARFRUIT': 20, 
                        'AMETHYSTS': 20,
                        'ORCHIDS': 20,
                        'CHOCOLATE': 250,
                        'STRAWBERRIES': 350,
                        'ROSES': 60,
                        'GIFT_BASKET': 60,
                        'COCONUT': 300,
                        'COCONUT_COUPON': 600}

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10000  
            current_position = state.position[product] if product in state.position else 0
            can_sell = len(order_depth.buy_orders) != 0 and current_position <= self.max_positions[product] 
            can_buy = len(order_depth.sell_orders) != 0 and current_position >= -self.max_positions[product]
            best_ask = float('inf')  # Set to infinity or a very high number
            best_ask_amount = 0
            best_bid = 0  # Set to zero
            best_bid_amount = 0
            acceptable_price = 100000
            if can_buy:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            
            if can_sell:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            
            if product == 'ORCHIDS':
                current_observations = state.observations.conversionObservations['ORCHIDS']
                humidity = current_observations.humidity
                if humidity > 80 or humidity < 60 and can_sell:
                    # out of feasible range, so production will go down --> price goes up...SELL
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    orders.append(Order(product, best_bid, -best_bid_amount))
                else:
                    if can_buy:
                    # within the feasible range so, price will go down...BUY
                        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                        orders.append(Order(product, best_ask, best_ask_amount))
            elif product == 'AMETHYSTS':
                if can_buy:
                    if best_ask < acceptable_price:
                        orders.append(Order(product, best_ask, best_ask_amount))
                elif can_sell:
                    if best_bid > acceptable_price:
                        orders.append(Order(product, best_bid, -best_bid_amount))
            result[product] = orders
    
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData