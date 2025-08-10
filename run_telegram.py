# run_telegram.py (Versión con Lógica de Envío Unificada)
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler
)

from config import settings
from core.agent import run_agent
from utils.action_executor import execute_action
from utils.database import init_db, is_group_muted

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Los manejadores de comandos y botones no cambian ---
# (direct_restart_command, direct_shutdown_command, menu_button_handler se mantienen igual)
async def direct_restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await execute_action({"action": "RESTART"}, update, context)

async def direct_shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await execute_action({"action": "SHUTDOWN"}, update, context)

async def menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context_data = {"chat_id": query.message.chat_id, "user_id": query.from_user.id}
    peticion = ""
    if query.data == 'menu_server': peticion = "dame el estado del servidor"
    elif query.data == 'menu_id': peticion = "cuál es mi id"
    elif query.data == 'menu_owner_info': peticion = "dame la info del bot"
    if peticion:
        agent_result = await run_agent(peticion, context_data)
        text_response = agent_result.get("text")
        parse_mode = agent_result.get("action_data", {}).get("parse_mode")
        if text_response:
            await query.edit_message_text(text=text_response, parse_mode=parse_mode)

# --- MANEJADOR PRINCIPAL REESTRUCTURADO ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    if update.message.chat.type != 'private' and is_group_muted(chat_id) and user.id != settings.SNAYDER_ID:
        return

    context_data = {"chat_id": chat_id, "user_id": user.id}
    if update.message.reply_to_message:
        context_data['user_id_to_manage'] = update.message.reply_to_message.from_user.id
    
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    try:
        agent_result = await run_agent(update.message.text, context_data)
        text_response = agent_result.get("text")
        action_data = agent_result.get("action_data")
        
        # --- NUEVA LÓGICA DE RESPUESTA UNIFICADA ---
        # Primero, revisamos si la acción principal es enviar un archivo.
        action_type = action_data.get("action") if action_data else None

        if action_type == "SEND_FILE":
            # Si la acción es enviar un archivo, el texto de la IA va como pie de foto.
            path = action_data.get("path")
            if path and os.path.exists(path):
                with open(path, 'rb') as photo_file:
                    await update.message.reply_photo(photo=photo_file, caption=text_response)
            else:
                await update.message.reply_text("Error: El archivo que solicité no se pudo encontrar.")
        
        elif text_response:
            # Si no es un archivo, simplemente enviamos la respuesta de texto.
            parse_mode = action_data.get("parse_mode") if action_data else None
            await update.message.reply_text(text_response, parse_mode=parse_mode)

        # Finalmente, pasamos la acción al ejecutor por si necesita hacer algo MÁS
        # (como reiniciar, apagar, etc., que no son respuestas directas)
        await execute_action(action_data, update, context)
        # ------------------------------------------------
        
    except Exception as e:
        logging.error(f"Error mayor en message_handler: {e}", exc_info=True)
        await update.message.reply_text("Lo siento, ocurrió un error crítico al procesar tu solicitud.")

def main() -> None:
    """Función principal que configura e inicia el bot."""
    print("🤖 Iniciando xSnazzyBot con arquitectura unificada...")
    init_db()
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("restart", direct_restart_command), group=0)
    application.add_handler(CommandHandler("shutdown", direct_shutdown_command), group=0)
    application.add_handler(CallbackQueryHandler(menu_button_handler), group=0)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler), group=1)

    print("✅ Bot en línea.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()