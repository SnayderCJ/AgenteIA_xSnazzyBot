import datetime
import qrcode
import pytz

def obtener_fecha_y_hora_actual() -> str:
    """Devuelve la fecha y hora actual para Milagro, Ecuador."""
    print("🛠️ Herramienta General llamada: obteniendo fecha y hora...")
    ecuador_timezone = pytz.timezone('America/Guayaquil')
    fecha_hora = datetime.datetime.now(ecuador_timezone)
    return fecha_hora.strftime("%A, %d de %B de %Y, %I:%M %p")

def generar_codigo_qr(texto: str) -> str:
    """Genera un código QR y devuelve un mensaje de confirmación con el nombre del archivo."""
    print(f"🛠️ Herramienta General llamada: generando QR para '{texto}'...")
    nombre_base = "".join(c for c in texto if c.isalnum()).lower()[:20] or "qr_generado"
    file_path = f"{nombre_base}.png"
    img = qrcode.make(texto)
    img.save(file_path)
    return f"Confirmado. Código QR generado y guardado como '{file_path}'."