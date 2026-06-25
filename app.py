from fastapi import FastAPI, Request, Response
import requests
import os
from google import genai

app = FastAPI()

# Inicializamos el cliente de Gemini usando la variable de entorno segura de Render
try:
    ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error al inicializar Gemini: {e}")
    ai_client = None

# 1. Verificación del Webhook (Requisito obligatorio de Meta)
@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    token_verificacion = "MI_TOKEN_SECRETO_123"
    
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == token_verificacion:
        return Response(content=params.get("hub.challenge"))
    return Response(content="Error de verificación", status_code=403)

# 2. Recepción de mensajes procesados por la IA con filtro privado y 5 compartimientos
@app.post("/webhook")
async def recibir_mensaje(request: Request):
    datos = await request.json()
    
    try:
        cambios = datos['entry'][0]['changes'][0]['value']
        if 'messages' in cambios:
            mensaje_texto = cambios['messages'][0]['text']['body']
            telefono_usuario = cambios['messages'][0]['from']
            
            # 🔒 FILTRO DE SEGURIDAD ABSOLUTO (Tu número autorizado)
            if telefono_usuario == "573222558500":
                
                if ai_client:
                    # Instrucción maestra con tus 5 compartimientos de trabajo
                    prompt_sistema = (
                        "Actúas como un asistente personal avanzado y consultor MCP privado.\n"
                        "Tu entorno de conocimiento y memoria permanente está dividido estrictamente en 5 compartimientos independientes:\n"
                        "1. 1_TRABAJO_DEPENDIENTE/ (Asuntos de la Personería, normativas, modelos de oficios, biblioteca jurídica).\n"
                        "2. 2_PROYECTO_LITERARIO/ (Tu Libro, control de capítulos, ritmo literario, notas de estilo).\n"
                        "3. 3_CANAL_YOUTUBE/ (Estrategia de contenido, ideas y estructuras de guiones).\n"
                        "4. 4_ORGANICA_VITAL (Gestión, finanzas u operaciones de este proyecto).\n"
                        "5. 5_LABS (Laboratorio de pruebas, experimentos técnicos y desarrollo).\n\n"
                        "Tu tarea es identificar a qué compartimiento se refiere el usuario según su mensaje y activar el "
                        "enfoque o rol correspondiente (Abogado, Editor Literario, Guionista, Gestor de Negocios o Desarrollador).\n"
                        "Sé sumamente claro, ejecutivo y confirma brevemente qué contexto estás operando."
                    )
                    
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=mensaje_texto,
                        config={'system_instruction': prompt_sistema}
                    )
                    respuesta_bot = response.text
                else:
                    respuesta_bot = "Servidor activo, pero la IA de Gemini no se encuentra inicializada en Render."
                
                # Te responde de vuelta de forma privada
                enviar_a_whatsapp(telefono_usuario, respuesta_bot)
            else:
                # Si es cualquier otro número, el servidor lo ignora por completo
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
