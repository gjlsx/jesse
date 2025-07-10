from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class SmartHold(Strategy):
    """
    Smart Buy and Hold Strategy.
    Buy at the beginning, hold long-term, but with basic risk management
    Only sell if extreme loss occurs
    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters
        self.position_size = 0.90      # Use 90% of balance for buying
        self.has_bought = False        # Track if we have already bought
        self.min_candles = 20          # Wait for enough data
        self.stop_loss_pct = 0.50      # Emergency stop loss at 50% loss
        self.entry_price = 0           # Record entry price
        
    def should_long(self):
        """
        Buy once at the beginning with some technical confirmation
        """
        # Only buy once and wait for enough data
        if not self.has_bought and len(self.candles) >= self.min_candles:
            # Simple confirmation: price above 20-period MA
            ma20 = ta.sma(self.candles, period=20)
            if self.price > ma20:
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
        Execute the buy order and record entry price
        """
        try:
            # Calculate buy amount (90% of balance)
            buy_amount = self.balance * self.position_size
            qty = utils.size_to_qty(buy_amount, self.price)
            
            # Execute buy order
            self.buy = qty, self.price
            
            # Record entry price and mark as bought
            self.entry_price = self.price
            self.has_bought = True
            
            print(f"Smart Hold: Bought {qty} at price {self.price}")
            
        except Exception as e:
            print(f"Buy error: {e}")
    
    def go_short(self):
        """
        Not used in buy and hold strategy
        """
        pass
    
    def update_position(self):
        """
        Hold position with emergency stop loss protection
        """
        try:
            # Check for emergency stop loss (50% loss)
            if self.is_long and self.entry_price > 0:
                current_loss_pct = (self.entry_price - self.price) / self.entry_price
                
                if current_loss_pct >= self.stop_loss_pct:
                    print(f"Emergency stop loss triggered at {current_loss_pct:.2%} loss")
                    self.liquidate()
                    
        except Exception as e:
            print(f"Update position error: {e}")
