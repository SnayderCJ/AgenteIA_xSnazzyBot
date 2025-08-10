import yt_dlp
import os

# Definimos la carpeta de descargas una sola vez
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def descargar_multimedia(url_o_busqueda: str, formato: str = 'video') -> dict:
    """
    Busca y descarga contenido de video, audio o subtítulos desde una URL o búsqueda.
    Parámetros:
    - url_o_busqueda (str): La URL o el texto a buscar en YouTube.
    - formato (str): Puede ser 'video' (para MP4), 'audio' (para MP3), o 'subtitulos' (para .srt).
    """
    print(f"🛠️ Herramienta de Descarga: descargando '{url_o_busqueda}' en formato '{formato}'...")

    # Configuramos las opciones de descarga según el formato solicitado
    if formato == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
            'default_search': 'ytsearch', 'noplaylist': True, 'quiet': True, 'no_warnings': True,
        }
        action_type = "SEND_AUDIO"
        expected_ext = ".mp3"

    elif formato == 'subtitulos':
        ydl_opts = {
            'writesubtitles': True,
            'subtitleslangs': ['es', 'en'], # Prioriza subtítulos en español o inglés
            'skip_download': True, # No descargar el video, solo los subtítulos
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s'), # Sin extensión para evitar conflictos
            'default_search': 'ytsearch', 'noplaylist': True, 'quiet': True, 'no_warnings': True,
        }
        action_type = "SEND_FILE" # Lo enviaremos como un documento
        expected_ext = ".es.vtt" # yt-dlp a menudo prefiere .vtt

    else: # 'video' es el formato por defecto
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'default_search': 'ytsearch', 'noplaylist': True, 'quiet': True, 'no_warnings': True,
        }
        action_type = "SEND_VIDEO"
        expected_ext = ".mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_o_busqueda, download=True)
            base_filename = ydl.prepare_filename(info).rsplit('.', 1)[0]
            final_filename = base_filename + expected_ext

            # Buscamos el archivo final, ya que a veces el nombre puede variar ligeramente
            found_file = None
            if os.path.exists(final_filename):
                found_file = final_filename
            # Si es subtítulo, puede tener otra extensión
            elif formato == 'subtitulos':
                possible_subtitle_files = [base_filename + ".es.srt", base_filename + ".en.srt", base_filename + ".es.vtt"]
                for f in possible_subtitle_files:
                    if os.path.exists(f):
                        found_file = f
                        break
            
            if found_file:
                return {
                    "action": action_type,
                    "path": found_file,
                    "caption": info.get('title', 'Archivo descargado')
                }
            else:
                return {"action": "SIMPLE_REPLY", "text": "Error: No se pudo encontrar el archivo después de la descarga."}
    
    except Exception as e:
        # Devuelve el error de yt-dlp de forma más limpia
        error_message = str(e).split('ERROR: ')[-1]
        return {"action": "SIMPLE_REPLY", "text": f"No pude descargar el contenido. Motivo: {error_message}"}