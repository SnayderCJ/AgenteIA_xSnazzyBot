# tools/general_tools.py
import datetime
import qrcode
import pytz
import os
import pyshorteners
import requests
import dns.resolver
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from duckduckgo_search import DDGS

def obtener_fecha_y_hora_actual() -> dict:
    """Devuelve la fecha y hora actual para Milagro, Ecuador."""
    print("🛠️ Herramienta General llamada: obteniendo fecha y hora...")
    ecuador_timezone = pytz.timezone('America/Guayaquil')
    fecha_hora = datetime.datetime.now(ecuador_timezone)
    
    texto_respuesta = fecha_hora.strftime("%A, %d de %B de %Y, %I:%M %p")
    return {"action": "SIMPLE_REPLY", "text": texto_respuesta}

def generar_codigo_qr(texto: str) -> dict:
    """Genera un código QR, lo guarda y devuelve una acción para enviarlo."""
    print(f"🛠️ Herramienta General llamada: generando QR para '{texto}'...")
    
    QR_FOLDER = "qrcodes"
    os.makedirs(QR_FOLDER, exist_ok=True)

    nombre_base = "".join(c for c in texto if c.isalnum()).lower()[:20] or "qr_generado"
    file_path = os.path.join(QR_FOLDER, f"{nombre_base}.png")
    
    img = qrcode.make(texto)
    img.save(file_path)
    
    # --- CAMBIO CLAVE ---
    # La herramienta ahora devuelve una acción específica y la ruta del archivo.
    texto_respuesta = f"Confirmado. Código QR generado y guardado como '{file_path}'."
    return {
        "action": "SEND_FILE", 
        "path": file_path,
        "text": texto_respuesta # El texto que la IA usará para formular su respuesta final.
    }

def acortar_url(url: str) -> dict:
    """Acorta una URL larga utilizando el servicio TinyURL."""
    print(f"🛠️ Herramienta General llamada: acortar_url para '{url}'...")
    try:
        s = pyshorteners.Shortener()
        url_corta = s.tinyurl.short(url)
        return {"action": "SIMPLE_REPLY", "text": f"URL acortada: {url_corta}"}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"No se pudo acortar la URL. Error: {e}"}

def buscar_imagen(query: str) -> dict:
    """Busca una imagen en la web y devuelve el primer resultado."""
    print(f"🛠️ Herramienta General llamada: buscar_imagen para '{query}'...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            if not results:
                return {"action": "SIMPLE_REPLY", "text": f"No encontré imágenes para '{query}'."}
            image_url = results[0]['image']
            return {"action": "SEND_PHOTO", "url": image_url, "caption": query}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"Error al buscar la imagen: {e}"}

def obtener_info_ip(ip_address: str = None) -> dict:
    """Obtiene información de geolocalización para una dirección IP. Si no se provee una IP, muestra la del servidor."""
    print(f"🛠️ Herramienta General llamada: obtener_info_ip para '{ip_address}'...")
    try:
        url = f"http://ip-api.com/json/{ip_address or ''}"
        response = requests.get(url).json()
        if response['status'] == 'success':
            info = (
                f"**Información para IP: `{response['query']}`**\n\n"
                f"**País:** {response['country']}\n"
                f"**Ciudad:** {response['city']}\n"
                f"**ISP:** {response['isp']}"
            )
            return {"action": "SIMPLE_REPLY", "text": info, "parse_mode": "Markdown"}
        else:
            return {"action": "SIMPLE_REPLY", "text": "No se pudo obtener información para esa IP."}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"Error al consultar la IP: {e}"}

def generar_enlace_mapa(lugar: str) -> dict:
    """Genera un enlace de Google Maps para una ubicación o lugar."""
    print(f"🛠️ Herramienta General llamada: generar_enlace_mapa para '{lugar}'...")
    # Codificamos el lugar para que sea seguro en una URL
    query_encoded = quote_plus(lugar)
    url = f"https://www.google.com/maps/search/?api=1&query={query_encoded}"
    return {"action": "SIMPLE_REPLY", "text": f"Aquí tienes el enlace al mapa para '{lugar}':\n{url}"}

def convertir_a_morse(texto: str) -> dict:
    """Convierte un texto a su representación en código morse."""
    print(f"🛠️ Herramienta General llamada: convertir_a_morse...")
    MORSE_CODE_DICT = {
        'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
        'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.',
        'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
        'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....',

        '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-',
        '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-', ' ':'/'
    }
    try:
        morse = ' '.join(MORSE_CODE_DICT[char.upper()] for char in texto)
        return {"action": "SIMPLE_REPLY", "text": f"Texto en Morse:\n`{morse}`", "parse_mode": "Markdown"}
    except KeyError as e:
        return {"action": "SIMPLE_REPLY", "text": f"No se pudo convertir. Caracter no soportado: '{e.args[0]}'"}

def invertir_texto(texto: str) -> dict:
    """Invierte el orden de los caracteres en un texto dado."""
    print(f"🛠️ Herramienta General llamada: invertir_texto...")
    texto_invertido = texto[::-1]
    return {"action": "SIMPLE_REPLY", "text": f"Texto invertido:\n`{texto_invertido}`", "parse_mode": "Markdown"}

def busqueda_web(query: str) -> dict:
    """Realiza una búsqueda general en la web usando DuckDuckGo y devuelve los primeros resultados."""
    print(f"🛠️ Herramienta General llamada: busqueda_web para '{query}'...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return {"action": "SIMPLE_REPLY", "text": f"No encontré resultados para '{query}'."}
            
            # Formateamos los resultados para una lectura fácil
            respuesta = f"**Resultados de búsqueda para '{query}':**\n\n"
            for r in results:
                respuesta += f"📄 **{r['title']}**\n[Leer más]({r['href']})\n\n"
            
            return {"action": "SIMPLE_REPLY", "text": respuesta, "parse_mode": "Markdown"}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"Error al realizar la búsqueda: {e}"}

def consultar_registro_spf(dominio: str) -> dict:
    """Consulta y muestra los registros SPF de un dominio de internet para verificar la autenticidad del correo."""
    print(f"🛠️ Herramienta General llamada: consultar_registro_spf para '{dominio}'...")
    try:
        answers = dns.resolver.resolve(dominio, 'TXT')
        spf_records = []
        for rdata in answers:
            if 'spf' in rdata.to_text().lower():
                spf_records.append(rdata.to_text())
        
        if not spf_records:
            return {"action": "SIMPLE_REPLY", "text": f"No se encontraron registros SPF para el dominio `{dominio}`.", "parse_mode": "Markdown"}

        respuesta = f"**Registros SPF para `{dominio}`:**\n\n" + "\n".join(spf_records)
        return {"action": "SIMPLE_REPLY", "text": respuesta, "parse_mode": "Markdown"}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"No se pudo consultar el dominio. Error: {e}"}

def obtener_vista_previa_web(url: str) -> dict:
    """Obtiene una vista previa (título y descripción) de una página web a partir de su URL."""
    print(f"🛠️ Herramienta General llamada: obtener_vista_previa_web para '{url}'...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        titulo = soup.title.string if soup.title else "Sin título"
        
        descripcion = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            descripcion = meta_desc.get('content', '')

        respuesta = f"**Vista Previa de:** {url}\n\n**Título:** {titulo}\n\n**Descripción:** {descripcion[:200]}..."
        return {"action": "SIMPLE_REPLY", "text": respuesta}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"No se pudo obtener la vista previa de la URL. Error: {e}"}