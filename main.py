from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)
import os
import random
from flask import Flask, request
import asyncio

# 🔧 Конфигурация
TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"
MASTER_CHAT_ID = 5225197085
BOT_USERNAME = "Gvozdi_i_Listya_Bot"
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://gvozdilistya.onrender.com{WEBHOOK_PATH}"

# 🍵 Цитаты
TEA_QUOTES = [
    "🍵 «Пей чай, и всё само расставится по местам.»",
    "🍵 «Чай не решает проблемы, но делает их теплее.»",
    "🍵 «Когда не знаешь, что делать — завари чай.»",
    "🍵 «Чай не торопит. В нём вечность на кончике пиалы.»",
    "🍵 «Даже молчание со вкусом чая становится разговором.»",
    "🍵 «Ум успокаивается, когда в руках горячая пиала.»",
    "🍵 «Жизнь не в суете. Жизнь в чае.»",
    "🍵 «Каждая церемония — возвращение домой.»",
    "🍵 «Тот, кто пьёт чай, уже не спешит.»",
    "🍵 «Чайный пьяница — тот, кто трезво видит с закрытыми глазами.»"
]

# Состояния
NAME, DATE, PLACE, COMMENTS, PHONE, REMIND, NOTE = range(7)

# Flask
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Flask роут
@flask_app.post(WEBHOOK_PATH)
async def webhook():
    await telegram_app.update_queue.put(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "OK", 200

@flask_app.get("/")
def home():
    return "Бот запущен!"

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(MASTER_CHAT_ID, f"👋 @{update.effective_user.username or 'гость'} запустил бота.")
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["🍵 Цитата дня от чайного пьяницы"],
        ["⏰ Напоминание", "💌 Оставить записку"],
        ["🤝 Поддержать проект"]
    ]
    await update.message.reply_text(
        "🛠️ Добро пожаловать в пространство *«Гвозди и Листья»* 🍃\n\n"
        "👇 Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# Остальной код не меняется (цитаты, записки, запись, напоминания и т.п.)

# Добавим сюда конец
def run():
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.Regex("🍵 Цитата дня от чайного пьяницы"), tea_quote))
    telegram_app.add_handler(MessageHandler(filters.COMMAND, unknown))
    telegram_app.add_handler(MessageHandler(filters.TEXT, unknown))

    telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    flask_app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    run()
