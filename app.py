import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGÊNCIA DE MAPEAMENTO ---
def identificar_colunas(df_cols):
    mapeamento = {'CLIENTE': None, 'VENDEDOR': None, 'CIDADE': None, 'MESES': []}
    
    # Dicionários de Sinônimos Táticos
    syn_cliente = ['EMPRESA', 'CLIENTE', 'NOME', 'RAZAO', 'IDENTIFICAO']
    syn_vendedor = ['VENDEDOR', 'REP', 'CONSULTOR', 'RESPONSAVEL', 'AGENTE', 'NOME DO VENDEDOR']
    syn_cidade = ['CIDADE', 'MUNICIPIO', 'LOCALIDADE', 'UF', 'REGIAO']
    
    # Padrões de Data (REGEX para Jan/25, 01/25, Janeiro 2025, etc.)
    padrao_data = r"(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|0[1-9]|1[0-2])[-/ ]?(20)?[2-9][0-9]"

    for col in df_cols:
        c_upper = str(col).upper().strip()
        
        # Identifica Meses/Série Temporal
        if re.search(padrao_data, c_upper) and 'TOTAL' not in c_upper:
            mapeamento['MESES'].append(col)
        elif any(s in c_upper for s in syn_cliente) and not mapeamento['CLIENTE']:
            mapeamento['CLIENTE'] = col
        elif any(s in c_upper for s in syn_vendedor) and not mapeamento['VENDEDOR']:
            mapeamento['VENDEDOR'] = col
        elif any(s in c_upper for s in syn_cidade) and not mapeamento['CIDADE']:
            mapeamento['CIDADE'] = col
            
    return mapeamento

def engine_star(row, lp, cp):
    if cp == 0: 
        return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.85):
        return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio do cliente e recupere margem."
    if cp < (lp * 0.98): 
        return "🔴 QUEDA", lp, "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix e frequência.\nORIENTAÇÃO: Recupere o giro histórico."
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão (Upsell).\nAÇÃO: Ofertar itens complementares.\nORIENTAÇÃO: Aproveite o momento de tração para elevar o ticket."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Manutenção e rituais de gestão.\nORIENTAÇÃO: Garanta a recorrência e satisfação."

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    lp_meses = st.number_input("Meses Longo Prazo", value=12, min_value=1)
    cp_meses = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | MATRIZ DE DECISÃO TÁTICA")

up = st.file_uploader("Arraste sua planilha aqui", type=['xlsx', 'csv'])

if up:
    df_raw = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
    mapa = identificar_colunas(df_raw.columns)
    
    if not mapa['MESES']:
        st.error("Erro: Não identifiquei colunas de faturamento temporal (ex: Jan/25).")
    else:
        # 1. Normalização de Dados
        df = df_raw.copy()
        for c in mapa['MESES']: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
        # 2. Agrupamento e Hierarquia
        chaves = [c for c in [mapa['CLIENTE'], mapa['VENDEDOR'], mapa['CIDADE']] if c]
        df_ag = df.groupby(chaves, as_index=False)[mapa['MESES']].sum()
        
        # 3. Cálculos de Governança
        # Faturamento Total de Longo Prazo (Base da Hierarquia)
        col_lp = mapa['MESES'][-lp_meses:]
        col_cp = mapa['MESES'][-cp_meses:]
        
        df_ag['TOTAL_LP'] = df_ag[col_lp].sum(axis=1).round(0)
        df_ag['MEDIA_LP'] = (df_ag['TOTAL_LP'] / len(col_lp)).round(0)
        df_ag['MEDIA_CP'] = (df_ag[col_cp].sum(axis=1) / len(col_cp)).round(0)
        
        # ORDENAÇÃO DECRESCENTE POR FATURAMENTO LP (Sua Regra de Ouro)
        df_ag = df_ag.sort_values('TOTAL_LP', ascending=False).reset_index(drop=True)
        
        # CURVA ABC
        df_ag['CURVA'] = (df_ag['TOTAL_LP'].cumsum() / df_ag['TOTAL_LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        # Aplicação do Método STAR
        res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
        df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
        
        # Formatação para Exibição
        cols_final = ['CURVA'] + chaves + mapa['MESES'] + ['TOTAL_LP', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader(f"Análise de {len(df_ag)} clientes ordenada por Faturamento Total ({lp_meses} meses)")
        
        def fmt_moeda(x): return f"R$ {int(x):,}".replace(",", ".") if x > 0 else "-"
        
        st.dataframe(df_ag[cols_final].style.apply(lambda x: ['background-color: #002b36' if i%2==0 else '' for i in range(len(x))], axis=0), use_container_width=True)

        # EXPORTAÇÃO EXECUTIVA (Excel Blindado)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_ag[cols_final].to_excel(wr, index=False, sheet_name='MATRIZ_STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            
            # Estilos C-Level
            header = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'white', 'border':1, 'align':'center', 'valign':'vcenter'})
            money = wb.add_format({'num_format':'"R$ "#,##0', 'align':'center', 'valign':'vcenter', 'border':1})
            text = wb.add_format({'text_wrap':True, 'valign':'vcenter', 'border':1})
            
            for i, col in enumerate(cols_final):
                ws.write(0, i, col, header)
                # Ajuste de largura inteligente
                width = 50 if col == 'AÇÃO' else (40 if col == mapa['CLIENTE'] else 15)
                ws.set_column(i, i, width)
            
            ws.set_default_row(70) # Altura para as ações respirarem

        st.download_button("📥 BAIXAR MATRIZ DE GOVERNANÇA STAR", output.getvalue(), "Giri_Matriz_STAR.xlsx")
