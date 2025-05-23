import json
import sqlite3
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Подключение к базе данных
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS ruler_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    size INTEGER,
    timestamp TEXT
)
""")
conn.commit()

TOKEN = "8139242386:AAEcyLRZdfkOD2BmIAn3MbEm24XxXyGqecg"  # 🔁 Замени на токен

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📏 Узнать размер", web_app=WebAppInfo(url="https://твоя-ссылка.vercel.app"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Жми кнопку и узнай размер линейки!", reply_markup=reply_markup)

# Получение данных из WebApp
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        data = json.loads(update.message.web_app_data.data)
        size = data.get("size")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO ruler_data (user_id, username, size, timestamp) VALUES (?, ?, ?, ?)",
            (user.id, user.username or "", size, timestamp)
        )
        conn.commit()

        await update.message.reply_text(f"✅ Сохранено: {size} см")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
