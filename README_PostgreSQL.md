# PostgreSQL Python 测试说明

## 文件说明

### 1. test_postgresql.py
完整的 PostgreSQL 测试脚本，包含所有 SQL 操作测试：
- 创建表
- 插入数据
- 查询数据
- 更新数据
- 创建索引
- 查看表结构
- 统计查询

### 2. test_postgresql_simple.py
简化版测试脚本，用于快速验证数据库连接和基本操作。

### 3. test_postgresql.sql
原始 SQL 测试脚本，可以直接在 psql 中执行。

## 数据库配置

- **主机**: localhost
- **端口**: 5432
- **数据库**: testdb
- **用户名**: wind
- **密码**: gj
- **编码**: UTF-8

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements_postgresql.txt
```

### 2. 启动 PostgreSQL 服务
```bash
# 使用提供的批处理文件
d:\tools\pgsql\start_postgresql.bat

# 或手动启动
cd d:\tools\pgsql\bin
postgres.exe -D "d:\tools\pgsql\data"
```

### 3. 运行 Python 测试

#### 完整测试
```bash
python test_postgresql.py
```

#### 快速测试
```bash
python test_postgresql_simple.py
```

### 4. 直接运行 SQL 测试
```bash
cd d:\tools\pgsql\bin
psql.exe -U wind -d testdb -f "test_postgresql.sql"
```

## 测试内容

### 完整测试包含：
1. ✅ 数据库连接测试
2. ✅ 表创建和删除
3. ✅ 数据插入（支持中文）
4. ✅ 基础查询（SELECT）
5. ✅ 条件查询（WHERE）
6. ✅ 排序查询（ORDER BY）
7. ✅ 聚合查询（COUNT, AVG, MAX, MIN）
8. ✅ 分组查询（GROUP BY）
9. ✅ 数据更新（UPDATE）
10. ✅ 索引创建
11. ✅ 表结构查询

### 快速测试包含：
1. ✅ 数据库连接验证
2. ✅ 版本信息获取
3. ✅ 临时表操作
4. ✅ 基础增删改查
5. ✅ 现有数据查询

## 输出示例

完整测试将显示详细的执行过程和结果，包括：
- 表格化的查询结果
- 操作影响的行数
- 错误信息（如有）
- 执行状态提示

## 故障排除

### 1. 连接失败
- 检查 PostgreSQL 服务是否运行
- 验证数据库配置信息
- 确认防火墙设置

### 2. 编码问题
- 确保数据库使用 UTF-8 编码
- 检查客户端编码设置

### 3. 依赖包问题
```bash
pip install psycopg2-binary
```

## 注意事项

1. 测试脚本会自动创建和删除测试表
2. 所有操作都在 `testdb` 数据库中进行
3. 中文字符需要 UTF-8 编码支持
4. 请确保 PostgreSQL 服务正在运行
