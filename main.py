
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
import asyncio
from flask import Flask
import threading
import random

MASTER_CHAT_ID = 5225197085
TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"

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
    "🍵 «Чайный пьяница — тот, кто трезво видит с закрытыми глазами.»",
    "🍵 «Пей чай, пока мысли не растворятся, как осадок в глине.»",
    "🍵 «Гвозди под ногами, чай в ладонях, и ты в себе.»",
    "🍵 «Тишина – это тоже вкус, просто редкий.»",
    "🍵 «Ушёл в пуэр — не ищите.»",
    "🍵 «В этом мире больше вкусов, чем решений.»",
    "🍵 «Тот, кто чувствует чай, не нуждается в словах.»"
]

NAME, DATE, PLACE, COMMENTS, PHONE, REMIND = range(6)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"
def run_flask():
    app.run(host="0.0.0.0", port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=MASTER_CHAT_ID, text=f"👋 @{user.username or 'гость'} запустил бота.")
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["🍵 Цитата дня от чайного пьяницы"],
        ["⏰ Напоминание", "💌 Оставить записку"],
        ["🤝 Поддержать проект"]
    ]
    await update.message.reply_text(
        "🛠️ Добро пожаловать в пространство *«Гвозди и Листья»* 🍃",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я не понял 🤔 Нажми кнопку ниже")

def main():
    threading.Thread(target=run_flask).start()
    app_ = ApplicationBuilder().token(TOKEN).build()
    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(MessageHandler(filters.COMMAND, unknown))
    app_.add_handler(MessageHandler(filters.TEXT, unknown))
    app_.run_polling()

if __name__ == "__main__":
    main()
