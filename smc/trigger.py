import ta

def confirm_trigger(df, poi_low, poi_high):
    last = df.iloc[-1]
    candle = last['close'] > last['open']
    rsi = df['rsi'].iloc[-1]
    rsi_prev = df['rsi'].iloc[-2]

    rsi_divergent = (last['close'] > df['close'].iloc[-2]) and (rsi < rsi_prev)
    if poi_low <= last['low'] <= poi_high and candle and rsi_divergent:
        return True
    return False

def add_macd(df):
    macd = ta.trend.macd_diff(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd_hist'] = macd
    return df

def is_momentum_strong(df):
    last_hist = df['macd_hist'].iloc[-1]
    prev_hist = df['macd_hist'].iloc[-2]
    return last_hist > 0 and prev_hist < 0
