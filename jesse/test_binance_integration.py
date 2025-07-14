#!/usr/bin/env python3
"""
币安集成测试脚本
用于测试币安API集成功能
"""

import os
import sys
import asyncio
import logging
from decimal import Decimal

# 添加Jesse路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jesse.services.binance_executor import get_binance_executor
from jesse.services.strategy_execution_config import get_config_manager
from jesse.services.risk_manager import get_risk_manager, OrderRequest

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_config_manager():
    """测试配置管理器"""
    print("\n=== 测试配置管理器 ===")
    
    config_manager = get_config_manager()
    
    # 显示当前配置
    binance_config = config_manager.get_exchange_config('binance')
    if binance_config:
        print(f"币安配置:")
        print(f"  - 启用: {binance_config.enabled}")
        print(f"  - 测试网: {binance_config.testnet}")
        print(f"  - API Key: {'已配置' if binance_config.api_key else '未配置'}")
        print(f"  - API Secret: {'已配置' if binance_config.api_secret else '未配置'}")
    
    # 显示风控配置
    risk_config = config_manager.get_risk_config()
    print(f"\n风控配置:")
    print(f"  - 启用: {risk_config.enabled}")
    print(f"  - 最大仓位比例: {risk_config.max_position_size*100}%")
    print(f"  - 最大日损失: {risk_config.max_daily_loss*100}%")
    print(f"  - 最大回撤: {risk_config.max_drawdown*100}%")


def test_binance_connection():
    """测试币安连接"""
    print("\n=== 测试币安连接 ===")
    
    try:
        # 使用测试网
        executor = get_binance_executor(testnet=True)
        
        if not executor.is_connected:
            print("❌ 币安API连接失败 - 可能是API密钥未配置")
            print("请在.env文件中配置以下变量:")
            print("BINANCE_API_KEY=your_api_key")
            print("BINANCE_API_SECRET=your_api_secret")
            print("BINANCE_TESTNET=true")
            return False
        
        print("✅ 币安API连接成功")
        
        # 获取账户信息
        account_info = executor.get_account_info()
        print(f"账户余额: {len(account_info['total_balance'])} 种资产")
        
        # 显示主要余额
        for asset, balance in account_info['total_balance'].items():
            if float(balance) > 0:
                print(f"  - {asset}: {balance}")
        
        return True
        
    except Exception as e:
        print(f"❌ 币安连接测试失败: {str(e)}")
        return False


def test_market_data():
    """测试市场数据获取"""
    print("\n=== 测试市场数据 ===")
    
    try:
        executor = get_binance_executor(testnet=True)
        
        # 测试交易对
        test_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
        
        for symbol in test_symbols:
            try:
                # 获取交易对信息
                symbol_info = executor.get_symbol_info(symbol)
                print(f"\n{symbol}:")
                print(f"  - 状态: {'活跃' if symbol_info['active'] else '非活跃'}")
                print(f"  - 类型: {symbol_info['type']}")
                print(f"  - 数量精度: {symbol_info['precision']['amount']}")
                print(f"  - 价格精度: {symbol_info['precision']['price']}")
                
                # 获取当前价格
                current_price = executor.get_current_price(symbol)
                print(f"  - 当前价格: ${current_price:,.2f}")
                
            except Exception as e:
                print(f"  - ❌ 获取{symbol}信息失败: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 市场数据测试失败: {str(e)}")
        return False


def test_risk_manager():
    """测试风险管理器"""
    print("\n=== 测试风险管理器 ===")
    
    try:
        risk_manager = get_risk_manager()
        
        # 显示风控状态
        status = risk_manager.get_risk_status()
        print(f"风控状态:")
        print(f"  - 交易暂停: {status['trading_halted']}")
        print(f"  - 日盈亏: {status['daily_pnl']*100:.2f}%")
        print(f"  - 持仓数量: {status['positions_count']}")
        print(f"  - 最近1分钟订单数: {status['order_count_last_minute']}")
        
        # 测试订单风控检查
        test_order = OrderRequest(
            symbol='BTC/USDT',
            side='buy',
            amount=0.001,
            price=50000.0
        )
        
        risk_result = risk_manager.check_order_risk(test_order, 1000.0)
        print(f"\n测试订单风控检查:")
        print(f"  - 订单: {test_order.side} {test_order.amount} {test_order.symbol}")
        print(f"  - 结果: {'✅ 通过' if risk_result.allowed else '❌ 拒绝'}")
        if not risk_result.allowed:
            print(f"  - 原因: {risk_result.reason}")
        if risk_result.adjusted_amount:
            print(f"  - 调整数量: {risk_result.adjusted_amount}")
        
        return True
        
    except Exception as e:
        print(f"❌ 风险管理器测试失败: {str(e)}")
        return False


def test_order_simulation():
    """测试订单模拟（不实际下单）"""
    print("\n=== 测试订单模拟 ===")
    
    try:
        executor = get_binance_executor(testnet=True)
        risk_manager = get_risk_manager()
        
        if not executor.is_connected:
            print("❌ 需要API连接才能进行订单测试")
            return False
        
        # 获取BTC当前价格
        symbol = 'BTC/USDT'
        current_price = executor.get_current_price(symbol)
        print(f"{symbol} 当前价格: ${current_price:,.2f}")
        
        # 模拟买单
        buy_order = OrderRequest(
            symbol=symbol,
            side='buy',
            amount=0.001,  # 0.001 BTC
            price=current_price * 0.99  # 低于市价1%的限价单
        )
        
        print(f"\n模拟限价买单:")
        print(f"  - 交易对: {buy_order.symbol}")
        print(f"  - 方向: {buy_order.side}")
        print(f"  - 数量: {buy_order.amount}")
        print(f"  - 价格: ${buy_order.price:,.2f}")
        
        # 风控检查
        risk_result = risk_manager.check_order_risk(buy_order, 1000.0)
        print(f"  - 风控检查: {'✅ 通过' if risk_result.allowed else '❌ 拒绝'}")
        if not risk_result.allowed:
            print(f"  - 拒绝原因: {risk_result.reason}")
            return False
        
        # 计算止损止盈
        stop_loss, take_profit = risk_manager.calculate_stop_loss_take_profit(buy_order, current_price)
        if stop_loss:
            print(f"  - 建议止损: ${stop_loss:,.2f}")
        if take_profit:
            print(f"  - 建议止盈: ${take_profit:,.2f}")
        
        print("\n⚠️  这只是模拟测试，没有实际下单")
        print("如需实际交易，请确保:")
        print("1. 已充分测试")
        print("2. 风控参数合理")
        print("3. 使用小额资金测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 订单模拟测试失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("🚀 Jesse 币安集成测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("配置管理器", test_config_manager),
        ("币安连接", test_binance_connection),
        ("市场数据", test_market_data),
        ("风险管理器", test_risk_manager),
        ("订单模拟", test_order_simulation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {str(e)}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  - {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！币安集成基础功能正常")
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接")
    
    print("\n💡 提示:")
    print("1. 确保在.env文件中配置了币安API密钥")
    print("2. 建议先在测试网环境进行充分测试")
    print("3. 实际交易前请仔细检查风控参数")


if __name__ == "__main__":
    main()
