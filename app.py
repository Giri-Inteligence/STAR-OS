import streamlit as st
import pandas as pd
import numpy as np
import re
import datetime
from io import BytesIO
import xlsxwriter

# DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; text-align: center !important; }
    div[data-testid="stDataFrame"] td:nth-child(2), div[data-testid="stDataFrame"] td:nth-child(3) { text-align: left !important; }
    </style>
    """, unsafe_allow_html=True)

# MOTOR DE LEITURA E TRANSFORMAÇÃO
def ler_dados_seguros(file):
    file.seek(0)
    if file.name.endswith('xlsx'):
        df_temp = pd.read_excel(file, header=None, nrows=15)
    else:
        df_temp = pd.read_csv(file, header=None, nrows=15)
    
    header_idx = 0
    for i in range(len(df_temp)):
        row_str = " ".join([str(x).upper() for x in df_temp.iloc[i].fillna('')])
        if any(k in row_str for k in ("CLIENTE", "EMPRESA", "DATA", "VENDEDOR", "VALOR")):
            header_idx = i
            break
            
    file.seek(0)
    df = pd.read_excel(file, header=header_idx) if file.name.endswith('xlsx') else pd.read_csv(file, header=header_idx)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

def identificar_e_pivotar(df):
    cols = df.columns.tolist()
    mapa = {'CLIENTE': None, 'VENDEDOR': None, 'DATA': None, 'VALOR': None, 'MESES_COL': []}
    syn_cliente = ("CLIENTE", "EMPRESA", "RAZAO", "NOME")
    syn_vendedor = ("VENDEDOR", "REP", "CONSULTOR", "PATRICIA", "JEFERSON")
    syn_valor = ("VALOR", "TOTAL", "FATURAMENTO", "LIQUIDO", "BRUTO")
    meses_pt = ("JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ")

    for c in cols:
        c_str = str(c).upper()
        if any(m in c_str for m in meses_pt) or re.search(r"\d{1,2}[/-]\d{2,4}", c_str):
            mapa['MESES_COL'].append(c)
        if any(s in c_str for s in syn_cliente) and not mapa['CLIENTE']: mapa['CLIENTE'] = c
        if any(s in c_str for s in syn_vendedor) and not mapa['VENDEDOR']: mapa['VENDEDOR'] = c
        if any(s in c_str for s in syn_valor) and not mapa['VALOR']: mapa['VALOR'] = c
        if ("DATA" in c_str or "EMISSAO" in c_str) and not mapa['DATA']: mapa['DATA'] = c

    if len(mapa['MESES_COL']) <= 1 and mapa['DATA'] and mapa['VALOR']:
        df[mapa['DATA']] = pd.to_datetime(df[mapa['DATA']], errors='coerce')
        df = df.dropna(subset=(mapa['DATA']))
        df['MES_REF'] = df[mapa['DATA']].dt.strftime('%b/%y').str.upper()
        chaves = [c for c in (mapa['CLIENTE'], mapa['VENDEDOR']) if c]
        df_pivot = df.pivot_table(index=chaves, columns='MES_REF', values=mapa['VALOR'], aggfunc='sum').fillna(0).reset_index()
        meses_ordenados = sorted(df_pivot.columns[len(chaves):], key=lambda x: datetime.datetime.strptime(x, '%b/%y'))
        return df_pivot[chaves + meses_ordenados], meses_ordenados, chaves

    return df, mapa['MESES_COL'], [c for c in (mapa['CLIENTE'], mapa['VENDEDOR']) if c]

def engine_star(row, lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except: lp_v, cp_v = 0.0, 0.0

    if cp_v <= 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if lp_v <= 0: return "🔵 ESTÁVEL", int(cp_v * 1.05), "OBJETIVO: Manutenção.\nAÇÃO: Validar satisfação inicial.\nORIENTAÇÃO: Acompanhe a integração do cliente novo."
    if cp_v < (lp_v * 0.85): return "🚨 QUEDA ACENTUADA", int(lp_v), "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência.\nORIENTAÇÃO: Entenda onde ele perde margem."
    if cp_v < (lp_v * 0.98): return "🔴 QUEDA", int(lp_v), "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix.\nORIENTAÇÃO: Sugira ajustes que reduzam perdas."
    if cp_v > (lp_v * 1.05): return "🟢 CRESCIMENTO", int(cp_v * 1.05), "OBJETIVO: Expansão.\nAÇÃO: Upsell tático.\nORIENTAÇÃO: Eleve o ticket médio."
    return "🔵 ESTÁVEL", int(lp_v * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Rituais de gestão.\nORIENTAÇÃO: Garanta a recorrência."

def format_sem_centavos(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

# INTERFACE E GOVERNANÇA
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    cp_m = st.number_input("Meses Curto Prazo", value=3, min_value=1)
    st.markdown("Longo Prazo: Dinâmico (Totalidade do histórico).")

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")
up = st.file_uploader("Upload da Planilha", type=('xlsx', 'csv'))

if up:
    df_raw = ler_dados_seguros(up)
    df_proc, col_meses, chaves = identificar_e_pivotar(df_raw)
    
    if not col_meses:
        st.error("Falha na detecção temporal.")
    else:
        for c in col_meses: df_proc[c] = pd.to_numeric(df_proc[c], errors='coerce').fillna(0)
        col_ativas = [c for c in col_meses if df_proc[c].sum() > 0]
        
        # Consolidação Numérica com Nomenclatura Preparada para Empilhamento
        df_proc['TOTAL LP'] = df_proc[col_ativas].sum(axis=1).round(0).astype(int)
        df_proc['MÉDIA LP'] = (df_proc[col_ativas].mean(axis=1)).round(0).astype(int)
        df_proc['MÉDIA CP'] = (df_proc[col_ativas[-min(cp_m, len(col_ativas)):]].mean(axis=1)).round(0).astype(int)
        
        df_proc = df_proc.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
        df_proc['CURVA'] = (df_proc['TOTAL LP'].cumsum() / df_proc['TOTAL LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_proc.apply(lambda r: engine_star(r, r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
        df_proc['STATUS'], df_proc['META'], df_proc['AÇÃO'] = zip(*res)

        ordem = ['CURVA'] + chaves + col_meses + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']
        cols_numericas = col_meses + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META']
        
        st.subheader("MATRIZ DE DECISÃO TÁTICA")
        st.dataframe(df_proc[ordem].style.format({c: format_sem_centavos for c in cols_numericas}), use_container_width=True)

        # EXPORTAÇÃO EXECUTIVA E GEOMETRIA DE DADOS
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_proc[ordem].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            
            # FORMATOS TRAVADOS
            h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
            b_f_texto = wb.add_format({'valign':'vcenter', 'align':'left', 'border':1, 'border_color':'#D9D9D9', 'text_wrap':True})
            b_f_num = wb.add_format({'num_format':'#,##0', 'valign':'vcenter', 'align':'center', 'border':1, 'border_color':'#D9D9D9'})
            b_f_status_base = wb.add_format({'valign':'vcenter', 'align':'center', 'border':1, 'border_color':'#D9D9D9', 'text_wrap':True})
            meta_f = wb.add_format({'num_format':'#,##0', 'valign':'vcenter', 'align':'center', 'bold':True, 'border':1, 'border_color':'#D9D9D9'})
            
            # GATILHOS DE STATUS
            fmt_qa = wb.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            fmt_q = wb.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            fmt_c = wb.add_format({'font_color':'#006100', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            fmt_e = wb.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            fmt_ina = wb.add_format({'valign':'vcenter', 'align':'center', 'border':1, 'border_color':'#D9D9D9'})
            
            # CONFIGURAÇÃO DE LINHA E EMPILHAMENTO DE CABEÇALHO
            ws.set_row(0, 45) # Altura expandida na linha zero para acomodar o texto empilhado
            
            for i, col in enumerate(ordem):
                ws.write(0, i, col, h_f)
                # COMPRESSÃO AGRESSIVA DAS COLUNAS
                if col == 'AÇÃO': ws.set_column(i, i, 75, b_f_texto)
                elif col == 'STATUS': ws.set_column(i, i, 22, b_f_status_base)
                elif col == 'CLIENTE' or 'RAZAO' in str(col): ws.set_column(i, i, 35, b_f_texto)
                elif col == 'VENDEDOR' or 'REP' in str(col) or 'CIDADE' in str(col): ws.set_column(i, i, 22, b_f_texto)
                elif col in ('CURVA', 'TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META'): ws.set_column(i, i, 9, meta_f if col == 'META' else b_f_num)
                else: ws.set_column(i, i, 9, b_f_num) # Meses cronológicos também comprimidos

            status_idx = ordem.index('STATUS')
            meta_idx = ordem.index('META')
            
            for row_num in range(1, len(df_proc) + 1):
                ws.write(row_num, meta_idx, int(df_proc.iloc[row_num-1]['META']), meta_f)
                
                st_val = str(df_proc.iloc[row_num-1]['STATUS'])
                current_fmt = b_f_status_base
                if "QUEDA ACENTUADA" in st_val: current_fmt = fmt_qa
                elif "QUEDA" in st_val: current_fmt = fmt_q
                elif "CRESCIMENTO" in st_val: current_fmt = fmt_c
                elif "ESTÁVEL" in st_val: current_fmt = fmt_e
                elif "INATIVO" in st_val: current_fmt = fmt_ina
                
                ws.write(row_num, status_idx, st_val, current_fmt)

            ws.set_default_row(75)

        st.download_button("📥 EXPORTAR MATRIZ STAR (ALTA DENSIDADE)", output.getvalue(), "Giri_Matriz_STAR_Densidade.xlsx")
