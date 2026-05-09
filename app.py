import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

# --- CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

# [Lógica de processamento de dados preservada conforme versões anteriores]

def exportar_matriz_star(df_proc, ordem, col_meses):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
        df_proc[ordem].to_excel(wr, index=False, sheet_name='STAR')
        wb, ws = wr.book, wr.sheets['STAR']
        
        # 1. FORMATOS COM ALINHAMENTO SUPERIOR (TOP) - PADRÃO GIRI
        f_h = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
        f_txt = wb.add_format({'valign':'top', 'align':'left', 'border':1, 'text_wrap':True, 'font_size': 10})
        f_num = wb.add_format({'num_format':'#,##0', 'valign':'top', 'align':'center', 'border':1})
        f_total = wb.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        
        # Status colorizados
        f_st_qa = wb.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        f_st_q = wb.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        f_st_c = wb.add_format({'font_color':'#006100', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        f_st_e = wb.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'top', 'align':'center', 'border':1})

        # 2. APLICAÇÃO DA REGRA DE ALTURA ÚNICA (O MAIOR TEXTO POSSÍVEL)
        # Travamos em 165, que é a altura exata para o manual de "Crescimento Acentuado" fluir em 90 de largura.
        ws.set_default_row(165) 
        ws.set_row(0, 45) # Cabeçalho diferenciado
        
        # 3. GEOMETRIA DAS COLUNAS
        for i, col in enumerate(ordem):
            ws.write(0, i, col, f_h)
            if col == 'AÇÃO': 
                ws.set_column(i, i, 90, f_txt) # Largura otimizada para o manual
            elif col == 'STATUS': 
                ws.set_column(i, i, 22)
            elif col in ('TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'META', 'CURVA') or col in col_meses: 
                ws.set_column(i, i, 9, f_num) # Compactação das métricas
            else: 
                ws.set_column(i, i, 25, f_txt)

        # 4. ESCRITA DOS DADOS
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
    return output.getvalue()

# [Botão de download e interface preservados]
