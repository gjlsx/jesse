#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jesse DB 测试脚本
测试 jesse_db 数据库的连接和基本操作
"""

import psycopg2
from psycopg2 import sql
import sys
from datetime import datetime

# Jesse 数据库连接配置
JESSE_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'jesse_db',  # 使用 jesse_db 数据库
    'user': 'wind',
    'password': 'gj'
}

def connect_to_jesse_db():
    """连接到 Jesse PostgreSQL 数据库"""
    try:
        conn = psycopg2.connect(**JESSE_DB_CONFIG)
        conn.set_client_encoding('UTF8')
        print("✅ Jesse 数据库连接成功!")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Jesse 数据库连接失败: {e}")
        return None

def execute_query(cursor, query, description=""):
    """执行查询并打印结果"""
    try:
        cursor.execute(query)
        
        # 如果是 SELECT 查询，获取结果
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description] if cursor.description else []
            
            if description:
                print(f"\n=== {description} ===")
            
            if colnames and results:
                # 打印列名
                print(" | ".join(f"{col:>15}" for col in colnames))
                print("-" * (len(colnames) * 18))
                
                # 打印数据行
                for row in results:
                    formatted_row = []
                    for item in row:
                        if item is None:
                            formatted_row.append("NULL")
                        elif isinstance(item, datetime):
                            formatted_row.append(item.strftime('%Y-%m-%d %H:%M:%S'))
                        else:
                            formatted_row.append(str(item))
                    print(" | ".join(f"{item:>15}" for item in formatted_row))
                print(f"({len(results)} 行记录)")
            else:
                print("查询无结果")
        else:
            # 对于非 SELECT 查询，显示影响的行数
            if cursor.rowcount >= 0:
                print(f"✅ {description}: {cursor.rowcount} 行受影响")
            else:
                print(f"✅ {description}: 执行成功")
                
    except psycopg2.Error as e:
        print(f"❌ 查询执行失败: {e}")

def test_jesse_db():
    """测试 Jesse 数据库操作"""
    conn = connect_to_jesse_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        print("\n🚀 开始测试 Jesse 数据库...")
        
        # 1. 查看数据库信息
        execute_query(cursor, "SELECT current_database(), version();", "数据库信息")
        
        # 2. 查看现有表
        execute_query(cursor, 
                     "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';", 
                     "现有表列表")
        
        # 3. 在 test_table 中插入测试数据
        insert_sql = """
        INSERT INTO test_table (name, description) VALUES
        ('Jesse 测试1', '这是第一个测试记录'),
        ('Jesse 测试2', '这是第二个测试记录'),
        ('交易系统测试', 'Jesse 交易系统数据库测试'),
        ('数据库连接测试', 'PostgreSQL UTF-8 编码测试'),
        ('中文字符测试', '测试中文字符的存储和显示');
        """
        execute_query(cursor, insert_sql, "插入测试数据")
        
        # 提交事务
        conn.commit()
        
        # 4. 查询所有测试数据
        execute_query(cursor, "SELECT * FROM test_table ORDER BY id;", "所有测试数据")
        
        # 5. 条件查询
        execute_query(cursor, 
                     "SELECT name, description FROM test_table WHERE name LIKE '%测试%';", 
                     "包含'测试'的记录")
        
        # 6. 统计查询
        execute_query(cursor, "SELECT COUNT(*) as total_records FROM test_table;", "记录总数")
        
        # 7. 更新测试
        execute_query(cursor, 
                     "UPDATE test_table SET description = '已更新的描述' WHERE name = 'Jesse 测试1';", 
                     "更新记录")
        
        execute_query(cursor, 
                     "SELECT name, description FROM test_table WHERE name = 'Jesse 测试1';", 
                     "更新后的记录")
        
        # 8. 测试时间戳
        execute_query(cursor, 
                     "SELECT name, created_at FROM test_table ORDER BY created_at DESC LIMIT 3;", 
                     "最新的3条记录（按时间排序）")
        
        # 9. 删除测试（删除并恢复）
        execute_query(cursor, 
                     "DELETE FROM test_table WHERE name = 'Jesse 测试2';", 
                     "删除测试记录")
        
        execute_query(cursor, "SELECT COUNT(*) as total_records FROM test_table;", "删除后记录数")
        
        # 恢复删除的记录
        execute_query(cursor, 
                     "INSERT INTO test_table (name, description) VALUES ('Jesse 测试2', '这是恢复的测试记录');", 
                     "恢复删除的记录")
        
        # 10. 最终验证
        execute_query(cursor, 
                     "SELECT id, name, LEFT(description, 20) as desc_preview, created_at FROM test_table ORDER BY id;", 
                     "最终数据验证")
        
        # 提交所有更改
        conn.commit()
        
        print("\n🎉 Jesse 数据库测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试执行过程中发生错误: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()
        print("📝 Jesse 数据库连接已关闭")

def test_connection():
    """测试 Jesse 数据库连接"""
    print("🔍 测试 Jesse 数据库连接...")
    conn = connect_to_jesse_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
            db_info = cursor.fetchone()
            print(f"📋 数据库: {db_info[0]}")
            print(f"👤 用户: {db_info[1]}")
            print(f"🌐 服务器: {db_info[2] if db_info[2] else 'localhost'}:{db_info[3]}")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Jesse 数据库测试程序")
    print("=" * 60)
    
    # 首先测试连接
    if test_connection():
        print("\n" + "=" * 60)
        # 运行完整测试
        success = test_jesse_db()
        
        if success:
            print("\n✅ Jesse 数据库所有测试成功完成!")
            sys.exit(0)
        else:
            print("\n❌ Jesse 数据库测试过程中出现错误!")
            sys.exit(1)
    else:
        print("\n❌ 无法连接到 Jesse 数据库，请检查:")
        print("   1. PostgreSQL 服务是否正在运行")
        print("   2. jesse_db 数据库是否存在")
        print("   3. 数据库配置是否正确")
        print("   4. 是否安装了 psycopg2 包")
        sys.exit(1)
