# run_telegram.py
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# Importamos desde nuestros nuevos módulos
from config import settings
from core.agent import run_agent
from utils.action_executor import execute_action

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador principal: recibe mensaje, lo pasa al agente y luego al ejecutor."""
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    agent_result = await run_agent(update.message.text)
    text_response = agent_result.get("text")
    action_data = agent_result.get("action_data")

    if text_response:
        await update.message.reply_text(text_response)

    await execute_action(action_data, update, context)

def main() -> None:
    """Función principal para iniciar el bot."""
    print("🤖 Iniciando xSnazzyBot con nueva arquitectura...")

    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Bot en línea. Habla con él en Telegram.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()