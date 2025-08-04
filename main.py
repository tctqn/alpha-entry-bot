import time
import os
from dotenv import load_dotenv
from data.data_fetcher import get_klines
from indicators.indicators import add_indicators
from utils.notifier import send_signal_telegram
from smc.structure import detect_structure
from smc.trend import determine_trend
from smc.entry import find_entry_exit
from smc.poi import detect_order_block
from smc.trigger import confirm_trigger, add_macd, is_momentum_strong
from utils.config_loader import load_config

# Load .env và config
load_dotenv()
config = load_config()

style = os.getenv("STYLE", "swing")
timeframes = config["timeframes"].get(style, {"HTFs": [], "LTFs": []})
htf_timeframes = timeframes["HTFs"]
entry_timeframes = timeframes["LTFs"]

def analyze_symbol(symbol, bot_token, chat_id, last_signals):
    try:
        trend_confirmed = False
        trend = None

        for htf in htf_timeframes:
            print(f"Đang lấy dữ liệu cho {symbol} với khung {htf}")
            df_htf = get_klines(symbol, htf, limit=210)
            df_htf = add_indicators(df_htf)
            trend = determine_trend(df_htf)
            print(f"\n📈 [{symbol} - {htf}] Xu hướng: {trend}")

            if trend != "sideway" and detect_structure(df_htf, trend):
                trend_confirmed = True
                break

        if not trend_confirmed:
            print(f"❌ Không có trend rõ ràng cho {symbol} ở HTF.")
            return

        for etf in entry_timeframes:
            print(f"Đang lấy dữ liệu cho {symbol} với khung {etf}")
            df_etf = get_klines(symbol, etf, limit=210)
            df_etf = add_indicators(df_etf)
            order_block = detect_order_block(df_etf, trend)

            if order_block is None:
                print(f"⚠️ [{symbol} - {etf}] Không tìm thấy Order Block.")
                continue

            if not confirm_trigger(df_etf, order_block, trend):
                print(f"⚠️ [{symbol} - {etf}] Chưa có trigger hợp lệ.")
                continue

            df_etf = add_macd(df_etf)
            if not is_momentum_strong(df_etf, trend):
                print(f"⚠️ [{symbol} - {etf}] Động lượng yếu.")
                continue

            entry, sl, tp = find_entry_exit(df_etf, trend)
            if None in (entry, sl, tp):
                print(f"⚠️ [{symbol} - {etf}] Entry/SL/TP không hợp lệ.")
                continue

            signal_key = f"{symbol}_{trend}_{round(entry, 1)}"
            if last_signals.get(symbol) == signal_key:
                print("⚠️ Đã gửi tín hiệu này trước đó, bỏ qua.")
                return

            last_signals[symbol] = signal_key

            message = (
                f"📌 Tín hiệu giao dịch cho {symbol} ({etf})\n"
                f"▶️ Xu hướng: {trend.upper()}\n"
                f"💰 Entry: {entry:.2f}\n"
                f"🛑 Stoploss: {sl:.2f}\n"
                f"🎯 Take Profit: {tp:.2f}"
            )
            send_signal_telegram(bot_token, chat_id, message)
            print("✅ Đã gửi tín hiệu Telegram.")
            return

        print(f"❌ Không có entry hợp lệ trên ETF cho {symbol}.")

    except Exception as e:
        print(f"🚨 Lỗi khi phân tích {symbol}: {e}")

def main():
    bot_token = config["TELEGRAM_TOKEN"]
    chat_id = config["TELEGRAM_CHAT_ID"]
    symbols = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
    sleep_minutes = int(os.getenv("CHECK_INTERVAL_MINUTES", 5))

    last_signals = {}

    while True:
        for symbol in symbols:
            analyze_symbol(symbol.strip(), bot_token, chat_id, last_signals)
        time.sleep(sleep_minutes * 60)

if __name__ == '__main__':
    main()
