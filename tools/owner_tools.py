def mostrar_info_bot() -> dict:
    """Muestra información predefinida sobre el bot."""
    print("🛠️ Herramienta Owner llamada: mostrar_info_bot...")
    info = "Soy xSnazzyBot, un asistente virtual con IA. Mi creador es Snayder."
    return {"action": "SIMPLE_REPLY", "text": info}

def mostrar_owner() -> dict:
    """Proporciona el nombre del propietario y creador del bot."""
    print("🛠️ Herramienta Owner llamada: mostrar_owner...")
    owner_info = "Mi propietario y creador es Snayder."
    return {"action": "SIMPLE_REPLY", "text": owner_info}

def solicitar_reinicio_bot() -> dict:
    """Solicita un reinicio del script del bot. Acción sensible solo para el dueño."""
    print("🛠️ Herramienta Owner llamada: solicitar_reinicio_bot...")
    return {"action": "RESTART"}

def solicitar_apagado_bot() -> dict:
    """Solicita apagar el bot por completo. Acción sensible solo para el dueño."""
    print("🛠️ Herramienta Owner llamada: solicitar_apagado_bot...")
    return {"action": "SHUTDOWN"}