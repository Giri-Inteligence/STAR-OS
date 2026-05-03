import streamlit as st

# 1. DESIGN EXECUTIVO GIRI - ALTA DENSIDADE REFINADA
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    /* FUNDO GRADIENTE RADIAL REFINADO */
    .stApp { 
        background: radial-gradient(circle at center, #001f3f 0%, #001220 70%, #000810 100%); 
        color: #ffffff; 
    }
    
    /* MENU LATERAL COMPACTO */
    [data-testid="stSidebar"] { min-width: 200px !important; max-width: 200px !important; }
    
    /* GRID DE FERRAMENTAS - CARDS COMPACTOS E CLICÁVEIS */
    .tool-card { 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(15px); 
        border-radius: 8px; 
        padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        text-align: center;
        height: 120px; /* Redução drástica da altura */
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .tool-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transform: scale(1.02);
    }

    .title-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #f0f2f6 !important;
        margin-top: 40px;
        margin-bottom: 40px;
        font-weight: 700;
        font-size: 1.6rem;
    }

    h4 { text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem; margin-bottom: 5px; color: #ffffff; font-weight: 600; }
    p { color: rgba(255,255,255,0.4); font-size: 0.75rem; line-height: 1.1; margin: 0; }

    /* BOTÃO TRANSPARENTE SOBREPOSTO AO CARD */
    .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 120px !important;
        width: 100% !important;
        position: absolute;
        top: -120px; /* Alinhado com a nova altura do card */
        z-index: 10;
    }
    
    .stButton button:hover {
        background-color: transparent !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br> ## GIRI | ARCHITECTURE", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("v5.2 | Hub Estratégico")

st.markdown('<h1 class="title-center">Dashboard Estratégico</h1>', unsafe_allow_html=True)

# GRID DE 4 COLUNAS PARA MÁXIMA EFICIÊNCIA HORIZONTAL
cols = st.columns(4)

# FERRAMENTA 1: MATRIZ STAR
with cols[0]:
    st.markdown("""
        <div class="tool-card">
            <h4>📍 Matriz STAR</h4>
            <p>Diagnóstico de Carteira e Governança de Churn</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("A1", key="btn_star"): 
        st.session_state.pagina_ativa = 'Matriz'
        st.rerun()

# FERRAMENTA 2: DESEMPENHO
with cols[1]:
    st.markdown("""
        <div class="tool-card">
            <h4>📊 Matriz de Desempenho</h4>
            <p>Gestão de Ritmo e Eficiência Individual</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("A2", key="btn_desempenho"): 
        st.session_state.pagina_ativa = 'Desempenho'
        st.rerun()

# FERRAMENTA 3: ARQUITETURA
with cols[2]:
    st.markdown("""
        <div class="tool-card">
            <h4>⚙️ Arquitetura Comercial</h4>
            <p>Estruturação de Processos e Playbooks</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("A3", key="btn_arch"): pass

# FERRAMENTA 4: PREVISIBILIDADE
with cols[3]:
    st.markdown("""
        <div class="tool-card">
            <h4>🚀 Pipeline Predictor</h4>
            <p>Previsibilidade de Receita B2B</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("A4", key="btn_pipe"): pass
