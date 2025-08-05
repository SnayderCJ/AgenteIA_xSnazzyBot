# core/master_agent.py (Versión con Failover Corregido)
from google.api_core import exceptions as google_exceptions

from .gemini_agent import run_agent as run_gemini_agent
from .groq_agent import run_agent as run_groq_agent

async def run_master_agent(prompt: str) -> dict:
    """
    Orquesta los agentes de IA. Intenta con Gemini primero, y si falla por
    cuota, usa Groq como respaldo.
    """
    try:
        print("▶️  Intentando con el cerebro principal (Gemini)...")
        # Ya no necesitamos ninguna comprobación extra aquí. Si falla, saltará al 'except'.
        result = await run_gemini_agent(prompt)
        return result
        
    except google_exceptions.ResourceExhausted as e:
        # ¡Ahora sí se activará este bloque cuando la cuota se agote!
        print(f"⚠️ Cuota de Gemini agotada. Cambiando al cerebro secundario (Groq)...")
        try:
            result = await run_groq_agent(prompt)
            return result
        except Exception as e2:
            print(f"❌ Fallo crítico: El cerebro secundario (Groq) también falló: {e2}")
            return {"text": "Error: Ambos sistemas de IA no están disponibles.", "action_data": None}
            
    except Exception as e:
        # Este bloque atrapará cualquier otro error inesperado de Gemini
        print(f"❌ Fallo crítico: Error inesperado con el cerebro principal (Gemini): {e}")
        return {"text": "Error crítico en el sistema de IA principal.", "action_data": None}