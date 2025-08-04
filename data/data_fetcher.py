from binance.client import Client
import pandas as pd

client = Client()

def get_klines(symbol='BTCUSDT', interval='5m', limit=210):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


# def fetch_btc_data():
#     btc_df = fetch_ohlcv('BTC/USDT', '1h', 50)
#     btc_df = add_indicators(btc_df)
#     btc_trend = determine_trend(btc_df)
#     return btc_trend

# def fetch_btcd_dominance():
#     dominance_df = fetch_ohlcv('BTC.D', '1h', 50)  # cần nguồn dữ liệu alt hoặc TradingView API
#     return determine_trend(dominance_df)
