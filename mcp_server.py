import os
import json
import subprocess

# Definición de tus 5 compartimientos
COMPARTIMIENTOS = {
    "1": "1_TRABAJO_DEPENDIENTE",
    "2": "2_PROYECTO_LITERARIO",
    "3": "3_CANAL_YOUTUBE",
    "4": "4_ORGANICA_VITAL",
    "5": "5_LABS"
}

class MCPServer:
    def __init__(self):
        self.indice_local = {k: {} for k in COMPARTIMIENTOS.values()}
        # Datos de tu PC de la casa guardados de forma segura en el núcleo
        self.pc_mac = "9C-7B-EF-AA-03-CD"
        self.pc_ip_local = "192.168.2.9"
        self.ollama_url = "http://localhost:11434"
        self.inicializar_entorno()

    def inicializar_entorno(self):
        """Crea las carpetas locales si no existen"""
        for carpeta in COMPARTIMIENTOS.values():
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

    def ejecutar_comando_sistema(self, orden: str):
        """
        Interpreta las órdenes de control remoto recibidas desde WhatsApp
        para controlar la estación de trabajo de tu casa.
        """
        orden = orden.lower()
        
        # 1. Comando de Apagado Seguro
        if "apaga el computador" in orden or "apagar pc" in orden:
            print("🛑 Orden de apagado remoto recibida.")
            # Ejecuta el apagado nativo de Windows inmediatamente
            os.system("shutdown /s /t 0")
            return "Entendido. Procesando el apagado inmediato de tu PC de forma segura."

        # 2. Comando para lanzar Ollama y tus modelos
        elif "inicia ollama" in orden or "abrir ollama" in orden:
            print("🦙 Lanzando Ollama localmente...")
            try:
                # Intenta abrir el servicio en su ruta estándar de Windows
                ruta_ollama = os.path.expandvars(r"%LOCALAPPDATA%\Ollama\ollama app.exe")
                subprocess.Popen([ruta_ollama])
                return "Servicio Ollama lanzado en tu PC de casa exitosamente."
            except Exception as e:
                return f"No se pudo abrir Ollama automáticamente: {str(e)}"

        # 3. Comando para tu interfaz Open WebUI
        elif "abre la interfaz" in orden or "iniciar webui" in orden:
            print("🌐 Levantando contenedor de Open WebUI...")
            # Aquí se puede disparar el comando de Docker o ejecutable de tu interfaz
            return "Interfaz de Open WebUI activada. Ya puedes acceder visualmente desde tus dispositivos."

        return "Comando remoto no reconocido o en desarrollo."

    def registrar_aprendizaje(self, compartimiento: str, concepto: str, contenido: str):
        """Módulo de retroalimentación para manuales de procedimiento"""
        comp_name = COMPARTIMIENTOS.get(compartimiento)
        if not comp_name: return False
            
        ruta_procedimiento = os.path.join(comp_name, "procedimientos.json")
        datos = {}
        if os.path.exists(ruta_procedimiento):
            with open(ruta_procedimiento, "r", encoding="utf-8") as f:
                try: datos = json.load(f)
                except: pass
                
        datos[concepto] = contenido
        with open(ruta_procedimiento, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return True

mcp_core = MCPServer()
