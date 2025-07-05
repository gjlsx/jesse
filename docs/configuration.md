# 配置说明

Jesse 有两种类型的配置需要修改：

1. **环境变量** - 包含敏感信息如密码、交易所 API 密钥等
2. **应用设置** - 通过仪表板访问的应用程序设置

让我们来详细了解这两种配置：

## 环境变量

这些配置值也称为环境变量，存储在项目内名为 `.env` 的文件中。以下是每个项目默认提供的值：

### 基础配置

```sh
# 仪表板登录密码
PASSWORD=test

# 应用程序端口
APP_PORT=9000
```

### 数据库配置

```sh
# 如果不使用 Docker，你可能想要设置为 "localhost"
POSTGRES_HOST=postgres
# POSTGRES_HOST=localhost
POSTGRES_NAME=jesse_db
POSTGRES_PORT=5432
POSTGRES_USERNAME=jesse_user
POSTGRES_PASSWORD=password
```

### Redis 配置

```sh
# 如果不使用 Docker，你可能想要设置为 "localhost"
# REDIS_HOST=localhost
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
```

### 实盘交易相关配置

> **注意**：如果你没有安装实盘交易插件，以下配置不需要关心。

#### 许可证和通知

```sh
# 在 https://jesse.trade/user/api-tokens 创建的 API 令牌
LICENSE_API_TOKEN=

# 通用通知设置
GENERAL_TELEGRAM_BOT_TOKEN=
GENERAL_TELEGRAM_BOT_CHAT_ID=
GENERAL_DISCORD_WEBHOOK=
GENERAL_SLACK_WEBHOOK=

# 仅错误通知
ERROR_TELEGRAM_BOT_TOKEN=
ERROR_TELEGRAM_BOT_CHAT_ID=
ERROR_DISCORD_WEBHOOK=
ERROR_SLACK_WEBHOOK=
```

#### 交易所 API 配置

**Bitget**
```sh
# USDT 永续合约
BITGET_USDT_PERPETUAL_API_KEY=
BITGET_USDT_PERPETUAL_API_SECRET=
BITGET_USDT_PERPETUAL_API_PASSPHRASE=
```

**Binance**
```sh
# 测试网期货
BINANCE_PERPETUAL_FUTURES_TESTNET_API_KEY=
BINANCE_PERPETUAL_FUTURES_TESTNET_API_SECRET=

# 正式期货
BINANCE_PERPETUAL_FUTURES_API_KEY=
BINANCE_PERPETUAL_FUTURES_API_SECRET=

# 现货交易
BINANCE_SPOT_API_KEY=
BINANCE_SPOT_API_SECRET=

# 美国站现货
BINANCE_US_SPOT_API_KEY=
BINANCE_US_SPOT_API_SECRET=
```

**Bybit**
```sh
# USDT 永续合约测试网
BYBIT_USDT_PERPETUAL_TESTNET_API_KEY=
BYBIT_USDT_PERPETUAL_TESTNET_API_SECRET=

# USDT 永续合约正式
BYBIT_USDT_PERPETUAL_API_KEY=
BYBIT_USDT_PERPETUAL_API_SECRET=

# USDC 永续合约测试网
BYBIT_USDC_PERPETUAL_TESTNET_API_KEY=
BYBIT_USDC_PERPETUAL_TESTNET_API_SECRET=

# USDC 永续合约正式
BYBIT_USDC_PERPETUAL_API_KEY=
BYBIT_USDC_PERPETUAL_API_SECRET=

# 现货测试网
BYBIT_SPOT_TESTNET_API_KEY=
BYBIT_SPOT_TESTNET_API_SECRET=

# 现货正式
BYBIT_SPOT_API_KEY=
BYBIT_SPOT_API_SECRET=
```

**DYDX**
```sh
# 永续合约测试网
DYDX_PERPETUAL_TESTNET_API_KEY=
DYDX_PERPETUAL_TESTNET_API_SECRET=
DYDX_PERPETUAL_TESTNET_API_PASSPHRASE=
DYDX_PERPETUAL_TESTNET_WALLET_ADDRESS=
DYDX_PERPETUAL_TESTNET_STARK_PRIVATE_KEY=

# 永续合约正式
DYDX_PERPETUAL_API_KEY=
DYDX_PERPETUAL_API_SECRET=
DYDX_PERPETUAL_API_PASSPHRASE=
DYDX_PERPETUAL_WALLET_ADDRESS=
DYDX_PERPETUAL_STARK_PRIVATE_KEY=
```

### 配置修改建议

通常，在修改 `.env` 文件之前停止应用程序，并在进行更改后重新启动它是一个好主意。

## 应用设置

在仪表板的右上角，你会看到一个齿轮图标。点击它，你会看到如下设置列表：

![settings-optimization](https://api1.jesse.trade/storage/images/docs/settings-optimization.jpg)

你可以随意更改这些设置。更改会自动保存，这就是为什么没有"保存"按钮的原因。

> **警告**：更改设置不会影响正在运行的会话。如果你有一个正在运行的会话，请停止并重新启动它以使更改生效。

注意：更改这些设置后，你不需要停止并重新启动 Jesse 本身。

## 主要配置项说明

### 1. 数据库连接
- **Docker 环境**：使用 `postgres` 作为主机名
- **本地环境**：使用 `localhost` 作为主机名
- 确保数据库服务正在运行并且凭据正确

### 2. Redis 连接
- **Docker 环境**：使用 `redis` 作为主机名
- **本地环境**：使用 `localhost` 作为主机名
- Redis 通常不需要密码（测试环境）

### 3. 端口配置
- 默认 Web 界面端口：9000
- 可以通过 `APP_PORT` 环境变量修改
- 确保选择的端口没有被其他应用占用

### 4. 密码安全
- 默认仪表板密码是 `test`
- **强烈建议**在生产环境中更改为强密码
- 密码用于保护 Web 界面访问

### 5. 交易所 API 安全
- 永远不要共享你的 API 密钥
- 为 Jesse 创建专用的 API 密钥
- 限制 API 密钥权限（只给予必要的交易权限）
- 使用测试网进行初始设置和测试

## 配置文件示例

以下是一个用于本地开发的 `.env` 文件示例：

```sh
PASSWORD=my_secure_password
APP_PORT=9000

# 本地数据库配置
POSTGRES_HOST=localhost
POSTGRES_NAME=jessedb
POSTGRES_PORT=5432
POSTGRES_USERNAME=wind
POSTGRES_PASSWORD=your_db_password

# 本地 Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 实盘交易（可选）
LICENSE_API_TOKEN=your_license_token
BINANCE_PERPETUAL_FUTURES_TESTNET_API_KEY=your_test_api_key
BINANCE_PERPETUAL_FUTURES_TESTNET_API_SECRET=your_test_api_secret
```

## 故障排除

### 1. 数据库连接失败
- 检查 PostgreSQL 服务是否运行
- 验证数据库凭据
- 确认数据库和用户是否存在

### 2. Redis 连接失败
- 检查 Redis 服务是否运行
- 验证主机名和端口
- 检查防火墙设置

### 3. 无法访问 Web 界面
- 确认端口配置正确
- 检查是否有端口冲突
- 验证密码设置

### 4. API 密钥问题
- 检查密钥格式是否正确
- 验证密钥权限设置
- 确认交易所账户状态

## 最佳实践

1. **备份配置**：定期备份你的 `.env` 文件
2. **版本控制**：不要将 `.env` 文件提交到版本控制系统
3. **环境分离**：为开发、测试和生产使用不同的配置
4. **定期更新**：定期更换 API 密钥和密码
5. **最小权限**：只给予 API 密钥必要的权限
