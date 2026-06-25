from fastapi import FastAPI, Request, Response
import requests
import os
from google import genai

app = FastAPI()

# Inicializamos el cliente de Gemini usando la variable de entorno segura
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

# 2. Recepción de mensajes procesados por la IA con filtro privado
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
                
                # Si Gemini está activo, procesa tu orden directa
                if ai_client:
                    # Instrucción del sistema para que sepa su rol estricto
                    prompt_sistema = (
                        "Eres un asistente personal privado conectado vía WhatsApp. "
                        "Tu objetivo es procesar las órdenes del usuario de forma clara y concisa."
                    )
                    
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=mensaje_texto,
                        config={'system_instruction': prompt_sistema}
                    )
                    respuesta_bot = response.text
                else:
                    respuesta_bot = "Servidor activo, pero la IA de Gemini no está configurada correctamente."
                
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
