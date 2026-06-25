from fastapi import FastAPI, Request, Response
import requests
import os
from google import genai
# Importamos el motor de tus 5 compartimientos
from mcp_server import mcp_core

app = FastAPI()

try:
    ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error al inicializar Gemini: {e}")
    ai_client = None

@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    token_verificacion = "MI_TOKEN_SECRETO_123"
    
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == token_verificacion:
        return Response(content=params.get("hub.challenge"))
    return Response(content="Error de verificación", status_code=403)

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    datos = await request.json()
    
    try:
        cambios = datos['entry'][0]['changes'][0]['value']
        if 'messages' in cambios:
            mensaje_texto = cambios['messages'][0]['text']['body']
            telefono_usuario = cambios['messages'][0]['from']
            
            # 🔒 FILTRO DE SEGURIDAD PRIVADO
            if telefono_usuario == "573222558500":
                
                if ai_client:
                    # Instrucción maestra con tus 5 compartimientos
                    prompt_sistema = (
                        "Actúas como un asistente personal avanzado y consultor MCP privado.\n"
                        "Tu entorno de conocimiento y memoria permanente está dividido en 5 compartimientos independientes:\n"
                        "1. 1_TRABAJO_DEPENDIENTE (Asuntos de la Personería, normativas, modelos de oficios, biblioteca jurídica).\n"
                        "2. 2_PROYECTO_LITERARIO (Tu Libro, control de capítulos, ritmo literario, notas de estilo).\n"
                        "3. 3_CANAL_YOUTUBE (Estrategia de contenido, ideas y estructuras de guiones).\n"
                        "4. 4_ORGANICA_VITAL (Gestión, finanzas u operaciones de este proyecto).\n"
                        "5. 5_LABS (Laboratorio de pruebas, experimentos técnicos y desarrollo).\n\n"
                        "REGLA DE APRENDIZAJE:\n"
                        "Si el usuario te dice que guardes, anotes o memorices una regla (ej: 'guarda que...'), "
                        "confirma en tu respuesta qué concepto vas a registrar y en qué número de compartimiento.\n\n"
                        "Identifica el compartimiento solicitado, adopta el rol experto y sé ejecutivo."
                    )
                    
                    # Interceptar comandos de aprendizaje directos antes de procesar con la IA
                    if "guarda que" in mensaje_texto.lower() or "anota que" in mensaje_texto.lower():
                        # Ejemplo simple de enrutamiento de aprendizaje local en el MCP
                        # Por defecto, analiza palabras clave para saber a cuál compartimiento enviarlo
                        comp_destino = "5" # Labs por defecto para pruebas
                        if "personeria" in mensaje_texto.lower() or "oficio" in mensaje_texto.lower(): comp_destino = "1"
                        elif "libro" in mensaje_texto.lower() or "capitulo" in mensaje_texto.lower(): comp_destino = "2"
                        elif "youtube" in mensaje_texto.lower() or "video" in mensaje_texto.lower(): comp_destino = "3"
                        elif "organica" in mensaje_texto.lower(): comp_destino = "4"
                        
                        mcp_core.registrar_aprendizaje(comp_destino, "Anotacion_WhatsApp", mensaje_texto)
                    
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=mensaje_texto,
                        config={'system_instruction': prompt_sistema}
                    )
                    respuesta_bot = response.text
                else:
                    respuesta_bot = "Servidor activo, pero la IA de Gemini no se encuentra inicializada."
                
                enviar_a_whatsapp(telefono_usuario, respuesta_bot)
            else:
                print(f"Mensaje bloqueado de un tercero: {telefono_usuario}")
                
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        
    return {"status": "ok"}

def enviar_a_whatsapp(telefono, texto):
    url = "https://graph.facebook.com/v20.0/TU_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": "Bearer TU_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": texto}
    }
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"No se pudo enviar a WhatsApp todavía: {e}")
