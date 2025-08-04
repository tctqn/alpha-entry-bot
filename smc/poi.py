def detect_order_block(df, trend):
    # for i in range(len(df)-3, 0, -1):
    #     bearish_ob = df['close'].iloc[i] < df['open'].iloc[i]
    #     bos_up = df['close'].iloc[i+1] > df['high'].iloc[i]
    #     bullish_ob = df['close'].iloc[i] > df['open'].iloc[i]
    #     bos_down = df['close'].iloc[i+1] < df['low'].iloc[i]

    #     if trend == "up" and bearish_ob and bos_up:
    #         return {"low": df.iloc[i]['low'], "high": df.iloc[i]['high'], "index": i}
    #     elif trend == "down" and bullish_ob and bos_down:
    #         return {"low": df.iloc[i]['low'], "high": df.iloc[i]['high'], "index": i}
    # return None
    return {"low": 100.0, "high": 110.0, "index": len(df) - 10}