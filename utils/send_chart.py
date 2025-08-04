import matplotlib.pyplot as plt
import requests
import io

def plot_and_send_chart(df, ob, symbol, tf, trend, telegram_token, chat_id):
    plt.figure(figsize=(12, 6))
    plt.plot(df['close'], label='Close Price')
    plt.axhline(ob['high'], color='r', linestyle='--', label='OB High')
    plt.axhline(ob['low'], color='g', linestyle='--', label='OB Low')
    plt.title(f"{symbol} - {tf} - {trend.upper()} Trend")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    requests.post(
        f"https://api.telegram.org/bot{telegram_token}/sendPhoto",
        data={"chat_id": chat_id},
        files={"photo": buf}
    )
    buf.close()
