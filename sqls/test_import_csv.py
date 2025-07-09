#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试CSV数据导入MySQL
先测试导入2条数据
"""

import csv
import os
import glob
from datetime import datetime
from sqls.database_manager import DatabaseManager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_csv_row(row, coin_name):
    """
    解析CSV行数据

    Args:
        row: CSV行数据
        coin_name: 币种名称

    Returns:
        dict: 解析后的数据字典
    """
    try:
        # 处理BOM问题，获取正确的字段名
        time_open_key = 'timeOpen'
        if 'timeOpen' not in row:
            # 查找包含timeOpen的键（可能有BOM前缀）
            for key in row.keys():
                if 'timeOpen' in key:
                    time_open_key = key
                    break

        # 解析时间字符串，去掉引号并转换为datetime
        time_open = datetime.fromisoformat(row[time_open_key].strip('"').replace('Z', '+00:00'))
        time_close = datetime.fromisoformat(row['timeClose'].strip('"').replace('Z', '+00:00'))
        time_high = datetime.fromisoformat(row['timeHigh'].strip('"').replace('Z', '+00:00'))
        time_low = datetime.fromisoformat(row['timeLow'].strip('"').replace('Z', '+00:00'))
        timestamp = datetime.fromisoformat(row['timestamp'].strip('"').replace('Z', '+00:00'))
        
        data = {
            'time_open': time_open,
            'time_close': time_close,
            'time_high': time_high,
            'time_low': time_low,
            'coin_name': coin_name,
            'coin_id': row['name'].strip('"'),
            'open_price': float(row['open']),
            'high_price': float(row['high']),
            'low_price': float(row['low']),
            'close_price': float(row['close']),
            'volume': float(row['volume']),
            'market_cap': float(row['marketCap']),
            'timestamp': timestamp
        }
        
        return data
    except Exception as e:
        logger.error(f"解析CSV行数据失败: {e}")
        logger.error(f"问题行数据: {row}")
        return None

def read_csv_file(file_path, limit=None):
    """
    读取CSV文件
    
    Args:
        file_path: CSV文件路径
        limit: 限制读取行数，None表示读取全部
        
    Returns:
        list: 解析后的数据列表
    """
    # 从文件名提取币种名称
    filename = os.path.basename(file_path)
    coin_name = filename.split('_')[0]
    
    logger.info(f"开始读取文件: {file_path}")
    logger.info(f"币种名称: {coin_name}")
    
    data_list = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用分号作为分隔符
            reader = csv.DictReader(file, delimiter=';')
            
            for i, row in enumerate(reader):
                if limit and i >= limit:
                    break
                    
                data = parse_csv_row(row, coin_name)
                if data:
                    data_list.append(data)
                    logger.info(f"解析第 {i+1} 行数据: {coin_name} - {data['timestamp']}")
    
    except Exception as e:
        logger.error(f"读取CSV文件失败: {e}")
        return []
    
    logger.info(f"成功读取 {len(data_list)} 条数据")
    return data_list

def find_historical_csv_files():
    """
    查找包含'historical'的CSV文件
    
    Returns:
        list: CSV文件路径列表
    """
    csv_dir = "storage/csv"
    pattern = os.path.join(csv_dir, "*historical*.csv")
    files = glob.glob(pattern)
    
    logger.info(f"找到 {len(files)} 个历史数据CSV文件:")
    for file in files:
        logger.info(f"  - {file}")
    
    return files

def test_import_data():
    """
    测试导入数据（只导入2条数据）
    """
    logger.info("开始测试数据导入...")
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    # 创建表
    logger.info("创建coinprice2表...")
    if not db_manager.create_coinprice2_table():
        logger.error("创建表失败，退出程序")
        return False
    
    # 查找CSV文件
    csv_files = find_historical_csv_files()
    if not csv_files:
        logger.error("没有找到历史数据CSV文件")
        return False
    
    # 只处理第一个文件，只读取2条数据进行测试
    test_file = csv_files[0]
    logger.info(f"测试文件: {test_file}")
    
    # 读取2条数据
    data_list = read_csv_file(test_file, limit=2)
    
    if not data_list:
        logger.error("没有读取到有效数据")
        return False
    
    # 插入数据
    logger.info("开始插入测试数据...")
    try:
        inserted_rows = db_manager.insert_coin_data(data_list)
        logger.info(f"测试成功！插入了 {inserted_rows} 条数据")
        
        # 打印插入的数据信息
        for i, data in enumerate(data_list, 1):
            logger.info(f"第{i}条: {data['coin_name']} - {data['timestamp']} - 价格: {data['close_price']}")
        
        return True
        
    except Exception as e:
        logger.error(f"插入数据失败: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("开始CSV数据导入测试")
    logger.info("=" * 50)
    
    success = test_import_data()
    
    if success:
        logger.info("=" * 50)
        logger.info("测试成功完成！")
        logger.info("=" * 50)
    else:
        logger.error("=" * 50)
        logger.error("测试失败！")
        logger.error("=" * 50)
