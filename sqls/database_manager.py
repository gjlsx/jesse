#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理模块
用于处理MySQL数据库连接和操作
"""

import pymysql
import logging
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager:
    """MySQL数据库管理类"""
    
    def __init__(self, connection_string: str = None):
        """
        初始化数据库管理器
        
        Args:
            connection_string: MySQL连接字符串
        """
        # 默认连接配置
        if connection_string is None:
            self.config = {
                'host': os.getenv('DB_HOST', 'zzb2020.mysql.polardb.rds.aliyuncs.com'),
                'port': int(os.getenv('DB_PORT', '3306')),
                'user': os.getenv('DB_USER', 'demt_write'),
                'password': os.getenv('DB_PASSWORD'),
                'database': os.getenv('DB_NAME', 'demt'),
                'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
                'autocommit': True
            }

            # 检查必需的环境变量
            if not self.config['password']:
                raise ValueError("DB_PASSWORD environment variable is required")
        else:
            self.config = self._parse_connection_string(connection_string)
    
    def _parse_connection_string(self, conn_str: str) -> Dict[str, Any]:
        """
        解析连接字符串
        
        Args:
            conn_str: 连接字符串
            
        Returns:
            Dict: 数据库配置字典
        """
        # 这里可以根据需要实现连接字符串解析
        # 目前使用默认配置
        return {
            'host': 'zzb2020.mysql.polardb.rds.aliyuncs.com',
            'port': 3306,
            'user': 'demt_write',
            'password': 'Demt_w1129',
            'database': 'demt',
            'charset': 'utf8mb4',
            'autocommit': True
        }
    
    @contextmanager
    def get_connection(self):
        """
        获取数据库连接的上下文管理器
        
        Yields:
            pymysql.Connection: 数据库连接对象
        """
        connection = None
        try:
            connection = pymysql.connect(**self.config)
            logger.info("数据库连接成功")
            yield connection
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
        finally:
            if connection:
                connection.close()
                logger.info("数据库连接已关闭")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        执行查询语句
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            List[Dict]: 查询结果
        """
        with self.get_connection() as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
                    logger.info(f"查询执行成功，返回 {len(result)} 条记录")
                    return result
            except Exception as e:
                logger.error(f"查询执行失败: {e}")
                raise
    
    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """
        执行非查询语句（INSERT, UPDATE, DELETE）
        
        Args:
            query: SQL语句
            params: 参数
            
        Returns:
            int: 受影响的行数
        """
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    affected_rows = cursor.execute(query, params)
                    conn.commit()
                    logger.info(f"语句执行成功，影响 {affected_rows} 行")
                    return affected_rows
            except Exception as e:
                logger.error(f"语句执行失败: {e}")
                conn.rollback()
                raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        批量执行语句
        
        Args:
            query: SQL语句
            params_list: 参数列表
            
        Returns:
            int: 受影响的行数
        """
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    affected_rows = cursor.executemany(query, params_list)
                    conn.commit()
                    logger.info(f"批量执行成功，影响 {affected_rows} 行")
                    return affected_rows
            except Exception as e:
                logger.error(f"批量执行失败: {e}")
                conn.rollback()
                raise
    
    def create_coinprice2_table(self) -> bool:
        """
        创建coinprice2表
        
        Returns:
            bool: 创建是否成功
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS coinprice2 (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            time_open DATETIME NOT NULL,
            time_close DATETIME NOT NULL,
            time_high DATETIME NOT NULL,
            time_low DATETIME NOT NULL,
            coin_name VARCHAR(100) NOT NULL,
            coin_id VARCHAR(50) NOT NULL,
            open_price DECIMAL(20, 10) NOT NULL,
            high_price DECIMAL(20, 10) NOT NULL,
            low_price DECIMAL(20, 10) NOT NULL,
            close_price DECIMAL(20, 10) NOT NULL,
            volume DECIMAL(25, 2) NOT NULL,
            market_cap DECIMAL(25, 2) NOT NULL,
            timestamp DATETIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_coin_name (coin_name),
            INDEX idx_coin_id (coin_id),
            INDEX idx_timestamp (timestamp),
            INDEX idx_time_open (time_open),
            UNIQUE KEY uk_coin_timestamp (coin_name, timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='加密货币历史价格数据表';
        """
        
        try:
            self.execute_non_query(create_table_sql)
            logger.info("coinprice2表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建coinprice2表失败: {e}")
            return False
    
    def insert_coin_data(self, data_list: List[Dict[str, Any]]) -> int:
        """
        批量插入币价数据
        
        Args:
            data_list: 数据列表
            
        Returns:
            int: 插入的行数
        """
        if not data_list:
            logger.warning("没有数据需要插入")
            return 0
        
        insert_sql = """
        INSERT IGNORE INTO coinprice2 (
            time_open, time_close, time_high, time_low, coin_name, coin_id,
            open_price, high_price, low_price, close_price, volume, market_cap, timestamp
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        params_list = []
        for data in data_list:
            params = (
                data['time_open'],
                data['time_close'],
                data['time_high'],
                data['time_low'],
                data['coin_name'],
                data['coin_id'],
                data['open_price'],
                data['high_price'],
                data['low_price'],
                data['close_price'],
                data['volume'],
                data['market_cap'],
                data['timestamp']
            )
            params_list.append(params)
        
        try:
            affected_rows = self.execute_many(insert_sql, params_list)
            logger.info(f"成功插入 {affected_rows} 条币价数据")
            return affected_rows
        except Exception as e:
            logger.error(f"插入币价数据失败: {e}")
            raise
    
    def check_table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在
        
        Args:
            table_name: 表名
            
        Returns:
            bool: 表是否存在
        """
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        
        try:
            result = self.execute_query(query, (self.config['database'], table_name))
            exists = result[0]['count'] > 0
            logger.info(f"表 {table_name} {'存在' if exists else '不存在'}")
            return exists
        except Exception as e:
            logger.error(f"检查表存在性失败: {e}")
            return False
