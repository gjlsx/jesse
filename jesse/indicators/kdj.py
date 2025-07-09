from collections import namedtuple

import numpy as np

from jesse.helpers import slice_candles
from jesse.indicators.ma import ma

# KDJ指标返回值的命名元组：包含K值、D值和J值
KDJ = namedtuple('KDJ', ['k', 'd', 'j'])

def _rolling_max(a, window):
    """
    计算滚动窗口内的最大值，使用NumPy的滑动窗口视图优化性能
    Calculate rolling maximum using NumPy's sliding window view for performance
    """
    from numpy.lib.stride_tricks import sliding_window_view
    a = np.asarray(a)
    if len(a) < window:
        # 如果数据长度小于窗口大小，返回累积最大值
        return np.maximum.accumulate(a)
    result = np.empty_like(a)
    # 对于前window-1个元素，使用累积最大值
    result[:window-1] = np.maximum.accumulate(a)[:window-1]
    windows = sliding_window_view(a, window_shape=window)
    result[window-1:] = np.max(windows, axis=1)
    return result

def _rolling_min(a, window):
    """
    计算滚动窗口内的最小值，使用NumPy的滑动窗口视图优化性能
    Calculate rolling minimum using NumPy's sliding window view for performance
    """
    from numpy.lib.stride_tricks import sliding_window_view
    a = np.asarray(a)
    if len(a) < window:
        # 如果数据长度小于窗口大小，返回累积最小值
        return np.minimum.accumulate(a)
    result = np.empty_like(a)
    # 对于前window-1个元素，使用累积最小值
    result[:window-1] = np.minimum.accumulate(a)[:window-1]
    windows = sliding_window_view(a, window_shape=window)
    result[window-1:] = np.min(windows, axis=1)
    return result

def kdj(candles: np.ndarray, fastk_period: int = 9, slowk_period: int = 3, slowk_matype: int = 0,
          slowd_period: int = 3, slowd_matype: int = 0, sequential: bool = False) -> KDJ:
    """
    KDJ - 随机指标 (KDJ随机震荡指标)
    The KDJ Oscillator

    KDJ指标是在KD指标(随机指标)基础上发展起来的技术分析工具，由George Lane创立，
    并在亚洲市场特别是中国股市中得到广泛应用。KDJ指标结合了动量观念、强弱指标和移动平均线的优点。

    计算原理:
    1. RSV (Raw Stochastic Value) = 100 × (收盘价 - N期内最低价) / (N期内最高价 - N期内最低价)
    2. K值 = RSV的移动平均 (通常为3期)
    3. D值 = K值的移动平均 (通常为3期)
    4. J值 = 3×K值 - 2×D值 (J线是KD的敏感指标)

    :param candles: np.ndarray - K线数据数组
    :param fastk_period: int - 快速K值周期(RSV计算周期)，默认: 9
    :param slowk_period: int - 慢速K值周期(K值平滑周期)，默认: 3
    :param slowk_matype: int - K值移动平均类型，默认: 0 (SMA)
    :param slowd_period: int - D值周期(D值平滑周期)，默认: 3
    :param slowd_matype: int - D值移动平均类型，默认: 0 (SMA)
    :param sequential: bool - 是否返回完整序列，默认: False

    :return: KDJ(k, d, j) - 命名元组包含K值、D值和J值

    交易信号解读:
    - K值、D值范围: 0-100
    - 超买区域: K>80, D>80 (卖出信号)
    - 超卖区域: K<20, D<20 (买入信号)
    - 金叉: K线上穿D线 (买入信号)
    - 死叉: K线下穿D线 (卖出信号)
    - J值: 超前指标，J>100为超买，J<0为超卖
    - 强势格局: K>D>J，弱势格局: J>D>K
    """
    # 检查移动平均类型是否支持
    if any(matype in (24, 29) for matype in (slowk_matype, slowd_matype)):
        raise ValueError("VWMA (matype 24) 和 VWAP (matype 29) 不能在KDJ指标中使用。")
    
    candles = slice_candles(candles, sequential)

    # 提取价格数据：收盘价、最高价、最低价
    candles_close = candles[:, 2]  # 收盘价
    candles_high = candles[:, 3]   # 最高价
    candles_low = candles[:, 4]    # 最低价

    # 计算指定周期内的最高价和最低价
    hh = _rolling_max(candles_high, fastk_period)  # 周期内最高价
    ll = _rolling_min(candles_low, fastk_period)   # 周期内最低价

    # 计算RSV (Raw Stochastic Value) - 未成熟随机值
    # RSV = 100 × (当前收盘价 - 周期内最低价) / (周期内最高价 - 周期内最低价)
    stoch = 100 * (candles_close - ll) / (hh - ll)
    
    # 计算K值：RSV的移动平均
    k = ma(stoch, period=slowk_period, matype=slowk_matype, sequential=True)
    
    # 计算D值：K值的移动平均
    d = ma(k, period=slowd_period, matype=slowd_matype, sequential=True)
    
    # 计算J值：J = 3×K - 2×D (超前指标，比KD更敏感)
    j = 3 * k - 2 * d

    if sequential:
        # 返回完整的时间序列数据
        return KDJ(k, d, j)
    else:
        # 仅返回最新值
        return KDJ(k[-1], d[-1], j[-1])
