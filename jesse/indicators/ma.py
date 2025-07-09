from typing import Union

import numpy as np

from jesse.helpers import get_candle_source, slice_candles


def ma(candles: np.ndarray, period: int = 30, matype: int = 0,  source_type: str = "close", sequential: bool = False) -> Union[
    float, np.ndarray]:
    """
    MA - 移动平均线统一接口 (Jesse框架几乎所有移动平均算法的集合)
    Moving Average - (nearly) All Moving Averages of Jesse

    :param candles: np.ndarray - K线数据数组
    :param period: int - 计算周期，默认: 30
    :param matype: int - 移动平均类型编号，默认: 0 (SMA)
    :param source_type: str - 数据源类型，默认: "close" (收盘价)
    :param sequential: bool - 是否返回完整序列，默认: False (仅返回最新值)

    :return: float | np.ndarray - 单个值或完整序列

    移动平均类型对照表:
    0: sma (简单移动平均 - Simple Moving Average)
    1: ema (指数移动平均 - Exponential Moving Average)
    移动平均类型对照表:
    0: sma (简单移动平均 - Simple Moving Average)
    1: ema (指数移动平均 - Exponential Moving Average)
    2: wma (加权移动平均 - Weighted Moving Average)
    3: dema (双重指数移动平均 - Double Exponential Moving Average)
    4: tema (三重指数移动平均 - Triple Exponential Moving Average)
    5: trima (三角移动平均 - Triangular Moving Average)
    6: kama (考夫曼自适应移动平均 - Kaufman Adaptive Moving Average)
    9: fwma (斐波那契加权移动平均 - Fibonacci's Weighted Moving Average)
    10: hma (赫尔移动平均 - Hull Moving Average)
    11: linearreg (线性回归 - Linear Regression)
    12: wilders (威尔德平滑 - Wilders Smoothing)
    13: sinwma (正弦加权移动平均 - Sine Weighted Moving Average)
    14: supersmoother (超级平滑滤波器 2极点巴特沃斯 - Super Smoother Filter 2pole Butterworth)
    15: supersmoother\_3\_pole (超级平滑滤波器 3极点巴特沃斯 - Super Smoother Filter 3pole Butterworth)
    16: gauss (高斯滤波器 - Gaussian Filter)
    17: high\_pass (单极点高通滤波器 - 1-pole High Pass Filter by John F. Ehlers)
    18: high\_pass\_2\_pole (双极点高通滤波器 - 2-pole High Pass Filter by John F. Ehlers)
    19: ht\_trendline (希尔伯特变换瞬时趋势线 - Hilbert Transform - Instantaneous Trendline)
    20: jma (Jurik移动平均 - Jurik Moving Average)
    21: reflex (反射指标 - Reflex indicator by John F. Ehlers)
    22: trendflex (趋势反射指标 - Trendflex indicator by John F. Ehlers)
    23: smma (平滑移动平均 - Smoothed Moving Average)
    24: vwma (成交量加权移动平均 - Volume Weighted Moving Average)
    25: pwma (帕斯卡加权移动平均 - Pascals Weighted Moving Average)
    26: swma (对称加权移动平均 - Symmetric Weighted Moving Average)
    27: alma (阿诺德-勒古移动平均 - Arnaud Legoux Moving Average)
    28: hwma (霍尔特-温特移动平均 - Holt-Winter Moving Average)
    29: vwap (成交量加权平均价格 - Volume weighted average price)
    30: nma (自然移动平均 - Natural Moving Average)
    31: edcf (埃勒斯距离系数滤波器 - Ehlers Distance Coefficient Filter)
    32: mwdx (MWDX平均 - MWDX Average)
    33: maaq (自适应Q移动平均 - Moving Average Adaptive Q)
    34: srwma (平方根加权移动平均 - Square Root Weighted Moving Average)
    35: sqwma (平方加权移动平均 - Square Weighted Moving Average)
    36: vpwma (可变幂加权移动平均 - Variable Power Weighted Moving Average)
    37: cwma (立方加权移动平均 - Cubed Weighted Moving Average)
    38: jsa (Jsa移动平均 - Jsa Moving Average)
    39: epma (端点移动平均 - End Point Moving Average)

    """

    # 数据预处理：切片K线数据
    candles = slice_candles(candles, sequential)

    # 根据matype参数调用对应的移动平均算法
    if matype == 0:
        # SMA - 简单移动平均：最基础的移动平均，适合长期趋势分析
        from . import sma
        res = sma(candles, period, source_type=source_type, sequential=True)
    elif matype == 1:
        # EMA - 指数移动平均：对近期价格更敏感，适合短期交易
        from . import ema
        res = ema(candles, period, source_type=source_type, sequential=True)
    elif matype == 2:
        # WMA - 加权移动平均：线性递减权重，介于SMA和EMA之间
        from . import wma
        res = wma(candles, period, source_type=source_type, sequential=True)
    elif matype == 3:
        # DEMA - 双重指数移动平均：减少滞后性的改进EMA
        from . import dema
        res = dema(candles, period, source_type=source_type, sequential=True)
    elif matype == 4:
        # TEMA - 三重指数移动平均：进一步减少滞后性
        from . import tema
        res = tema(candles, period, source_type=source_type, sequential=True)
    elif matype == 5:
        # TRIMA - 三角移动平均：双重平滑处理，更稳定
        from . import trima
        res = trima(candles, period, source_type=source_type, sequential=True)
    elif matype == 6:
        # KAMA - 考夫曼自适应移动平均：根据市场波动自动调整敏感度
        from . import kama
        res = kama(candles, period, source_type=source_type, sequential=True)
    elif matype == 9:
        # FWMA - 斐波那契加权移动平均：使用斐波那契数列作为权重
        from . import fwma
        res = fwma(candles, period, source_type=source_type, sequential=True)
    elif matype == 10:
        # HMA - 赫尔移动平均：平滑且响应迅速的移动平均
        from . import hma
        res = hma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 11:
        # LinearReg - 线性回归：使用线性回归拟合价格趋势
        from . import linearreg
        res = linearreg(candles, period, source_type=source_type, sequential=True)
    elif matype == 12:
        # Wilders - 威尔德平滑：RSI指标中使用的平滑方法
        from . import wilders
        res = wilders(candles, period, source_type=source_type,  sequential=True)
    elif matype == 13:
        # SinWMA - 正弦加权移动平均：使用正弦函数分配权重
        from . import sinwma
        res = sinwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 14:
        # SuperSmoother - 超级平滑滤波器：消除价格噪音的数字滤波器
        from . import supersmoother
        res = supersmoother(candles, period, source_type=source_type,  sequential=True)
    elif matype == 15:
        # SuperSmoother 3-pole - 三极点超级平滑滤波器：更强的噪音过滤
        from . import supersmoother_3_pole
        res = supersmoother_3_pole(candles, period, source_type=source_type,  sequential=True)
    elif matype == 16:
        # Gauss - 高斯滤波器：基于高斯分布的平滑滤波器
        from . import gauss
        res = gauss(candles, period, source_type=source_type,  sequential=True)
    elif matype == 17:
        # High Pass - 高通滤波器：去除低频趋势，保留高频变化
        from . import high_pass
        res = high_pass(candles, period, source_type=source_type,  sequential=True)
    elif matype == 18:
        # High Pass 2-pole - 双极点高通滤波器：更强的去趋势效果
        from . import high_pass_2_pole
        res = high_pass_2_pole(candles, period, source_type=source_type,  sequential=True)
    elif matype == 20:
        # JMA - Jurik移动平均：专业级的低滞后平滑算法
        from . import jma
        res = jma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 21:
        # Reflex - 反射指标：John Ehlers开发的价格反射指标
        from . import reflex
        res = reflex(candles, period, source_type=source_type,  sequential=True)
    elif matype == 22:
        # TrendFlex - 趋势反射指标：结合趋势和反射的复合指标
        from . import trendflex
        res = trendflex(candles, period, source_type=source_type,  sequential=True)
    elif matype == 23:
        # SMMA - 平滑移动平均：类似于EMA的平滑算法
        from . import smma
        res = smma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 24:
        # VWMA - 成交量加权移动平均：考虑成交量权重的移动平均
        if len(candles.shape) == 1:
          raise ValueError("vwma只支持标准K线数据，不支持单维数组。")
        from . import vwma
        res = vwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 25:
        # PWMA - 帕斯卡加权移动平均：使用帕斯卡三角形权重
        from . import pwma
        res = pwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 26:
        # SWMA - 对称加权移动平均：对称分布权重的移动平均
        from . import swma
        res = swma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 27:
        # ALMA - 阿诺德-勒古移动平均：可调节滞后性的自适应算法
        from . import alma
        res = alma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 28:
        # HWMA - 霍尔特-温特移动平均：考虑趋势和季节性的移动平均
        from . import hwma
        res = hwma(candles, source_type=source_type,  sequential=True)
    elif matype == 29:
        # VWAP - 成交量加权平均价格：机构交易常用基准价格
        from . import vwap
        if len(candles.shape) == 1:
          raise ValueError("vwap只支持标准K线数据，不支持单维数组。")
        res = vwap(candles, source_type=source_type,  sequential=True)
    elif matype == 30:
        # NMA - 自然移动平均：基于自然对数的移动平均
        from . import nma
        res = nma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 31:
        # EDCF - 埃勒斯距离系数滤波器：高级数字信号处理滤波器
        from . import edcf
        res = edcf(candles, period, source_type=source_type,  sequential=True)
    elif matype == 32:
        # MWDX - MWDX平均：多重加权距离平均算法
        from . import mwdx
        res = mwdx(candles, source_type=source_type,  sequential=True)
    elif matype == 33:
        # MAAQ - 自适应Q移动平均：自适应量化移动平均
        from . import maaq
        res = maaq(candles, period, source_type=source_type,  sequential=True)
    elif matype == 34:
        # SRWMA - 平方根加权移动平均：使用平方根函数分配权重
        from . import srwma
        res = srwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 35:
        # SQWMA - 平方加权移动平均：使用平方函数分配权重
        from . import sqwma
        res = sqwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 36:
        # VPWMA - 可变幂加权移动平均：可调节幂次的加权移动平均
        from . import vpwma
        res = vpwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 37:
        # CWMA - 立方加权移动平均：使用立方函数分配权重
        from . import cwma
        res = cwma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 38:
        # JSA - Jsa移动平均：专有的Jsa算法移动平均
        from . import jsa
        res = jsa(candles, period, source_type=source_type,  sequential=True)
    elif matype == 39:
        # EPMA - 端点移动平均：基于端点计算的移动平均
        from . import epma
        res = epma(candles, period, source_type=source_type,  sequential=True)
    elif matype == 7 or matype == 8 or matype == 19:
        # 无效的matype值：这些编号被保留或未实现
        raise ValueError("无效的matype值，请检查输入参数。")

    # 根据sequential参数返回相应结果
    return res if sequential else res[-1]
