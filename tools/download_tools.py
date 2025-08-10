import yt_dlp
import os

def descargar_audio(url_o_busqueda: str) -> dict:
    """
    Busca un video en YouTube por nombre o URL, descarga el audio y lo convierte a MP3.
    """
    print(f"🛠️ Herramienta de Descarga llamada: descargar_audio para '{url_o_busqueda}'...")
    
    DOWNLOAD_FOLDER = "downloads"
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch', # Buscar si no es una URL
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_o_busqueda, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            
            if os.path.exists(filename):
                return {
                    "action": "SEND_AUDIO",
                    "path": filename,
                    "caption": info.get('title', 'Audio descargado')
                }
            else:
                return {"action": "SIMPLE_REPLY", "text": "Error: No se pudo encontrar el archivo MP3 después de la descarga."}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"No pude descargar el audio. Error: {e}"}