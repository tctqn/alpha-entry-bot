import ta

def confirm_trigger(df, poi_low, poi_high):
    # Kiểm tra nếu DataFrame không đủ dữ liệu
    if len(df) < 2:
        raise ValueError("DataFrame không đủ dữ liệu để xác nhận trigger.")
    
    # Kiểm tra các cột cần thiết
    required_columns = ['close', 'open', 'low', 'rsi']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột '{col}' trong DataFrame.")
        if df[col].isnull().any():
            raise ValueError(f"Cột '{col}' chứa giá trị NaN.")

    # Lấy dữ liệu cuối cùng
    last = df.iloc[-1]
    candle = last['close'] > last['open']
    rsi = df['rsi'].iloc[-1]
    rsi_prev = df['rsi'].iloc[-2]

    # Kiểm tra phân kỳ RSI
    rsi_divergent = (last['close'] > df['close'].iloc[-2]) and (rsi < rsi_prev)
    
    # Xác nhận trigger
    if poi_low <= last['low'] <= poi_high and candle and rsi_divergent:
        return True
    return False

def add_macd(df):
    macd_indicator = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd_hist'] = macd_indicator.macd_diff()
    return df

def is_momentum_strong(df):
    last_hist = df['macd_hist'].iloc[-1]
    prev_hist = df['macd_hist'].iloc[-2]
    return last_hist > 0 and prev_hist < 0
