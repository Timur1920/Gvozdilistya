import asyncio
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)

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

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

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

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.COMMAND, unknown))
application.add_handler(MessageHandler(filters.TEXT, unknown))

@app.route('/')
def home():
    return "Bot is running"

@app.post(f"/{TOKEN}")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.create_task(application.process_update(update))
    return "ok"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    bot.set_webhook(f"https://gvozdilistya.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=port)
