import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

# DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    st.subheader("📅 JANELAS DE GOVERNANÇA")
    lp_val = st.number_input("Longo Prazo (Meses)", value=12)
    cp_val = st.number_input("Curto Prazo (Meses)", value=3)

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
st.markdown('</div>', unsafe_allow_html=True)

def format_br(val):
    try: return f"{int(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    cols = [str(c).upper() for c in df_raw.columns]
    df_raw.columns = cols # Normaliza para evitar erro de caixa alta/baixa

    # FILTRO RÍGIDO: Só aceitamos o que é FOCO (Vendedor, Segmento, Cidade)
    focos_permitidos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
    dimensoes_reais = [c for c in cols if any(f in c for f in focos_permitidos)]

    with st.sidebar:
        st.markdown("---")
        st.subheader("📂 CHAVES DE GOVERNANÇA")
        dims_selecionadas = []
        for d in dimensoes_reais:
            if st.checkbox(d, key=f"chk_{d}"):
                dims_selecionadas.append(d)
        
        if not dimensoes_reais:
            st.error("Colunas de Vendedor, Segmento ou Cidade não detectadas.")

    if dims_selecionadas:
        # Identifica meses
        col_meses = [c for c in cols if any(m in c for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c]
        
        df = df_raw.copy()
        for col in col_meses:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        cols_cp = col_meses[-cp_val:]
        cols_lp = col_meses[-(lp_val + cp_val):-cp_val]
        
        # Agrupamento pelas chaves escolhidas
        chaves = ['EMPRESA'] + dims_selecionadas
        df_agrupado = df.groupby(chaves)[col_meses].sum().reset_index()

        df_agrupado['MEDIA_LP'] = (df_agrupado[cols_lp].sum(axis=1) / len(cols_lp)).round(0)
        df_agrupado['MEDIA_CP'] = (df_agrupado[cols_cp].sum(axis=1) / len(cols_cp)).round(0)

        def engine_star(row):
            lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
            if cp == 0: return "⚫ INATIVO", lp, "REATIVAÇÃO: Visita imediata necessária."
            if cp < (lp * 0.85): return "🔴 QUEDA", lp, "DEFESA: Investigar perda de share."
            if cp > (lp * 1.15): return "🟢 CRESCIMENTO", int(cp * 1.10), "EXPANSÃO: Aplicar Upsell."
            return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Blindagem de conta."

        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*df_agrupado.apply(engine_star, axis=1))

        st.subheader("Matriz de Decisão Tática")
        exibir = chaves + ['MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        st.dataframe(df_agrupado[exibir].sort_values('MEDIA_LP', ascending=False).style.format({"MEDIA_LP": format_br, "MEDIA_CP": format_br, "META": format_br}), use_container_width=True)
