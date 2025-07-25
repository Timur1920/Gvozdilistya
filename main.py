from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
import asyncio

# 🔧 Твои данные
MASTER_CHAT_ID = 5225197085
TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"

# 💾 Хранилище отзывов (10 последних)
last_reviews = []

# 📌 Состояния
NAME, DATE, PLACE, COMMENTS, REVIEW, REMIND = range(6)

# ▶️ Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["💬 Отзывы", "🤝 Поддержать проект"],
        ["⏰ Напоминание", "📲 Связь с мастером"]
    ]
    await update.message.reply_text(
        "🛠️ Добро пожаловать в пространство *«Гвозди и Листья»* 🍃\n\n"
        "🔩 Стояние на гвоздях\n"
        "🍵 Чайные церемонии\n"
        "💆 Банки\n"
        "🏕 Выездные практики в природе\n\n"
        "👇 Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# 🌿 О практике
async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Добро пожаловать в «Гвозди и Листья» — пространство для глубины, покоя и присутствия:\n\n"
        "🔩 Стояние на гвоздях — через боль к свободе\n"
        "🍵 Китайский чай (пуэр, улун, да хун пао) — как медитация\n"
        "🔥 Банки — древняя телесная практика\n"
        "🌀 Душевные разговоры — по-настоящему\n"
        "🏕 Выездные церемонии в лесу или на природе\n\n"
        "Ты можешь записаться, задать вопрос или просто побыть рядом 🌿"
    )

# 📅 Заявка
async def sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Когда удобно провести сессию? (дата/время)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text
    await update.message.reply_text("Где провести? (дома, на природе или у меня в гостях?)")
    return PLACE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['place'] = update.message.text
    await update.message.reply_text("Есть пожелания или вопросы? Если нет, то просто укажи свой номер телефона📱")
    return COMMENTS

async def get_comments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['comments'] = update.message.text
    user = update.message.from_user

    text = (
        f"📥 *Новая заявка:*\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📅 Время: {context.user_data['date']}\n"
        f"📍 Место: {context.user_data['place']}\n"
        f"💬 Пожелания: {context.user_data['comments']}\n"
        f"Telegram: @{user.username}"
    )

    await context.bot.send_message(chat_id=MASTER_CHAT_ID, text=text, parse_mode="Markdown")
    await update.message.reply_text("Заявка отправлена! Я скоро с тобой свяжусь 🙌")
    return ConversationHandler.END

# 💬 Отзывы
async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["✍️ Оставить отзыв", "👀 Посмотреть отзывы"],
        ["🔙 Назад"]
    ]
    await update.message.reply_text(
        "Выбери, что хочешь сделать с отзывами:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def review_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пришли свой отзыв: можешь написать, прикрепить фото или видео 🙏")
    return REVIEW

async def receive_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"✍️ Новый отзыв от @{user.username or 'аноним'}"

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await context.bot.send_photo(MASTER_CHAT_ID, file_id, caption=caption)
        last_reviews.append(('photo', file_id, caption))
    elif update.message.video:
        file_id = update.message.video.file_id
        await context.bot.send_video(MASTER_CHAT_ID, file_id, caption=caption)
        last_reviews.append(('video', file_id, caption))
    elif update.message.text:
        await context.bot.send_message(MASTER_CHAT_ID, f"{caption}\n\n{update.message.text}")
        last_reviews.append(('text', update.message.text, caption))
    else:
        await update.message.reply_text("Формат не поддерживается 😢")
        return ConversationHandler.END

    if len(last_reviews) > 10:
        last_reviews.pop(0)

    await update.message.reply_text("Спасибо за отзыв! 🌟")
    return ConversationHandler.END

async def show_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not last_reviews:
        await update.message.reply_text("Пока нет отзывов. Будь первым!")
        return

    await update.message.reply_text("🗂 Это крайние 10 отзывов:")

    for kind, content, caption in last_reviews:
        if kind == 'photo':
            await update.message.reply_photo(content, caption=caption)
        elif kind == 'video':
            await update.message.reply_video(content, caption=caption)
        elif kind == 'text':
            await update.message.reply_text(f"{caption}\n\n{content}")

# 🤝 Поддержка
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💚 Хочешь поддержать проект?\n\n"
        "📲 Перевод по номеру: *+7 912 852‑81‑81*\n"
        "_Сбербанк / Т-Банк_ ну или за чайной церемонией 🐲",
        parse_mode="Markdown"
    )

# 📲 Связь
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📲 Связь с Тимуром: @Timpimi")

# ⏰ Напоминание
async def reminder_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Через сколько минут напомнить тебе попить чай или сделать выдох? 🫖")
    return REMIND

async def reminder_wait(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(update.message.text)
        await update.message.reply_text(f"⏳ Ок, напомню через {minutes} минут 🍵")

        await asyncio.sleep(minutes * 60)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="🍵 Время на чай или глубокий выдох ☁️")
    except:
        await update.message.reply_text("Напиши просто число минут, например 10")

    return ConversationHandler.END

# 🔙 Назад
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)

# ❓ Неизвестные сообщения
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Не понял тебя 🙃 Нажми кнопку ниже!")

# ▶️ Главная
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    signup_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Записаться") | filters.Regex("📅 Записаться"), sign_up)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_place)],
            COMMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comments)],
        },
        fallbacks=[]
    )

    review_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("✍️ Оставить отзыв"), review_entry)],
        states={ REVIEW: [MessageHandler(filters.ALL, receive_review)] },
        fallbacks=[]
    )

    remind_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("⏰ Напоминание"), reminder_set)],
        states={ REMIND: [MessageHandler(filters.TEXT & ~filters.COMMAND, reminder_wait)] },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(signup_conv)
    app.add_handler(review_conv)
    app.add_handler(remind_conv)
    app.add_handler(MessageHandler(filters.Regex("🧘 О практике"), practice))
    app.add_handler(MessageHandler(filters.Regex("🤝 Поддержать проект"), support))
    app.add_handler(MessageHandler(filters.Regex("📲 Связь с мастером"), contact))
    app.add_handler(MessageHandler(filters.Regex("💬 Отзывы"), reviews))
    app.add_handler(MessageHandler(filters.Regex("👀 Посмотреть отзывы"), show_reviews))
    app.add_handler(MessageHandler(filters.Regex("🔙 Назад"), back_to_menu))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(MessageHandler(filters.TEXT, unknown))

    app.run_polling()

if __name__ == "__main__":
    main()
