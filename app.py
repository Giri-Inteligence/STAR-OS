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
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp_val, cp_val):
    lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
    
    # REGRA 0: INATIVIDADE (Meta Zero para Diagnóstico)
    if cp == 0: 
        return "⚫ INATIVO", 0, "DIAGNÓSTICO: Cliente sem compra há 90 dias. Retomar contato e entender o ocorrido antes de ofertar."
    
    # REGRA 1: QUEDA ACENTUADA (Severidade > 20%)
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, "INTERVENÇÃO IMEDIATA: Colapso de volume (>20%). Exige ação de diretoria e defesa de share."
        
    # REGRA 2: QUEDA (Sensibilidade 5% a 20%)
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, "DEFESA: Desvio negativo detectado. Investigar concorrência ou falha pontual."
    
    # REGRA 3: CRESCIMENTO (Meta de 5% sobre o Curto Prazo)
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "EXPANSÃO: Tração positiva detectada. Manter rampa com meta de 5% sobre o realizado recente."
    
    # REGRA 4: ESTABILIDADE (+/- 5%)
    return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Ritual de atendimento e blindagem de conta."

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    cols = [str(c).upper() for c in df_raw.columns]
    df_raw.columns = cols 

    focos_permitidos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
    dimensoes_reais = [c for c in cols if any(f in c for f in focos_permitidos)]

    with st.sidebar:
        st.markdown("---")
        st.subheader("📂 CHAVES DE GOVERNANÇA")
        dims_selecionadas = []
        for d in dimensoes_reais:
            if st.checkbox(d, key=f"chk_{d}"):
                dims_selecionadas.append(d)

    if dims_selecionadas or not dimensoes_reais:
        col_meses = [c for c in cols if any(m in c for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c]
        
        df = df_raw.copy()
        for col in col_meses:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        cols_cp = col_meses[-cp_val:]
        cols_lp = col_meses[-(lp_val + cp_val):-cp_val]
        
        chaves = ['EMPRESA'] + dims_selecionadas
        df_agrupado = df.groupby(chaves)[col_meses].sum().reset_index()

        df_agrupado['TOTAL_ACUMULADO'] = df_agrupado[col_meses].sum(axis=1).round(0)
        df_agrupado['MEDIA_LP'] = (df_agrupado[cols_lp].sum(axis=1) / len(cols_lp)).round(0)
        df_agrupado['MEDIA_CP'] = (df_agrupado[cols_cp].sum(axis=1) / len(cols_cp)).round(0)

        res = df_agrupado.apply(lambda row: engine_star(row, lp_val, cp_val), axis=1)
        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res)

        colunas_exibicao = chaves + col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader("Matriz de Decisão Tática")
        format_map = {col: format_br for col in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}
        
        st.dataframe(
            df_agrupado[colunas_exibicao].sort_values('TOTAL_ACUMULADO', ascending=False).style.format(format_map),
            use_container_width=True
        )

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_agrupado[colunas_exibicao].to_excel(writer, index=False, sheet_name='STAR_OS')
        st.download_button("📥 EXPORTAR PLANO DE TRABALHO", output.getvalue(), "Plano_STAR_Giri.xlsx")
