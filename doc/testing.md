# Jesse 测试指南

## 📋 目录
- [概述](#概述)
- [测试环境配置](#测试环境配置)
- [运行测试](#运行测试)
- [测试框架](#测试框架)
- [编写测试](#编写测试)
- [最佳实践](#最佳实践)

## 概述

Jesse 项目支持两种测试运行方式：
- **简单模式**：直接运行 Python 文件
- **专业模式**：使用 pytest 测试框架

## 测试环境配置

### 方案1：开发模式安装（推荐）

以开发模式安装 Jesse 项目，解决导入路径问题：

```bash
# 在项目根目录执行
pip install -e .
```

**优点：**
- ✅ 一次配置，全局生效
- ✅ 代码修改立即生效，无需重新安装
- ✅ 无需在测试文件中添加路径配置
- ✅ 支持在任何地方 `import jesse`

### 方案2：环境变量方式

如果不想修改系统安装，可以使用环境变量：

```bash
# Windows PowerShell
$env:PYTHONPATH = "D:\work\aiwork\jesse"
python jesse/tests/test_math_utils.py

# Linux/Mac
export PYTHONPATH="/path/to/jesse"
python jesse/tests/test_math_utils.py
```

## 运行测试

### 简单模式（直接运行）

```bash
# 运行单个测试文件
python jesse/tests/test_math_utils.py

# 输出示例：
# ========================================
# Jesse Math Utils 测试
# ========================================
# 🧮 测试 igcdex 函数...
# ✅ igcdex(2, 3) = (-1, 1, 1)
# ✅ igcdex(10, 12) = (-1, 1, 2)
# 🎉 所有 igcdex 测试通过!
# ✨ 所有测试完成!
```

### 专业模式（pytest）

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest jesse/tests/test_math_utils.py

# 详细输出
pytest -v

# 运行特定标记的测试
pytest -m "math and unit"

# 输出示例：
# ==================== test session starts ====================
# platform win32 -- Python 3.10.6, pytest-6.2.5
# rootdir: D:\work\aiwork\jesse, configfile: pytest.ini
# collected 3 items
#
# jesse/tests/test_math_utils.py::test_igcdex_basic_cases PASSED [ 33%]
# jesse/tests/test_math_utils.py::test_igcdex_larger_numbers PASSED [ 66%]
# jesse/tests/test_math_utils.py::test_igcdex_edge_cases PASSED [100%]
#
# ==================== 3 passed in 2.70s ====================
```

## 测试框架

### pytest 配置

项目包含 `pytest.ini` 配置文件：

```ini
[tool:pytest]
# 测试发现路径
testpaths = tests jesse/tests

# 测试文件和函数的命名模式
python_files = test_*.py *_test.py
python_functions = test_*
python_classes = Test*

# 输出选项
addopts = 
    -v
    --tb=short
    --strict-markers
    --color=yes

# 标记定义
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    math: marks tests related to math utilities
```

### 测试标记

使用装饰器为测试添加标记：

```python
import pytest

@pytest.mark.math
@pytest.mark.unit
def test_igcdex_basic_cases():
    """测试 igcdex 函数的基本用例"""
    # 测试代码
```

### 运行特定标记

```bash
# 只运行数学相关的单元测试
pytest -m "math and unit"

# 排除慢速测试
pytest -m "not slow"

# 只运行集成测试
pytest -m integration
```

## 编写测试

### 基本测试结构

```python
import pytest
import jesse.math_utils as mu

@pytest.mark.math
@pytest.mark.unit
def test_igcdex_basic_cases():
    """测试 igcdex 函数的基本用例"""
    # 测试用例 1: gcd(2,3) = 1
    result = mu.igcdx(2, 3)
    expected = (-1, 1, 1)
    assert result == expected, f"igcdex(2, 3) = {result}, 期望 {expected}"
    
    # 验证数学公式: x*a + y*b = gcd(a,b)
    x, y, g = result
    assert x*2 + y*3 == g, f"验证失败: {x}*2 + {y}*3 ≠ {g}"

def test_edge_cases():
    """测试边界情况"""
    # 零值测试
    # 负数测试
    # 大数测试
    pass
```

### 兼容两种运行方式

为了同时支持直接运行和 pytest，可以这样编写：

```python
import pytest
import jesse.math_utils as mu

@pytest.mark.math
def test_function():
    # pytest 测试逻辑
    assert mu.some_function() == expected_result

def simple_test():
    # 简单模式测试逻辑
    print("🧮 测试开始...")
    result = mu.some_function()
    assert result == expected_result
    print("✅ 测试通过!")

if __name__ == "__main__":
    # 直接运行文件时使用简单模式
    print("=" * 40)
    print("模块测试 (简单模式)")
    print("=" * 40)
    simple_test()
    print("🎉 所有测试完成!")
```

## 最佳实践

### 1. 测试组织

```
tests/
├── unit/                 # 单元测试
│   ├── test_math_utils.py
│   ├── test_indicators.py
│   └── test_strategies.py
├── integration/          # 集成测试
│   ├── test_exchange_api.py
│   └── test_database.py
└── data/                # 测试数据
    ├── candles/
    └── fixtures/
```

### 2. 命名规范

- **测试文件**：`test_*.py` 或 `*_test.py`
- **测试函数**：`test_*`
- **测试类**：`Test*`

### 3. 断言最佳实践

```python
# ✅ 好的断言 - 提供清晰的错误信息
def test_calculation():
    result = calculate_rsi([1, 2, 3, 4, 5])
    expected = 50.0
    assert abs(result - expected) < 0.01, \
        f"RSI计算错误: 得到 {result}, 期望 {expected}"

# ❌ 不好的断言 - 错误信息不清楚  
def test_calculation():
    assert calculate_rsi([1, 2, 3, 4, 5]) == 50.0
```

### 4. 测试数据管理

```python
# 使用 pytest fixture 管理测试数据
@pytest.fixture
def sample_candles():
    return [
        [1625097600, 50000, 51000, 49000, 50500, 1000],
        [1625101200, 50500, 52000, 50000, 51500, 1200],
        # ... 更多数据
    ]

def test_strategy(sample_candles):
    strategy = MyStrategy()
    result = strategy.analyze(sample_candles)
    assert result is not None
```

### 5. 数据库测试

```python
@pytest.fixture
def test_db():
    """创建测试数据库"""
    # 设置测试数据库
    db_config = {
        'database': 'jesse_test_db',
        # ... 其他配置
    }
    setup_test_database(db_config)
    yield db_config
    # 清理测试数据库
    cleanup_test_database(db_config)

def test_database_operations(test_db):
    # 使用测试数据库进行测试
    pass
```

### 6. 模拟外部依赖

```python
from unittest.mock import patch, MagicMock

@patch('jesse.services.api.get_market_data')
def test_strategy_with_mock_data(mock_get_data):
    # 模拟 API 响应
    mock_get_data.return_value = {
        'price': 50000,
        'volume': 1000
    }
    
    # 测试策略逻辑
    strategy = MyStrategy()
    result = strategy.should_long()
    
    # 验证 API 被正确调用
    mock_get_data.assert_called_once()
    assert result is True
```

### 7. 性能测试

```python
import time
import pytest

@pytest.mark.slow
def test_strategy_performance():
    """测试策略执行性能"""
    strategy = MyStrategy()
    large_dataset = generate_large_candle_data(10000)
    
    start_time = time.time()
    result = strategy.backtest(large_dataset)
    execution_time = time.time() - start_time
    
    # 验证性能要求（比如要求在1秒内完成）
    assert execution_time < 1.0, f"策略执行太慢: {execution_time:.2f}s"
    assert result is not None
```

### 8. 错误处理测试

```python
def test_error_handling():
    """测试错误处理"""
    strategy = MyStrategy()
    
    # 测试无效输入
    with pytest.raises(ValueError, match="无效的K线数据"):
        strategy.analyze([])
    
    # 测试网络错误
    with patch('requests.get', side_effect=ConnectionError):
        with pytest.raises(ConnectionError):
            strategy.fetch_market_data()
```

## 调试测试

### 使用 pytest 调试

```bash
# 在第一个失败处停止
pytest -x

# 显示本地变量
pytest --tb=long

# 进入调试器
pytest --pdb

# 详细输出
pytest -s -v
```

### 使用 VS Code 调试

在 VS Code 中可以直接点击测试函数旁边的"运行"按钮，或者设置断点进行调试。

## 持续集成

### GitHub Actions 配置示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=jesse --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

通过这个测试指南，你可以：
- ✅ 快速配置测试环境
- ✅ 选择适合的测试运行方式
- ✅ 编写高质量的测试代码
- ✅ 使用现代化的测试工具和最佳实践

测试是保证代码质量的重要环节，建议在开发新功能时同步编写相应的测试用例。
