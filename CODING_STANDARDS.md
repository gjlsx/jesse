# 编码规范文档

## 📝 注释语言规范

### 🎯 基本原则

#### **strategies/ 目录下的 Python 文件**
- ✅ **必须使用英文注释**
- ✅ 类和方法文档字符串
- ✅ 变量和参数说明
- ✅ 代码逻辑注释
- ✅ 错误信息输出

#### **其他目录的文件**
- ✅ **尽量使用中文注释**
- ✅ 配置文件说明
- ✅ 文档文件
- ✅ 其他非策略代码

### 📊 具体规范

| 文件类型 | 注释语言 | 示例 |
|---------|---------|------|
| `strategies/*.py` | **英文** | `# Check if there are 5 consecutive down days` |
| `.env` | **中文** | `# 数据库连接配置` |
| `docker-compose.yml` | **中文** | `# Jesse 工作空间容器` |
| `README.md` | **中文** | `# Jesse 项目模板` |
| `docs/*.md` | **中文** | `# 快速开始指南` |

### 🔧 代码示例

#### **策略文件示例（英文注释）**
```python
# strategies/NewStrategy/__init__.py
class NewStrategy(Strategy):
    """
    New Trading Strategy
    Strategy description in English
    """
    
    def __init__(self):
        super().__init__()
        # Strategy parameters in English
        self.param1 = 10  # Parameter description
        
    def should_long(self) -> bool:
        """
        Determine if should go long
        Check trading conditions
        """
        # Check market conditions
        return True
```

#### **配置文件示例（中文注释）**
```python
# config/settings.py
# 系统配置文件
# 数据库连接设置
DATABASE_HOST = "localhost"  # 数据库主机地址
DATABASE_PORT = 5432         # 数据库端口
```

### 📝 开发规范

#### **创建新策略时**
1. 使用英文类名和方法名
2. 使用英文文档字符串
3. 使用英文变量注释
4. 使用英文错误信息

#### **创建配置文件时**
1. 使用中文文件说明
2. 使用中文配置注释
3. 使用中文错误提示

### 🎯 策略特定规范

#### **策略类命名规范**
- 使用英文 PascalCase 命名，**长度控制在10个字符内**
- 推荐简洁命名：`RSIStrategy`、`MAStrategy`、`DipBuying`
- 避免冗长命名：~~`MovingAverageStrategy`~~ → `MAStrategy`
- 避免中文拼音：~~`moveAverage`~~ → `MAStrategy`
- 策略描述使用英文：`"""Multi-MA Dip Buying Strategy"""`

#### **类名简化对照表**
| 冗长命名 | 推荐简化 | 字符数 |
|---------|---------|--------|
| `MovingAverageStrategy` | `MAStrategy` | 10 |
| `RelativeStrengthIndexStrategy` | `RSIStrategy` | 11 ❌ → `RSI` (3) ✅ |
| `BollingerBandStrategy` | `BBStrategy` | 10 |
| `MACDStrategy` | `MACD` | 4 |
| `DipBuyingStrategy` | `DipBuying` | 9 |

#### **技术指标属性规范**
```python
@property
def ma14(self):
    """14-period moving average"""
    return ta.sma(self.candles, period=14, sequential=True)
```

#### **方法参数和返回值规范**
```python
def should_long(self):
    """
    Determine if should go long
    Returns True when entry conditions are met
    """
    return condition_check
```

### 📊 文件类型补充规范

| 文件类型 | 注释语言 | 额外要求 |
|---------|---------|---------|
| `strategies/*.py` | **英文** | 类名、方法名、变量名必须英文 |
| `sqls/*.py` | **中文** | 数据库测试脚本，中文注释便于理解 |
| `sqls/*.sql` | **中文** | SQL 脚本中文注释 |
| `storage/` | **中文** | 存储相关配置文件 |

### ⚡ 性能和最佳实践

#### **策略代码性能规范**
```python
class YourStrategy(Strategy):
    def __init__(self):
        super().__init__()
        # Cache frequently used values
        self.ma_periods = [14, 21, 60]  # Use constants
        self.position_size = 0.3        # Avoid magic numbers
        
    @property  # Use properties for indicators
    def rsi(self):
        """RSI indicator with proper caching"""
        return ta.rsi(self.candles, period=14)
```

#### **错误处理规范**
```python
def go_long(self):
    """Execute long position with error handling"""
    try:
        qty = utils.size_to_qty(self.balance * self.position_size, self.price)
        self.buy = qty, self.price
    except Exception as e:
        print(f"Long position error: {e}")  # English error messages
```

### 🔄 版本控制规范

#### **Git 提交信息规范**
```bash
# 策略相关提交（英文）
git commit -m "feat: add RSI strategy with overbought/oversold signals"
git commit -m "fix: correct moving average calculation in MA strategy"

# 配置相关提交（中文）  
git commit -m "配置: 更新数据库连接参数"
git commit -m "文档: 添加环境配置说明"
```

#### **Pull Request 规范**
- 策略代码修改：使用英文标题和描述
- 配置文档修改：使用中文标题和描述
- 代码审查：关注注释语言规范一致性

### 🛠️ 开发工具配置

#### **IDE 配置建议**
```json
// .vscode/settings.json
{
    "editor.rulers": [80, 120],
    "files.associations": {
        "*.py": "python"
    }
}
```

#### **代码格式化**
- 使用 `black` 进行 Python 代码格式化
- 策略文件强制英文注释检查
- 配置文件允许中文注释

### 🔄 修改规范

如需修改此规范：
1. 编辑 `CODING_STANDARDS.md` 文件
2. 更新相关示例
3. 通知团队成员
4. 更新现有代码以符合新规范

### 📋 检查清单

#### **策略文件检查**
- [ ] 类文档字符串使用英文
- [ ] 方法文档字符串使用英文
- [ ] 变量注释使用英文
- [ ] 代码逻辑注释使用英文
- [ ] 错误信息使用英文
- [ ] 类名使用英文 PascalCase
- [ ] 方法名使用英文 snake_case
- [ ] 技术指标使用 @property 装饰器

#### **配置文件检查**
- [ ] 文件头部说明使用中文
- [ ] 配置项注释使用中文
- [ ] 错误提示使用中文
- [ ] 文档说明使用中文

#### **代码质量检查**
- [ ] 无魔法数字，使用常量
- [ ] 适当的错误处理
- [ ] 性能优化（缓存、属性装饰器）
- [ ] 代码可读性良好

### 🚨 常见问题修正

#### **问题1：策略类命名不规范**
```python
# ❌ 错误示例
class moveAverage(Strategy):  # 小写开头，拼音命名

# ✅ 正确示例  
class MAStrategy(Strategy):  # 英文 PascalCase，10字符内
```

#### **问题2：注释语言混用**
```python
# ❌ 错误示例（策略文件中使用中文）
def should_long(self):
    """判断是否应该做多"""  # 中文注释
    # 检查市场条件         # 中文注释
    return True

# ✅ 正确示例（策略文件中使用英文）
def should_long(self):
    """Determine if should go long"""  # 英文注释  
    # Check market conditions        # 英文注释
    return True
```

---

**最后更新**: 2025年7月6日
**维护者**: wind ai开发团队 