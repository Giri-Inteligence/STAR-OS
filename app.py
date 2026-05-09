import streamlit as st
import pandas as pd
import numpy as np
import re
import datetime
from io import BytesIO
import xlsxwriter

# 1. AMBIENTE EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DE DADOS ---
def ler_dados_seguros(file):
    file.seek(0)
    df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

def identificar_e_pivotar(df):
    cols = df.columns.tolist()
    mapa = {'CLIENTE': None, 'VENDEDOR': None, 'MESES_COL': []}
    syn_cliente = ("CLIENTE", "EMPRESA", "RAZAO", "NOME")
    syn_vendedor = ("VENDEDOR", "REP", "CONSULTOR")
    meses_pt = ("JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ")

    for c in cols:
        c_str = str(c).upper()
        if any(m in c_str for m in meses_pt) or re.search(r"\d{1,2}[/-]\d{2,4}", c_str):
            mapa['MESES_COL'].append(c)
        if any(s in c_str for s in syn_cliente) and not mapa['CLIENTE']: mapa['CLIENTE'] = c
        if any(s in c_str for s in syn_vendedor) and not mapa['VENDEDOR']: mapa['VENDEDOR'] = c

    return df, mapa['MESES_COL'], [c for c in (mapa['CLIENTE'], mapa['VENDEDOR']) if c]

def engine_star(lp, cp):
    try: lp_v, cp_v = float(lp), float(cp)
    except: lp_v, cp_v = 0.0, 0.0

    # MANUAL TÁTICO WILLIAM BERTO (LITERAL)
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
up = st.file_uploader("Upload da Base", type=('xlsx', 'csv'))

if up:
    df_raw = ler_dados_seguros(up)
    df_proc, col_meses, chaves = identificar_e_pivotar(df_raw)
    
    if col_meses:
        for c in chaves: df_proc[c] = df_proc[c].fillna("-").astype(str)
        for c in col_meses: df_proc[c] = pd.to_numeric(df_proc[c], errors='coerce').fillna(0)
        
        # MUDANÇA DE NOMES PARA EMPILHAMENTO NO EXCEL
        df_proc['TOTAL LP'] = df_proc[col_meses].sum(axis=1).astype(int)
        df_proc['MÉDIA LP'] = (df_proc[col_meses].mean(axis=1)).astype(int)
        df_proc['MÉDIA CP'] = (df_proc[col_meses[-3:]].mean(axis=1)).astype(int)
        
        df_proc = df_proc.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
        df_proc['CURVA'] = (df_proc['TOTAL LP'].cumsum() / df_proc['TOTAL LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_proc.apply(lambda r: engine_star(r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
        df_proc['STATUS'], df_proc['META'], df_proc['AÇÃO'] = zip(*res)

        ordem = ['CURVA'] + chaves + col_meses + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_proc[ordem].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            
            # --- FORMATOS RÍGIDOS (RESTAURAÇÃO COMPLETA) ---
            f_h = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
            f_txt = wb.add_format({'valign':'vcenter', 'align':'left', 'border':1, 'text_wrap':True})
            f_num = wb.add_format({'num_format':'#,##0', 'valign':'vcenter', 'align':'center', 'border':1})
            
            # TRAVA: TOTAL LP (CINZA + NEGRITO)
            f_total = wb.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            
            # TRAVA: CORES DOS STATUS
            f_st_qa = wb.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            f_st_q = wb.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            f_st_c = wb.add_format({'font_color':'#006100', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})
            f_st_e = wb.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'vcenter', 'align':'center', 'border':1})

            # CONFIGURAÇÃO DE CÉLULA (MÁXIMA DENSIDADE)
            ws.set_default_row(180) 
            ws.set_row(0, 45) # Altura para o cabeçalho empilhado
            
            for i, col in enumerate(ordem):
                ws.write(0, i, col, f_h)
                if col == 'AÇÃO': ws.set_column(i, i, 75, f_txt)
                elif col == 'STATUS': ws.set_column(i, i, 22)
                elif col in ('TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META'): ws.set_column(i, i, 9)
                elif col in col_meses: ws.set_column(i, i, 9)
                else: ws.set_column(i, i, 28, f_txt)

            # ESCRITA RÍGIDA LINHA POR LINHA
            for r_idx, row in df_proc.iterrows():
                ex_row = r_idx + 1
                for c_idx, col_name in enumerate(ordem):
                    val = row[col_name]
                    
                    if col_name == 'STATUS':
                        fmt = f_num
                        if "QUEDA ACENTUADA" in str(val): fmt = f_st_qa
                        elif "QUEDA" in str(val): fmt = f_st_q
                        elif "CRESCIMENTO" in str(val): fmt = f_st_c
                        elif "ESTÁVEL" in str(val): fmt = f_st_e
                        ws.write_string(ex_row, c_idx, str(val), fmt)
                    
                    elif col_name == 'TOTAL LP':
                        ws.write_number(ex_row, c_idx, int(val), f_total)
                    
                    elif col_name in ('MÉDIA LP', 'MÉDIA CP', 'META') or col_name in col_meses:
                        ws.write_number(ex_row, c_idx, int(val), f_num)
                    
                    else:
                        ws.write_string(ex_row, c_idx, str(val), f_txt)

        st.download_button("📥 BAIXAR MATRIZ STAR (V138 - RESTAURAÇÃO TOTAL)", output.getvalue(), "Giri_Matriz_STAR_Final.xlsx")
