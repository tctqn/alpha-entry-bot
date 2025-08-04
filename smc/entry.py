def find_entry_exit(df, trend):
    entry = df['close'].iloc[-1]
    if trend == "uptrend":
        sl = df['low'].iloc[-3]
        tp = entry + 2 * (entry - sl)
    elif trend == "downtrend":
        sl = df['high'].iloc[-3]
        tp = entry - 2 * (sl - entry)
    else:
        return None, None, None
    return entry, sl, tp
