import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import os
import hdf5plugin 
from src.api_client import TelemetryClient
from src.engine import DiagnosticEngine
from src.actions import apply_flash_correction

# --- ESTRATÉGIA CORINGA PARA PLUGINS HDF5 (ZFP/SZ) ---
try:
    # Tenta o atributo moderno das versões recentes
    os.environ["HDF5_PLUGIN_PATH"] = hdf5plugin.get_config().plugin_dir
except AttributeError:
    try:
        # Tenta o atributo alternativo 'directory'
        os.environ["HDF5_PLUGIN_PATH"] = hdf5plugin.get_config().directory
    except AttributeError:
        # Fallback manual apontando direto para a pasta do pacote no Conda
        os.environ["HDF5_PLUGIN_PATH"] = os.path.join(os.path.dirname(hdf5plugin.__file__), 'plugins')

# Configuração da Página Bárbaro
st.set_page_config(page_title="AgroSentinel Dashboard", layout="wide")
st.title("🚜 AgroSentinel AI | Painel de Controle 4.0")

# Inicializa Motores (IA e API)
client = TelemetryClient()
engine = DiagnosticEngine()
machine_id = "TRACTOR_8R_410"

# Memória do Gráfico (Session State para persistência no Streamlit)
if 'df_history' not in st.session_state:
    st.session_state.df_history = pd.DataFrame(columns=['time', 'temp', 'ia'])

# Layout de Colunas para Métricas em Tempo Real
col1, col2, col3 = st.columns(3)
placeholder_graph = st.empty()

# Loop de Monitoramento Infinito
while True:
    # 1. Ingestão de Dados e Inteligência (Deep Learning)
    data = client.fetch_machine_data(machine_id)
    prob_ia, sim_cos, status = engine.analyze(data)
    
    # 2. Atualiza os Cards de Métricas Superiores
    col1.metric("Temperatura Motor", f"{data['coolant_temp']} °C", 
                delta=f"{data['coolant_temp']-100:.1f}°C" if data['coolant_temp'] > 100 else None)
    col2.metric("Risco IA (Deep Learning)", f"{prob_ia:.2%}")
    col3.metric("Status Operacional", status, delta_color="inverse" if status == "CRÍTICO" else "normal")

    # 3. Atualiza o Histórico (Mantém os últimos 40 pontos)
    new_data = {
        'time': time.strftime("%H:%M:%S"),
        'temp': data['coolant_temp'],
        'ia': prob_ia * 100
    }
    st.session_state.df_history = pd.concat([st.session_state.df_history, pd.DataFrame([new_data])]).tail(40)

    # 4. Renderização do Gráfico "Prova dos Nove"
    with placeholder_graph.container():
        fig = go.Figure()
        # Linha de Calor (Física)
        fig.add_trace(go.Scatter(x=st.session_state.df_history['time'], y=st.session_state.df_history['temp'], 
                                 name="Calor (°C)", line=dict(color='#FFA500', width=3)))
        # Linha de Risco (IA)
        fig.add_trace(go.Scatter(x=st.session_state.df_history['time'], y=st.session_state.df_history['ia'], 
                                 name="Risco IA (%)", line=dict(color='#FF0000', width=2, dash='dot')))
        
        # Ajuste de layout Dark Mode e largura responsiva
        fig.update_layout(height=450, template="plotly_dark", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width='stretch') # 'stretch' substitui o use_container_width=True

        # Gatilho de Ação Remota (SHA-256)
        if status == "CRÍTICO":
            st.error(f"🚨 DISSIPAÇÃO TÉRMICA CRÍTICA DETECTADA EM {machine_id}!")
            if st.button("🚀 EXECUTAR SOFTWARE FLASHING (ASSINAR SHA-256)"):
                sucesso, chave = apply_flash_correction(machine_id, prob_ia)
                if sucesso:
                    st.success(f"Binário Transmitido! Hash SHA-256: {chave}")
                    st.balloons()
                    time.sleep(3)

    time.sleep(2)
    st.rerun()

