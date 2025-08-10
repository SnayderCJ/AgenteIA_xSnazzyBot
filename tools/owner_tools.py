from utils import database

# --- Herramientas de Información (no necesitan contexto extra) ---
def mostrar_info_bot() -> dict:
    print("🛠️ Herramienta Owner llamada: mostrar_info_bot...")
    info = "Soy xSnazzyBot, un asistente virtual con IA. Mi creador es Snayder."
    return {"action": "SIMPLE_REPLY", "text": info}

def mostrar_owner() -> dict:
    print("🛠️ Herramienta Owner llamada: mostrar_owner...")
    owner_info = "Mi propietario y creador es Snayder."
    return {"action": "SIMPLE_REPLY", "text": owner_info}

# --- Herramientas de Control del Bot (no necesitan contexto extra) ---
def solicitar_reinicio_bot() -> dict:
    print("🛠️ Herramienta Owner llamada: solicitar_reinicio_bot...")
    return {"action": "RESTART"}

def solicitar_apagado_bot() -> dict:
    print("🛠️ Herramienta Owner llamada: solicitar_apagado_bot...")
    return {"action": "SHUTDOWN"}

# --- Herramientas de Gestión (AHORA CON CONTEXTO) ---
def silenciar_grupo(chat_id: int, silenciar: bool) -> dict:
    """Activa o desactiva el modo silencio para el bot en el chat de grupo actual."""
    print(f"🛠️ Herramienta Owner llamada: silenciar_grupo (chat_id={chat_id}, silenciar={silenciar})...")
    database.set_group_mute(chat_id, silenciar)
    estado = "silenciado" if silenciar else "reactivado"
    return {"action": "SIMPLE_REPLY", "text": f"Confirmado. El bot ha sido {estado} en este grupo."}

def gestionar_bot_admin(user_id_to_manage: int, accion: str) -> dict:
    """Gestiona la lista de admins del bot, basado en el usuario al que se está respondiendo."""
    print(f"🛠️ Herramienta Owner llamada: gestionar_bot_admin (user_id={user_id_to_manage}, accion={accion})...")
    if accion.lower() == 'agregar':
        database.add_bot_admin(user_id_to_manage)
        return {"action": "SIMPLE_REPLY", "text": f"Confirmado. Usuario {user_id_to_manage} añadido como admin del bot."}
    elif accion.lower() == 'remover':
        database.remove_bot_admin(user_id_to_manage)
        return {"action": "SIMPLE_REPLY", "text": f"Confirmado. Usuario {user_id_to_manage} removido como admin del bot."}
    return {"action": "SIMPLE_REPLY", "text": "Acción no válida. Use 'agregar' o 'remover'."}

def configurar_mencion_owner(activar: bool) -> dict:
    """Activa o desactiva la mención automática al propietario."""
    print(f"🛠️ Herramienta Owner llamada: configurar_mencion_owner (activar={activar})...")
    database.update_setting('mention_owner', str(activar))
    estado = "activada" if activar else "desactivada"
    return {"action": "SIMPLE_REPLY", "text": f"Confirmado. La mención automática al propietario ha sido {estado}."}

def mostrar_info_codigo() -> dict:
    """
    Proporciona información sobre el código fuente del bot, como un enlace al repositorio.
    """
    print("🛠️ Herramienta Owner llamada: mostrar_info_codigo...")
    # NUNCA muestres el código directamente. En su lugar, puedes poner un enlace a tu GitHub.
    texto = "Mi código fuente está gestionado en un repositorio privado por Snayder."
    return {"action": "SIMPLE_REPLY", "text": texto}

def mostrar_info_token() -> dict:
    """
    Proporciona información sobre el estado del token del bot de forma segura.
    """
    print("🛠️ Herramienta Owner llamada: mostrar_info_token...")
    # ¡NUNCA JAMÁS devuelvas el token!
    texto = "El token del bot es información altamente sensible y está gestionado de forma segura en las variables de entorno del servidor. No puede ser visualizado."
    return {"action": "SIMPLE_REPLY", "text": texto}