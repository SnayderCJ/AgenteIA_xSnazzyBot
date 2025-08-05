# 🤖 xSnazzyBot - Asistente de IA Avanzado 🧠

✨ *Descripción*

¡Bienvenido al panel de control de xSnazzyBot! Este es un asistente virtual avanzado que opera en Telegram, diseñado con una arquitectura de software moderna y escalable. A diferencia de los bots tradicionales, xSnazzyBot funciona como un **Agente de IA con Herramientas**, capaz de entender lenguaje natural y ejecutar acciones complejas. 🚀

A través de este proyecto, he implementado un sistema robusto que no solo responde a las solicitudes, sino que también garantiza una alta disponibilidad mediante un sistema de "failover" que cambia de cerebro de IA si el principal falla. Todo el sistema está construido sobre una base modular que permite añadir nuevas habilidades de forma sencilla y ordenada.

🚀 *Características Principales*

* **IA con Personalidad:** El bot sigue un conjunto de reglas estrictas (`CONTEXTO_SISTEMA`) que definen su comportamiento formal, directo y eficiente.
* **Sistema de Herramientas (Tool-Use):** La IA puede utilizar funciones de Python como "herramientas" para realizar tareas del mundo real (generar QRs, obtener la hora, etc.).
* **Alta Disponibilidad (Failover):** Utiliza Google Gemini como cerebro principal y cambia automáticamente a Groq (Llama 3) si se detectan fallos o límites de cuota.
* **Modelo Híbrido:** Combina la flexibilidad de la IA conversacional con la fiabilidad de comandos directos (`/restart`, `/shutdown`) para acciones críticas exclusivas del propietario.
* **Arquitectura Profesional:** Estructura de proyecto modular y escalable para un fácil mantenimiento y expansión.

🛠️ *Tecnologías Utilizadas*

* **Backend y Lógica Principal:**
    * **Python:** El lenguaje que impulsa todo el proyecto.
    * **python-telegram-bot:** Librería para la integración con la API de Telegram.

* **Cerebros de IA:**
    * **Google Gemini:** Modelo de IA principal para el procesamiento de lenguaje.
    * **Groq (Llama 3):** Modelo de IA secundario para el sistema de failover.
    * **google-generativeai / groq:** Librerías de Python para interactuar con las APIs de IA.

* **Herramientas y Utilidades:**
    * **python-dotenv:** Para la gestión segura de claves de API y secretos.
    * **qrcode & Pillow:** Para la generación de imágenes de códigos QR.
    * **pytz:** Para el manejo preciso de zonas horarias.

## ⚙️ Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto desde cero.

1.  **Clonar o Crear el Repositorio:**
    ```bash
    git clone [https://github.com/SnayderCJ/AgenteIA_xSnazzyBot.git](https://github.com/SnayderCJ/AgenteIA_xSnazzyBot.git) # Opcional si usas Git
    cd AgenteIA_xSnazzyBot
    ```

2.  **Crear y Activar Entorno Virtual:**
    ```bash
    # En Windows
    py -m venv venv
    venv\Scripts\activate

    # En Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar las Dependencias:**
     Instala todo con un solo comando:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las Variables de Entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto. Este archivo es secreto. Rellénalo con tus claves:
    ```
    # .env - Archivo de configuración de secretos

    # Clave de la API de Google Gemini
    GOOGLE_API_KEY="AIzaSy..."

    # Clave de la API de Groq
    GROQ_API_KEY="gsk_..."

    # Token de tu bot de Telegram (obtenido de BotFather)
    TELEGRAM_BOT_TOKEN="71...:AAG..."

    # Tu ID numérico de usuario de Telegram
    SNAYDER_ID="123456789"
    ```

5.  **Ejecutar el Bot:**
    Una vez activado el entorno y configurado el `.env`, inicia el bot:
    ```bash
    python run_telegram.py
    ```

6.  **Interactuar con el Bot:**
    * Abre tu aplicación de Telegram y busca el chat con tu bot.
    * ¡Empieza a darle órdenes!

## 💬 Uso y Comandos

Interactúa con xSnazzyBot de dos maneras:

* **Comandos Directos (Solo Dueño):** Para una fiabilidad del 100%.
    * `/restart`
    * `/shutdown`

* **Lenguaje Natural (IA):** Habla con él de forma normal para todo lo demás.
    * `Hola`
    * `qué hora es`
    * `dame la información del bot`
    * `crea un qr para la web de google`
    * `necesito reiniciar el sistema`

## 🚀 ¡Explora las capacidades de tu IA y llévala al siguiente nivel! Si tienes dudas o ideas, ya sabes dónde encontrarme. 😊