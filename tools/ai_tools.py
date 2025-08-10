import openai
from config import settings

# La librería de openai usa la variable de entorno directamente si está configurada,
# pero es buena práctica asignarla explícitamente.
openai.api_key = settings.OPENAI_API_KEY

def generar_imagen_ia(prompt: str) -> dict:
    """
    Genera una imagen a partir de una descripción de texto usando DALL-E 3.
    """
    print(f"🛠️ Herramienta IA llamada: generar_imagen_ia para '{prompt}'...")
    if not openai.api_key:
        return {"action": "SIMPLE_REPLY", "text": "Error: La API Key de OpenAI no está configurada."}

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        image_url = response.data[0].url
        return {"action": "SEND_PHOTO", "url": image_url, "caption": prompt}
    except Exception as e:
        return {"action": "SIMPLE_REPLY", "text": f"No pude generar la imagen. Error: {e}"}