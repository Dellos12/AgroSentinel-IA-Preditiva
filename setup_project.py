
import os
import subprocess
import sys

def setup():
    print("=== [AGROSENTINEL-AI] INICIANDO CONFIGURAÇÃO DE AMBIENTE ===")

    # 1. Garantir que a árvore de diretórios exista (sem apagar arquivos)
    directories = [
        "data/raw", 
        "data/vectordb", 
        "models", 
        "src"
    ]
    
    for folder in directories:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[+] Pasta criada: {folder}")
        else:
            print(f"[OK] Pasta já existente: {folder}")

    # 2. Gerar o requirements.txt otimizado para CPU
    # Nota: Usamos a URL específica do PyTorch para evitar o download de binários de GPU (3GB+ economizados)
    requirements = """# --- Core Data & Performance (CPU Optimized) ---
numpy>=1.24.0
pandas>=2.0.0
h5py>=3.8.0
hdf5plugin>=4.1.1
pyyaml>=6.0

# --- AI & Vector Math (CPU Only) ---
--find-links https://download.pytorch.org
torch
scikit-learn
sentence-transformers

# --- Connectivity & Logs ---
requests>=2.28.0
tqdm>=4.65.0
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)
    print("[OK] Arquivo 'requirements.txt' gerado com foco em CPU.")

    # 3. Gerar um config.yml básico (se não existir)
    if not os.path.exists("config.yml"):
        config_content = """# Configurações do AgroSentinel-AI
system:
  device: "cpu"
  threads: 4

telemetry:
  machine_id: "TRACTOR_8R_410"
  threshold_alert: 0.88 # Similaridade de Cosseno (Energia -> Calor)

api:
  endpoint: "https://api.agro-telemetry.com"
  timeout: 30
"""
        with open("config.yml", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("[OK] Arquivo 'config.yml' criado.")
    else:
        print("[SKIP] 'config.yml' já existe. Pulando criação.")

    # 4. Instruções de Instalação para o Usuário
    print("\n" + "="*50)
    print("PRÓXIMOS PASSOS BÁRBAROS:")
    print("1. Certifique-se de estar no ambiente Conda correto.")
    print("2. Execute o comando abaixo para instalar as bibliotecas:")
    print("   pip install -r requirements.txt")
    print("3. Após isso, você poderá rodar o seu 'main.py'.")
    print("="*50)

if __name__ == "__main__":
    setup()
