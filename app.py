import streamlit as st
import pandas as pd
import numpy as np
import re
import datetime
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

# --- MOTOR DE LEITURA INTELIGENTE (CORREÇÃO DE PONTEIRO) ---
def ler_dados_seguros(file):
    """Lê o arquivo de forma segura, ignorando cabeçalhos falsos de ERPs."""
    file.seek(0) # Rebobina o arquivo para a estaca zero
    if file.name.endswith('xlsx'):
        df_temp = pd.read_excel(file, header=None, nrows=15)
    else:
        df_temp = pd.read_csv(file, header=None, nrows=15)
        
    header_idx = 0
    # Procura a linha que contém as palavras-chave do negócio
    for i in range(len(df_temp)):
        row_str = " ".join([str(x).upper() for x in df_temp.iloc[i].fillna('')])
        if any(k in row_str for k in ["CLIENTE", "EMPRESA", "JAN", "FEV", "VENDEDOR", "CIDADE"]):
            header_idx = i
            break
            
    file.seek(0) # Rebobina NOVAMENTE para a leitura oficial
    if file.name.endswith('xlsx'):
        return pd.read_excel(file, header=header_idx)
    else:
        return pd.read_csv(file, header=header_idx)

# --- MOTOR DE MAPEAMENTO E NORMALIZAÇÃO ---
def identificar_colunas(df):
    mapa = {'CLIENTE': None, 'VENDEDOR': None, 'CIDADE': None, 'MESES': []}
    syn_cliente = ['EMPRESA', 'CLIENTE', 'NOME', 'RAZAO', 'IDENTIFICAO']
    syn_vendedor = ['VENDEDOR', 'REP', 'CONSULTOR', 'RESPONSAVEL', 'AGENTE', 'PATRICIA', 'JEFERSON']
    syn_cidade = ['CIDADE', 'MUNICIPIO', 'LOCALIDADE', 'UF', 'REGIAO']

    for col in df.columns:
        c_str = str(col).strip().upper()
        is_date = False
        
        if isinstance(col, (pd.Timestamp, datetime.date)): 
            is_date = True
        elif re.search(r"\b(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)\b", c_str): 
            is_date = True
        elif re.search(r"\b\d{1,2}[/-]\d{2,4}\b", c_str): 
            is_date = True
            
        if is_date and 'TOTAL' not in c_str: 
            mapa['MESES'].append(col)
        elif any(s in c_str for s in syn_cliente) and not mapa['CLIENTE']: 
            mapa['CLIENTE'] = col
        elif any(s in c_str for s in syn_vendedor) and not mapa['VENDEDOR']: 
            mapa['VENDEDOR'] = col
        elif any(s in c_str for s in syn_cidade) and not mapa['CIDADE']: 
            mapa['CIDADE'] = col
            
    return mapa

