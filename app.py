from fastapi import FastAPI, Request, Response
import requests

app = FastAPI()

# 1. Verificación del Webhook (Requisito que Meta/WhatsApp te pedirá)
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
            
            # Nota: Aquí conectaremos la IA más adelante.
            respuesta_bot = f"¡Hola! Recibí tu mensaje: '{mensaje_texto}'. El servidor web está funcionando."
            
            # Enviar la respuesta de vuelta a WhatsApp
            enviar_a_whatsapp(telefono_usuario, respuesta_bot)
            
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
