# utils/action_executor.py (Versión Simplificada)
import os
import sys
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import settings

async def execute_action(action_data: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Toma el diccionario de acción y ejecuta acciones que NO son respuestas de mensaje
    directas, como reinicios, apagados o menús.
    """
    if not action_data:
        return

    action_type = action_data.get("action")
    user_id = update.effective_user.id
    
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

    elif action_type == "SHOW_MENU":
        keyboard = [
            [InlineKeyboardButton("📊 Estado del Servidor", callback_data='menu_server')],
            [InlineKeyboardButton("🆔 Mostrar mis IDs", callback_data='menu_id')],
            [InlineKeyboardButton("ℹ️ Info del Bot (Owner)", callback_data='menu_owner_info')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Menú de opciones:", reply_markup=reply_markup)
        return