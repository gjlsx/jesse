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
    'database': 'jessedb',  # 修正为实际存在的数据库名
    'user': 'wind',
    'password': 'gj'
}

# 连接到 postgres 默认数据库的配置（用于诊断）
ADMIN_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',  # 连接到默认数据库
    'user': 'wind',
    'password': 'gj'
}

def diagnose_database():
    """诊断数据库连接问题"""
    print("🔍 开始诊断数据库连接问题...")
    
    # 1. 测试连接到默认 postgres 数据库
    try:
        print("\n1️⃣ 测试连接到 postgres 默认数据库...")
        conn = psycopg2.connect(**ADMIN_DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ 成功连接到 postgres 数据库")
        
        # 2. 查询所有数据库
        print("\n2️⃣ 查询现有数据库:")
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
        databases = cursor.fetchall()
        
        for db in databases:
            if db[0] == 'jessedb':
                print(f"✅ {db[0]} (目标数据库)")
            else:
                print(f"📄 {db[0]}")
        
        # 3. 检查 jessedb 是否存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'jessedb';")
        jesse_db_exists = cursor.fetchone()
        
        if jesse_db_exists:
            print("\n✅ jessedb 数据库存在")
            
            # 4. 检查用户权限
            print("\n3️⃣ 检查用户 'wind' 的权限:")
            cursor.execute("""
                SELECT r.rolname, r.rolsuper, r.rolcreaterole, r.rolcreatedb, r.rolcanlogin
                FROM pg_roles r 
                WHERE r.rolname = 'wind';
            """)
            user_info = cursor.fetchone()
            
            if user_info:
                print(f"用户: {user_info[0]}")
                print(f"超级用户: {user_info[1]}")
                print(f"可创建角色: {user_info[2]}")
                print(f"可创建数据库: {user_info[3]}")
                print(f"可登录: {user_info[4]}")
            else:
                print("❌ 用户 'wind' 不存在")
        else:
            print("\n❌ jessedb 数据库不存在")
            
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ 连接 postgres 数据库失败: {e}")
        return False
    
    # 5. 尝试直接连接 jessedb
    print("\n4️⃣ 尝试直接连接 jessedb 数据库...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ 成功连接到 jessedb 数据库")
        
        # 查询版本信息
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"数据库版本: {version[:80]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ 连接 jessedb 失败: {e}")
        print(f"错误代码: {e.pgcode if hasattr(e, 'pgcode') else '未知'}")
        return False

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
        
        print("\n📋 检查 jessedb 中的 test_table 数据...")
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
    
    # 首先诊断数据库问题
    if not diagnose_database():
        print("\n❌ 数据库诊断发现问题，请查看上述信息")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("开始运行功能测试")
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
