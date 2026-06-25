from fastapi import FastAPI, Request, Response
import requests
from mcp_server import mcp_app  # Importamos tu servidor MCP

app = FastAPI()

# Montamos el servidor MCP dentro de nuestra aplicación web
app.mount("/mcp", mcp_app)

# 1. Verificación del Webhook (Requisito que Meta/WhatsApp te pedirá más adelante)
@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    token_verificacion = "MI_TOKEN_SECRETO_123"  # Puedes cambiar este token después
    
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == token_verificacion:
        return Response(content=params.get("hub.challenge"))
    return Response(content="Error de verificación", status_code=403)

# 2. Recepción de los mensajes de WhatsApp
@app.post("/webhook")
async def recibir_mensaje(request: Request):
    datos = await request.json()
    
    try:
        # Extraer el texto y el número de quien escribe
        cambios = datos['entry'][0]['changes'][0]['value']
        if 'messages' in cambios:
            mensaje_texto = cambios['messages'][0]['text']['body']
            telefono_usuario = cambios['messages'][0]['from']
            
            # Nota temporal: Aquí es donde conectaremos la IA más adelante.
            # Por ahora, responderá confirmando que el mensaje llegó.
            respuesta_bot = f"¡Hola! Recibí tu mensaje: '{mensaje_texto}'. El servidor MCP ya está conectado."
            
            # Enviar la respuesta de vuelta a WhatsApp
            enviar_a_whatsapp(telefono_usuario, respuesta_bot)
            
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        
    return {"status": "ok"}

def enviar_a_whatsapp(telefono, texto):
    # Estos valores los rellenaremos cuando configuremos Meta
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
    # Intentar enviar (dará error controlado hasta que configuremos las credenciales reales)
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"No se pudo enviar a WhatsApp todavía: {e}")
