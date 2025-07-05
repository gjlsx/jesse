from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
from datetime import datetime, time

class Trendstrade(Strategy):
    """
    Trend Line Bounce Strategy

    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters
        self.ma_periods = [3, 6, 14, 21, 60, 120]  # 6 moving averages
        self.position_size = 0.3  # Use 30% of balance
        self.stop_loss_pct = 0.02  # 2% stop loss
        self.take_profit_pct = 0.05  # 5% take profit
        self.beijing_time = time(8, 0)  # Beijing time 8:00
    
    @property
    def ma3(self):
        """3-period moving average"""
        return ta.sma(self.candles, period=3, sequential=True)
    
    @property
    def ma6(self):
        """6-period moving average"""
        return ta.sma(self.candles, period=6, sequential=True)
    
    @property
    def ma14(self):
        """14-period moving average"""
        return ta.sma(self.candles, period=14, sequential=True)
    
    @property
    def ma21(self):
        """21-period moving average"""
        return ta.sma(self.candles, period=21, sequential=True)
    
    @property
    def ma60(self):
        """60-period moving average"""
        return ta.sma(self.candles, period=60, sequential=True)
    
    @property
    def ma120(self):
        """120-period moving average"""
        return ta.sma(self.candles, period=120, sequential=True)
    
    def is_beijing_morning(self):
        """Check if it's Beijing time 8:00"""
        # Get current time (UTC+8)
        current_time = datetime.now().time()
        return current_time.hour == 8 and current_time.minute == 0
    
    def get_ma_support_level(self):
        """Get moving average support level"""
        ma_values = []
        
        # Safely get all MA values
        try:
            if len(self.ma3) > 0:
                ma_values.append(self.ma3[-1])
        except:
            pass
            
        try:
            if len(self.ma6) > 0:
                ma_values.append(self.ma6[-1])
        except:
            pass
            
        try:
            if len(self.ma14) > 0:
                ma_values.append(self.ma14[-1])
        except:
            pass
            
        try:
            if len(self.ma21) > 0:
                ma_values.append(self.ma21[-1])
        except:
            pass
            
        try:
            if len(self.ma60) > 0:
                ma_values.append(self.ma60[-1])
        except:
            pass
            
        try:
            if len(self.ma120) > 0:
                ma_values.append(self.ma120[-1])
        except:
            pass
        
        # Filter out None values and sort by price proximity
        valid_mas = [ma for ma in ma_values if ma is not None]
        if not valid_mas:
            return None
        
        # Find the MA closest to current price as support level
        current_price = self.price
        closest_ma = min(valid_mas, key=lambda x: abs(x - current_price))
        return closest_ma
    
    def is_ma_bounce_signal(self):
        """Check if it's a moving average bounce signal"""
        if len(self.candles) < 120:  # Need enough historical data
            return False
        
        current_price = self.price
        ma_support = self.get_ma_support_level()
        
        if ma_support is None:
            return False
        
        # Price is close to support level (within 1%)
        price_near_ma = abs(current_price - ma_support) / ma_support < 0.01
        
        # Check if there's a falling and bouncing pattern
        if len(self.candles) >= 2:
            prev_price = self.candles[-2][2]  # Previous candle's high
            price_falling = current_price < prev_price
            
            # Price was falling and now bouncing above MA
            return price_near_ma and price_falling and current_price >= ma_support * 0.99
        
        return False
    
    def should_long(self) -> bool:
        """
        Determine if should go long
        Beijing time 8:00 + MA bounce signal
        """
        # Check if it's Beijing time 8:00
        if not self.is_beijing_morning():
            return False
        
        # Check MA bounce signal
        return self.is_ma_bounce_signal()
    
    def should_short(self) -> bool:
        """
        This strategy only goes long, no short
        """
        return False
    
    def should_cancel_entry(self) -> bool:
        """
        Determine if should cancel entry orders
        Cancel if price moves too far from support level
        """
        if len(self.candles) < 2:
            return False
        
        current_price = self.price
        ma_support = self.get_ma_support_level()
        
        if ma_support is None:
            return True
        
        # Cancel if price moves more than 2% away from support level
        return abs(current_price - ma_support) / ma_support > 0.02
    
    def go_long(self):
        """
        Execute long position
        """
        # Calculate position size
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        
        # Set buy order
        self.buy = qty, self.price
        
        # Set stop loss (2% below entry price)
        self.stop_loss = qty, self.price * (1 - self.stop_loss_pct)
        
        # Set take profit (5% above entry price)
        self.take_profit = qty, self.price * (1 + self.take_profit_pct)
    
    def go_short(self):
        """
        This strategy doesn't short
        """
        pass
    
    def update_position(self):
        """
        Update existing positions
        Close position if price falls below important MAs
        """
        if not self.is_long:
            return
        
        current_price = self.price
        
        # Check if price is below important MAs
        ma_values = [
            self.ma14[-1] if len(self.ma14) > 0 else None,
            self.ma21[-1] if len(self.ma21) > 0 else None,
            self.ma60[-1] if len(self.ma60) > 0 else None
        ]
        
        valid_mas = [ma for ma in ma_values if ma is not None]
        
        if valid_mas:
            # If price is below all important MAs, close position
            below_all_mas = all(current_price < ma for ma in valid_mas)
            if below_all_mas:
                self.liquidate() 