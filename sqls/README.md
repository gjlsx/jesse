# SQL 测试脚本目录

此目录包含所有与数据库相关的 SQL 脚本和 Python 测试文件。

## 📁 文件说明

### SQL 脚本
- **`test_postgresql.sql`** - PostgreSQL 中文测试脚本
  - 包含完整的数据库操作测试（增删改查）
  - 支持中文字符测试
  - 包含索引创建和表结构查询

- **`test_postgresql_english.sql`** - PostgreSQL 英文测试脚本
  - 英文版本的数据库操作测试
  - 避免编码问题的简化版本

### Python 测试脚本
- **`test_postgresql.py`** - 完整的 PostgreSQL Python 测试
  - 使用 psycopg2 连接数据库
  - 详细的测试输出和错误处理
  - 支持中文字符显示

- **`test_postgresql_simple.py`** - 简化版 PostgreSQL 测试
  - 快速连接和基本操作验证
  - 轻量级测试选项
  - 现已配置为测试 jesse_db 数据库

- **`test_jesse_db.py`** - Jesse 专用数据库测试
  - 专门测试 jesse_db 数据库
  - 包含 Jesse 项目相关的测试数据
  - 完整的数据库操作验证

### 其他文件
- **`requirements_postgresql.txt`** - Python 依赖包清单
- **`redis_test.py`** - Redis 测试脚本（如果需要）

## 🚀 使用方法

### 运行 SQL 测试
```bash
# 切换到 PostgreSQL bin 目录
cd d:\tools\pgsql\bin

# 运行中文测试脚本
psql.exe -U wind -d testdb -f "d:\work\aiwork\jesse\sqls\test_postgresql.sql"

# 运行英文测试脚本  
psql.exe -U wind -d testdb -f "d:\work\aiwork\jesse\sqls\test_postgresql_english.sql"

# 测试 jesse_db 数据库
psql.exe -U wind -d jesse_db -f "d:\work\aiwork\jesse\sqls\test_postgresql.sql"
```

### 运行 Python 测试
```bash
# 切换到项目目录
cd d:\work\aiwork\jesse\sqls

# 运行完整测试
python test_postgresql.py

# 运行简化测试（jesse_db）
python test_postgresql_simple.py

# 运行 Jesse 专用测试
python test_jesse_db.py
```

## 📊 数据库配置

### testdb 数据库
- **用途**: 通用测试数据库
- **表**: employees (员工测试数据)

### jesse_db 数据库  
- **用途**: Jesse 项目专用数据库
- **表**: test_table (项目测试数据)

### 连接参数
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'testdb',  # 或 'jesse_db'
    'user': 'wind',
    'password': 'gj'
}
```

## ⚠️ 注意事项

1. 确保 PostgreSQL 服务正在运行
2. 所有脚本都支持 UTF-8 编码
3. Python 脚本需要安装 psycopg2-binary 依赖
4. SQL 脚本可以直接在 psql 中执行

## 📈 测试覆盖

- ✅ 数据库连接测试
- ✅ 表创建和删除
- ✅ 数据插入和查询
- ✅ 数据更新和删除
- ✅ 索引创建
- ✅ 聚合查询
- ✅ 中文字符支持
- ✅ 事务处理
- ✅ 错误处理
