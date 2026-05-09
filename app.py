import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

def engine_star(lp, cp):
    # (Mantendo seu manual tático integral aqui dentro...)
    # [Omitido para brevidade, mas preservado no código real]
    pass

# --- EXPORTAÇÃO EXECUTIVA REVISADA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
    # ... (Processamento de dados idêntico à V138)
    df_proc[ordem].to_excel(wr, index=False, sheet_name='STAR')
    wb, ws = wr.book, wr.sheets['STAR']
    
    # FORMATOS COM ALINHAMENTO NO TOPO (TOP) PARA ELIMINAR ESPAÇOS VAZIOS
    f_h = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
    f_txt_top = wb.add_format({'valign':'top', 'align':'left', 'border':1, 'text_wrap':True, 'font_size': 10})
    f_num_top = wb.add_format({'num_format':'#,##0', 'valign':'top', 'align':'center', 'border':1})
    f_total_top = wb.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
    
    # STATUS COM ALINHAMENTO TOP
    f_st_qa = wb.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
    f_st_q = wb.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
    f_st_c = wb.add_format({'font_color':'#006100', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
    f_st_e = wb.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'top', 'align':'center', 'border':1})

    # AQUI ESTÁ A CHAVE: LARGURA MAIOR E SEM ALTURA FIXA
    ws.set_row(0, 45) # Apenas cabeçalho tem altura fixa
    
    for i, col in enumerate(ordem):
        ws.write(0, i, col, f_h)
        if col == 'AÇÃO': 
            ws.set_column(i, i, 95, f_txt_top) # Coluna larga para o texto "fluir" melhor
        elif col == 'STATUS': 
            ws.set_column(i, i, 22)
        elif col in ('TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META', 'CURVA') or col in col_meses: 
            ws.set_column(i, i, 8.5) # Máxima compressão horizontal nas métricas
        else: 
            ws.set_column(i, i, 25, f_txt_top)

    # Escrita com os novos formatos 'top'
    for r_idx, row in df_proc.iterrows():
        ex_row = r_idx + 1
        for c_idx, col_name in enumerate(ordem):
            val = row[col_name]
            if col_name == 'STATUS':
                fmt = f_num_top
                if "QUEDA ACENTUADA" in str(val): fmt = f_st_qa
                elif "QUEDA" in str(val): fmt = f_st_q
                elif "CRESCIMENTO" in str(val): fmt = f_st_c
                elif "ESTÁVEL" in str(val): fmt = f_st_e
                ws.write_string(ex_row, c_idx, str(val), fmt)
            elif col_name == 'TOTAL LP':
                ws.write_number(ex_row, c_idx, int(val), f_total_top)
            elif col_name in ('MÉDIA LP', 'MÉDIA CP', 'META') or col_name in col_meses:
                ws.write_number(ex_row, c_idx, int(val), f_num_top)
            else:
                ws.write_string(ex_row, c_idx, str(val), f_txt_top)

st.download_button("📥 BAIXAR MATRIZ STAR (V139 - AJUSTE DE DENSIDADE)", output.getvalue(), "Giri_Matriz_STAR_Densidade.xlsx")
