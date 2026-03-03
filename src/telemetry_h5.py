# %%
import h5py
import hdf5plugin
import numpy as np
from datetime import datetime
import os




class TelemetryStorage:
    def __init__(self, base_path: str = "data/raw/"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def store_snapshot(self, machine_id: str, data: dict):
        """
        Salva dados de telemetria com IDs únicos para evitar o erro 'name already exists'.
        Utiliza compressão ZFP para otimizar o processamento em CPU.
        """
        filename = os.path.join(self.base_path, f"{machine_id}_history.h5")
        
        # Converte o dicionário da API em vetor numérico para o H5
        vector_data = np.array([
            data['coolant_temp'], 
            data['engine_rpm'], 
            data['engine_load'], 
            data['mechanical_eff']
        ], dtype=np.float32)

        with h5py.File(filename, 'a') as f:
            # Organização por pasta de data (ISO 8601)
            group_name = datetime.now().strftime("%Y_%m_%d")
            grp = f.require_group(group_name)
            
            # CHAVE ÚNICA: Timestamp com microsegundos para evitar colisões no loop
            # O '%f' garante que 500 logs no mesmo segundo tenham nomes diferentes
            timestamp_key = f"log_{datetime.now().strftime('%H%M%S_%f')}"
            
            # Prevenção Bárbaro: se o nome existir, removemos antes de criar
            if timestamp_key in grp:
                del grp[timestamp_key]

            # Criação do Dataset com Compressão de Precisão (ZFP)
            dset = grp.create_dataset(
                timestamp_key, 
                data=vector_data,
                **hdf5plugin.Zfp(precision=12) 
            )
            
            # Metadados para auditoria via Swagger/RAG
            dset.attrs['units'] = "C, RPM, %, %"
            dset.attrs['machine'] = machine_id

        return True

