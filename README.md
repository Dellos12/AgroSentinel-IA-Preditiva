
# 🚜 AgroSentinel AI: Monitoramento Preditivo & Manutenção 4.0

![Status](https://img.shields.io)
![Python](https://img.shields.io)
![IA](https://img.shields.io)

## 🎯 Visão Geral
Sistema de telemetria avançada para maquinário agrícola focado em diferenciar **falhas lógicas** de **falhas mecânicas** em tempo real. Utiliza Redes Neurais para prever quando a energia mecânica está sendo dissipada como calor.

### 🚀 Tecnologias Bárbaras:
- **Telemetria HDF5 (h5py):** Armazenamento binário de alta performance com compressão ZFP.
- **Deep Learning (PyTorch):** Modelo treinado para detecção de anomalias térmicas (Acurácia: 94.9%).
- **Matemática Vetorial:** Similaridade de Cosseno para auditoria de sinais.
- **Segurança (SHA-256):** Checksum de integridade para Software Flashing (OTA).
- **RAG (Retrieval-Augmented Generation):** Diálogo técnico baseado na norma **ISO 15143-3 (AEMP 2.0)**.
- **Interfaces:** Dashboard em **Streamlit** e Documentação de API em **Swagger (FastAPI)**.

## 🛠️ Como Executar
1. `conda activate agro_telemetria`
2. `pip install -r requirements.txt`
3. `python src/api_gateway.py` (Backend & Swagger)
4. `streamlit run dashboard.py` (Operação Visual)

## 📊 Prova dos Nove
O sistema valida a eficácia de cada intervenção eletrônica. Se a temperatura não cai após o Flashing, o AgroSentinel eleva o status para **Falha Mecânica de Campo**, gerando automaticamente uma Ordem de Serviço.

## 🔐 Auditoria de Integridade
Cada ciclo de **Software Flashing** realizado por este sistema gera um log de auditoria criptográfico. 
- **Algoritmo:** SH6 (SHA-256)
- **Última Validação de Sistema:** `3654d4cb704d022da6380f0f76cee550c2ce3678d2e20e05e2cb28c0ec54216b`
- **Norma de Referência:** [ISO 15143-3 / AEMP 2.0](https://www.iso.org)

