import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | INTELLIGENCE")
    st.markdown("---")
    lp_val = st.number_input("Janela Longo Prazo (Meses)", value=12)
    cp_val = st.number_input("Janela Curto Prazo (Meses)", value=3)

st.title("STAR-OS | MATRIZ DE GOVERNANÇA")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
st.markdown('</div>', unsafe_allow_html=True)

def format_br(val):
    return f"{val:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    cols = df.columns.tolist()
    
    # Identifica colunas de meses para ESCONDER dos seletores
    col_meses = [c for c in cols if any(m in c.upper() for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) or 'TOTAL' in c.upper()]
    # Colunas que sobram são as "Dimensões de Gestão"
    col_gestao = [c for c in cols if c not in col_meses and c != 'EMPRESA']

    with st.sidebar:
        st.subheader("📂 DIMENSÕES")
        dim_vendedor = st.selectbox("👤 Vendedor", ["Nenhum"] + col_gestao)
        dim_segmento = st.selectbox("🏢 Segmento", ["Nenhum"] + col_gestao)

    # Limpeza de dados de faturamento
    for col in [c for c in col_meses if 'TOTAL' not in c.upper()]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Lógica de Médias
    meses_limpos = [c for c in col_meses if 'TOTAL' not in c.upper()]
    if len(meses_limpos) >= cp_val:
        cols_cp = meses_limpos[-cp_val:]
        cols_lp = meses_limpos[-(lp_val + cp_val):-cp_val]
        
        df['MEDIA_LP'] = (df[cols_lp].sum(axis=1) / len(cols_lp)).round(0).astype(int)
        df['MEDIA_CP'] = (df[cols_cp].sum(axis=1) / len(cols_cp)).round(0).astype(int)

        # MOTOR DE STATUS (⚫ PARA INATIVO)
        def engine_star(row):
            lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
            if cp == 0: return "⚫ INATIVO", lp, "RECUPERAÇÃO: Sem compra há 90 dias. Visita imediata."
            if cp < (lp * 0.85): return "🔴 QUEDA", lp, "DEFESA: Perda de share. Investigar concorrência."
            if cp > (lp * 1.15): return "🟢 CRESCIMENTO", int(cp * 1.10), "EXPANSÃO: Tração positiva. Upsell."
            return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Garantir rituais e blindagem."

        df['STATUS'], df['META'], df['AÇÃO'] = zip(*df.apply(engine_star, axis=1))

        # EXIBIÇÃO LIMPA
        exibir = ['EMPRESA']
        if dim_vendedor != "Nenhum": exibir.append(dim_vendedor)
        if dim_segmento != "Nenhum": exibir.append(dim_segmento)
        exibir += ['MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader("Matriz de Decisão Tática")
        st.dataframe(df[exibir].style.format({"MEDIA_LP": format_br, "MEDIA_CP": format_br, "META": format_br}), use_container_width=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df[exibir].to_excel(writer, index=False, sheet_name='STAR_OS')
        st.download_button("📥 BAIXAR PLANO DE AÇÃO", output.getvalue(), "Plano_STAR_Giri.xlsx")
