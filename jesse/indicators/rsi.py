import numpy as np
from typing import Union
from numba import njit

from jesse.helpers import get_candle_source, slice_candles


@njit(cache=True)
def _rsi(p: np.ndarray, period: int) -> np.ndarray:
    """
    使用循环和威尔德平滑法计算相对强弱指数
    Compute the Relative Strength Index using a loop and Wilder's smoothing.
    
    RSI公式:
    RS = 平均涨幅 / 平均跌幅
    RSI = 100 - (100 / (1 + RS))
    """
    n = len(p)
    rsi_arr = np.full(n, np.nan)
    if n < period + 1:
        return rsi_arr
    
    # 计算连续价格之间的差值
    diff = np.empty(n - 1)
    for i in range(n - 1):
        diff[i] = p[i+1] - p[i]

    # 计算前'period'个差值的初始平均涨幅和跌幅
    sum_gain = 0.0
    sum_loss = 0.0
    for i in range(period):
        change = diff[i]
        if change > 0:
            sum_gain += change  # 累积涨幅
        else:
            sum_loss += -change  # 累积跌幅(取绝对值)
    avg_gain = sum_gain / period  # 平均涨幅
    avg_loss = sum_loss / period  # 平均跌幅

    # 计算第一个RSI值(索引为'period')
    if avg_loss == 0:
        rsi_arr[period] = 100.0  # 如果没有跌幅，RSI为100
    else:
        rs = avg_gain / avg_loss  # 相对强度
        rsi_arr[period] = 100 - (100 / (1 + rs))

    # 递归更新平均涨幅和跌幅，计算后续的RSI值
    for i in range(period, n - 1):
        change = diff[i]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0
        # 使用威尔德平滑法更新平均值
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        if avg_loss == 0:
            rsi_arr[i+1] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_arr[i+1] = 100 - (100 / (1 + rs))
    return rsi_arr


def rsi(candles: np.ndarray, period: int = 14, source_type: str = "close", sequential: bool = False) -> Union[float, np.ndarray]:
    """
    RSI - 相对强弱指数 (使用Numba优化的高性能计算)
    RSI - Relative Strength Index using Numba for optimization

    RSI是由J. Welles Wilder于1978年开发的动量振荡指标，用于测量价格变动的速度和变化。
    RSI在0到100之间波动，通常用于识别超买和超卖条件。

    计算原理:
    1. 计算价格变动: diff = price[t] - price[t-1]
    2. 分离涨幅和跌幅: gain = max(diff, 0), loss = max(-diff, 0)
    3. 计算平均涨幅和平均跌幅 (使用威尔德平滑)
    4. 相对强度 RS = 平均涨幅 / 平均跌幅
    5. RSI = 100 - (100 / (1 + RS))

    :param candles: np.ndarray - K线数据数组
    :param period: int - 计算周期，默认: 14
    :param source_type: str - 数据源类型，默认: "close" (收盘价)
    :param sequential: bool - 是否返回完整序列，默认: False

    :return: float | np.ndarray - RSI值或RSI序列

    交易信号解读:
    - RSI > 70: 超买区域，可能的卖出信号
    - RSI < 30: 超卖区域，可能的买入信号
    - RSI 50: 中性线，高于50表示上涨动能，低于50表示下跌动能
    - 背离: RSI与价格走势相反，可能预示趋势反转
    """
    if len(candles.shape) == 1:
        source = candles
    else:
        candles = slice_candles(candles, sequential)
        source = get_candle_source(candles, source_type=source_type)

    p = np.asarray(source, dtype=float)
    result = _rsi(p, period)
    return result if sequential else result[-1]
