def determine_trend(df):
    last = df.iloc[-1]
    if last['ema50'] > last['ema200'] and last['rsi'] > 50:
        return "uptrend"
    elif last['ema50'] < last['ema200'] and last['rsi'] < 50:
        return "downtrend"
    else:
        return "sideway"
