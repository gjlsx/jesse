from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class BuyHold(Strategy):
    """
    Aggressive Buy and Hold Strategy
    - Buy every 3 days for 30 days total (10 purchases)
    - Use 100% of available balance each time
    - Never sell, never stop loss
    - Hold forever regardless of price movement ÎÄµµÀï¡£
    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters
        self.position_size = 1.0       # Use 100% of available balance (full position)
        self.buy_interval = 3          # Buy every 3 days
        self.total_buy_days = 30       # Total buying period: 30 days
        self.buy_count = 0             # Track number of purchases
        self.max_buys = 10             # Maximum 10 purchases (30/3 = 10)
        self.last_buy_day = -999       # Track last buy day
        
    def should_long(self):
        """
        Buy every 3 days for 30 days total
        Use all available balance each time
        """
        # Check if we're still in the 30-day buying period
        if self.buy_count >= self.max_buys:
            return False
            
        # Check if enough days have passed since last buy
        current_day = len(self.candles)
        days_since_last_buy = current_day - self.last_buy_day
        
        # Buy on first opportunity and then every 3 days
        if self.buy_count == 0 or days_since_last_buy >= self.buy_interval:
            return True
            
        return False
    
    def should_short(self):
        """
        Never short in buy and hold strategy
        """
        return False
    
    def should_cancel_entry(self):
        """
        Never cancel entry orders
        """
        return False
    
    def go_long(self):
        """
        Execute buy order with all available balance
        Buy every 3 days for 30 days total
        """
        try:
            # Use all available balance for buying
            if self.balance > 0:
                buy_amount = self.balance * self.position_size  # 100% of balance
                qty = utils.size_to_qty(buy_amount, self.price)
                
                # Execute buy order
                self.buy = qty, self.price
                
                # Update tracking variables
                self.buy_count += 1
                self.last_buy_day = len(self.candles)
                
                print(f"Buy and Hold: Purchase #{self.buy_count}/10 - Bought {qty} at price {self.price}")
                print(f"Next buy in {self.buy_interval} days")
            
        except Exception as e:
            print(f"Buy error: {e}")
    
    def go_short(self):
        """
        Not used in buy and hold strategy
        """
        pass
    
    def update_position(self):
        """
        Never sell - hold forever strategy
        No stop loss, no profit taking, just hold
        """
        # Absolutely no selling logic
        # Buy and hold forever regardless of price movement
        # No stop loss, no profit taking
        pass
