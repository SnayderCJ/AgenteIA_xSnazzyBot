# utils/action_executor.py
import os
import sys
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode # Importamos ParseMode para el formato

from config import settings

async def execute_action(action_data: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Toma el diccionario de acción del agente y ejecuta la lógica correspondiente.
    Es el "brazo ejecutor" del bot.
    """
    if not action_data:
        return

    action_type = action_data.get("action")
    user_id = update.effective_user.id
    chat_id = update.message.chat_id
    text_to_send = action_data.get("text", "")
    parse_mode = action_data.get("parse_mode") # Obtenemos el modo de formato

    # --- Acciones que requieren ser Dueño ---
    if action_type in ["RESTART", "SHUTDOWN"]:
        if user_id != settings.SNAYDER_ID:
            await update.message.reply_text("Acción denegada. Se requiere autorización del propietario.")
            return

        if action_type == "RESTART":
            # El texto de confirmación ya lo envía la IA. Aquí solo ejecutamos.
            os.execv(sys.executable, ['python'] + sys.argv)
        
        elif action_type == "SHUTDOWN":
            # El texto de confirmación ya lo envía la IA. Aquí solo ejecutamos.
            async def _shutdown():
                await asyncio.sleep(1)
                await context.application.shutdown()
            asyncio.create_task(_shutdown())
            return

    # --- Acción para mostrar el menú interactivo ---
    elif action_type == "SHOW_MENU":
        keyboard = [
            [InlineKeyboardButton("📊 Estado del Servidor", callback_data='menu_server')],
            [InlineKeyboardButton("🆔 Mostrar mis IDs", callback_data='menu_id')],
            [InlineKeyboardButton("ℹ️ Info del Bot (Owner)", callback_data='menu_owner_info')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Menú de opciones:", reply_markup=reply_markup)
        return # Terminamos aquí, ya que el menú es la única respuesta

    # --- Lógica para enviar archivos generados por herramientas ---
    # Buscamos si la respuesta de la herramienta indica que se generó un archivo
    if isinstance(text_to_send, str) and "generado" in text_to_send and ".png" in text_to_send:
        try:
            # Extraemos el nombre del archivo del texto de respuesta
            filename = text_to_send.split("'")[1]
            if os.path.exists(filename):
                await context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))
                logging.info(f"Archivo {filename} enviado al chat {chat_id}")
        except Exception as e:
            logging.error(f"No se pudo extraer o enviar el archivo: {e}")

    # Nota: La respuesta de texto principal (`SIMPLE_REPLY`) ya se envía desde `run_telegram.py`.
    # Este archivo solo se encarga de las acciones *adicionales* o especiales.
    # Si en el futuro una acción necesitara enviar un texto específico, se añadiría aquí.
    # Por ejemplo, si una herramienta devolviera una acción "SEND_MARKDOWN_REPLY", aquí
    # se podría añadir un `elif` para manejar `update.message.reply_text(text_to_send, parse_mode=ParseMode.MARKDOWN)`.
    # Por ahora, la estructura actual es suficiente.