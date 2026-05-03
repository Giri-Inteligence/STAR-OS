import streamlit as st

# 1. DESIGN EXECUTIVO GIRI - CAMADAS DE PROFUNDIDADE (GLASSMORPHISM)
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    /* FUNDO COM GRADIENTE RADIAL MAIS PROFUNDO */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); 
        color: #ffffff; 
    }
    
    /* REMOÇÃO DE CABEÇALHOS PADRÃO */
    header {visibility: hidden;}
    
    /* MENU LATERAL ULTRA-CLEAN */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* CARDS ESTILO 'GLASS' (VIDRO) */
    .tool-card { 
        background: rgba(255, 255, 255, 0.01); 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px);
        border-radius: 4px; /* Cantos mais retos transmitem seriedade */
        padding: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        text-align: left; /* Alinhamento à esquerda é mais executivo */
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    
    .tool-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 150, 255, 0.1);
    }

    .title-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 6px;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 60px;
        margin-bottom: 50px;
        font-weight: 800;
        font-size: 1.8rem;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    .card-id {
        font-family: 'Courier New', monospace;
        font-size: 0.6rem;
        color: rgba(255, 255, 255, 0.2);
        margin-bottom: 8px;
    }

    h4 { 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        font-size: 0.85rem; 
        margin: 0; 
        color: #ffffff; 
        font-weight: 700; 
    }
    
    p { 
        color: rgba(255, 255, 255, 0.4); 
        font-size: 0.65rem; 
        line-height: 1.4; 
        margin-top: 8px; 
        font-weight: 300; 
        letter-spacing: 0.5px;
    }

    /* GATILHO INVISÍVEL */
    .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 130px !important;
        width: 100% !important;
        position: absolute;
        top: -130px;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br><br><h2 style='letter-spacing:2px; font-size:1rem;'>GIRI | ARCHITECTURE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.6rem; color:grey;'>SYSTEMS GOVERNANCE v5.5</p>", unsafe_allow_html=True)

st.markdown('<h1 class="title-center">Dashboard Estratégico</h1>', unsafe_allow_html=True)

# GRID DE 4 COLUNAS
cols = st.columns(4)

# FERRAMENTAS COM DESIGN REFINADO
tools = [
    ("MATRIZ STAR", "DIAGNÓSTICO DE CARTEIRA E GOVERNANÇA DE CHURN", "MOD-01", "btn_star"),
    ("MATRIZ DE DESEMPENHO", "GESTÃO DE RITMO E EFICIÊNCIA INDIVIDUAL", "MOD-02", "btn_desempenho"),
    ("ARQUITETURA COMERCIAL", "ESTRUTURAÇÃO DE PROCESSOS E PLAYBOOKS", "MOD-03", "btn_arch"),
    ("PIPELINE PREDICTOR", "PREVISIBILIDADE DE RECEITA B2B", "MOD-04", "btn_pipe")
]

for i, (title, desc, mod_id, key) in enumerate(tools):
    with cols[i % 4]:
        st.markdown(f"""
            <div class="tool-card">
                <div>
                    <div class="card-id">{mod_id}</div>
                    <h4>{title}</h4>
                </div>
                <p>{desc}</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("", key=key):
            if "MATRIZ STAR" in title: st.session_state.pagina_ativa = 'Matriz'
            elif "DESEMPENHO" in title: st.session_state.pagina_ativa = 'Desempenho'
            st.rerun()
