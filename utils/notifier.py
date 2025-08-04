import requests
import json
from datetime import datetime
from utils.config_loader import load_config

config = load_config()
TELEGRAM_BOT_TOKEN = config["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]

def send_signal_telegram(signal, chart_path=None):
    text = f"""
📊 Signal Alert
Entry: {signal['entry'].upper()}
Price: {signal['price']:.2f}
Stoploss: {signal['stoploss']:.2f}
Takeprofit: {signal['takeprofit']:.2f}
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text.strip()})

    if chart_path:
        with open(chart_path, 'rb') as photo:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                files={'photo': photo},
                data={'chat_id': TELEGRAM_CHAT_ID}
            )

def save_log(signal, filepath):
    log_entry = {
        "time": datetime.utcnow().isoformat(),
        "signal": signal
    }
    with open(filepath, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
