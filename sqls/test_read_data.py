#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试从数据库读取2条数据
验证环境变量配置和数据库连接
"""

import os
from sqls.database_manager import DatabaseManager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_read_data():
    """
    测试读取数据库中的2条数据
    """
    logger.info("开始测试数据库读取...")
    
    try:
        # 初始化数据库管理器
        db_manager = DatabaseManager()
        
        # 查询前2条数据
        query = """
        SELECT coin_name, timestamp, open_price, close_price, volume 
        FROM coinprice2 
        ORDER BY timestamp DESC 
        LIMIT 2
        """
        
        logger.info("执行查询: 获取最新的2条数据")
        result = db_manager.execute_query(query)
        
        if result:
            logger.info(f"成功读取 {len(result)} 条数据:")
            for i, row in enumerate(result, 1):
                logger.info(f"第{i}条: {row['coin_name']} - {row['timestamp']} - 开盘价: {row['open_price']} - 收盘价: {row['close_price']} - 成交量: {row['volume']}")
        else:
            logger.warning("没有读取到数据")
            
        # 查询数据库总数据量
        count_query = "SELECT COUNT(*) as total FROM coinprice2"
        count_result = db_manager.execute_query(count_query)
        if count_result:
            total_count = count_result[0]['total']
            logger.info(f"数据库总数据量: {total_count} 条")
        
        # 查询各币种数据量
        coin_query = """
        SELECT coin_name, COUNT(*) as count 
        FROM coinprice2 
        GROUP BY coin_name 
        ORDER BY count DESC
        """
        coin_result = db_manager.execute_query(coin_query)
        if coin_result:
            logger.info("各币种数据量:")
            for row in coin_result:
                logger.info(f"  {row['coin_name']}: {row['count']} 条")
        
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    # 设置环境变量（实际使用时应该在系统环境中设置）
    os.environ['DB_PASSWORD'] = 'Demt_w1129'
    
    logger.info("=" * 50)
    logger.info("开始数据库读取测试")
    logger.info("=" * 50)
    
    success = test_read_data()
    
    if success:
        logger.info("=" * 50)
        logger.info("测试成功完成！")
        logger.info("=" * 50)
    else:
        logger.error("=" * 50)
        logger.error("测试失败！")
        logger.error("=" * 50)
