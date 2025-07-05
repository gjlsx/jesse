#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL 数据库测试脚本
连接到本地 PostgreSQL 数据库并执行基础操作测试
"""

import psycopg2
from psycopg2 import sql
import sys
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'testdb',
    'user': 'wind',
    'password': 'gj'
}

def connect_to_db():
    """连接到 PostgreSQL 数据库"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        print("✅ 数据库连接成功!")
        return conn
    except psycopg2.Error as e:
        print(f"❌ 数据库连接失败: {e}")
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
                print(" | ".join(f"{col:>12}" for col in colnames))
                print("-" * (len(colnames) * 15))
                
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
                    print(" | ".join(f"{item:>12}" for item in formatted_row))
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

def run_postgresql_tests():
    """执行 PostgreSQL 测试"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        print("\n🚀 开始执行 PostgreSQL 基础操作测试...")
        
        # 1. 删除已存在的表
        execute_query(cursor, "DROP TABLE IF EXISTS employees;", "删除已存在的表")
        
        # 2. 创建测试表
        create_table_sql = """
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE,
            department VARCHAR(50),
            salary DECIMAL(10,2),
            hire_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        execute_query(cursor, create_table_sql, "创建 employees 表")
        
        # 3. 插入测试数据
        insert_sql = """
        INSERT INTO employees (name, email, department, salary, hire_date) VALUES
        ('张三', 'zhangsan@example.com', 'IT', 8000.00, '2023-01-15'),
        ('李四', 'lisi@example.com', 'HR', 6500.00, '2023-02-20'),
        ('王五', 'wangwu@example.com', 'Finance', 7200.00, '2023-03-10'),
        ('赵六', 'zhaoliu@example.com', 'IT', 9500.00, '2023-04-05'),
        ('陈七', 'chenqi@example.com', 'Marketing', 7800.00, '2023-05-12');
        """
        execute_query(cursor, insert_sql, "插入测试数据")
        
        # 提交事务
        conn.commit()
        
        # 4. 基础查询测试
        execute_query(cursor, "SELECT * FROM employees;", "所有员工信息")
        
        execute_query(cursor, 
                     "SELECT name, email, salary FROM employees WHERE department = 'IT';", 
                     "IT部门员工")
        
        execute_query(cursor, 
                     "SELECT name, department, salary FROM employees ORDER BY salary DESC;", 
                     "按薪资排序")
        
        # 5. 统计查询
        stats_sql = """
        SELECT 
            department,
            COUNT(*) as employee_count,
            ROUND(AVG(salary), 2) as avg_salary,
            MAX(salary) as max_salary,
            MIN(salary) as min_salary
        FROM employees 
        GROUP BY department;
        """
        execute_query(cursor, stats_sql, "部门统计信息")
        
        # 6. 更新操作测试
        execute_query(cursor, 
                     "SELECT name, salary FROM employees WHERE name = '张三';", 
                     "更新前 - 张三的薪资")
        
        execute_query(cursor, 
                     "UPDATE employees SET salary = 8500.00 WHERE name = '张三';", 
                     "更新张三的薪资")
        
        execute_query(cursor, 
                     "SELECT name, salary FROM employees WHERE name = '张三';", 
                     "更新后 - 张三的薪资")
        
        # 7. 创建索引
        execute_query(cursor, "CREATE INDEX idx_department ON employees(department);", "创建部门索引")
        execute_query(cursor, "CREATE INDEX idx_email ON employees(email);", "创建邮箱索引")
        
        # 8. 查看表结构
        table_structure_sql = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = 'employees'
        ORDER BY ordinal_position;
        """
        execute_query(cursor, table_structure_sql, "表结构信息")
        
        # 9. 最终验证
        execute_query(cursor, "SELECT COUNT(*) as total_records FROM employees;", "记录总数")
        
        execute_query(cursor, 
                     "SELECT id, name, department, salary, hire_date FROM employees ORDER BY id;", 
                     "最终员工列表")
        
        # 提交所有更改
        conn.commit()
        
        print("\n🎉 所有测试执行完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试执行过程中发生错误: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()
        print("📝 数据库连接已关闭")

def test_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"📋 PostgreSQL 版本: {version}")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 版本查询失败: {e}")
            return False
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("PostgreSQL 数据库测试程序")
    print("=" * 60)
    
    # 首先测试连接
    if test_connection():
        print("\n" + "=" * 60)
        # 运行完整测试
        success = run_postgresql_tests()
        
        if success:
            print("\n✅ 所有测试成功完成!")
            sys.exit(0)
        else:
            print("\n❌ 测试过程中出现错误!")
            sys.exit(1)
    else:
        print("\n❌ 无法连接到数据库，请检查:")
        print("   1. PostgreSQL 服务是否正在运行")
        print("   2. 数据库配置是否正确")
        print("   3. 是否安装了 psycopg2 包")
        print("\n安装 psycopg2: pip install psycopg2-binary")
        sys.exit(1)
