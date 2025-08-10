from .general_tools import *
from .bot_tools import *
from .owner_tools import *
from .download_tools import *
from .ai_tools import *

# Esta lista es la que el agente usará.
all_available_tools = [
    # General
    obtener_fecha_y_hora_actual, generar_codigo_qr, acortar_url, buscar_imagen,
    obtener_info_ip, generar_enlace_mapa, convertir_a_morse,
    # Bot
    mostrar_identificadores, obtener_estado_servidor, mostrar_menu,
    # Owner
    mostrar_info_bot, mostrar_owner, solicitar_reinicio_bot, solicitar_apagado_bot,
    silenciar_grupo, gestionar_bot_admin, configurar_mencion_owner,
    mostrar_info_codigo, mostrar_info_token,
    # Downloads
    descargar_audio,
    # AI
    generar_imagen_ia,
]