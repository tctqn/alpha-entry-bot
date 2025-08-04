def detect_structure(data, trend=None):
    latest = data.iloc[-1]
    previous = data.iloc[-2]

    current_trend = trend or ("bullish" if latest['ema50'] > latest['ema200'] else "bearish")

    choch = (
        (previous['ema50'] < previous['ema200'] and latest['ema50'] > latest['ema200']) or
        (previous['ema50'] > previous['ema200'] and latest['ema50'] < latest['ema200'])
    )

    return {
        "trend": current_trend,
        "choch": choch,
    }
