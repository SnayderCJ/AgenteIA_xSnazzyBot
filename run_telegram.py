# run_telegram.py (Versión Final con Manejo de Errores)
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
from telegram.constants import ParseMode

# --- NUEVA IMPORTACIÓN PARA MANEJAR EL ERROR ESPECÍFICO ---
from google.api_core import exceptions as google_exceptions

from config import settings
from core.agent import run_agent
from utils.action_executor import execute_action
from utils.database import init_db, is_group_muted

# Configuración del logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


# --- Los manejadores de comandos y botones no cambian ---
async def direct_restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await execute_action({"action": "RESTART"}, update, context)

async def direct_shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await execute_action({"action": "SHUTDOWN"}, update, context)

async def menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context_data = {
        "chat_id": query.message.chat_id,
        "user_id": query.from_user.id
    }
    peticion = ""
    if query.data == 'menu_server':
        peticion = "dame el estado del servidor"
    elif query.data == 'menu_id':
        peticion = "cuál es mi id"
    elif query.data == 'menu_owner_info':
        peticion = "dame la info del bot"
    
    # --- AÑADIMOS EL MANEJO DE ERRORES AQUÍ TAMBIÉN ---
    if peticion:
        try:
            agent_result = await run_agent(peticion, context_data)
            text_response = agent_result.get("text")
            parse_mode = agent_result.get("action_data", {}).get("parse_mode")
            if text_response:
                await query.edit_message_text(text=text_response, parse_mode=parse_mode)
        except google_exceptions.ResourceExhausted:
            await query.edit_message_text(text="⚠️ **Sistema Sobrecargado.** Límite de solicitudes alcanzado. Inténtalo de nuevo mañana.")
        except Exception as e:
            logging.error(f"Error en menu_button_handler: {e}")
            await query.edit_message_text(text="Lo siento, ocurrió un error interno.")


# --- MANEJADOR PRINCIPAL CON BLOQUE TRY...EXCEPT ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    if update.message.chat.type != 'private' and is_group_muted(chat_id) and user.id != settings.SNAYDER_ID:
        logging.info(f"Mensaje ignorado en grupo silenciado {chat_id}")
        return

    context_data = {
        "chat_id": chat_id,
        "user_id": user.id,
    }
    if update.message.reply_to_message:
        context_data['user_id_to_manage'] = update.message.reply_to_message.from_user.id
    
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    try:
        # --- INICIA EL BLOQUE PROTEGIDO ---
        agent_result = await run_agent(update.message.text, context_data)
        
        text_response = agent_result.get("text")
        action_data = agent_result.get("action_data")
        parse_mode = action_data.get("parse_mode") if action_data else None

        if text_response:
            await update.message.reply_text(text_response, parse_mode=parse_mode)
        
        await execute_action(action_data, update, context)
        # --- TERMINA EL BLOQUE PROTEGIDO ---

    except google_exceptions.ResourceExhausted as e:
        # --- Si se atrapa el error de cuota, responde esto al usuario ---
        logging.warning(f"Límite de cuota de Gemini alcanzado: {e}")
        await update.message.reply_text(
            "⚠️ **Sistema Temporalmente Sobrecargado**\n\n"
            "Se ha alcanzado el límite de solicitudes gratuitas por hoy. "
            "Mis funciones de IA estarán disponibles de nuevo mañana.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    except Exception as e:
        # --- Si se atrapa cualquier otro error, responde esto ---
        logging.error(f"Error inesperado en el agente: {e}")
        await update.message.reply_text("Lo siento, ocurrió un error interno al procesar tu solicitud.")


def main() -> None:
    # ... (El resto de la función main no cambia) ...
    print("🤖 Iniciando xSnazzyBot (Modo Cerebro Único)...")
    init_db()
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("restart", direct_restart_command), group=0)
    application.add_handler(CommandHandler("shutdown", direct_shutdown_command), group=0)
    application.add_handler(CallbackQueryHandler(menu_button_handler), group=0)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler), group=1)

    print("✅ Bot en línea. Cerebro: Gemini.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()