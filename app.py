import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; word-wrap: break-word !important; min-width: 300px; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
    cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")

def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp, cp):
    if cp == 0: 
        return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência.\nORIENTAÇÃO: Foque no negócio do cliente."
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix.\nORIENTAÇÃO: Recupere o giro."
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão.\nAÇÃO: Upsell tático.\nORIENTAÇÃO: Eleve o ticket médio."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Validar satisfação.\nORIENTAÇÃO: Mantenha a recorrência."

uploaded_file = st.file_uploader("Upload da Base", type=['xlsx'])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    
    # Blindagem: Se houver colunas com nomes repetidos no Excel, o Pandas adiciona .1, .2. Vamos limpar.
    cols = df_raw.columns.tolist()

    # Identificação da Coluna Mestra
    col_cliente = next((c for c in ["EMPRESA", "CLIENTE", "NOME", "RAZAO SOCIAL"] if c in cols), cols[0])

    focos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
    dim_reais = [c for c in cols if any(f in c for f in focos)]

    with st.sidebar:
        st.subheader("📂 CHAVES DE GOVERNANÇA")
        dims_sel = [d for d in dim_reais if st.checkbox(d, key=f"chk_{d}")]

    meses_ref = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    col_meses = [c for c in cols if any(m in c for m in meses_ref) and 'TOTAL' not in c]

    if col_meses:
        df = df_raw.copy()
        for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # A CORREÇÃO TÁTICA: Usamos drop() para garantir que as chaves não causem conflito no reset_index
        chaves_agrupamento = list(dict.fromkeys([col_cliente] + dims_sel))
        
        # Agrupamento com tratamento de erro para reset_index
        df_agrupado = df.groupby(chaves_agrupamento, as_index=False)[col_meses].sum()

        df_agrupado['TOTAL_ACUMULADO'] = df_agrupado[col_meses].sum(axis=1).round(0)
        
        disponivel = len(col_meses)
        idx_cp = col_meses[-min(cp_val, disponivel):]
        idx_lp = col_meses[-min((lp_val+cp_val), disponivel):-min(cp_val, disponivel)] if disponivel > cp_val else col_meses
        
        df_agrupado['MEDIA_LP'] = df_agrupado[idx_lp].mean(axis=1).round(0)
        df_agrupado['MEDIA_CP'] = df_agrupado[idx_cp].mean(axis=1).round(0)

        res = df_agrupado.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res)

        df_final = df_agrupado.sort_values('TOTAL_ACUMULADO', ascending=False)
        colunas_ex = chaves_agrupamento + col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        # Remoção de duplicatas na lista de exibição para evitar novo erro de "Already Exists"
        colunas_ex = list(dict.fromkeys(colunas_ex))

        st.subheader("Matriz de Decisão Tática")
        st.dataframe(df_final[colunas_ex].style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_final[colunas_ex].to_excel(writer, index=False, sheet_name='MATRIZ_STAR')
            workbook, worksheet = writer.book, writer.sheets['MATRIZ_STAR']
            
            h_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#001220', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            b_fmt = workbook.add_format({'bold': True, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
            wrap_fmt = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left'})
            
            for col_num, value in enumerate(colunas_ex):
                worksheet.write(0, col_num, value, h_fmt)
            
            ws_rows = len(df_final)
            worksheet.set_column(colunas_ex.index('AÇÃO'), colunas_ex.index('AÇÃO'), 60)
            worksheet.set_default_row(70)

        st.download_button("📥 EXPORTAR PLANO", output.getvalue(), "Plano_STAR_Giri.xlsx")
