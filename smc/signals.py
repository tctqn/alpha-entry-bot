def generate_signal(structure, latest):
    entry = None
    if structure['trend'] == "bullish" and latest['rsi'] < 30 and latest['macd'] > latest['macd_signal']:
        entry = "long"
    elif structure['trend'] == "bearish" and latest['rsi'] > 70 and latest['macd'] < latest['macd_signal']:
        entry = "short"

    if entry is None:
        return None

    signal = {
        "entry": entry,
        "price": latest['close'],
        "stoploss": latest['close'] * (0.98 if entry == "long" else 1.02),
        "takeprofit": latest['close'] * (1.04 if entry == "long" else 0.96),
    }
    return signal
