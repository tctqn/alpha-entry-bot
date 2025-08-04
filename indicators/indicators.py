import pandas as pd
import ta

def calculate_rsi(data, period=14):
    rsi = ta.momentum.RSIIndicator(close=data['close'], window=period)
    data['rsi'] = rsi.rsi()
    return data

def calculate_ema(data):
    data['ema50'] = data['close'].ewm(span=50, adjust=False).mean()
    data['ema200'] = data['close'].ewm(span=200, adjust=False).mean()
    return data

def calculate_macd(data):
    macd = ta.trend.MACD(close=data['close'])
    data['macd'] = macd.macd()
    data['macd_signal'] = macd.macd_signal()
    data['macd_hist'] = macd.macd_diff()
    return data

def add_indicators(data):
    data = calculate_rsi(data)
    data = calculate_ema(data)
    data = calculate_macd(data)
    return data
