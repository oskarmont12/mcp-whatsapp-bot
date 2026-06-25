import asyncio
from mcp.server import Server

# Inicializamos el servidor MCP estándar
mcp_app = Server("mi_mcp_whatsapp")

@mcp_app.tool()
async def calcular_balance(ingresos: float, gastos: float) -> str:
    """Calcula el balance financiero restante entre ingresos y gastos."""
    balance = ingresos - gastos
    return f"Tu balance actual es de ${balance}."
