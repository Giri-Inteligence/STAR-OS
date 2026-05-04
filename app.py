import streamlit as st

# 1. DESIGN EXECUTIVO GIRI - ESTÉTICA DE ALTA PERFORMANCE
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    /* FUNDO COM GRADIENTE RADIAL PROFUNDO */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); 
        color: #ffffff; 
    }
    
    header {visibility: hidden;}
    
    /* MENU LATERAL COMPACTO */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        min-width: 200px !important;
        max-width: 200px !important;
    }
    
    /* CARDS ESTILO 'GLASS' COM ALTURA ACHATADA */
    .tool-card { 
        background: rgba(255, 255, 255, 0.02); 
        backdrop-filter: blur(20px); 
        border-radius: 4px; 
        padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        text-align: center;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .title-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 50px;
        margin-bottom: 50px;
        font-weight: 800;
        font-size: 1.8rem;
    }

    h4 { 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        font-size: 0.9rem; 
        margin-bottom: 8px; 
        color: #ffffff; 
        font-weight: 700; 
    }
    
    p { 
        color: rgba(255, 255, 255, 0.4); 
        font-size: 0.7rem; 
        line-height: 1.2; 
        margin: 0; 
        font-weight: 400; 
    }

    /* GATILHO INVISÍVEL */
    .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 110px !important;
        width: 100% !important;
        position: absolute;
        top: -110px;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br><br><h2 style='letter-spacing:2px; font-size:1rem;'>GIRI | ARCHITECTURE</h2>", unsafe_allow_html=True)

st.markdown('<h1 class="title-center">Dashboard Estratégico</h1>', unsafe_allow_html=True)

# GRID DE 4 COLUNAS - ESCALÁVEL
cols = st.columns(4)

# FERRAMENTA 1
with cols[0]:
    st.markdown('<div class="tool-card"><h4>MATRIZ STAR</h4><p>Diagnóstico de Carteira e Governança de Churn</p></div>', unsafe_allow_html=True)
    if st.button("", key="btn_star"): 
        st.session_state.pagina_ativa = 'Matriz'
        st.rerun()

# FERRAMENTA 2
with cols[1]:
    st.markdown('<div class="tool-card"><h4>MATRIZ DE DESEMPENHO</h4><p>Gestão de Ritmo e Eficiência Individual</p></div>', unsafe_allow_html=True)
    if st.button("", key="btn_desempenho"): 
        st.session_state.pagina_ativa = 'Desempenho'
        st.rerun()

# FERRAMENTA 3
with cols[2]:
    st.markdown('<div class="tool-card"><h4>ARQUITETURA COMERCIAL</h4><p>Estruturação de Processos e Playbooks</p></div>', unsafe_allow_html=True)
    if st.button("", key="btn_arch"): pass

# FERRAMENTA 4
with cols[3]:
    st.markdown('<div class="tool-card"><h4>PIPELINE PREDICTOR</h4><p>Previsibilidade de Receita B2B</p></div>', unsafe_allow_html=True)
    if st.button("", key="btn_pipe"): pass
