import psutil

def mostrar_identificadores(user_id: int, chat_id: int) -> dict:
    """
    Muestra el ID del usuario que envía el mensaje y el ID del chat actual.
    Necesita el 'user_id' y el 'chat_id' del contexto.
    """
    print("🛠️ Herramienta Bot llamada: mostrar_identificadores...")
    texto_respuesta = f"ID de Usuario: `{user_id}`\nID de este Chat: `{chat_id}`"
    return {"action": "SIMPLE_REPLY", "text": texto_respuesta}

def obtener_estado_servidor() -> dict:
    """
    Obtiene y muestra el estado actual de los recursos del servidor (CPU, RAM, Disco).
    """
    print("🛠️ Herramienta Bot llamada: obtener_estado_servidor...")
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    texto_respuesta = (
        "📊 **Estado del Servidor**\n\n"
        f"💻 **CPU:** {cpu}%\n"
        f"🧠 **RAM:** {ram}%\n"
        f"💾 **Disco:** {disk}%"
    )
    return {"action": "SIMPLE_REPLY", "text": texto_respuesta}

def mostrar_menu() -> dict:
    """
    Solicita la visualización de un menú interactivo con botones en el chat.
    """
    print("🛠️ Herramienta Bot llamada: mostrar_menu...")
    return {"action": "SHOW_MENU"}