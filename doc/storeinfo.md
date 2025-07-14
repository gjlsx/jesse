# Jesse 存储和缓存系统详解

## 📋 目录
- [概述](#概述)
- [全局状态存储 (Store)](#全局状态存储-store)
- [文件缓存系统 (Cache)](#文件缓存系统-cache)
- [Redis 消息系统](#redis-消息系统)
- [配置和环境变量](#配置和环境变量)
- [实际应用示例](#实际应用示例)
- [总结](#总结)

## 概述

Jesse 交易框架采用**多层存储架构**来管理不同类型的数据和状态：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  全局状态存储    │    │   文件缓存系统   │    │  Redis消息系统  │
│     Store       │    │     Cache       │    │     Redis       │
│   (运行时状态)   │    │   (持久化缓存)   │    │   (实时通信)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 全局状态存储 (Store)

### 架构设计

Jesse 使用**全局单例模式**的 `Store` 类来管理常驻内存变量：

```python
# jesse/store/__init__.py
class StoreClass:
    # 类级别属性 - 常驻内存的核心状态
    app = AppState()              # 应用状态
    orders = OrdersState()        # 订单状态  
    completed_trades = ClosedTrades()  # 完成交易
    logs = LogsState()            # 日志状态
    exchanges = ExchangesState()  # 交易所状态
    candles = CandlesState()      # K线数据状态
    positions = PositionsState()  # 持仓状态
    tickers = TickersState()      # 行情数据
    trades = TradesState()        # 交易状态
    orderbooks = OrderbookState() # 订单簿状态

    def __init__(self) -> None:
        self.vars = {}  # 动态变量存储

    def reset(self, force_install_routes: bool = False) -> None:
        """重置所有状态"""
        if not jh.is_unit_testing() or force_install_routes:
            install_routes()

        self.app = AppState()
        self.orders = OrdersState()
        self.completed_trades = ClosedTrades()
        # ... 重置其他状态

# 全局单例实例
store = StoreClass()
```

### 状态访问示例

```python
# 在策略中访问全局状态
from jesse.store import store

class MyStrategy(Strategy):
    def should_long(self):
        # 获取当前持仓
        current_position = store.positions.get_position(
            self.exchange, self.symbol
        )
        
        # 获取当前价格
        current_candle = store.candles.get_current_candle(
            self.exchange, self.symbol, self.timeframe
        )
        
        # 获取订单状态
        pending_orders = store.orders.get_orders(
            self.exchange, self.symbol
        )
        
        return trading_logic_here
```

### 特点

- ✅ **进程级全局单例** - 整个Jesse进程共享同一个store实例
- ✅ **分类状态管理** - 不同类型的数据分别管理
- ✅ **内存常驻** - 进程运行期间始终在内存中
- ✅ **线程安全** - 支持多线程访问

## 文件缓存系统 (Cache)

### 缓存架构

Jesse 实现了基于文件的持久化缓存系统，采用**两层存储结构**：

```python
# jesse/services/cache.py
class Cache:
    def __init__(self, path: str) -> None:
        self.path = path
        self.driver = jh.get_config('env.caching.driver', 'pickle')
        
        if self.driver == 'pickle':
            os.makedirs(path, exist_ok=True)
            
            # 加载缓存索引数据库
            if os.path.isfile(f"{self.path}cache_database.pickle"):
                with open(f"{self.path}cache_database.pickle", 'rb') as f:
                    try:
                        self.db = pickle.load(f)
                    except (EOFError, pickle.UnpicklingError, UnicodeDecodeError):
                        self.db = {}
            else:
                self.db = {}
```

### 缓存存储结构

#### 1. 缓存索引数据库 (`cache_database.pickle`)
```python
self.db = {
    'BTC-USDT_RSI_14': {
        'expire_seconds': 3600,
        'expire_at': 1625825400.0,
        'path': 'storage/temp/BTC-USDT_RSI_14.pickle'
    },
    'ETH-USDT_MA_20': {
        'expire_seconds': 7200,
        'expire_at': 1625829000.0,
        'path': 'storage/temp/ETH-USDT_MA_20.pickle'
    }
}
```

#### 2. 实际数据文件
- `storage/temp/BTC-USDT_RSI_14.pickle` - 存储实际的 RSI 数据
- `storage/temp/ETH-USDT_MA_20.pickle` - 存储实际的 MA 数据

### 缓存操作方法

#### 设置缓存
```python
def set_value(self, key: str, data: Any, expire_seconds: int = 60 * 60) -> None:
    if self.driver is None:
        return

    # 添加记录到数据库
    expire_at = None if expire_seconds is None else time() + expire_seconds
    data_path = f"{self.path}{key}.pickle"
    self.db[key] = {
        'expire_seconds': expire_seconds,
        'expire_at': expire_at,
        'path': data_path,
    }
    self._update_db()

    # 存储文件
    with open(data_path, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
```

#### 获取缓存
```python
def get_value(self, key: str) -> Any:
    if self.driver is None:
        raise ValueError('Caching driver is not set.')

    try:
        item = self.db[key]
    except KeyError:
        return False

    # 检查是否过期
    if item['expire_at'] is not None and time() > item['expire_at']:
        # 清理过期缓存
        try:
            os.remove(item['path'])
        except FileNotFoundError:
            pass
        del self.db[key]
        self._update_db()
        return False

    # 检查文件是否存在
    if not os.path.exists(item['path']):
        del self.db[key]
        self._update_db()
        return False

    # 续期缓存
    if item['expire_at'] is not None:
        item['expire_at'] = time() + item['expire_seconds']
        self._update_db()

    # 读取缓存数据
    try:
        with open(item['path'], 'rb') as f:
            cache_value = pickle.load(f)
    except (EOFError, pickle.UnpicklingError, FileNotFoundError):
        # 清理损坏的缓存
        try:
            os.remove(item['path'])
        except FileNotFoundError:
            pass
        del self.db[key]
        self._update_db()
        return False

    return cache_value
```

#### 清空缓存
```python
def flush(self) -> None:
    if self.driver is None:
        return

    keys_to_remove = list(self.db.keys())
    
    for key in keys_to_remove:
        item = self.db[key]
        try:
            os.remove(item['path'])
        except FileNotFoundError:
            pass
        del self.db[key]
    
    self._update_db()
```

### 缓存使用示例

```python
from jesse.services.cache import cache

# 缓存技术指标
def calculate_rsi_with_cache(symbol, period=14):
    cache_key = f"{symbol}_RSI_{period}"
    
    # 尝试从缓存获取
    cached_rsi = cache.get_value(cache_key)
    if cached_rsi is not False:
        return cached_rsi
    
    # 计算RSI
    rsi_values = ta.rsi(get_candles(symbol), period)
    
    # 缓存结果（1小时过期）
    cache.set_value(cache_key, rsi_values, expire_seconds=3600)
    
    return rsi_values

# 缓存历史数据
def get_historical_data_cached(symbol, timeframe, days=30):
    cache_key = f"history_{symbol}_{timeframe}_{days}d"
    
    cached_data = cache.get_value(cache_key)
    if cached_data is not False:
        return cached_data
    
    # 从数据库查询
    historical_data = fetch_from_database(symbol, timeframe, days)
    
    # 缓存2小时
    cache.set_value(cache_key, historical_data, expire_seconds=7200)
    
    return historical_data
```

## Redis 消息系统

### Redis 架构

Jesse 使用 Redis 作为**消息发布/订阅系统**，实现实时通信：

```python
# jesse/services/redis.py
async def init_redis():
    return await aioredis.create_redis_pool(
        address=(ENV_VALUES['REDIS_HOST'], ENV_VALUES['REDIS_PORT']),
        password=ENV_VALUES['REDIS_PASSWORD'] or None,
        db=int(ENV_VALUES.get('REDIS_DB') or 0),
    )

# 全局Redis连接
async_redis = asyncio.run(init_redis())
sync_redis = redis.Redis(
    host=ENV_VALUES['REDIS_HOST'], 
    port=ENV_VALUES['REDIS_PORT'], 
    db=int(ENV_VALUES.get('REDIS_DB') or 0),
    password=ENV_VALUES['REDIS_PASSWORD'] if ENV_VALUES['REDIS_PASSWORD'] else None
)
```

### 消息发布

```python
def sync_publish(event: str, msg, compression: bool = False):
    if compression:
        msg = jh.gzip_compress(msg)
        msg = base64.b64encode(msg).decode('utf-8')

    sync_redis.publish(
        f"{ENV_VALUES['APP_PORT']}:channel:1", json.dumps({
            'id': os.getpid(),
            'event': f'{jh.app_mode()}.{event}',
            'is_compressed': compression,
            'data': msg
        }, ignore_nan=True, cls=NpEncoder)
    )

async def async_publish(event: str, msg, compression: bool = False):
    # 异步版本
    await async_redis.publish(channel, message)
```

### WebSocket 连接管理

```python
# jesse/services/ws_manager.py
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.is_subscribed = False
        
    async def start_redis_listener(self, channel_pattern):
        if not self.is_subscribed:
            self.redis_subscriber, = await async_redis.psubscribe(channel_pattern)
            self.is_subscribed = True
            self.reader_task = asyncio.create_task(self._redis_listener(self.redis_subscriber))
            
    async def _redis_listener(self, channel):
        try:
            async for ch, message in channel.iter():
                message_dict = json.loads(message)
                await self.broadcast(message_dict)
        except Exception as e:
            print(f"Redis listener error: {str(e)}")
```

### 实时日志推送

```python
# jesse/services/logger.py
def info(msg: str, send_notification=False, webhook=None) -> None:
    log_dict = {
        'id': jh.generate_unique_id(),
        'session_id': store.app.session_id,
        'timestamp': jh.now_to_timestamp(),
        'message': msg
    }
    
    if jh.is_live():
        sync_publish('info_log', log_dict)

def error(msg: str, send_notification=True) -> None:
    log_dict = {
        'id': jh.generate_unique_id(),
        'timestamp': jh.now_to_timestamp(),
        'message': msg
    }
    
    if (jh.is_backtesting() and jh.is_debugging()) or jh.is_live():
        sync_publish('error_log', log_dict)
```

## 配置和环境变量

### 全局配置管理

```python
# jesse/services/env.py
ENV_VALUES = {}

if jh.is_jesse_project():
    load_dotenv()
    ENV_VALUES = dotenv_values('.env')

# jesse/config.py  
config = {
    'env': {
        'caching': {
            'driver': 'pickle'
        },
        'logging': {
            'strategy_execution': True,
            'order_submission': True,
            # ... 其他日志配置
        }
    }
}
```

## 实际应用示例

### 策略中的综合使用

```python
from jesse.store import store
from jesse.services.cache import cache
from jesse.services.redis import sync_publish

class SmartStrategy(Strategy):
    def should_long(self):
        # 1. 访问全局状态
        current_position = store.positions.get_position(
            self.exchange, self.symbol
        )
        
        # 2. 使用缓存获取技术指标
        cache_key = f"{self.symbol}_complex_indicator"
        indicator = cache.get_value(cache_key)
        
        if indicator is False:
            # 计算复杂指标
            indicator = self.calculate_complex_indicator()
            # 缓存30分钟
            cache.set_value(cache_key, indicator, 1800)
            
        # 3. 实时推送分析结果
        sync_publish('strategy_analysis', {
            'symbol': self.symbol,
            'indicator_value': indicator,
            'signal': 'bullish' if indicator > 50 else 'bearish'
        })
        
        return indicator > 50 and current_position.size == 0
    
    def calculate_complex_indicator(self):
        # 复杂的技术分析计算
        ma_short = ta.sma(self.candles, 10)
        ma_long = ta.sma(self.candles, 30)
        rsi = ta.rsi(self.candles, 14)
        
        # 综合指标
        return (ma_short[-1] / ma_long[-1] - 1) * 100 + rsi[-1]
```

### 缓存优化示例

```python
# 大数据量缓存策略
def get_market_data_with_smart_cache():
    cache_key = "market_overview"
    
    # 尝试获取缓存
    market_data = cache.get_value(cache_key)
    if market_data is not False:
        return market_data
    
    # 从多个源获取数据
    btc_data = fetch_crypto_data('BTC-USDT')
    eth_data = fetch_crypto_data('ETH-USDT')
    market_sentiment = analyze_market_sentiment()
    
    # 组合数据
    market_data = {
        'btc': btc_data,
        'eth': eth_data,
        'sentiment': market_sentiment,
        'timestamp': time.time()
    }
    
    # 缓存5分钟
    cache.set_value(cache_key, market_data, 300)
    
    return market_data
```

## 总结

### 存储系统对比

| 存储类型 | 用途 | 生命周期 | 访问速度 | 持久化 |
|----------|------|----------|----------|--------|
| **Store (全局状态)** | 运行时核心状态 | 进程生命周期 | 极快 | 否 |
| **Cache (文件缓存)** | 计算结果缓存 | 可配置过期 | 快 | 是 |
| **Redis (消息)** | 实时通信 | 消息生命周期 | 快 | 可选 |
| **Config (配置)** | 应用配置 | 应用生命周期 | 快 | 是 |

### 设计优势

1. **🎯 分层明确** - 不同类型数据使用最适合的存储方式
2. **⚡ 性能优化** - 内存 > 文件缓存 > 数据库的访问策略
3. **🔄 实时通信** - Redis实现了高效的实时数据推送
4. **🛡️ 容错机制** - 缓存损坏自动清理，Redis断线自动重连
5. **📈 可扩展性** - 模块化设计，易于扩展新的存储类型

### 最佳实践

1. **合理使用缓存** - 计算耗时的结果才需要缓存
2. **设置合适过期时间** - 根据数据更新频率设置过期时间
3. **监控缓存命中率** - 定期清理无效缓存
4. **Redis消息压缩** - 大数据量消息使用压缩
5. **状态管理规范** - 通过Store统一管理运行时状态

Jesse 的存储和缓存系统通过这种多层架构设计，既保证了**性能**（内存访问快），又保证了**可靠性**（数据持久化），还支持了**实时性**（Redis消息）和**模块化**（分类管理），为高效的量化交易提供了坚实的基础架构支撑。
