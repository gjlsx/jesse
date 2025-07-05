from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class RSIStrategy(Strategy):
    """
    RSI 均值回归策略
    当RSI超卖时做多，当RSI超买时做空
    """
    
    def __init__(self):
        super().__init__()
        # 策略参数
        self.rsi_period = 14
        self.oversold_threshold = 30
        self.overbought_threshold = 70
        self.position_size = 0.3  # 使用30%的余额
    
    @property
    def rsi(self):
        """RSI指标"""
        return ta.rsi(self.candles, period=self.rsi_period)
    
    def should_long(self) -> bool:
        """
        判断是否应该做多
        RSI 超卖时做多
        """
        return self.rsi <= self.oversold_threshold
    
    def should_short(self) -> bool:
        """
        判断是否应该做空
        RSI 超买时做空
        """
        return self.rsi >= self.overbought_threshold
    
    def should_cancel_entry(self) -> bool:
        """
        判断是否应该取消入场订单
        如果RSI回到中性区域，取消入场订单
        """
        return 40 < self.rsi < 60
    
    def go_long(self):
        """
        执行做多操作
        """
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        self.buy = qty, self.price
        # 设置止损（在入场价格下方2%）
        self.stop_loss = qty, self.price * 0.98
        # 设置止盈（在入场价格上方3%）
        self.take_profit = qty, self.price * 1.03
    
    def go_short(self):
        """
        执行做空操作
        """
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        self.sell = qty, self.price
        # 设置止损（在入场价格上方2%）
        self.stop_loss = qty, self.price * 1.02
        # 设置止盈（在入场价格下方3%）
        self.take_profit = qty, self.price * 0.97
    
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