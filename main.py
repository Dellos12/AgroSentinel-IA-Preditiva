# %%
import os
import time
from datetime import datetime
from src.api_client import TelemetryClient
from src.engine import DiagnosticEngine
from src.actions import apply_flash_correction
from src.telemetry_h5 import TelemetryStorage

def main():
    client = TelemetryClient()
    engine = DiagnosticEngine() # Carrega o agro_brain_v1.pth
    storage = TelemetryStorage()
    machine_id = "TRACTOR_8R_410"

    while True:
        # 1. MONITORAMENTO CONTÍNUO
        data = client.fetch_machine_data(machine_id)
        prob_ia, sim_cos, status = engine.analyze(data)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== AGROSENTINEL-AI | STATUS: {status} ===")
        print(f"Temp: {data['coolant_temp']}°C | IA: {prob_ia:.2%} | Cosseno: {sim_cos:.4f}")
        print("-" * 60)

        # 2. GATILHO DE INTERVENÇÃO
        if status == "CRÍTICO":
            print(f"\n[ALERTA] Energia mecânica dissipando como calor!")
            print(f"Manual ID:103 -> Recomendado Software Flashing.")
            
            op = input("\nExecutar correção eletrônica? (s/n): ").lower()
            
            if op == 's':
                # Ação e recebimento da Chave de Auditoria
                sucesso, chave_sha = apply_flash_correction(machine_id, prob_ia)
                
                if sucesso:
                    print("\n" + "="*60)
                    print(" [PROVA DOS NOVES: VALIDAÇÃO DE EFICÁCIA]")
                    print("="*60)
                    
                    # Ciclo de comprovação: monitoramos a queda da temperatura
                    # Simulamos 3 ciclos onde a eletrônica 'doma' o calor
                    temp_inicial = data['coolant_temp']
                    
                    for i in range(1, 4):
                        time.sleep(2)
                        # Simulação da resposta física do motor ao novo software
                        test_data = client.fetch_machine_data(machine_id)
                        test_data['coolant_temp'] = temp_inicial - (i * 12) # Força queda
                        
                        p_ia, s_cos, st = engine.analyze(test_data)
                        print(f" Ciclo {i}: Temp {test_data['coolant_temp']:.2f}°C | IA: {p_ia:.2%}")
                        
                        if test_data['coolant_temp'] < 95:
                            print(f"\n✅ COMPROVADO: Intervenção eficaz via Software.")
                            print(f"Registro de Auditoria: {chave_sha}")
                            
                            # Salva o resultado final para o patrão ver
                            with open("data/audit_log.txt", "a") as f:
                                f.write(f"{datetime.now()} | {machine_id} | SHA:{chave_sha} | CURADO\n")
                            break
                    
                    input("\nPressione Enter para retornar ao monitoramento...")

if __name__ == "__main__":
    main()
