from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update: Update, context):
    keyboard = [[
        KeyboardButton("📏 Узнать размер", web_app=WebAppInfo(url="https://your-mini-app-url.vercel.app"))
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Жми на кнопку!", reply_markup=reply_markup)

app = ApplicationBuilder().token("8139242386:AAEM27uS51BB8fWJAMXPbsxuY_-wS1HvYRM").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
