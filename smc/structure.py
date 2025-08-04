def detect_smc_structure(df, trend):
    recent = df.tail(5)
    if trend == "uptrend" and recent['high'].iloc[-1] > recent['high'].iloc[-2]:
        return True
    elif trend == "downtrend" and recent['low'].iloc[-1] < recent['low'].iloc[-2]:
        return True
    return False

def is_structure_confirmed(df, trend):
    recent = df.tail(10)
    if trend == 'uptrend':
        return recent['high'].iloc[-1] > recent['high'].iloc[-2]
    elif trend == 'downtrend':
        return recent['low'].iloc[-1] < recent['low'].iloc[-2]
    return False
