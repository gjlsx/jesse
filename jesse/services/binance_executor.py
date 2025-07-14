"""
币安交易执行器
基于CCXT库实现的币安交易所集成
支持现货和期货交易
"""

import ccxt
import logging
import time
from typing import Dict, Optional, List, Any
from decimal import Decimal
import jesse.helpers as jh
from jesse.services.env import ENV_VALUES

logger = logging.getLogger(__name__)


class BinanceExecutor:
    """币安交易执行器"""
    
    def __init__(self, testnet: bool = False):
        """
        初始化币安交易执行器
        
        Args:
            testnet: 是否使用测试网
        """
        self.testnet = testnet
        self.exchange = None
        self.is_connected = False
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """初始化交易所连接"""
        try:
            # 从环境变量获取API密钥
            api_key = ENV_VALUES.get('BINANCE_API_KEY', '')
            api_secret = ENV_VALUES.get('BINANCE_API_SECRET', '')
            
            if not api_key or not api_secret:
                logger.warning("币安API密钥未配置，将使用只读模式")
            
            # 配置CCXT
            config = {
                'apiKey': api_key,
                'secret': api_secret,
                'timeout': 30000,
                'enableRateLimit': True,
                'verbose': False,
            }
            
            # 测试网配置
            if self.testnet:
                config['sandbox'] = True
                config['urls'] = {
                    'api': {
                        'public': 'https://testnet.binance.vision/api',
                        'private': 'https://testnet.binance.vision/api',
                    }
                }
            
            # 代理配置（如果需要）
            proxy = ENV_VALUES.get('BINANCE_PROXY', '')
            if proxy:
                config['proxies'] = {'http': proxy, 'https': proxy}
            
            self.exchange = ccxt.binance(config)
            
            # 测试连接
            if api_key and api_secret:
                self._test_connection()
            
            logger.info(f"币安交易执行器初始化成功 (测试网: {self.testnet})")
            
        except Exception as e:
            logger.error(f"币安交易执行器初始化失败: {str(e)}")
            raise
    
    def _test_connection(self):
        """测试API连接"""
        try:
            # 获取账户信息来测试连接
            account_info = self.exchange.fetch_balance()
            self.is_connected = True
            logger.info("币安API连接测试成功")
            return True
        except Exception as e:
            logger.error(f"币安API连接测试失败: {str(e)}")
            self.is_connected = False
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """获取账户信息"""
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            balance = self.exchange.fetch_balance()
            return {
                'total_balance': balance['total'],
                'free_balance': balance['free'],
                'used_balance': balance['used'],
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"获取账户信息失败: {str(e)}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """获取交易对信息"""
        try:
            markets = self.exchange.load_markets()
            if symbol not in markets:
                raise ValueError(f"不支持的交易对: {symbol}")
            
            market = markets[symbol]
            return {
                'symbol': symbol,
                'base': market['base'],
                'quote': market['quote'],
                'active': market['active'],
                'type': market['type'],  # spot, future, etc.
                'precision': market['precision'],
                'limits': market['limits'],
                'fees': market['fees']
            }
        except Exception as e:
            logger.error(f"获取交易对信息失败 {symbol}: {str(e)}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """获取当前价格"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return float(ticker['last'])
        except Exception as e:
            logger.error(f"获取价格失败 {symbol}: {str(e)}")
            raise
    
    def place_market_order(self, symbol: str, side: str, amount: float, 
                          reduce_only: bool = False) -> Dict[str, Any]:
        """
        下市价单
        
        Args:
            symbol: 交易对，如 'BTC/USDT'
            side: 'buy' 或 'sell'
            amount: 数量
            reduce_only: 是否只减仓（期货）
        """
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            # 验证参数
            if side not in ['buy', 'sell']:
                raise ValueError("side必须是'buy'或'sell'")
            
            if amount <= 0:
                raise ValueError("数量必须大于0")
            
            # 获取交易对信息进行精度处理
            symbol_info = self.get_symbol_info(symbol)
            amount_precision = symbol_info['precision']['amount']
            amount = round(amount, amount_precision)
            
            # 构建订单参数
            params = {}
            if reduce_only:
                params['reduceOnly'] = True
            
            # 下单
            order = self.exchange.create_market_order(symbol, side, amount, None, None, params)
            
            logger.info(f"市价单已提交: {symbol} {side} {amount}")
            return self._format_order_response(order)
            
        except Exception as e:
            logger.error(f"下市价单失败 {symbol} {side} {amount}: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, amount: float, price: float,
                         reduce_only: bool = False) -> Dict[str, Any]:
        """
        下限价单
        
        Args:
            symbol: 交易对
            side: 'buy' 或 'sell'
            amount: 数量
            price: 价格
            reduce_only: 是否只减仓
        """
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            # 验证参数
            if side not in ['buy', 'sell']:
                raise ValueError("side必须是'buy'或'sell'")
            
            if amount <= 0 or price <= 0:
                raise ValueError("数量和价格必须大于0")
            
            # 获取交易对信息进行精度处理
            symbol_info = self.get_symbol_info(symbol)
            amount_precision = symbol_info['precision']['amount']
            price_precision = symbol_info['precision']['price']
            
            amount = round(amount, amount_precision)
            price = round(price, price_precision)
            
            # 构建订单参数
            params = {}
            if reduce_only:
                params['reduceOnly'] = True
            
            # 下单
            order = self.exchange.create_limit_order(symbol, side, amount, price, None, params)
            
            logger.info(f"限价单已提交: {symbol} {side} {amount} @ {price}")
            return self._format_order_response(order)
            
        except Exception as e:
            logger.error(f"下限价单失败 {symbol} {side} {amount} @ {price}: {str(e)}")
            raise
    
    def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """取消订单"""
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            result = self.exchange.cancel_order(order_id, symbol)
            logger.info(f"订单已取消: {order_id}")
            return self._format_order_response(result)
            
        except Exception as e:
            logger.error(f"取消订单失败 {order_id}: {str(e)}")
            raise
    
    def get_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """获取订单状态"""
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            order = self.exchange.fetch_order(order_id, symbol)
            return self._format_order_response(order)
            
        except Exception as e:
            logger.error(f"获取订单状态失败 {order_id}: {str(e)}")
            raise
    
    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """获取未完成订单"""
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            orders = self.exchange.fetch_open_orders(symbol)
            return [self._format_order_response(order) for order in orders]
            
        except Exception as e:
            logger.error(f"获取未完成订单失败: {str(e)}")
            raise
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """获取持仓信息（期货）"""
        try:
            if not self.is_connected:
                raise Exception("未连接到币安API")
            
            positions = self.exchange.fetch_positions()
            # 只返回有持仓的
            active_positions = [pos for pos in positions if float(pos['contracts']) != 0]
            
            return [{
                'symbol': pos['symbol'],
                'side': pos['side'],
                'size': float(pos['contracts']),
                'entry_price': float(pos['entryPrice']) if pos['entryPrice'] else 0,
                'mark_price': float(pos['markPrice']) if pos['markPrice'] else 0,
                'unrealized_pnl': float(pos['unrealizedPnl']) if pos['unrealizedPnl'] else 0,
                'percentage': float(pos['percentage']) if pos['percentage'] else 0,
            } for pos in active_positions]
            
        except Exception as e:
            logger.error(f"获取持仓信息失败: {str(e)}")
            raise
    
    def _format_order_response(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """格式化订单响应"""
        return {
            'id': order['id'],
            'symbol': order['symbol'],
            'side': order['side'],
            'type': order['type'],
            'amount': float(order['amount']),
            'price': float(order['price']) if order['price'] else None,
            'filled': float(order['filled']),
            'remaining': float(order['remaining']),
            'status': order['status'],
            'timestamp': order['timestamp'],
            'fee': order.get('fee', {}),
            'trades': order.get('trades', [])
        }


# 全局实例
_binance_executor = None


def get_binance_executor(testnet: bool = False) -> BinanceExecutor:
    """获取币安交易执行器实例"""
    global _binance_executor
    if _binance_executor is None:
        _binance_executor = BinanceExecutor(testnet=testnet)
    return _binance_executor
