import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import h5py
import hdf5plugin
import numpy as np
import os

# 1. Dataset para ler o Histórico H5 (Indústria 4.0)
class AgroDataset(Dataset):
    def __init__(self, h5_path):
        self.h5_path = h5_path
        self.data_keys = []
        if os.path.exists(h5_path):
            with h5py.File(self.h5_path, 'r') as f:
                for day in f.keys():
                    for log_id in f[day].keys():
                        self.data_keys.append(f"{day}/{log_id}")

    def __len__(self):
        return len(self.data_keys)

    # No seu train.py, altere o __getitem__:

    def __getitem__(self, idx):
        with h5py.File(self.h5_path, 'r') as f:
            raw_vec = f[self.data_keys[idx]][:]
            
            # NORMALIZAÇÃO: Dividimos pelos valores máximos esperados
            # [Temp/120, RPM/2500, Load/1.0, Eff/1.0]
            norm_vec = np.array([
                raw_vec[0]/120.0, 
                raw_vec[1]/2500.0, 
                raw_vec[2], 
                raw_vec[3]
            ], dtype=np.float32)
            
            x = torch.tensor(norm_vec, dtype=torch.float32)
            
            # Ajuste do alvo: Se a temp (raw_vec[0]) for > 100, falha = 1
            y = torch.tensor([1.0] if raw_vec[0] > 100 else [0.0], dtype=torch.float32)
            return x, y


# 2. Arquitetura da Rede Neural (Cérebro AgroSentinel)
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

def treinar_modelo():
    print("\n" + "="*50)
    print(" [TREINAMENTO] INICIANDO APRENDIZADO DE MÁQUINA ")
    print("="*50)
    
    dataset_path = "data/raw/TRACTOR_8R_410_history.h5"
    if not os.path.exists(dataset_path):
        print(f"[ERRO] Arquivo {dataset_path} não encontrado!")
        return

    # Preparação
    dataset = AgroDataset(dataset_path)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    model = AgroPredictor()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()

    print(f"\nTotal de Logs para Treino: {len(dataset)}")
    print(f"{'Época':<10} | {'Perda (Loss)':<15} | {'Evolução (Acc)':<20}")
    print("-" * 55)

    model.train()
    for epoch in range(10):
        total_loss, correct, total = 0, 0, 0
        
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            predicted = (outputs > 0.5).float()
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
        
        # Cálculo da Curva de Aprendizado
        acc = 100 * correct / total
        progress_bar = "█" * int(acc / 5)
        print(f"EP {epoch+1:02d}      | {total_loss/len(loader):.4f}        | {progress_bar} {acc:.1f}%")

    # SALVAMENTO CORRIGIDO (state_dict)
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/agro_brain_v1.pth")
    print("-" * 55)
    print("[BÁRBARO] Modelo salvo em: models/agro_brain_v1.pth\n")

if __name__ == "__main__":
    # Otimização CPU para PyTorch
    torch.set_num_threads(4)
    treinar_modelo()

