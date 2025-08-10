# Importamos las herramientas de cada módulo
from .general_tools import *
from .bot_tools import *
from .owner_tools import *
from .download_tools import *
from .ai_tools import *

all_available_tools = [
    
    # General
    obtener_fecha_y_hora_actual, generar_codigo_qr, acortar_url, buscar_imagen,
    obtener_info_ip, generar_enlace_mapa, convertir_a_morse, 
    invertir_texto, busqueda_web, consultar_registro_spf, obtener_vista_previa_web,
    
    # Bot
    mostrar_identificadores, obtener_estado_servidor, mostrar_menu,
    
    # Owner
    mostrar_info_bot, mostrar_owner, solicitar_reinicio_bot, solicitar_apagado_bot,
    silenciar_grupo, gestionar_bot_admin, configurar_mencion_owner,
    mostrar_info_codigo, mostrar_info_token,
    
    # Downloads
    descargar_multimedia, 
    # AI
    generar_imagen_ia,
]