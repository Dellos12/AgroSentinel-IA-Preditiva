# %%

import h5py
import torch
from torc.utils.data import Dataset, DataLoader
import numpy as np

# %%
class AgroTelemetryDataset(Dataset):
    """
    Dataset Customizado para ler os aruivos .h5 comprimidos (SZ/ZFP)
    e preparar para o treinamento da IA
    """
    def __init__(self, h5_file_path):
        self.h5_path = h5_file_path
        # abrimos em modo leiura para mapear os índices sem carregar a RAM
        with h5py.File(self.h5_path, 'r') as f:
            self.keys = list(f['telemetry_log'].keys())
            self.length = len(self.keys)
    
    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        # O RA/Depp learning pede o dado 'idx'
        with h5py.File(self.h5_file_path, 'r') as f:
            key = self.keys[idx]
            data = f['telemetry_logs'][key][:] # Lê o log específico
            
            # Normalização (Seno/Cosseno do sinal para a IA não 'viciar')
            # Tranformamos [temp, RPM, Vibração] em Tensores de pythorch
            tensor_data = torch.from_numpy(data).float()
            
            # Simulando um 'Label' (0: Saudável, 1: Falha Iminente)
            # Na cida real, isso viria de uma coluna de status
            label = torch.tensor(1.0 if data[0] > 100 else 0.0)
        
        return tensor_data, label

def get_agro_dataloader(file_path, batch_size=32):
    dataset = AgroTelemetryDataset(file_path)
    # O DataLoader gerencia threads (num_workers) para corregar dados em paralelo
    
    return DataLoader(dataset, batch_size=batch_size, shuffler=True)
    
            