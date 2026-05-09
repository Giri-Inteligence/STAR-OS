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
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
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
        return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn e Reconexão.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Contenção de Perda e Defesa de Share.\nAÇÃO: Investigar entrada de concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele e entenda onde perde margem."
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, "OBJETIVO: Estabilização de Giro.\nAÇÃO: Identificar se a queda é sazonal ou substituição de mix.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas."
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão de Share e Upsell.\nAÇÃO: Analisar mix de clientes similares e elevar Ticket Médio.\nORIENTAÇÃO: Recomende itens complementares."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Manutenção e Blindagem.\nAÇÃO: Prevenir inércia e validar satisfação.\nORIENTAÇÃO: Confirme se os objetivos estão sendo atingidos."

uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    # Normalização de colunas: remove espaços e coloca em maiúsculo
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    # Identificação inteligente da coluna de Empresa/Cliente
    col_cliente = None
    possiveis_clientes = ["EMPRESA", "CLIENTE", "NOME", "RAZAO SOCIAL", "NOME DO CLIENTE"]
    for p in possiveis_clientes:
        if p in cols:
            col_cliente = p
            break
    if not col_cliente:
        col_cliente = cols[0] # Fallback: usa a primeira coluna

    focos_permitidos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
    dimensoes_reais = [c for c in cols if any(f in c for f in focos_permitidos)]

    with st.sidebar:
        st.subheader("📂 CHAVES DE GOVERNANÇA")
        dims_selecionadas = [d for d in dimensoes_reais if st.checkbox(d, key=f"chk_{d}")]

    # Filtro de meses (Ignora colunas que não são meses)
    meses_validos = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    col_meses = [c for c in cols if any(m in c for m in meses_validos) and 'TOTAL' not in c]

    if not col_meses:
        st.error("Erro: Nenhuma coluna de faturamento mensal (JAN, FEV, etc) foi encontrada.")
    else:
        df = df_raw.copy()
        for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Montagem segura das chaves de agrupamento
        chaves_agrupamento = [col_cliente] + dims_selecionadas
        
        # O ERRO ACONTECIA AQUI. Agora usamos chaves_agrupamento que foi validada.
        df_agrupado = df.groupby(chaves_agrupamento)[col_meses].sum().reset_index()

        df_agrupado['TOTAL_ACUMULADO'] = df_agrupado[col_meses].sum(axis=1).round(0)
        
        # Lógica de Médias (Curto vs Longo Prazo)
        # Proteção para não estourar o limite de colunas caso o arquivo tenha poucos meses
        disponivel = len(col_meses)
        idx_cp = col_meses[-min(cp_val, disponivel):]
        idx_lp = col_meses[-min((lp_val+cp_val), disponivel):-min(cp_val, disponivel)] if disponivel > cp_val else col_meses
        
        df_agrupado['MEDIA_LP'] = (df_agrupado[idx_lp].mean(axis=1)).round(0)
        df_agrupado['MEDIA_CP'] = (df_agrupado[idx_cp].mean(axis=1)).round(0)

        res = df_agrupado.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res)

        df_final = df_agrupado.sort_values('TOTAL_ACUMULADO', ascending=False)
        colunas_exibicao = chaves_agrupamento + col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader("Matriz de Decisão Tática")
        st.dataframe(df_final[colunas_exibicao].style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

        # Geração do Excel com formatação executiva
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_final[colunas_exibicao].to_excel(writer, index=False, sheet_name='MATRIZ_STAR')
            workbook, worksheet = writer.book, writer.sheets['MATRIZ_STAR']

            header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#001220', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            num_fmt = workbook.add_format({'num_format': '#,##0', 'align': 'center', 'valign': 'vcenter'})
            wrap_fmt = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left'})
            bold_part = workbook.add_format({'bold': True, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})

            for col_num, value in enumerate(colunas_exibicao):
                worksheet.write(0, col_num, value, header_fmt)

            acao_idx = colunas_exibicao.index('AÇÃO')
            status_idx = colunas_exibicao.index('STATUS')

            for row_num, row_data in enumerate(df_final[colunas_exibicao].values):
                for col_num, cell_value in enumerate(row_data):
                    if col_num == acao_idx:
                        parts = str(cell_value).split('\n')
                        rich_text = []
                        for p in parts:
                            if ':' in p:
                                label, content = p.split(':', 1)
                                rich_text.extend([bold_part, label + ':', wrap_fmt, content + '\n'])
                        if rich_text:
                            worksheet.write_rich_string(row_num + 1, col_num, *rich_text, wrap_fmt)
                        else:
                            worksheet.write(row_num + 1, col_num, cell_value, wrap_fmt)
                    else:
                        fmt = num_fmt if isinstance(cell_value, (num_fmt, int, float)) else wrap_fmt
                        worksheet.write(row_num + 1, col_num, cell_value, fmt)

            worksheet.set_column(acao_idx, acao_idx, 60)
            worksheet.set_column(0, acao_idx-1, 20)
            worksheet.set_default_row(70) # Aumenta altura das linhas para o texto respirar

        st.download_button("📥 EXPORTAR PLANO EXECUTIVO", output.getvalue(), "Plano_STAR_Giri.xlsx")
