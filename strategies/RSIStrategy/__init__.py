

from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class RSIStrategy(Strategy):
    """
    RSI Mean Reversion Strategy
    Go long when RSI is oversold, go short when RSI is overbought
    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters
        self.rsi_period = 14
        self.oversold_threshold = 30
        self.overbought_threshold = 70
        self.position_size = 0.3  # Use 30% of balance
    
    @property
    def rsi(self):
        """RSI indicator"""
        return ta.rsi(self.candles, period=self.rsi_period)
    
    def should_long(self) -> bool:
        """
        Determine if should go long
        Go long when RSI is oversold
        """
        return self.rsi <= self.oversold_threshold
    
    def should_short(self) -> bool:
        """
        Spot trading doesn't allow short positions
        Always return False for spot exchange
        """
        return False
    
    def should_cancel_entry(self) -> bool:
        """
        Determine if should cancel entry orders
        Cancel entry orders if RSI returns to neutral zone
        """
        return 40 < self.rsi < 60
    
    def go_long(self):
        """
        Execute long position
        """
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        self.buy = qty, self.price
        # Set stop loss (2% below entry price)
        self.stop_loss = qty, self.price * 0.98
        # Set take profit (3% above entry price)
        self.take_profit = qty, self.price * 1.03
    
    def go_short(self):
        """
        Spot trading doesn't support short positions
        This method is not used in spot trading
        """
        pass
    
    def update_position(self):
        """
        更新现有仓位
        如果持有多头且RSI超买，平仓
        如果持有空头且RSI超卖，平仓
        """
        if self.is_long and self.rsi >= self.overbought_threshold:
            self.liquidate()
        elif self.is_short and self.rsi <= self.oversold_threshold:
            self.liquidate() 