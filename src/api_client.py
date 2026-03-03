# %%
import time
import random
from typing import Dict, Any

class TelemetryClient:
    def __init__(self, config_path: str = "config.yml"):
        self.api_url = "https://api.agro-telemetry.com" # Simulado

    def fetch_machine_data(self, machine_id: str) -> Dict[str, Any]:
        """
        Simula a chegada de pacotes AEMP 2.0 via HTTPS.
        Retorna: Temperatura (°C), RPM, Carga (%) e Eficiência (0-1).
        """
        # Simulação de telemetria real com oscilação térmica
        # Se a carga sobe e a eficiência cai, a energia vira calor
        load = random.uniform(0.7, 0.95)
        temp = 85 + (load * 35) + random.uniform(-2, 5) # Calor proporcional à carga
        eff = 0.95 - (load * 0.3) # Eficiência cai com sobrecarga
        
        return {
            "machine_id": machine_id,
            "timestamp": time.time(),
            "coolant_temp": round(temp, 2),
            "engine_rpm": int(2100 + (load * 300)),
            "engine_load": round(load, 2),
            "mechanical_eff": round(eff, 2)
        }

