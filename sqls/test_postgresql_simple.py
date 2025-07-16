#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版 PostgreSQL 测试脚本
快速验证数据库连接和基本操作
"""

import psycopg2
import sys

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'jessedb',  # 改为测试 jesse_db
    'user': 'wind',
    'password': 'gj'
}

def quick_test():
    """快速测试数据库连接和基本操作"""
    try:
        # 连接数据库
        print("🔗 连接数据库...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        cursor = conn.cursor()
        
        # 测试查询
        print("📊 查询数据库版本...")
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL: {version}")
        
        # 测试创建临时表
        print("📝 创建临时测试表...")
        cursor.execute("""
            CREATE TEMP TABLE temp_test (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                test_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 插入测试数据
        print("📥 插入测试数据...")
        cursor.execute("""
            INSERT INTO temp_test (name, test_data) VALUES 
            ('Jesse测试1', 'Jesse数据库连接测试'), 
            ('Jesse测试2', '中文字符编码测试'), 
            ('Jesse测试3', 'PostgreSQL功能验证');
        """)
        
        # 查询测试数据
        print("📤 查询测试数据...")
        cursor.execute("SELECT id, name, test_data, created_at FROM temp_test;")
        results = cursor.fetchall()
        
        print("\n查询结果:")
        print("ID | 名称        | 测试数据              | 创建时间")
        print("-" * 60)
        for row in results:
            print(f"{row[0]:2} | {row[1]:10} | {row[2]:20} | {row[3]}")
        
        # 提交事务
        conn.commit()
        print(f"\n✅ 测试成功！共 {len(results)} 条记录")
        
        # 清理
        cursor.close()
        conn.close()
        print("🔚 连接已关闭")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ 数据库错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def check_test_table():
    """检查 test_table 表的数据"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        cursor = conn.cursor()
        
        print("\n📋 检查 jesse_db 中的 test_table 数据...")
        cursor.execute("""
            SELECT name, LEFT(description, 30) as desc_preview, created_at 
            FROM test_table 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        
        results = cursor.fetchall()
        if results:
            print("\ntest_table 中的数据:")
            print("名称        | 描述预览                      | 创建时间")
            print("-" * 70)
            for row in results:
                print(f"{row[0]:10} | {row[1]:28} | {row[2]}")
        else:
            print("❓ test_table 表为空或不存在")
            
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ 查询 test_table 表失败: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Jesse DB PostgreSQL 快速测试")
    print("=" * 50)
    
    # 运行快速测试
    success = quick_test()
    
    if success:
        # 如果基本测试成功，尝试查询之前的测试数据
        check_test_table()
        print("\n🎉 所有测试完成!")
        sys.exit(0)
    else:
        print(f"\n❌ 测试失败，请检查:")
        print("   1. PostgreSQL 服务是否运行")
        print("   2. 数据库配置是否正确")
        print("   3. 网络连接是否正常")
        sys.exit(1)
