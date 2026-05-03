import streamlit as st

# 1. DESIGN EXECUTIVO GIRI - ALTA DENSIDADE
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    /* FUNDO GRADIENTE RADIAL REFINADO */
    .stApp { 
        background: radial-gradient(circle at center, #001f3f 0%, #001220 70%, #000810 100%); 
        color: #ffffff; 
    }
    
    /* MENU LATERAL */
    [data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; }
    
    /* GRID DE FERRAMENTAS - CARDS COMPACTOS */
    .tool-card { 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(15px); 
        border-radius: 10px; 
        padding: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        text-align: center;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .tool-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateY(-3px);
    }

    .title-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #f0f2f6 !important;
        margin-top: 50px;
        margin-bottom: 50px;
        font-weight: 700;
        font-size: 1.8rem;
    }

    h4 { text-transform: uppercase; letter-spacing: 1px; font-size: 1rem; margin-bottom: 10px; color: #ffffff; }
    p { color: rgba(255,255,255,0.5); font-size: 0.8rem; line-height: 1.2; margin: 0; }

    /* BOTÕES INVISÍVEIS PARA TORNAR O CARD CLICÁVEL */
    .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 180px !important;
        width: 100% !important;
        position: absolute;
        top: -180px;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br> ## GIRI | ARCHITECTURE", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("v5.1 | Hub Estratégico")

st.markdown('<h1 class="title-center">Dashboard Estratégico</h1>', unsafe_allow_html=True)

# 2. GRID DINÂMICO (3 COLUNAS PARA ESCALABILIDADE)
# Aqui podemos expandir para 4 colunas conforme as 13 ferramentas entrarem
cols = st.columns(3)

# FERRAMENTA 1
with cols[0]:
    st.markdown("""
        <div class="tool-card">
            <h4>📍 Matriz STAR</h4>
            <p>Diagnóstico de Carteira e Governança de Churn</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar 1", key="btn_star"):
        pass # Lógica de navegação

# FERRAMENTA 2
with cols[1]:
    st.markdown("""
        <div class="tool-card">
            <h4>📊 Matriz de Desempenho</h4>
            <p>Gestão de Ritmo e Eficiência Individual</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar 2", key="btn_desempenho"):
        pass

# FERRAMENTA 3 (ESPAÇO PARA FUTURA FERRAMENTA)
with cols[2]:
    st.markdown("""
        <div class="tool-card">
            <h4>⚙️ Arquitetura Comercial</h4>
            <p>Estruturação de Processos e Playbooks</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar 3", key="btn_arch"):
        pass

# Próxima linha de ferramentas (Exemplo de como escalar)
st.markdown("<br>", unsafe_allow_html=True)
cols2 = st.columns(3)
with cols2[0]:
    st.markdown('<div class="tool-card"><h4>🚀 Pipeline Predictor</h4><p>Previsibilidade de Receita B2B</p></div>', unsafe_allow_html=True)
    st.button("Acessar 4", key="btn_pipe")
