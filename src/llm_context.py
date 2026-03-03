import h5py
import numpy as np
from datetime import datetime

class AgroLLMContext:
    def __init__(self, h5_path="data/raw/TRACTOR_8R_410_history.h5"):
        self.h5_path = h5_path

    def recuperar_ultimo_ciclo(self):
        """Busca os dados brutos para compor o prompt do LLM"""
        with h5py.File(self.h5_path, 'r') as f:
            last_day = list(f.keys())[-1]
            last_log = list(f[last_day].keys())[-1]
            data = f[last_day][last_log][:]
            return {
                "temp": data[0],
                "rpm": data[1],
                "load": data[2],
                "eff": data[3]
            }

    def gerar_prompt_diagnostico(self, machine_id, analise_ia):
        dados = self.recuperar_ultimo_ciclo()
        # Este é o modelo de prompt que enviamos para o LLM
        prompt = f"""
        [CONTEXTO AGRO 4.0]
        Máquina: {machine_id}
        Telemetria Atual: Temp {dados['temp']}°C, RPM {dados['rpm']}, Carga {dados['load']*100}%
        Diagnóstico Deep Learning: {analise_ia:.2%} de risco térmico.
        
        [TAREFA]
        Como especialista em manutenção preditiva, explique por que a força mecânica 
        está virando calor e valide se o Software Flashing [ID:103] é a solução.
        """
        return prompt

