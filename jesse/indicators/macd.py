from collections import namedtuple

import numpy as np
from numba import njit
from jesse.helpers import get_candle_source, slice_candles

# MACD指标返回值的命名元组：包含MACD线、信号线和柱状图
MACD = namedtuple('MACD', ['macd', 'signal', 'hist'])

@njit
def ema_numba(source, period):
    """
    使用Numba加速的指数移动平均计算
    Exponential Moving Average calculation accelerated by Numba
    """
    ema_array = np.empty_like(source)
    alpha = 2.0 / (period + 1)  # 平滑系数
    ema_array[0] = source[0]
    for i in range(1, len(source)):
        ema_array[i] = alpha * source[i] + (1 - alpha) * ema_array[i - 1]
    return ema_array

@njit
def subtract_arrays(a, b):
    """
    高效的数组减法操作，使用Numba加速
    Efficient array subtraction operation accelerated by Numba
    """
    c = np.empty_like(a)
    for i in range(len(a)):
        c[i] = a[i] - b[i]
    return c

@njit
def clean_nan(arr):
    """
    清理数组中的NaN值，将其替换为0.0
    Clean NaN values in array, replace with 0.0
    """
    # 使用 nan != nan 为 True 的特性来检测NaN
    for i in range(arr.shape[0]):
        if arr[i] != arr[i]:
            arr[i] = 0.0
    return arr


def macd(candles: np.ndarray, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9,
         source_type: str = "close",
         sequential: bool = False) -> MACD:
    """
    MACD - 平滑异同移动平均线 (使用numba优化的快速计算)
    MACD - Moving Average Convergence/Divergence using numba for faster computation

    MACD是由Gerald Appel于1970年代开发的趋势跟踪动量指标，通过计算两个不同周期的
    指数移动平均线之间的差值来识别趋势变化和动量。

    计算公式:
    1. MACD线 = EMA(12) - EMA(26)
    2. 信号线 = EMA(MACD线, 9)
    3. 柱状图 = MACD线 - 信号线

    :param candles: np.ndarray - K线数据数组
    :param fast_period: int - 快线EMA周期，默认: 12
    :param slow_period: int - 慢线EMA周期，默认: 26
    :param signal_period: int - 信号线EMA周期，默认: 9
    :param source_type: str - 数据源类型，默认: "close" (收盘价)
    :param sequential: bool - 是否返回完整序列，默认: False

    :return: MACD(macd, signal, hist) - 命名元组包含MACD线、信号线和柱状图
    
    交易信号解读:
    - 金叉: MACD线上穿信号线，买入信号
    - 死叉: MACD线下穿信号线，卖出信号
    - 柱状图正值增大: 上涨动能增强
    - 柱状图负值减小: 下跌动能减弱
    """

    if len(candles.shape) == 1:
        source = candles
    else:
        candles = slice_candles(candles, sequential)
        source = get_candle_source(candles, source_type=source_type)

    # 使用numba加速函数计算快线和慢线EMA
    ema_fast = ema_numba(source, fast_period)
    ema_slow = ema_numba(source, slow_period)

    # 使用numba编译的减法循环计算MACD线
    macd_line = subtract_arrays(ema_fast, ema_slow)
    macd_line_cleaned = clean_nan(macd_line)

    # 计算信号线，即MACD线的EMA
    signal_line = ema_numba(macd_line_cleaned, signal_period)
    
    # 计算柱状图，即MACD线与信号线的差值
    hist = subtract_arrays(macd_line, signal_line)

    if sequential:
        # 返回完整的时间序列数据
        return MACD(macd_line_cleaned, signal_line, hist)
    else:
        # 仅返回最新值
        return MACD(macd_line_cleaned[-1], signal_line[-1], hist[-1])
