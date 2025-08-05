from groq import Groq
from config import settings
from tools import all_available_tools
import json

client = Groq(api_key=settings.GROQ_API_KEY)

def _format_tools_for_groq():
    """Formatea nuestras funciones de Python a un JSON que Llama 3 entiende."""
    formatted_tools = []
    for tool in all_available_tools:
        # Extraemos la descripción y los parámetros del docstring (simplificado)
        # Una implementación real aquí sería más robusta.
        description = tool.__doc__.strip().split('\n')[0]
        formatted_tools.append({
            "type": "function",
            "function": {
                "name": tool.__name__,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        })
    return formatted_tools

async def run_agent(prompt: str) -> dict:
    """Ejecuta el agente usando Groq (Llama 3) como cerebro."""
    print("🧠  Cerebro Secundario (Groq) activado.")
    try:
        messages = [
            {"role": "system", "content": settings.CONTEXTO_SISTEMA},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="llama3-70b-8192", messages=messages,
            tools=_format_tools_for_groq(), tool_choice="auto"
        )

        message = response.choices[0].message
        action_dict = None

        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            tool_function = next((f for f in all_available_tools if f.__name__ == tool_name), None)
            tool_response = tool_function(**tool_args)
            action_dict = tool_response

            # Segunda llamada con el resultado de la herramienta
            messages.append(message)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(tool_response)})

            second_response = client.chat.completions.create(model="llama3-70b-8192", messages=messages)
            final_text = second_response.choices[0].message.content
        else:
            final_text = message.content
            action_dict = {"action": "SIMPLE_REPLY", "text": final_text}

        return {"text": final_text, "action_data": action_dict}
    except Exception as e:
        print(f"❌ Error en el agente Groq: {e}")
        return {"text": "Error en el procesamiento del sistema secundario.", "action_data": None}