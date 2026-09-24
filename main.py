import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Получаем ключи из переменных среды
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
    Ты — персональный ассистент Осипова Никиты Романовича (33 года, управляющий ресторана/бара).
    Твоя сфера: HoReCa (операционный менеджмент, аналитика, P&L, Food Cost, стандарты сервиса, обучение персонала).
    Стиль общения: деловой, структурированный, точный, с использованием профессионального сленга (ABC-анализ, чек-лист, ТТК, стоп-лист).
    Отвечай четко, проактивно и по делу.
    """
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Приветствую, Никита Романович! Ваш персональный Telegram-ассистент готов к работе. Направьте задачу или вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Отправляем индикатор печати
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обращении к нейросети: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
