"""
风险管理系统
实现多层风控机制，包括仓位管理、止损止盈、最大回撤控制等
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal
import jesse.helpers as jh
from jesse.services.strategy_execution_config import get_risk_config, RiskConfig

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """持仓信息"""
    symbol: str
    side: str  # 'long' or 'short'
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    timestamp: float


@dataclass
class OrderRequest:
    """订单请求"""
    symbol: str
    side: str  # 'buy' or 'sell'
    amount: float
    price: Optional[float] = None  # None表示市价单
    reduce_only: bool = False
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


@dataclass
class RiskCheckResult:
    """风控检查结果"""
    allowed: bool
    reason: str = ""
    adjusted_amount: Optional[float] = None


class RiskManager:
    """风险管理器"""
    
    def __init__(self):
        self.risk_config = get_risk_config()
        self.positions: Dict[str, Position] = {}
        self.daily_pnl = 0.0
        self.daily_start_balance = 0.0
        self.max_drawdown_reached = 0.0
        self.order_count_per_minute: List[float] = []
        self.last_reset_time = time.time()
        
        # 风控状态
        self.trading_halted = False
        self.halt_reason = ""
        
        logger.info("风险管理器初始化完成")
    
    def update_config(self, config: RiskConfig):
        """更新风控配置"""
        self.risk_config = config
        logger.info("风控配置已更新")
    
    def update_positions(self, positions: List[Position]):
        """更新持仓信息"""
        self.positions = {pos.symbol: pos for pos in positions}
        
        # 计算总的未实现盈亏
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in positions)
        
        # 检查最大回撤
        self._check_max_drawdown(total_unrealized_pnl)
    
    def update_daily_balance(self, current_balance: float):
        """更新每日余额（用于计算日损失）"""
        current_time = time.time()
        
        # 检查是否需要重置日统计
        if current_time - self.last_reset_time > 24 * 3600:  # 24小时
            self.daily_start_balance = current_balance
            self.daily_pnl = 0.0
            self.last_reset_time = current_time
            logger.info("日统计已重置")
        
        # 计算日盈亏
        if self.daily_start_balance > 0:
            self.daily_pnl = (current_balance - self.daily_start_balance) / self.daily_start_balance
    
    def check_order_risk(self, order: OrderRequest, current_balance: float) -> RiskCheckResult:
        """
        检查订单风险
        
        Args:
            order: 订单请求
            current_balance: 当前余额
            
        Returns:
            风控检查结果
        """
        if not self.risk_config.enabled:
            return RiskCheckResult(allowed=True)
        
        # 检查交易是否被暂停
        if self.trading_halted:
            return RiskCheckResult(allowed=False, reason=f"交易已暂停: {self.halt_reason}")
        
        # 检查订单频率
        freq_check = self._check_order_frequency()
        if not freq_check.allowed:
            return freq_check
        
        # 检查最小订单金额
        min_amount_check = self._check_min_order_amount(order)
        if not min_amount_check.allowed:
            return min_amount_check
        
        # 检查仓位大小
        position_check = self._check_position_size(order, current_balance)
        if not position_check.allowed:
            return position_check
        
        # 检查日损失限制
        daily_loss_check = self._check_daily_loss()
        if not daily_loss_check.allowed:
            return daily_loss_check
        
        return RiskCheckResult(allowed=True)
    
    def _check_order_frequency(self) -> RiskCheckResult:
        """检查订单频率"""
        current_time = time.time()
        
        # 清理1分钟前的记录
        self.order_count_per_minute = [
            t for t in self.order_count_per_minute 
            if current_time - t < 60
        ]
        
        # 检查是否超过限制
        if len(self.order_count_per_minute) >= self.risk_config.max_orders_per_minute:
            return RiskCheckResult(
                allowed=False, 
                reason=f"订单频率过高，每分钟最多{self.risk_config.max_orders_per_minute}个订单"
            )
        
        # 记录当前订单时间
        self.order_count_per_minute.append(current_time)
        return RiskCheckResult(allowed=True)
    
    def _check_min_order_amount(self, order: OrderRequest) -> RiskCheckResult:
        """检查最小订单金额"""
        if order.price:
            order_value = order.amount * order.price
        else:
            # 市价单，需要获取当前价格估算
            # 这里简化处理，实际应该获取实时价格
            order_value = order.amount * 50000  # 假设价格，实际应该动态获取
        
        if order_value < self.risk_config.min_order_amount:
            return RiskCheckResult(
                allowed=False,
                reason=f"订单金额过小，最小金额为{self.risk_config.min_order_amount}USDT"
            )
        
        return RiskCheckResult(allowed=True)
    
    def _check_position_size(self, order: OrderRequest, current_balance: float) -> RiskCheckResult:
        """检查仓位大小"""
        # 获取当前持仓
        current_position = self.positions.get(order.symbol)
        current_size = current_position.size if current_position else 0.0
        
        # 计算新的仓位大小
        if order.side == 'buy':
            new_size = current_size + order.amount
        else:
            new_size = current_size - order.amount
        
        # 估算仓位价值（简化处理）
        estimated_price = order.price if order.price else 50000  # 应该获取实时价格
        position_value = abs(new_size) * estimated_price
        
        # 检查仓位比例
        max_position_value = current_balance * self.risk_config.max_position_size
        
        if position_value > max_position_value:
            # 计算调整后的数量
            max_allowed_size = max_position_value / estimated_price
            adjusted_amount = max_allowed_size - abs(current_size)
            
            if adjusted_amount <= 0:
                return RiskCheckResult(
                    allowed=False,
                    reason=f"仓位过大，最大仓位比例为{self.risk_config.max_position_size*100}%"
                )
            
            return RiskCheckResult(
                allowed=True,
                adjusted_amount=adjusted_amount,
                reason=f"订单数量已调整以符合仓位限制"
            )
        
        return RiskCheckResult(allowed=True)
    
    def _check_daily_loss(self) -> RiskCheckResult:
        """检查日损失限制"""
        if self.daily_pnl < -self.risk_config.max_daily_loss:
            self._halt_trading(f"达到日最大损失限制{self.risk_config.max_daily_loss*100}%")
            return RiskCheckResult(
                allowed=False,
                reason=f"达到日最大损失限制{self.risk_config.max_daily_loss*100}%"
            )
        
        return RiskCheckResult(allowed=True)
    
    def _check_max_drawdown(self, current_unrealized_pnl: float):
        """检查最大回撤"""
        if current_unrealized_pnl < self.max_drawdown_reached:
            self.max_drawdown_reached = current_unrealized_pnl
        
        # 计算回撤比例（简化处理，实际应该基于账户净值）
        if abs(self.max_drawdown_reached) > self.risk_config.max_drawdown * 10000:  # 假设基准
            self._halt_trading(f"达到最大回撤限制{self.risk_config.max_drawdown*100}%")
    
    def _halt_trading(self, reason: str):
        """暂停交易"""
        self.trading_halted = True
        self.halt_reason = reason
        logger.error(f"交易已暂停: {reason}")
        
        # 这里可以添加紧急通知逻辑
        self._send_emergency_notification(reason)
    
    def _send_emergency_notification(self, reason: str):
        """发送紧急通知"""
        # TODO: 实现紧急通知逻辑
        logger.critical(f"紧急通知: {reason}")
    
    def resume_trading(self):
        """恢复交易"""
        self.trading_halted = False
        self.halt_reason = ""
        logger.info("交易已恢复")
    
    def calculate_stop_loss_take_profit(self, order: OrderRequest, current_price: float) -> Tuple[Optional[float], Optional[float]]:
        """
        计算止损止盈价格
        
        Args:
            order: 订单请求
            current_price: 当前价格
            
        Returns:
            (止损价格, 止盈价格)
        """
        if not self.risk_config.enabled:
            return None, None
        
        stop_loss = None
        take_profit = None
        
        if order.side == 'buy':  # 做多
            if self.risk_config.stop_loss_percentage > 0:
                stop_loss = current_price * (1 - self.risk_config.stop_loss_percentage)
            if self.risk_config.take_profit_percentage > 0:
                take_profit = current_price * (1 + self.risk_config.take_profit_percentage)
        else:  # 做空
            if self.risk_config.stop_loss_percentage > 0:
                stop_loss = current_price * (1 + self.risk_config.stop_loss_percentage)
            if self.risk_config.take_profit_percentage > 0:
                take_profit = current_price * (1 - self.risk_config.take_profit_percentage)
        
        return stop_loss, take_profit
    
    def get_risk_status(self) -> Dict[str, any]:
        """获取风控状态"""
        return {
            'trading_halted': self.trading_halted,
            'halt_reason': self.halt_reason,
            'daily_pnl': self.daily_pnl,
            'max_drawdown_reached': self.max_drawdown_reached,
            'order_count_last_minute': len(self.order_count_per_minute),
            'positions_count': len(self.positions),
            'config': {
                'max_position_size': self.risk_config.max_position_size,
                'max_daily_loss': self.risk_config.max_daily_loss,
                'max_drawdown': self.risk_config.max_drawdown,
                'enabled': self.risk_config.enabled
            }
        }


# 全局风险管理器实例
_risk_manager = None


def get_risk_manager() -> RiskManager:
    """获取风险管理器实例"""
    global _risk_manager
    if _risk_manager is None:
        _risk_manager = RiskManager()
    return _risk_manager