# --- NÚCLEO TÁTICO BLINDADO (ANTI-STRING) ---
def engine_star(row, lp, cp):
    # Imunidade Numérica: Garante que lixo textual vire zero e não quebre a ferramenta
    try:
        cp_val = float(str(cp).replace(',', '.')) if pd.notnull(cp) and str(cp).strip() not in ['', '-'] else 0.0
    except: cp_val = 0.0
        
    try:
        lp_val = float(str(lp).replace(',', '.')) if pd.notnull(lp) and str(lp).strip() not in ['', '-'] else 0.0
    except: lp_val = 0.0

    if cp_val <= 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if lp_val <= 0: return "🔵 ESTÁVEL", int(cp_val * 1.05), "OBJETIVO: Manutenção inicial.\nAÇÃO: Validar satisfação.\nORIENTAÇÃO: Acompanhe a integração do cliente novo."
    if cp_val < (lp_val * 0.85): return "🚨 QUEDA ACENTUADA", int(lp_val), "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Entenda onde ele perde margem."
    if cp_val < (lp_val * 0.98): return "🔴 QUEDA", int(lp_val), "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix e frequência.\nORIENTAÇÃO: Sugira ajustes que reduzam perdas."
    if cp_val > (lp_val * 1.05): return "🟢 CRESCIMENTO", int(cp_val * 1.05), "OBJETIVO: Expansão (Upsell).\nAÇÃO: Analisar mix de clientes similares.\nORIENTAÇÃO: Aproveite a tração para elevar o ticket."
    return "🔵 ESTÁVEL", int(lp_val * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Manutenção e rituais.\nORIENTAÇÃO: Garanta a recorrência."

def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    lp_m = st.number_input("Meses Longo Prazo", value=12, min_value=1)
    cp_m = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | MATRIZ DE DECISÃO TÁTICA")
up = st.file_uploader("Upload da Planilha (Aceita Exportações de ERP)", type=['xlsx', 'csv'])

if up:
    df_raw = ler_dados_seguros(up)
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    
    mapa = identificar_colunas(df_raw)
    
    if not mapa['MESES']:
        st.error("Erro Estrutural: Não foi possível identificar as colunas de faturamento mensal.")
    else:
        df = df_raw.copy()
        for c in mapa['MESES']: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
        chaves_base = [mapa['CLIENTE'] or df.columns[0]]
        with st.sidebar:
            st.subheader("CHAVES")
            dims_sel = [d for d in [mapa['VENDEDOR'], mapa['CIDADE']] if d and st.checkbox(d, key=f"c_{d}")]
        
        chaves_final = list(dict.fromkeys(chaves_base + dims_sel))
        df_ag = df.groupby(chaves_final, as_index=False)[mapa['MESES']].sum()
        
        # Filtro de Sanidade: Ignora meses projetados vazios
        col_com_dados = [c for c in mapa['MESES'] if df_ag[c].sum() > 0]
        
        if not col_com_dados:
            st.error("O arquivo lido não possui faturamento válido (valores maiores que zero) nas colunas detectadas.")
        else:
            c_lp = col_com_dados[-min(lp_m, len(col_com_dados)):]
            c_cp = col_com_dados[-min(cp_m, len(col_com_dados)):]
            
            df_ag['TOTAL_LP'] = df_ag[c_lp].sum(axis=1).round(0)
            df_ag['MEDIA_LP'] = (df_ag['TOTAL_LP'] / max(1, len(c_lp))).round(0)
            df_ag['MEDIA_CP'] = (df_ag[c_cp].sum(axis=1) / max(1, len(c_cp))).round(0)
            
            df_ag = df_ag.sort_values('TOTAL_LP', ascending=False).reset_index(drop=True)
            df_ag['CURVA'] = (df_ag['TOTAL_LP'].cumsum() / df_ag['TOTAL_LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
            
            res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)

            # --- PREPARAÇÃO DE EXIBIÇÃO (ANTI-DUPLICIDADE) ---
            df_view = df_ag.copy()
            df_view = df_view.loc[:, ~df_view.columns.duplicated()]
            
            nomes_meses_str = [str(c).split(' ')[0] if isinstance(c, (pd.Timestamp, datetime.date)) else str(c) for c in mapa['MESES']]
            df_view = df_view.rename(columns=dict(zip(mapa['MESES'], nomes_meses_str)))

            ordem_view = ['CURVA'] + chaves_final + nomes_meses_str + ['TOTAL_LP', 'STATUS', 'META', 'AÇÃO']
            ordem_view = list(dict.fromkeys(ordem_view))

            st.subheader(f"GOVERNANÇA STAR: {len(df_ag)} CLIENTES PRIORIZADOS")
            
            # Formatação Executiva na Tela
            cols_format = [c for c in nomes_meses_str + ['TOTAL_LP', 'META'] if c in df_view.columns]
            st.dataframe(df_view[ordem_view].style.format({c: format_br for c in cols_format}), use_container_width=True)

            # EXPORTAÇÃO EXCEL C-LEVEL
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
                df_view[ordem_view].to_excel(wr, index=False, sheet_name='STAR')
                wb, ws = wr.book, wr.sheets['STAR']
                
                # Cores e Contrastes Fixados
                h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
                
                for i, col in enumerate(ordem_view): ws.write(0, i, col, h_f)
                ws.set_default_row(75)
                ws.set_column(1, 1, 45) # Identidade do Cliente
                ws.set_column(len(ordem_view)-1, len(ordem_view)-1, 80) # Instruções STAR

            st.download_button("📥 EXPORTAR LAUDO DE GOVERNANÇA", output.getvalue(), "Matriz_STAR_Giri.xlsx")
