
import h5py
import numpy as np
from src.telemetry_h5 import TelemetryStorage
import random

def popular_banco_bárbaro():
    storage = TelemetryStorage()
    machine_id = "TRACTOR_8R_410"
    print(f"[*] Gerando 500 logs de telemetria (Norma AEMP 2.0)...")

    for i in range(500):
        # Simulando variação: 80% operando normal, 20% com falha térmica
        is_failure = random.random() > 0.8
        
        load = random.uniform(0.5, 0.95)
        rpm = 1800 + (load * 400)
        
        if is_failure:
            # Força mecânica virando calor (Eficiência cai, Temp sobe)
            temp = random.uniform(105, 120)
            eff = random.uniform(0.4, 0.6)
        else:
            temp = random.uniform(80, 95)
            eff = random.uniform(0.8, 0.95)

        data = {
            "machine_id": machine_id,
            "coolant_temp": round(temp, 2),
            "engine_rpm": int(rpm),
            "engine_load": round(load, 2),
            "mechanical_eff": round(eff, 2)
        }
        
        storage.store_snapshot(machine_id, data)

    print(f"[OK] Banco de dados populado em data/raw/{machine_id}_history.h5")

if __name__ == "__main__":
    popular_banco_bárbaro()
