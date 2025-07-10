

from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class TestStrategy(Strategy):
    """
    Consecutive Drop Buy + Consecutive Rise Sell Strategy
    1. Buy in 5 days after 5 consecutive down days, keep buying if price doesn't exceed the opening price of the last down day
    2. Sell in 5 days after 5 consecutive up days, until remaining 1/4 position
    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters
        self.consecutive_days = 5  # Consecutive days
        self.buy_days = 5  # Buy days
        self.sell_days = 10  # Sell days (extended to 10 days)
        self.max_position_ratio = 0.75  # Maximum position ratio 3/4
        self.min_position_ratio = 0.25  # Minimum position ratio 1/4
        self.daily_buy_ratio = 0.15  # Daily buy ratio (0.75/5)
        self.daily_sell_ratio = 0.10  # Daily sell ratio (0.5/10 = 0.05 would be more logical)
        
        # State variables
        self.buy_phase = False  # Whether in buy phase
        self.sell_phase = False  # Whether in sell phase
        self.buy_day_count = 0  # Buy day counter
        self.sell_day_count = 0  # Sell day counter
        self.last_drop_open_price = 0  # Opening price of last down day
    
    def is_consecutive_drop(self):
        """Check if there are 5 consecutive down days"""
        if len(self.candles) < self.consecutive_days:
            return False
        
        for i in range(self.consecutive_days):
            current_close = self.candles[-(i+1)][2]  # Close price
            current_open = self.candles[-(i+1)][1]   # Open price
            if current_close >= current_open:  # Not down
                return False
        
        return True
    
    def is_consecutive_rise(self):
        """Check if there are 5 consecutive up days"""
        if len(self.candles) < self.consecutive_days:
            return False
        
        for i in range(self.consecutive_days):
            current_close = self.candles[-(i+1)][2]  # Close price
            current_open = self.candles[-(i+1)][1]   # Open price
            if current_close <= current_open:  # Not up
                return False
        
        return True
    
    def get_total_value(self):
        """Get total portfolio value (balance + position value)"""
        total_value = self.balance
        if hasattr(self, 'position') and hasattr(self.position, 'qty'):
            if self.position.qty > 0:
                position_value = self.position.qty * self.price
                total_value += position_value
        return total_value
    def get_current_position_ratio(self):
        """Get current position ratio"""
        total_value = self.get_total_value()
        if total_value <= 0:
            return 0
        
        position_value = 0
        if hasattr(self, 'position') and hasattr(self.position, 'qty'):
            if self.position.qty > 0:
                position_value = self.position.qty * self.price
        
        return position_value / total_value
    
    def should_long(self) -> bool:
        """
        Determine if should go long
        Start buy phase after 5 consecutive down days, keep buying if price doesn't exceed the opening price of the last down day
        """
        # Check if there are 5 consecutive down days, start new buy phase
        if self.is_consecutive_drop() and not self.buy_phase and not self.sell_phase:
            self.buy_phase = True
            self.buy_day_count = 0
            self.sell_phase = False
            self.sell_day_count = 0
            # Record the opening price of the last down day
            self.last_drop_open_price = self.candles[-self.consecutive_days][1]
            return True
        
        # In buy phase and not reached maximum position
        if self.buy_phase:
            current_ratio = self.get_current_position_ratio()
            # Check if reached maximum position 3/4
            if current_ratio >= self.max_position_ratio:
                self.buy_phase = False
                return False
            
            # Check if price doesn't exceed the opening price of the last down day
            if self.price <= self.last_drop_open_price:
                return True
        
        return False
    
    def should_short(self) -> bool:
        """
        Spot trading doesn't allow short positions
        Always return False for spot exchange
        """
        return False
    
    def should_cancel_entry(self) -> bool:
        """
        Determine if should cancel entry orders
        """
        return False
    
    def go_long(self):
        """
        Execute long operation
        Buy in 5 days, keep buying if price doesn't exceed the opening price of the last down day
        """
        try:
            # Calculate daily buy amount (15% of TOTAL portfolio value)
            total_portfolio_value = self.get_total_value()
            buy_amount = total_portfolio_value * self.daily_buy_ratio
            
            # Make sure we don't exceed available balance
            if buy_amount > self.balance:
                buy_amount = self.balance
            
            if buy_amount > 0:
                qty = utils.size_to_qty(buy_amount, self.price)
                
                # Set buy order
                self.buy = qty, self.price
                
                print(f"Buy: {buy_amount} USDT ({self.daily_buy_ratio:.1%} of total portfolio {total_portfolio_value:.2f})")
            
            # Update buy day counter
            self.buy_day_count += 1
            
            # Check if reached maximum position 3/4
            current_ratio = self.get_current_position_ratio()
            if current_ratio >= self.max_position_ratio:
                self.buy_phase = False
                
        except Exception as e:
            print(f"Buy error: {e}")
    
    def go_short(self):
        """
        Spot trading doesn't support short positions
        This method is not used in spot trading
        """
        pass
    
    def update_position(self):
        """
        Update existing positions
        Handle selling logic for spot trading
        """
        try:
            # Check if there are 5 consecutive up days, start new sell phase
            if self.is_consecutive_rise() and not self.sell_phase and not self.buy_phase:
                self.sell_phase = True
                self.sell_day_count = 0
                self.buy_phase = False
                self.buy_day_count = 0
            
            # Handle selling in sell phase
            if self.sell_phase and hasattr(self, 'position') and hasattr(self.position, 'qty'):
                if self.position.qty > 0:
                    current_ratio = self.get_current_position_ratio()
                    
                    # Check if reached minimum position 1/4
                    if current_ratio <= self.min_position_ratio:
                        self.sell_phase = False
                        return
                    
                    # Calculate daily sell amount (10% of TOTAL portfolio value)
                    total_portfolio_value = self.get_total_value()
                    sell_value = total_portfolio_value * self.daily_sell_ratio
                    sell_qty = sell_value / self.price
                    
                    # Make sure we don't sell more than we have
                    current_qty = self.position.qty
                    if sell_qty > current_qty:
                        sell_qty = current_qty
                    
                    # Ensure we don't sell below minimum position (25%)
                    remaining_qty = current_qty - sell_qty
                    remaining_value = remaining_qty * self.price
                    remaining_ratio = remaining_value / total_portfolio_value
                    
                    if remaining_ratio >= self.min_position_ratio and sell_qty > 0:
                        self.liquidate(sell_qty)
                        print(f"Sell: {sell_value:.2f} USDT ({self.daily_sell_ratio:.1%} of total portfolio {total_portfolio_value:.2f})")
                    else:
                        # Adjust sell amount to exactly keep 25% position
                        target_value = total_portfolio_value * self.min_position_ratio
                        target_qty = target_value / self.price
                        sell_qty = current_qty - target_qty
                        if sell_qty > 0:
                            self.liquidate(sell_qty)
                            print(f"Final sell to reach 25% minimum position")
                    
                    # Update sell day counter
                    self.sell_day_count += 1
            
            # Check if buy phase should end
            if self.buy_phase:
                current_ratio = self.get_current_position_ratio()
                if current_ratio >= self.max_position_ratio:
                    self.buy_phase = False
                    self.buy_day_count = self.buy_days
            
            # Check if sell phase should end (10 days or minimum position reached)
            if self.sell_phase:
                current_ratio = self.get_current_position_ratio()
                if current_ratio <= self.min_position_ratio or self.sell_day_count >= self.sell_days:
                    self.sell_phase = False
                    self.sell_day_count = 0
                    
        except Exception as e:
            print(f"Update position error: {e}")
    
 