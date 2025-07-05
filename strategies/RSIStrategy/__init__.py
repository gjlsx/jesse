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
        Determine if should go short
        Go short when RSI is overbought
        """
        return self.rsi >= self.overbought_threshold
    
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
        Execute short position
        """
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        self.sell = qty, self.price
        # Set stop loss (2% above entry price)
        self.stop_loss = qty, self.price * 1.02
        # Set take profit (3% below entry price)
        self.take_profit = qty, self.price * 0.97
    
    def update_position(self):
        """
        Update existing positions
        If holding long and RSI is overbought, close position
        If holding short and RSI is oversold, close position
        """
        if self.is_long and self.rsi >= self.overbought_threshold:
            self.liquidate()
        elif self.is_short and self.rsi <= self.oversold_threshold:
            self.liquidate() 