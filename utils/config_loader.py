from dotenv import load_dotenv
import os

TIMEFRAMES = {
    "position": {
        "HTFs": ["1M", "1w", "3d"],
        "LTFs": ["1d", "4h"]
    },
    "swing": {
        "HTFs": ["1d", "12h", "6h"],
        "LTFs": ["4h", "2h", "1h"]
    },
    "intraday": {
        "HTFs": ["4h", "2h", "1h"],
        "LTFs": ["30m", "15m", "5m"]
    },
    "scalp": {
        "HTFs": ["1h", "30m", "15m"],
        "LTFs": ["5m", "1m"]
    }
}


def load_config(path=".env"):
    load_dotenv(dotenv_path=path)
    return {
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "BINANCE_API_KEY": os.getenv("BINANCE_API_KEY"),
        "BINANCE_API_SECRET": os.getenv("BINANCE_API_SECRET"),
        "timeframes": TIMEFRAMES
    }

