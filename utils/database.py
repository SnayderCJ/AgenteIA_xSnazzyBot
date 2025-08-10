import sqlite3

DB_FILE = "bot_data.db"

def init_db():
    """Inicializa la base de datos y crea las tablas si no existen."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    # Tabla para silenciar grupos
    cur.execute('''
        CREATE TABLE IF NOT EXISTS muted_groups (
            chat_id INTEGER PRIMARY KEY,
            is_muted BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    # Tabla para administradores del bot
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bot_admins (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    # Tabla para ajustes generales
    cur.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    con.commit()
    con.close()
    print("🗃️ Base de datos inicializada correctamente.")

# --- Funciones para Muted Groups (mutegp) ---
def set_group_mute(chat_id: int, status: bool):
    """Activa o desactiva el silencio para un grupo."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO muted_groups (chat_id, is_muted) VALUES (?, ?)", (chat_id, status))
    con.commit()
    con.close()

def is_group_muted(chat_id: int) -> bool:
    """Verifica si un grupo está silenciado."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT is_muted FROM muted_groups WHERE chat_id = ?", (chat_id,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else False

# --- Funciones para Bot Admins (botadm) ---
def add_bot_admin(user_id: int):
    """Añade un usuario a la lista de administradores del bot."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO bot_admins (user_id) VALUES (?)", (user_id,))
    con.commit()
    con.close()

def remove_bot_admin(user_id: int):
    """Elimina a un usuario de la lista de administradores del bot."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("DELETE FROM bot_admins WHERE user_id = ?", (user_id,))
    con.commit()
    con.close()

def get_bot_admins() -> list:
    """Devuelve la lista de todos los IDs de administradores del bot."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT user_id FROM bot_admins")
    # aplanamos la lista de tuplas a una lista de enteros
    admins = [row[0] for row in cur.fetchall()]
    con.close()
    return admins
    
# --- Funciones para Ajustes (stmention) ---
def update_setting(key: str, value: str):
    """Guarda o actualiza un ajuste general."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    con.commit()
    con.close()

def get_setting(key: str) -> str | None:
    """Obtiene el valor de un ajuste."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else None