from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class MovingAverageStrategy(Strategy):
    """
    移动平均线交叉策略
    当快线上穿慢线时做多，当快线下穿慢线时做空
    """
    print ("移动平均线交叉策略")
    def __init__(self):
        super().__init__()
        # 策略参数
        self.fast_period = 10
        self.slow_period = 20
        self.position_size = 0.5  # 使用50%的余额
    
    @property
    def fast_sma(self):
        """快速移动平均线"""
        return ta.sma(self.candles, period=self.fast_period, sequential=True)
    
    @property
    def slow_sma(self):
        """慢速移动平均线"""
        return ta.sma(self.candles, period=self.slow_period, sequential=True)
    
    def should_long(self) -> bool:
        """
        判断是否应该做多
        当快线上穿慢线时做多
        """
        return utils.crossed(self.fast_sma, self.slow_sma, direction='above')
    
    def should_short(self) -> bool:
        """
        判断是否应该做空
        当快线下穿慢线时做空
        """
        return utils.crossed(self.fast_sma, self.slow_sma, direction='below')
    
    def should_cancel_entry(self) -> bool:
        """
        判断是否应该取消入场订单
        """
        return False
    
    def go_long(self):
        """
        执行做多操作
        """
        # 计算仓位大小
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        # 设置买入订单
        self.buy = qty, self.price
        # 设置止损（在慢均线下方1%）
        self.stop_loss = qty, self.slow_sma[-1] * 0.99
        # 设置止盈（在当前价格上方2%）
        self.take_profit = qty, self.price * 1.02
    
    def go_short(self):
        """
        执行做空操作
        """
        # 计算仓位大小
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        # 设置卖出订单
        self.sell = qty, self.price
        # 设置止损（在慢均线上方1%）
        self.stop_loss = qty, self.slow_sma[-1] * 1.01
        # 设置止盈（在当前价格下方2%）
        self.take_profit = qty, self.price * 0.98
    
    def update_position(self):
        """
        更新现有仓位
        """
        pass 