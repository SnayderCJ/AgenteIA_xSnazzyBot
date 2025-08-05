from .general_tools import obtener_fecha_y_hora_actual, generar_codigo_qr
from .owner_tools import mostrar_info_bot, mostrar_owner, solicitar_reinicio_bot, solicitar_apagado_bot

# Esta lista es la que el agente usará.
# Cada vez que añadas una nueva función en cualquier archivo de tools,
# simplemente impórtala aquí y añádela a esta lista.
all_available_tools = [
    obtener_fecha_y_hora_actual,
    generar_codigo_qr,
    mostrar_info_bot,
    mostrar_owner,
    solicitar_reinicio_bot,
    solicitar_apagado_bot,
]