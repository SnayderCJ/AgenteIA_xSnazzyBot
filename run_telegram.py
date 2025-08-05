import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler # <<< Importamos CommandHandler

# Importamos desde nuestros nuevos módulos
from config import settings
from core.agent import run_agent
from utils.action_executor import execute_action

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- NUEVAS FUNCIONES PARA COMANDOS DIRECTOS ---

async def direct_restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ejecuta la acción de reinicio directamente, solo para el dueño."""
    action_data = {"action": "RESTART"}
    # Llamamos directamente al ejecutor de acciones
    await execute_action(action_data, update, context)

async def direct_shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ejecuta la acción de apagado directamente, solo para el dueño."""
    action_data = {"action": "SHUTDOWN"}
    # Llamamos directamente al ejecutor de acciones
    await execute_action(action_data, update, context)

# ------------------------------------------------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para la IA que recibe todos los mensajes de texto normales."""
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    agent_result = await run_agent(update.message.text)
    text_response = agent_result.get("text")
    action_data = agent_result.get("action_data")

    if text_response:
        await update.message.reply_text(text_response)
    
    await execute_action(action_data, update, context)

def main() -> None:
    """Función principal para iniciar el bot."""
    print("🤖 Iniciando xSnazzyBot con arquitectura híbrida...")
    
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # --- REGISTRO DE MANEJADORES ---
    # Prioridad 0 (la más alta): Comandos directos y críticos
    application.add_handler(CommandHandler("restart", direct_restart_command), group=0)
    application.add_handler(CommandHandler("shutdown", direct_shutdown_command), group=0)

    # Prioridad 1 (la más baja): Manejador general de la IA
    # Se activará para cualquier mensaje de texto que NO sea uno de los comandos de arriba.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler), group=1)

    print("✅ Bot en línea. Usa comandos directos (/restart, /shutdown) o habla con la IA.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()