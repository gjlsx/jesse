import ccxt
import os

# 可选：设置代理（如使用 clash 本地）
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10810'


#大陆或者美国会被墙的交易所会卡住，需要设置代理或支持location服务器
exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('WLD/USDT', '1h')
for candle in ohlcv[-5:]:
    print(candle)