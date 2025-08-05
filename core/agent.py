import google.generativeai as genai
from config import settings
from tools import all_available_tools

genai.configure(api_key=settings.GOOGLE_API_KEY)

generation_config = {"temperature": 0.2, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=settings.CONTEXTO_SISTEMA,
    generation_config=generation_config,
    tools=all_available_tools
)

# NO crearemos un chat global. Crearemos uno nuevo por cada conversación para evitar ecos.
# Esto hace al bot "sin memoria" entre conversaciones, pero mucho más seguro y predecible.
# chat = model.start_chat(enable_automatic_function_calling=True)

async def run_agent(prompt: str) -> dict:
    """Ejecuta el agente y devuelve la respuesta de texto y la acción a realizar."""
    print(f"🧠  Enviando prompt al cerebro: '{prompt}'")
    try:
        # --- LÓGICA DE MEMORIA CORREGIDA ---
        # Creamos una sesión de chat nueva para cada mensaje del usuario.
        # Esto previene que las acciones de herramientas antiguas afecten a los nuevos mensajes.
        chat = model.start_chat(enable_automatic_function_calling=True)
        # ------------------------------------

        response = await chat.send_message_async(prompt)
        
        final_text = "".join(part.text for part in response.parts)
        action_dict = None
        
        # Esta lógica ahora es segura porque el historial es nuevo en cada ejecución
        for message in reversed(chat.history):
            if message.role == 'user' and message.parts[0].function_response:
                action_dict = message.parts[0].function_response.response
                break

        if action_dict is None:
            action_dict = {"action": "SIMPLE_REPLY", "text": final_text}

        return {"text": final_text, "action_data": action_dict}

    except Exception as e:
        print(f"❌ Error en el agente: {e}")
        return {"text": "Error en el procesamiento.", "action_data": None}