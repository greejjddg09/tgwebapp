import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Создаём таблицу, если нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS webapp_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    data TEXT
)
''')
conn.commit()

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = update.message.web_app_data.data

    cursor.execute('INSERT INTO webapp_data (user_id, data) VALUES (?, ?)', (user_id, data))
    conn.commit()

    await update.message.reply_text(f"Данные сохранены: {data}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Жду данные из WebApp.")

def main():
    app = ApplicationBuilder().token("8139242386:AAEM27uS51BB8fWJAMXPbsxuY_-wS1HvYRM").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    app.run_polling()

if __name__ == "__main__":
    main()
