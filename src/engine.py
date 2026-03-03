# %%

import torch
import torch.nn as nn
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Precisamos redefinir a arquitetura para o PyTorch carregar os pesos (.pth)
class AgroPredictor(nn.Module):
    def __init__(self):
        super(AgroPredictor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

class DiagnosticEngine:
    def __init__(self, model_path: str = "models/agro_brain_v1.pth"):
        self.device = torch.device("cpu")
        self.model = AgroPredictor().to(self.device)
        
        # Carregando o "Cérebro" treinado no train.py
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval() # Modo de inferência (leitura apenas)
            self.has_model = True
            print(f"[ENGINE] Inteligência Artificial carregada: {model_path}")
        else:
            self.has_model = False
            print("[ENGINE] Aviso: Modelo .pth não encontrado. Usando apenas Cosseno.")

        # Vetor de Referência (Cosseno) para auditoria: [Temp/120, RPM/2500, Load, Eff]
        self.reference_failure = np.array([[0.95, 0.88, 0.90, 0.40]])

    def analyze(self, data: dict):
        """
        Analisa os dados da API usando IA (Rede Neural) e Similaridade de Cosseno.
        """
        # 1. Normalização dos dados para os Tensores da IA
        input_array = np.array([
            data['coolant_temp'] / 120.0,
            data['engine_rpm'] / 2500.0,
            data['engine_load'],
            data['mechanical_eff']
        ], dtype=np.float32)

        # 2. Diagnóstico via Rede Neural (Deep Learning)
        probabilidade_ia = 0.0
        if self.has_model:
            with torch.no_grad():
                input_tensor = torch.from_numpy(input_array).view(1, -1)
                probabilidade_ia = self.model(input_tensor).item()

        # 3. Auditoria via Similaridade de Cosseno (Geometria)
        sim_cosseno = float(cosine_similarity(input_array.reshape(1, -1), self.reference_failure))

        # Status baseado no consenso (IA + Cosseno)
        status = "CRÍTICO" if (probabilidade_ia > 0.85 or sim_cosseno > 0.92) else "NOMINAL"
        
        return probabilidade_ia, sim_cosseno, status
