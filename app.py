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
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE LEITURA E TRANSFORMAÇÃO ---
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

    # MANUAL TÁTICO WILLIAM BERTO - INTEGRAL
    txt_ina = "OBJETIVO: Diagnóstico de causa\nPRÉ-CONTATO: Revisar último pedido. Identificar o que parou de ser comprado e em que momento.\nCONTATO: Contato de diagnóstico. Entender o motivo da inatividade sem pressão de venda.\nORIENTAÇÃO: Não ofertar produto na primeira interação. Primeiro entender o que aconteceu. Registrar motivo antes de qualquer ação de reconquista."
    txt_q_ac = "OBJETIVO: Recuperação emergencial\nPRÉ-CONTATO: Revisar histórico completo do cliente. Identificar exatamente quais produtos caíram, em que momento e qual era o volume anterior. Calcular o gap entre a média histórica e o momento atual.\nCONTATO: Priorizar visita presencial ou ligação direta — não mensagem. Abrir diagnóstico sem pressão. Entender se houve mudança interna no cliente, problema de relacionamento ou entrada de concorrente.\nORIENTAÇÃO: Este cliente está em risco de perda. O objetivo da primeira interação não é vender — é entender. Registrar causa com precisão. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    txt_q = "OBJETIVO: Estabilização\nPRÉ-CONTATO: Revisar histórico de mix. Identificar quais produtos reduziram ou desapareceram nos últimos 3 meses.\nCONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudança operacional, financeira ou troca de fornecedor.\nORIENTAÇÃO: Registrar causa identificada. Se houver abertura, propor recomposição de mix com base no histórico anterior."
    txt_est = "OBJETIVO: Blindagem e crescimento incremental\nPRÉ-CONTATO: Revisar mix atual. Mapear categorias que o cliente não compra mas que são compatíveis com seu perfil.\nCONTATO: Manter frequência de relacionamento. Explorar oportunidade de expansão de mix.\nORIENTAÇÃO: Cliente estável não é cliente seguro. Monitorar frequência de pedidos e introduzir novos itens gradualmente."
    txt_cre = "OBJETIVO: Consolidação\nPRÉ-CONTATO: Identificar o driver do crescimento. Avaliar se é sazonalidade ou mudança estrutural no cliente.\nCONTATO: Reforçar relacionamento. Garantir abastecimento e antecipar demanda dos próximos períodos.\nORIENTAÇÃO: Proteger o cliente. Momento de crescimento é o de maior risco de abordagem pelo concorrente."
    txt_cre_ac = "OBJETIVO: Consolidação e proteção\nPRÉ-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar esse volume ou se é pontual. Verificar se há mix ainda não explorado.\nCONTATO: Reforçar presença. Garantir que o abastecimento está adequado ao novo patamar de compra. Antecipar pedidos futuros.\nORIENTAÇÃO: Crescimento acentuado atrai concorrência. Este é o momento de maior risco de abordagem externa. Aumentar frequência de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."

    if cp_v <= 0: return "⚫ INATIVO", 0, txt_ina
    if lp_v <= 0: return "🔵 ESTÁVEL", int(cp_v * 1.05), txt_est
    if cp_v < (lp_v * 0.85): return "🚨 QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < (lp_v * 0.98): return "🔴 QUEDA", int(lp_v), txt_q
    if cp_v > (lp_v * 1.20): return "🚀 CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_cre_ac
    if cp_v > (lp_v * 1.05): return "🟢 CRESCIMENTO", int(cp_v * 1.05), txt_cre
    return "🔵 ESTÁVEL", int(lp_v * 1.05), txt_est

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    cp_m = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")
up = st.file_uploader("Upload da Planilha", type=('xlsx', 'csv'))

if up:
    df_raw = ler_dados_seguros(up)
    df_proc, col_meses, chaves = identificar_e_pivotar(df_raw)
    
    if col_meses:
        for c in chaves: df_proc[c] = df_proc[c].fillna("-").astype(str)
        for c in col_meses: df_proc[c] = pd.to_numeric(df_proc[c], errors='coerce').fillna(0)
        
        col_ativas = [c for c in col_meses if df_proc[c].sum() > 0]
        df_proc['TOTAL LP'] = df_proc[col_ativas].sum(axis=1).fillna(0).astype(int)
        df_proc['MÉDIA LP'] = (df_proc[col_ativas].mean(axis=1)).fillna(0).astype(int)
        df_proc['MÉDIA CP'] = (df_proc[col_ativas[-min(cp_m, len(col_ativas)):]].mean(axis=1)).fillna(0).astype(int)
        
        df_proc = df_proc.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
        df_proc['CURVA'] = (df_proc['TOTAL LP'].cumsum() / df_proc['TOTAL LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_proc.apply(lambda r: engine_star(r, r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
        df_proc['STATUS'], df_proc['META'], df_proc['AÇÃO'] = zip(*res)

        ordem = ['CURVA'] + chaves + col_meses + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']
        
        # EXPORTAÇÃO CORRIGIDA (V135)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_proc[ordem].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            
            # FORMATOS EXECUTIVOS
            h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
            b_f_texto = wb.add_format({'valign':'vcenter', 'align':'left', 'border':1, 'text_wrap':True})
            b_f_num = wb.add_format({'num_format':'#,##0', 'valign':'vcenter', 'align':'center', 'border':1})
            total_f = wb.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            
            # APLICAÇÃO DE LARGURA E ALTURA
            ws.set_default_row(180) # ALTURA PARA CABER O MANUAL TODO
            ws.set_row(0, 40) # Cabeçalho menor
            
            for i, col in enumerate(ordem):
                ws.write(0, i, col, h_f)
                if col == 'AÇÃO': ws.set_column(i, i, 80, b_f_texto)
                elif col == 'STATUS': ws.set_column(i, i, 20, b_f_texto)
                elif col in chaves: ws.set_column(i, i, 30, b_f_texto)
                elif col == 'TOTAL LP': ws.set_column(i, i, 12, total_f)
                else: ws.set_column(i, i, 10, b_f_num)

            # ESCREVER DADOS COM SEGURANÇA
            for r_idx, row in df_proc.iterrows():
                for c_idx, col_name in enumerate(ordem):
                    val = row[col_name]
                    if col_name == 'AÇÃO':
                        ws.write_string(r_idx + 1, c_idx, str(val), b_f_texto)
                    elif col_name in ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META'] or col_name in col_meses:
                        ws.write_number(r_idx + 1, c_idx, int(val), total_f if col_name == 'TOTAL LP' else b_f_num)
                    else:
                        ws.write_string(r_idx + 1, c_idx, str(val), b_f_texto)

        st.download_button("📥 BAIXAR MATRIZ STAR (V135 - LEITURA COMPLETA)", output.getvalue(), "Matriz_STAR_Giri_V135.xlsx")
