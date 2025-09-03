import asyncio
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8471689023:AAFZZqQ6KGs5EXuP0mtUqpQXkhK0ZB0rBBA"
ADMIN_ID = 1437371039  # твой Telegram ID

# Таблица значений (1–64)
slot_table = {
    1: "🍷🍷🍷", 2: "🍒🍷🍷", 3: "🍋🍷🍷", 4: "7️⃣🍷🍷",
    5: "🍷🍒🍷", 6: "🍒🍒🍷", 7: "🍋🍒🍷", 8: "7️⃣🍒🍷",
    9: "🍷🍋🍷", 10: "🍒🍋🍷", 11: "🍋🍋🍷", 12: "7️⃣🍋🍷",
    13: "🍷7️⃣🍷", 14: "🍒7️⃣🍷", 15: "🍋7️⃣🍷", 16: "7️⃣7️⃣🍷",
    17: "🍷🍷🍒", 18: "🍒🍷🍒", 19: "🍋🍷🍒", 20: "🍒7️⃣🍒",
    21: "🍷🍒🍒", 22: "🍒🍒🍒", 23: "🍋🍒🍒", 24: "7️⃣🍒🍒",
    25: "🍷🍋🍒", 26: "🍒🍋🍒", 27: "🍋🍋🍒", 28: "7️⃣🍋🍒",
    29: "🍷7️⃣🍒", 30: "🍒7️⃣🍒", 31: "🍋7️⃣🍒", 32: "7️⃣7️⃣🍒",
    33: "🍷🍷🍋", 34: "🍒🍷🍋", 35: "🍋🍷🍋", 36: "7️⃣🍷🍋",
    37: "🍷🍒🍋", 38: "🍒🍒🍋", 39: "🍋🍒🍋", 40: "7️⃣🍒🍋",
    41: "🍷🍋🍋", 42: "🍒🍋🍋", 43: "🍋🍋🍋", 44: "7️⃣🍋🍋",
    45: "🍷7️⃣🍋", 46: "🍒7️⃣🍋", 47: "🍋7️⃣🍋", 48: "7️⃣7️⃣🍋",
    49: "🍷🍷7️⃣", 50: "🍒🍷7️⃣", 51: "🍋🍷7️⃣", 52: "7️⃣🍷7️⃣",
    53: "🍷🍒7️⃣", 54: "🍒🍒7️⃣", 55: "🍋🍒7️⃣", 56: "7️⃣🍒7️⃣",
    57: "🍷🍋7️⃣", 58: "🍒🍋7️⃣", 59: "🍋🍋7️⃣", 60: "7️⃣🍋7️⃣",
    61: "🍷7️⃣7️⃣", 62: "🍒7️⃣7️⃣", 63: "🍋7️⃣7️⃣", 64: "7️⃣7️⃣7️⃣"
}

# Варианты фраз
jackpot_responses = [
    "🎉 Джекпот! Бог слот-машины улыбнулся!",
    "🔥 Удача на твоей стороне, это три семёрки!",
    "💰 Ты сорвал куш! Теперь можешь открывать казино.",
    "🎰 777! Если бы это было в Вегасе — ты бы уже был миллионером."
]

medium_responses = [
    "🍋🍋🍋! Средний куш, забирай приз! 🤑",
    "Лимончики сыграли! 🍋🍋🍋 — не джекпот, но приятно.",
    "🍋🍋🍋 — кисленькая, но прибыльная комбинация."
]

small_responses = [
    "🍒🍒🍒! Маленький выигрыш, но начало есть! 🍒",
    "Три вишенки 🍒🍒🍒 — держи утешительный приз.",
    "🍒🍒🍒 — мелочь, а приятно."
]

lose_responses = [
    "❌ Не повезло... автомат смеётся.",
    "😅 Увы, сегодня без выигрыша.",
    "🙃 Почти! Но нет.",
    "🚬 Автомат съел монетку и молчит."
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            "Привет! Я работаю только в группе. Добавь меня в группу 🎰"
        )
    else:
        await update.message.reply_text(
            "Привет, я готов крутить 🎰 в этой группе! Отправь 🎰 чтобы испытать удачу."
        )

# Обработка бросков эмодзи
async def handle_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type

    if chat_type == "private":
        await update.message.reply_text("Я работаю только в группе 🎰")
        return

    if update.message and update.message.dice:
        emoji = update.message.dice.emoji
        value = update.message.dice.value
        user = update.message.from_user

        if emoji == "🎰":
            await asyncio.sleep(2)  # задержка
            combo = slot_table.get(value, f"неизвестно ({value})")
            mention = f"@{user.username}" if user.username else user.first_name

            chat = update.message.chat
            if chat.username:
                msg_link = f"https://t.me/{chat.username}/{update.message.message_id}"
            else:
                msg_link = "(группа приватная, ссылка недоступна)"

            if combo == "7️⃣7️⃣7️⃣":  # джекпот
                reply = f"{mention} покрутил и выпало:\n {combo}\n{random.choice(jackpot_responses)}"
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"🔥 У {mention} выпал ДЖЕКПОТ! 🎰 ({combo})\nСсылка: {msg_link}"
                )

            elif combo == "🍋🍋🍋":  # средний выигрыш
                reply = f"{mention} покрутил и выпало:\n {combo}\n{random.choice(medium_responses)}"
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"⚡ У {mention} средний выигрыш! 🍋🍋🍋 ({combo})\nСсылка: {msg_link}"
                )

            elif combo == "🍒🍒🍒":  # маленький выигрыш
                reply = f"{mention} покрутил и выпало:\n {combo}\n{random.choice(small_responses)}"
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"🍒 У {mention} маленький выигрыш! 🍒🍒🍒 ({combo})\nСсылка: {msg_link}"
                )

            else:  # проигрыш
                reply = f"{mention} покрутил и выпало:\n {combo}\n{random.choice(lose_responses)}"

        else:
            await asyncio.sleep(2)
            reply = f"{emoji} Выпало: {value}"

        await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Dice.ALL, handle_dice))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
