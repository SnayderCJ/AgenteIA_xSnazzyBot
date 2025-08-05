import os
import sys
import logging
import asyncio # Importamos asyncio para el apagado
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
            os.execv(sys.executable, ['python'] + sys.argv)
        
        elif action_type == "SHUTDOWN":
            await update.message.reply_text("Confirmado. Apagando sistemas. Adiós.")
            
            # --- LÓGICA DE APAGADO CORREGIDA ---
            async def _shutdown():
                # Damos un segundo para asegurar que todos los mensajes se envíen
                await asyncio.sleep(1)
                # Apagamos la aplicación de forma segura
                await context.application.shutdown()
            
            # Programamos la tarea de apagado para que se ejecute en segundo plano
            asyncio.create_task(_shutdown())
            return # Salimos del ejecutor para no procesar más cosas

    # --- El resto de la lógica sigue igual ---
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