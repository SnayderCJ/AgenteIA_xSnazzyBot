# utils/action_executor.py (Versión con Apagado Directo)
import os
import sys
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import settings

async def execute_action(action_data: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toma el diccionario de acción y ejecuta la lógica correspondiente."""
    if not action_data:
        return

    action_type = action_data.get("action")
    user_id = update.effective_user.id
    chat_id = update.message.chat_id

    if action_type in ["RESTART", "SHUTDOWN"]:
        if user_id != settings.SNAYDER_ID:
            await update.message.reply_text("Acción denegada. Se requiere autorización del propietario.")
            return

        if action_type == "RESTART":
            await update.message.reply_text("Confirmado. Reiniciando el sistema...")
            # os.execv reemplaza el proceso actual con uno nuevo, reiniciando el script.
            os.execv(sys.executable, ['python'] + sys.argv)
        
        elif action_type == "SHUTDOWN":
            await update.message.reply_text("Confirmado. Apagando sistemas. Adiós.")
            # --- SOLUCIÓN FINAL ---
            # Usamos sys.exit() para terminar el proceso de Python de forma limpia e inmediata
            # después de enviar el mensaje final. Es el método más fiable.
            sys.exit("Apagado seguro solicitado por el propietario.")
            # --------------------

    # --- El resto de la lógica para otras acciones sigue igual ---
    if action_type == "SIMPLE_REPLY":
        pass

    text_from_tool = action_data.get("text", "")
    if isinstance(text_from_tool, str) and "generado" in text_from_tool and ".png" in text_from_tool:
        try:
            filename = text_from_tool.split("'")[1]
            if os.path.exists(filename):
                await context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))
                logging.info(f"Archivo {filename} enviado al chat {chat_id}")
        except Exception as e:
            logging.error(f"No se pudo extraer o enviar el archivo: {e}")