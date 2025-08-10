# core/gemini_agent.py (Versión Final Contextual)
import inspect
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

async def run_agent(prompt: str, context_data: dict) -> dict:
    """Ejecuta el agente con el prompt y un diccionario de contexto (chat_id, etc.)."""
    chat = model.start_chat(enable_automatic_function_calling=True)
    print("🧠  Enviando prompt al cerebro (Gemini)...")
    try:
        response = await chat.send_message_async(prompt)
        response_part = response.parts[0]
        final_text = "".join(part.text for part in response.parts)
        action_dict = None

        if response_part.function_call:
            function_call = response_part.function_call
            tool_name = function_call.name
            tool_args_from_ia = dict(function_call.args)
            tool_to_call = next((f for f in all_available_tools if f.__name__ == tool_name), None)

            if tool_to_call:
                # --- LÓGICA DE INYECCIÓN DE CONTEXTO ---
                # Combinamos los argumentos de la IA con el contexto que tenemos
                final_args = tool_args_from_ia.copy()
                # Obtenemos los parámetros que la función realmente necesita
                tool_params = inspect.signature(tool_to_call).parameters
                # Si la función necesita 'chat_id' y lo tenemos, lo añadimos
                if 'chat_id' in tool_params and 'chat_id' in context_data:
                    final_args['chat_id'] = context_data['chat_id']
                # Si la función necesita 'user_id_to_manage' y lo tenemos, lo añadimos
                if 'user_id_to_manage' in tool_params and 'user_id_to_manage' in context_data:
                    final_args['user_id_to_manage'] = context_data['user_id_to_manage']
                # ----------------------------------------
                
                tool_response = tool_to_call(**final_args)
                action_dict = tool_response
        else:
            action_dict = {"action": "SIMPLE_REPLY", "text": final_text}

        return {"text": final_text, "action_data": action_dict}
    except Exception as e:
        print(f"❌ Error en el agente Gemini: {e}")
        raise e