#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全量导入CSV历史数据到MySQL
处理所有包含'historical'的CSV文件
"""

import csv
import os
import glob
from datetime import datetime
from sqls.database_manager import DatabaseManager
import logging
import time

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

def read_csv_file(file_path):
    """
    读取整个CSV文件
    
    Args:
        file_path: CSV文件路径
        
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
                data = parse_csv_row(row, coin_name)
                if data:
                    data_list.append(data)
                    if (i + 1) % 50 == 0:  # 每50行显示一次进度
                        logger.info(f"已解析 {i+1} 行数据...")
    
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
    files.sort()  # 按文件名排序
    
    logger.info(f"找到 {len(files)} 个历史数据CSV文件:")
    for i, file in enumerate(files, 1):
        logger.info(f"  {i}. {os.path.basename(file)}")
    
    return files

def import_all_data():
    """
    导入所有历史数据
    """
    start_time = time.time()
    logger.info("开始全量数据导入...")
    
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
    
    total_inserted = 0
    successful_files = 0
    failed_files = []
    
    # 处理每个CSV文件
    for i, csv_file in enumerate(csv_files, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"处理第 {i}/{len(csv_files)} 个文件")
        logger.info(f"文件: {os.path.basename(csv_file)}")
        logger.info(f"{'='*60}")
        
        try:
            # 读取CSV数据
            data_list = read_csv_file(csv_file)
            
            if not data_list:
                logger.warning(f"文件 {csv_file} 没有有效数据，跳过")
                failed_files.append(csv_file)
                continue
            
            # 分批插入数据（每批100条）
            batch_size = 100
            file_inserted = 0
            
            for j in range(0, len(data_list), batch_size):
                batch_data = data_list[j:j + batch_size]
                
                try:
                    inserted_rows = db_manager.insert_coin_data(batch_data)
                    file_inserted += inserted_rows
                    logger.info(f"批次 {j//batch_size + 1}: 插入 {inserted_rows} 条数据")
                    
                except Exception as e:
                    logger.error(f"批次 {j//batch_size + 1} 插入失败: {e}")
                    continue
            
            total_inserted += file_inserted
            successful_files += 1
            
            logger.info(f"文件 {os.path.basename(csv_file)} 处理完成")
            logger.info(f"本文件插入: {file_inserted} 条数据")
            logger.info(f"累计插入: {total_inserted} 条数据")
            
        except Exception as e:
            logger.error(f"处理文件 {csv_file} 失败: {e}")
            failed_files.append(csv_file)
            continue
    
    # 输出最终统计
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"\n{'='*60}")
    logger.info("全量导入完成！")
    logger.info(f"{'='*60}")
    logger.info(f"总文件数: {len(csv_files)}")
    logger.info(f"成功处理: {successful_files} 个文件")
    logger.info(f"失败文件: {len(failed_files)} 个")
    logger.info(f"总插入数据: {total_inserted} 条")
    logger.info(f"总耗时: {duration:.2f} 秒")
    
    if failed_files:
        logger.warning("失败的文件:")
        for failed_file in failed_files:
            logger.warning(f"  - {os.path.basename(failed_file)}")
    
    return len(failed_files) == 0

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("开始CSV历史数据全量导入")
    logger.info("=" * 80)
    
    success = import_all_data()
    
    if success:
        logger.info("=" * 80)
        logger.info("全量导入成功完成！")
        logger.info("=" * 80)
    else:
        logger.error("=" * 80)
        logger.error("全量导入过程中有错误发生！")
        logger.error("=" * 80)
