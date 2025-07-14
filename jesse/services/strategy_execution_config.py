"""
策略执行配置管理
管理交易所API密钥、风控参数等配置
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import jesse.helpers as jh
from jesse.services.env import ENV_VALUES


@dataclass
class ExchangeConfig:
    """交易所配置"""
    name: str
    api_key: str = ""
    api_secret: str = ""
    api_passphrase: str = ""  # OKX等需要
    testnet: bool = True
    proxy: str = ""
    enabled: bool = False


@dataclass
class RiskConfig:
    """风控配置"""
    max_position_size: float = 0.1  # 最大仓位比例
    max_daily_loss: float = 0.05    # 最大日损失比例
    max_drawdown: float = 0.2       # 最大回撤比例
    stop_loss_percentage: float = 0.02  # 默认止损比例
    take_profit_percentage: float = 0.04  # 默认止盈比例
    max_orders_per_minute: int = 10  # 每分钟最大订单数
    min_order_amount: float = 10.0   # 最小订单金额(USDT)
    enabled: bool = True


@dataclass
class NotificationConfig:
    """通知配置"""
    email_enabled: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_to: str = ""
    
    telegram_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    webhook_enabled: bool = False
    webhook_url: str = ""


@dataclass
class StrategyExecutionConfig:
    """策略执行总配置"""
    exchanges: Dict[str, ExchangeConfig]
    risk: RiskConfig
    notifications: NotificationConfig
    
    # TradingView配置
    tradingview_webhook_port: int = 9001
    tradingview_webhook_secret: str = ""
    
    # 其他配置
    log_level: str = "INFO"
    auto_start: bool = False


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_file = "strategy_execution_config.json"
        self.config: Optional[StrategyExecutionConfig] = None
        self.load_config()
    
    def load_config(self) -> StrategyExecutionConfig:
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = self._dict_to_config(data)
            else:
                # 创建默认配置
                self.config = self._create_default_config()
                self.save_config()
            
            # 从环境变量覆盖敏感信息
            self._load_from_env()
            
            return self.config
            
        except Exception as e:
            jh.error(f"加载配置失败: {str(e)}")
            # 返回默认配置
            self.config = self._create_default_config()
            return self.config
    
    def save_config(self):
        """保存配置"""
        try:
            if self.config:
                # 不保存敏感信息到文件
                config_dict = asdict(self.config)
                
                # 清除敏感信息
                for exchange_name, exchange_config in config_dict['exchanges'].items():
                    exchange_config['api_key'] = ""
                    exchange_config['api_secret'] = ""
                    exchange_config['api_passphrase'] = ""
                
                config_dict['notifications']['email_password'] = ""
                config_dict['notifications']['telegram_bot_token'] = ""
                config_dict['tradingview_webhook_secret'] = ""
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            jh.error(f"保存配置失败: {str(e)}")
    
    def _create_default_config(self) -> StrategyExecutionConfig:
        """创建默认配置"""
        return StrategyExecutionConfig(
            exchanges={
                'binance': ExchangeConfig(
                    name='binance',
                    testnet=True,
                    enabled=False
                ),
                'okx': ExchangeConfig(
                    name='okx',
                    testnet=True,
                    enabled=False
                )
            },
            risk=RiskConfig(),
            notifications=NotificationConfig(),
            tradingview_webhook_port=9001,
            tradingview_webhook_secret="",
            log_level="INFO",
            auto_start=False
        )
    
    def _dict_to_config(self, data: Dict[str, Any]) -> StrategyExecutionConfig:
        """字典转配置对象"""
        exchanges = {}
        for name, exchange_data in data.get('exchanges', {}).items():
            exchanges[name] = ExchangeConfig(**exchange_data)
        
        risk = RiskConfig(**data.get('risk', {}))
        notifications = NotificationConfig(**data.get('notifications', {}))
        
        return StrategyExecutionConfig(
            exchanges=exchanges,
            risk=risk,
            notifications=notifications,
            tradingview_webhook_port=data.get('tradingview_webhook_port', 9001),
            tradingview_webhook_secret=data.get('tradingview_webhook_secret', ''),
            log_level=data.get('log_level', 'INFO'),
            auto_start=data.get('auto_start', False)
        )
    
    def _load_from_env(self):
        """从环境变量加载敏感配置"""
        if not self.config:
            return
        
        # 币安配置
        if 'binance' in self.config.exchanges:
            binance_config = self.config.exchanges['binance']
            binance_config.api_key = ENV_VALUES.get('BINANCE_API_KEY', '')
            binance_config.api_secret = ENV_VALUES.get('BINANCE_API_SECRET', '')
            binance_config.proxy = ENV_VALUES.get('BINANCE_PROXY', '')
            binance_config.testnet = ENV_VALUES.get('BINANCE_TESTNET', 'true').lower() == 'true'
        
        # OKX配置
        if 'okx' in self.config.exchanges:
            okx_config = self.config.exchanges['okx']
            okx_config.api_key = ENV_VALUES.get('OKX_API_KEY', '')
            okx_config.api_secret = ENV_VALUES.get('OKX_API_SECRET', '')
            okx_config.api_passphrase = ENV_VALUES.get('OKX_API_PASSPHRASE', '')
            okx_config.proxy = ENV_VALUES.get('OKX_PROXY', '')
            okx_config.testnet = ENV_VALUES.get('OKX_TESTNET', 'true').lower() == 'true'
        
        # TradingView配置
        self.config.tradingview_webhook_secret = ENV_VALUES.get('TRADINGVIEW_WEBHOOK_SECRET', '')
        
        # 通知配置
        notifications = self.config.notifications
        notifications.email_username = ENV_VALUES.get('EMAIL_USERNAME', '')
        notifications.email_password = ENV_VALUES.get('EMAIL_PASSWORD', '')
        notifications.telegram_bot_token = ENV_VALUES.get('TELEGRAM_BOT_TOKEN', '')
    
    def get_exchange_config(self, exchange_name: str) -> Optional[ExchangeConfig]:
        """获取交易所配置"""
        if self.config and exchange_name in self.config.exchanges:
            return self.config.exchanges[exchange_name]
        return None
    
    def get_risk_config(self) -> RiskConfig:
        """获取风控配置"""
        return self.config.risk if self.config else RiskConfig()
    
    def get_notification_config(self) -> NotificationConfig:
        """获取通知配置"""
        return self.config.notifications if self.config else NotificationConfig()
    
    def update_exchange_config(self, exchange_name: str, config: ExchangeConfig):
        """更新交易所配置"""
        if self.config:
            self.config.exchanges[exchange_name] = config
            self.save_config()
    
    def update_risk_config(self, config: RiskConfig):
        """更新风控配置"""
        if self.config:
            self.config.risk = config
            self.save_config()
    
    def update_notification_config(self, config: NotificationConfig):
        """更新通知配置"""
        if self.config:
            self.config.notifications = config
            self.save_config()
    
    def is_exchange_enabled(self, exchange_name: str) -> bool:
        """检查交易所是否启用"""
        exchange_config = self.get_exchange_config(exchange_name)
        return exchange_config and exchange_config.enabled and exchange_config.api_key and exchange_config.api_secret
    
    def get_enabled_exchanges(self) -> Dict[str, ExchangeConfig]:
        """获取已启用的交易所"""
        if not self.config:
            return {}
        
        return {
            name: config for name, config in self.config.exchanges.items()
            if self.is_exchange_enabled(name)
        }


# 全局配置管理器实例
_config_manager = None


def get_config_manager() -> ConfigManager:
    """获取配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_exchange_config(exchange_name: str) -> Optional[ExchangeConfig]:
    """快捷方法：获取交易所配置"""
    return get_config_manager().get_exchange_config(exchange_name)


def get_risk_config() -> RiskConfig:
    """快捷方法：获取风控配置"""
    return get_config_manager().get_risk_config()


def get_notification_config() -> NotificationConfig:
    """快捷方法：获取通知配置"""
    return get_config_manager().get_notification_config()
