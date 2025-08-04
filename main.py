import time
from data.data_fetcher import get_klines
from indicators.indicators import add_indicators
from utils.notifier import send_telegram_message
from smc.structure import detect_smc_structure
from smc.trend import determine_trend
from smc.entry import find_entry_exit
from smc.poi import detect_order_block
from smc.trigger import confirm_trigger, add_macd, is_momentum_strong
from utils.config_loader import load_config

config = load_config()
htf_timeframes = config["timeframes"]["HTF"]
entry_timeframes = config["timeframes"]["EntryTF"]

def analyze_symbol(symbol, bot_token, chat_id, last_signals):
    try:
        # 1️⃣ Xác định xu hướng và cấu trúc từ HTF
        trend_confirmed = False
        for htf in htf_timeframes:
            df_htf = get_klines(symbol, htf, limit=210)
            df_htf = add_indicators(df_htf)
            trend = determine_trend(df_htf)
            print(f"\n📈 [{symbol} - {htf}] Xu hướng: {trend}")

            if trend != "sideway" and detect_smc_structure(df_htf, trend):
                trend_confirmed = True
                break  # Dùng trend đầu tiên được xác nhận

        if not trend_confirmed:
            print(f"❌ Không có trend rõ ràng cho {symbol} ở HTF.")
            return

        # 2️⃣ Kiểm tra POI + Trigger + Momentum trên Entry TF
        for etf in entry_timeframes:
            df_etf = get_klines(symbol, etf, limit=210)
            df_etf = add_indicators(df_etf)
            order_block = detect_order_block(df_etf, trend)
            
            if order_block is None or None in order_block:
                print(f"⚠️ [{symbol} - {etf}] Không tìm thấy OB.")
                continue

            if not order_block:
                print(f"⚠️ [{symbol} - {etf}] Không tìm thấy OB.")
                continue

            if not confirm_trigger(df_etf, order_block, trend):
                print(f"⚠️ [{symbol} - {etf}] Chưa có trigger.")
                continue

            df_etf = add_macd(df_etf)
            if not is_momentum_strong(df_etf, trend):
                print(f"⚠️ [{symbol} - {etf}] Động lượng yếu.")
                continue

            # ✅ Nếu mọi điều kiện hợp lệ → gửi tín hiệu
            entry, sl, tp = find_entry_exit(df_etf, trend)
            signal_key = f"{symbol}_{trend}_{round(entry, 1)}"
            if last_signals.get(symbol) == signal_key:
                print("⚠️ Đã gửi tín hiệu này trước đó, không gửi lại.")
                return

            last_signals[symbol] = signal_key

            message = (
                f"📌 Tín hiệu giao dịch {symbol} ({etf})\n"
                f"▶️ Xu hướng: {trend.upper()}\n"
                f"💰 Entry: {entry:.2f}\n"
                f"🛑 Stoploss: {sl:.2f}\n"
                f"🎯 Take Profit: {tp:.2f}"
            )
            send_telegram_message(bot_token, chat_id, message)
            print("✅ Đã gửi tín hiệu Telegram")
            return  # ✅ Chỉ cần gửi 1 tín hiệu hợp lệ đầu tiên

        print(f"❌ Không có entry hợp lệ trên ETF cho {symbol}.")

    except Exception as e:
        print(f"🚨 Lỗi với {symbol}: {e}")

def main():
    bot_token = config["telegram"]["bot_token"]
    chat_id = config["telegram"]["chat_id"]
    symbols = config["symbols"]
    sleep_minutes = config["check_interval_minutes"]

    last_signals = {}

    while True:
        for symbol in symbols:
            analyze_symbol(symbol, bot_token, chat_id, last_signals)
        time.sleep(sleep_minutes * 60)

if __name__ == '__main__':
    main()
