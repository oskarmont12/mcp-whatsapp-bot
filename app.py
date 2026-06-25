from fastapi import FastAPI, Request, Response
import requests

app = FastAPI()

# 1. Verificación del Webhook (Requisito obligatorio de Meta)
@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    token_verificacion = "MI_TOKEN_SECRETO_123"
    
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == token_verificacion:
        return Response(content=params.get("hub.challenge"))
    return Response(content="Error de verificación", status_code=403)

# 2. Recepción de mensajes con filtro privado
@app.post("/webhook")
async def recibir_mensaje(request: Request):
    datos = await request.json()
    
    try:
        cambios = datos['entry'][0]['changes'][0]['value']
        if 'messages' in cambios:
            mensaje_texto = cambios['messages'][0]['text']['body']
            telefono_usuario = cambios['messages'][0]['from']
            
            # =========================================================================
            # 🔒 FILTRO DE SEGURIDAD ABSOLUTO
            # Reemplaza "TU_NUMERO_DE_TELEFONO" por tu número real (ej: "573XXXXXXXXX")
            # =========================================================================
            if telefono_usuario == "573222558500":
                # Si eres tú, la IA procesará el mensaje. 
                # (Nota: Aquí conectaremos el modelo de IA más adelante)
                respuesta_bot = f"Ejecutando tu orden: '{mensaje_texto}'. Conexión MCP exitosa."
                
                # Te responde solo a ti (Ida y vuelta)
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
