# tools/__init__.py
# Importamos las herramientas de cada módulo
from .general_tools import obtener_fecha_y_hora_actual, generar_codigo_qr # <<< Esta es la línea que falla
from .bot_tools import mostrar_identificadores, obtener_estado_servidor, mostrar_menu
from .owner_tools import (
    mostrar_info_bot, 
    mostrar_owner, 
    solicitar_reinicio_bot, 
    solicitar_apagado_bot,
    silenciar_grupo,
    gestionar_bot_admin,
    configurar_mencion_owner,
    mostrar_info_codigo,
    mostrar_info_token
)

# Esta lista es la que el agente usará.
all_available_tools = [
    # General
    obtener_fecha_y_hora_actual, generar_codigo_qr,
    # Bot
    mostrar_identificadores, obtener_estado_servidor, mostrar_menu,
    # Owner
    mostrar_info_bot, mostrar_owner, solicitar_reinicio_bot, solicitar_apagado_bot,
    silenciar_grupo, gestionar_bot_admin, configurar_mencion_owner,
    mostrar_info_codigo, mostrar_info_token,
]