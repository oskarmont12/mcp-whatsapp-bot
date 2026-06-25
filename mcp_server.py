import os
import json

# Definición rigurosa de tus 5 compartimientos
COMPARTIMIENTOS = {
    "1": "1_TRABAJO_DEPENDIENTE",
    "2": "2_PROYECTO_LITERARIO",
    "3": "3_CANAL_YOUTUBE",
    "4": "4_ORGANICA_VITAL",
    "5": "5_LABS"
}

class MCPServer:
    def __init__(self):
        # Base de datos ligera en RAM para indexar resúmenes (Ahorro de tokens)
        self.indice_local = {k: {} for k in COMPARTIMIENTOS.values()}
        self.inicializar_entorno()

    def inicializar_entorno(self):
        """Crea las carpetas locales en el servidor si no existen"""
        for carpeta in COMPARTIMIENTOS.values():
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                print(f"📁 Compartimiento creado: {carpeta}")

    def buscar_modelo_local(self, compartimiento: str, palabra_clave: str):
        """
        Busca de forma matemática/semántica en el índice local 
        sin ir a Gemini, protegiendo tu consumo de memoria y tokens.
        """
        comp_name = COMPARTIMIENTOS.get(compartimiento)
        if not comp_name:
            return None
            
        print(f"🔍 Buscando '{palabra_clave}' localmente en {comp_name}...")
        # Lógica de escaneo híbrido (GitHub/OneDrive) se conectará aquí
        return f"Modelo preliminar detectado en {comp_name}"

    def registrar_aprendizaje(self, compartimiento: str, concepto: str, contenido: str):
        """
        Módulo de retroalimentación: Permite al MCP escribir y actualizar 
        sus propios manuales de procedimiento según tus órdenes por WhatsApp.
        """
        comp_name = COMPARTIMIENTOS.get(compartimiento)
        if not comp_name:
            return False
            
        ruta_procedimiento = os.path.join(comp_name, "procedimientos.json")
        
        # Cargar bitácora existente o crear una nueva
        datos = {}
        if os.path.exists(ruta_procedimiento):
            with open(ruta_procedimiento, "r", encoding="utf-8") as f:
                try: datos = json.load(f)
                except: pass
                
        # Inyectar el nuevo conocimiento aprendido
        datos[concepto] = contenido
        
        with open(ruta_procedimiento, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            
        print(f"🧠 MCP aprendió algo nuevo en {comp_name}: {concepto}")
        return True

# Instancia global para ser llamada desde app.py
mcp_core = MCPServer()
