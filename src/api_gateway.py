import sys
import os
import json
import h5py
import hdf5plugin  # Essencial para os filtros de compressão
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import Response
from pydantic import BaseModel, Field

# --- CORREÇÃO DE INFRAESTRUTURA (SOLUÇÃO ATTRIBUTEERROR) ---
# O hdf5plugin armazena o caminho dos drivers no objeto de configuração
try:
    # Forma recomendada nas versões recentes
    os.environ["HDF5_PLUGIN_PATH"] = hdf5plugin.get_config().plugin_dir
except AttributeError:
    # Fallback caso a estrutura do pacote mude
    os.environ["HDF5_PLUGIN_PATH"] = os.path.join(os.path.dirname(hdf5plugin.__file__), 'plugins')

# Garante que a raiz do projeto esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine import DiagnosticEngine
from src.actions import apply_flash_correction

app = FastAPI(
    title="AgroSentinel 4.0 | API Gateway",
    description="Auditoria HDF5 com Descompressão ZFP Otimizada para CPU",
    version="3.5.0"
)

# Inicializa o motor de diagnóstico (IA + Cosseno)
engine = DiagnosticEngine()
KNOWLEDGE_BASE = "data/vectordb/seed_llm_knowledge.json"

class FlashRequest(BaseModel):
    machine_id: str = Field(..., example="TRACTOR_8R_410")
    intensity: float = Field(..., ge=0.0, le=1.0, example=0.95)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", media_type="image/x-icon")

@app.get("/", tags=["Status"])
def home():
    return {
        "status": "Online",
        "ia_engine": "models/agro_brain_v1.pth carregado",
        "hdf5_plugins": os.environ["HDF5_PLUGIN_PATH"],
        "swagger_docs": "/docs"
    }

@app.get("/diagnostico/rag/{machine_id}", tags=["IA & RAG"])
def diagnostico_rag(machine_id: str = Path(..., example="TRACTOR_8R_410")):
    """
    [PROVA DOS NOVE] Realiza o diálogo RAG lendo dados reais do HDF5.
    """
    try:
        path = f"data/raw/{machine_id}_history.h5"
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Arquivo HDF5 não encontrado.")
        
        # Abertura com suporte aos plugins carregados no os.environ
        with h5py.File(path, 'r') as f:
            last_day = list(f.keys())[-1]
            last_log = list(f[last_day].keys())[-1]
            # Agora a descompressão ZFP funcionará sem o erro 500
            data = f[last_day][last_log][:] 
        
        # Processamento via IA
        prob_ia, sim_cos, status = engine.analyze({
            'coolant_temp': float(data[0]),
            'engine_rpm': int(data[1]),
            'engine_load': float(data[2]),
            'mechanical_eff': float(data[3])
        })

        with open(KNOWLEDGE_BASE, "r") as f:
            kb = json.load(f)
        
        # Busca a diretriz no JSON baseada no calor
        diretriz = kb['diretrizes_tecnicas'][0] if data[0] > 100 else kb['diretrizes_tecnicas'][1]

        return {
            "status_maquina": status,
            "ia_probabilidade": f"{prob_ia:.2%}",
            "rag_diagnostico": diretriz['diagnostico'],
            "prescricao_iso": diretriz['prescricao'],
            "norma": kb['versao_norma']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de Processamento: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Log de inicialização para conferência no terminal
    print(f"[H5-CONFIG] Plugins localizados em: {os.environ['HDF5_PLUGIN_PATH']}")
    uvicorn.run(app, host="127.0.0.1", port=8000)

