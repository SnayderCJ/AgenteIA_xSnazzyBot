# tools/general_tools.py
import datetime
import qrcode
import pytz
import os

def obtener_fecha_y_hora_actual() -> dict:
    """Devuelve la fecha y hora actual para Milagro, Ecuador."""
    print("🛠️ Herramienta General llamada: obteniendo fecha y hora...")
    ecuador_timezone = pytz.timezone('America/Guayaquil')
    fecha_hora = datetime.datetime.now(ecuador_timezone)
    
    texto_respuesta = fecha_hora.strftime("%A, %d de %B de %Y, %I:%M %p")
    return {"action": "SIMPLE_REPLY", "text": texto_respuesta}

def generar_codigo_qr(texto: str) -> dict:
    """Genera un código QR y lo guarda dentro de una carpeta 'qrcodes'."""
    print(f"🛠️ Herramienta General llamada: generando QR para '{texto}'...")
    
    QR_FOLDER = "qrcodes"
    os.makedirs(QR_FOLDER, exist_ok=True) 

    nombre_base = "".join(c for c in texto if c.isalnum()).lower()[:20] or "qr_generado"
    file_path = os.path.join(QR_FOLDER, f"{nombre_base}.png")
    
    img = qrcode.make(texto)
    img.save(file_path)
    
    texto_respuesta = f"Confirmado. Código QR generado y guardado como '{file_path}'."
    return {"action": "SIMPLE_REPLY", "text": texto_respuesta}