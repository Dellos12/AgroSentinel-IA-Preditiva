import mcp.server.fastmcp as fastmcp
from src.engine import DiagnosticEngine
from src.api_client import TelemetryClient
from src.actions import apply_flash_correction

# Inicializa o Servidor MCP Bárbaro
mcp = fastmcp.FastMCP("AgroSentinel-Gateway")

engine = DiagnosticEngine()
client = TelemetryClient()

@mcp.tool()
def verificar_saude_maquina(machine_id: str) -> str:
    """Consulta o status da IA e do Cosseno via MCP."""
    data = client.fetch_machine_data(machine_id)
    prob_ia, sim_cos, status = engine.analyze(data)
    return f"Status: {status} | IA: {prob_ia:.2%} | Cosseno: {sim_cos:.4f} | Temp: {data['coolant_temp']}C"

@mcp.tool()
def disparar_correcao_eletronica(machine_id: str, intensidade: float) -> str:
    """Executa o Software Flashing com SHA-256 via comando MCP."""
    sucesso, chave_sha = apply_flash_correction(machine_id, intensidade)
    if sucesso:
        return f"Correção Aplicada! SHA-256: {chave_sha}"
    return "Falha na aplicação do Patch."

if __name__ == "__main__":
    mcp.run()

