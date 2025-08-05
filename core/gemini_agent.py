# core/gemini_agent.py (Versión Definitiva y Corregida)
import google.generativeai as genai

from config import settings
from tools import all_available_tools

# Configura la API Key desde los ajustes
genai.configure(api_key=settings.GOOGLE_API_KEY)

generation_config = {"temperature": 0.2, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=settings.CONTEXTO_SISTEMA,
    generation_config=generation_config,
    tools=all_available_tools
)

async def run_agent(prompt: str) -> dict:
    """
    Ejecuta el agente con Gemini. Crea una sesión limpia para cada mensaje para
    evitar errores de estado y propaga las excepciones si falla.
    """
    # Se crea una sesión de chat nueva para cada mensaje. Esta es la forma más estable.
    chat = model.start_chat(enable_automatic_function_calling=True)
    print("🧠  Enviando prompt al cerebro (Gemini)...")
    try:
        # El SDK maneja la llamada a herramientas automáticamente en esta única llamada
        response = await chat.send_message_async(prompt)
        
        final_text = "".join(part.text for part in response.parts)
        action_dict = None
        
        # Buscamos en el historial de ESTA SESIÓN si se ejecutó una herramienta
        for message in reversed(chat.history):
            if message.role == 'user' and message.parts[0].function_response:
                action_dict = message.parts[0].function_response.response
                break

        if action_dict is None:
            action_dict = {"action": "SIMPLE_REPLY", "text": final_text}

        return {"text": final_text, "action_data": action_dict}

    except Exception as e:
        print(f"❌ Error en el agente Gemini: {e}")
        # Propagamos el error para que el master_agent lo maneje y active el failover
        raise e