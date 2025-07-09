# CSV历史数据导入指南

## 📋 概述

本文档记录了将CSV历史价格数据导入MySQL数据库的完整过程，包括数据库表设计、Python程序实现和导入结果。

## 🎯 项目背景

- **数据源**: CoinMarketCap历史价格数据
- **数据格式**: CSV文件（分号分隔）
- **目标数据库**: MySQL (阿里云PolarDB)
- **数据表**: `coinprice2`
- **币种数量**: 12个主流加密货币

## 🗄️ 数据库配置

### 连接信息
```
服务器: zzb2020.mysql.polardb.rds.aliyuncs.com
端口: 3306
数据库: demt
用户: demt_write
密码: [通过环境变量DB_PASSWORD设置]
字符集: utf8mb4
```

### 环境变量配置
为了安全起见，数据库密码通过环境变量配置：

#### 方法1：直接设置环境变量
```bash
# Windows
set DB_PASSWORD=your_password_here

# Linux/Mac
export DB_PASSWORD=your_password_here
```

#### 方法2：使用.env文件（推荐）
```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，填入实际密码
# DB_PASSWORD=your_actual_password_here
```

支持的环境变量：
- `DB_HOST` - 数据库主机地址（默认：zzb2020.mysql.polardb.rds.aliyuncs.com）
- `DB_PORT` - 数据库端口（默认：3306）
- `DB_USER` - 数据库用户名（默认：demt_write）
- `DB_PASSWORD` - 数据库密码（**必需**）
- `DB_NAME` - 数据库名称（默认：demt）
- `DB_CHARSET` - 字符集（默认：utf8mb4）

⚠️ **安全提醒**：
- `.env`文件已添加到`.gitignore`中，不会被提交到版本控制
- 请勿在代码或文档中直接写入真实密码

### 表结构设计

```sql
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
```

## 📁 数据文件

### CSV文件列表（12个）
```
storage/csv/
├── BNB_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Bitcoin_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Cardano_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Chainlink_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Dogecoin_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Ethereum_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Hyperliquid_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Solana_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Stellar_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── Sui_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
├── TRON_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
└── XRP_7_10_2024-7_10_2025_historical_data_coinmarketcap.csv
```

### CSV数据格式
```
timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;timestamp
"2025-07-08T00:00:00.000Z";"2025-07-08T23:59:59.999Z";"2025-07-08T00:46:00.000Z";"2025-07-08T16:19:00.000Z";"2781";661.0180847877;662.4974202565;657.5650920717;660.7628950885;1517607541.52;93091616770.26;"2025-07-08T23:59:59.999Z"
```

## 🔧 技术实现

### 核心文件结构
```
├── database_manager.py      # 数据库操作模块
├── test_import_csv.py      # 测试导入程序（2条数据）
└── import_all_csv.py       # 全量导入程序
```

### 关键技术特点

1. **模块化设计**
   - `DatabaseManager`类封装所有数据库操作
   - 支持连接池管理和事务处理
   - 提供批量插入和错误处理

2. **数据处理优化**
   - 自动处理CSV文件的BOM问题
   - 分批处理（每批100条）提高性能
   - 使用`INSERT IGNORE`避免重复数据

3. **错误处理机制**
   - 完善的异常捕获和日志记录
   - 文件级别的错误隔离
   - 详细的进度监控和统计

## 📊 导入结果

### 执行时间
- **开始时间**: 2025-07-10 02:51:00
- **结束时间**: 2025-07-10 02:51:10
- **总耗时**: 9.30秒

### 数据统计

| 币种 | 数据条数 | 时间范围 | 状态 |
|------|----------|----------|------|
| BNB | 362条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Bitcoin | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Cardano | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Chainlink | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Dogecoin | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Ethereum | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Hyperliquid | 221条 | 2024-11-14 ~ 2025-07-08 | ✅ |
| Solana | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Stellar | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| Sui | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| TRON | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |
| XRP | 364条 | 2024-07-10 ~ 2025-07-08 | ✅ |

### 总计
- **总文件数**: 12个
- **成功处理**: 12个文件（100%成功率）
- **失败文件**: 0个
- **总插入数据**: **4,223条**历史价格数据

## 🚀 使用方法

### 1. 环境准备
```bash
# 安装依赖
pip install pymysql

# 设置数据库密码环境变量
# Windows
set DB_PASSWORD=your_actual_password

# Linux/Mac
export DB_PASSWORD=your_actual_password

# 确保CSV文件在正确位置
ls storage/csv/*historical*.csv
```

### 2. 测试导入（2条数据）
```bash
python test_import_csv.py
```

### 3. 全量导入
```bash
python import_all_csv.py
```

### 4. 验证数据
```sql
-- 查看总数据量
SELECT COUNT(*) FROM coinprice2;

-- 查看各币种数据量
SELECT coin_name, COUNT(*) as count 
FROM coinprice2 
GROUP BY coin_name 
ORDER BY count DESC;

-- 查看时间范围
SELECT coin_name, 
       MIN(timestamp) as start_date, 
       MAX(timestamp) as end_date 
FROM coinprice2 
GROUP BY coin_name;
```

## 📝 注意事项

1. **数据完整性**
   - 使用唯一约束`uk_coin_timestamp`防止重复数据
   - Hyperliquid数据较少（221条）是因为上市时间较晚

2. **性能优化**
   - 分批插入避免内存溢出
   - 创建适当索引提高查询性能
   - 使用`INSERT IGNORE`提高插入效率

3. **错误处理**
   - 程序具有完善的错误恢复机制
   - 单个文件失败不影响其他文件处理
   - 详细的日志记录便于问题排查

## 🔄 后续维护

### 数据更新
- 可重复运行导入程序更新数据
- 新数据会自动跳过已存在的记录
- 建议定期备份数据库

### 扩展功能
- 可添加更多币种的CSV文件
- 支持不同时间格式的数据源
- 可扩展为实时数据导入

## 📚 相关文档

- [Jesse交易框架文档](README.md)
- [数据库配置指南](configuration.md)
- [策略开发指南](strategies.md)

---

**创建时间**: 2025-07-10  
**最后更新**: 2025-07-10  
**版本**: 1.0
