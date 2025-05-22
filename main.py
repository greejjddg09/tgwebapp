import json
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔹 Подключение к SQLite и создание таблицы, если не существует
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS webapp_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    data TEXT,
    ip TEXT,
    user_agent TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# 🔹 Команда /start — отправка кнопки с WebApp
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        KeyboardButton(
            "📏 Узнать размер",
            web_app=WebAppInfo(url="https://tgwebapp-mocha.vercel.app/")  # ← замени на свою ссылку
        )
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Жми кнопку ниже и узнай размер!", reply_markup=reply_markup)

# 🔹 Обработка данных от WebApp
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    data_raw = update.message.web_app_data.data

    try:
        data_json = json.loads(data_raw)
        size = data_json.get("size", "?")
        ip = data_json.get("ip", "")
        user_agent = data_json.get("ua", "")
    except Exception:
        size = data_raw
        ip = ""
        user_agent = ""

    cursor.execute(
        "INSERT INTO webapp_data (user_id, username, data, ip, user_agent) VALUES (?, ?, ?, ?, ?)",
        (user.id, user.username or "", size, ip, user_agent)
    )
    conn.commit()

    await update.message.reply_text(f"✅ Сохранил: {size}")

# 🔹 Запуск бота
def main():
    app = ApplicationBuilder().token("8139242386:AAEM27uS51BB8fWJAMXPbsxuY_-wS1HvYRM").build()  # ← вставь токен своего бота
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.run_polling()

if __name__ == "__main__":
    main()
