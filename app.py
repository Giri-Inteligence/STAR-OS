import streamlit as st

# 1. ARQUITETURA VISUAL GIRI - REFINAMENTO C-LEVEL
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    /* GRADIENTE RADIAL SOFISTICADO (ELIMINA O FUNDO CHAPADO) */
    .stApp { 
        background: radial-gradient(circle at center, #001f3f 0%, #001220 70%, #000810 100%); 
        color: #ffffff; 
    }
    
    /* MENU LATERAL MINIMALISTA */
    [data-testid="stSidebar"] { 
        min-width: 240px !important; 
        max-width: 240px !important; 
        background-color: rgba(0, 8, 16, 0.5) !important;
    }
    
    /* CARDS DE NAVEGAÇÃO */
    .main-card { 
        background: rgba(255, 255, 255, 0.02); 
        backdrop-filter: blur(25px); 
        border-radius: 12px; 
        padding: 60px 40px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        margin-bottom: 20px; 
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .main-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* TÍTULO CENTRALIZADO E MINIMALISTA */
    .title-center {
        text-align: center;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #f0f2f6 !important;
        margin-top: 80px;
        margin-bottom: 60px;
        font-weight: 700;
        font-size: 2.2rem;
    }

    h4 { 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        margin-bottom: 10px;
        color: #ffffff;
        font-weight: 500;
    }

    /* BOTÕES EXECUTIVOS */
    .stButton button {
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 10px;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 4px;
    }
    
    .stButton button:hover {
        border: 1px solid #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING LATERAL ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    st.caption("v5.0 | Strategic Governance")

# --- CORPO DO DASHBOARD ---
st.markdown('<h1 class="title-center">DASHBOARD ESTRATÉGICO</h1>', unsafe_allow_html=True)

# Grid de Navegação
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="main-card">
            <h4>📍 Matriz STAR</h4>
            <p style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>Governança e Diagnóstico de Carteira</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("ACESSAR MATRIZ STAR")

with c2:
    st.markdown("""
        <div class="main-card">
            <h4>📊 Matriz de Desempenho</h4>
            <p style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>Gestão de Ritmo e Eficiência Individual</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("ACESSAR DESEMPENHO")
