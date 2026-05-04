import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Architecture Hub", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] { background-color: #000810 !important; border-right: 1px solid rgba(255, 255, 255, 0.1) !important; min-width: 240px !important; }
    .sidebar-title { margin-top: -30px; margin-bottom: 20px; letter-spacing: 2px; font-size: 1.1rem; font-weight: 800; color: white; text-transform: uppercase; }

    .tool-card { 
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border-radius: 4px; padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.08); text-align: center; height: 110px; display: flex; 
        flex-direction: column; justify-content: center; transition: all 0.3s ease;
    }
    
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }

    .stSelectbox div[data-baseweb="select"] { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important; 
        border-radius: 4px !important; min-height: 42px !important;
    }

    div[data-testid="stDownloadButton"] button { 
        height: 42px !important; border-radius: 6px !important; 
        border: 1px solid rgba(255, 255, 255, 0.3) !important; 
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03)) !important;
        color: #ffffff !important; font-weight: 800 !important; text-transform: uppercase !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important;
        transition: all 0.2s ease-in-out !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES GLOBAIS ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "0"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp, cp):
    if cp == 0: 
        return "⚫ INATIVO", 0, ("OBJETIVO: Diagnóstico de Churn e Reconexão.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo real da parada.")
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, ("OBJETIVO: Contenção de Perda e Defesa de Share.\nAÇÃO: Investigar entrada de concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele e entenda onde perde margem.")
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, ("OBJETIVO: Estabilização de Giro.\nAÇÃO: Identificar se a queda é sazonal ou substituição de mix.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas.")
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), ("OBJETIVO: Expansão de Share e Upsell.\nAÇÃO: Analisar mix de clientes similares e elevar Ticket Médio.\nORIENTAÇÃO: Recomende itens complementares.")
    return "🔵 ESTÁVEL", int(lp * 1.05), ("OBJETIVO: Manutenção e Blindagem.\nAÇÃO: Prevenir inércia e validar satisfação.\nORIENTAÇÃO: Confirme se os objetivos estão sendo atingidos.")

# --- NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'
with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    if st.session_state.pagina_ativa != 'Dashboard' and st.button("⬅ VOLTAR"):
        st.session_state.pagina_ativa = 'Dashboard'; st.rerun()
    if st.session_state.pagina_ativa == 'Matriz':
        lp_val = st.number_input("Longo Prazo (Meses)", value=15, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

# --- TELA: MATRIZ STAR ---
if st.session_state.pagina_ativa == 'Matriz':
    st.markdown('<div class="title-center">MATRIZ STAR</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        df_raw.columns = [str(c).upper() for c in df_raw.columns]
        dimensoes_reais = [c for c in df_raw.columns if any(f in c for f in ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"])]
        
        with st.sidebar:
            st.subheader("GOVERNANÇA")
            dims_selecionadas = [d for d in dimensoes_reais if st.checkbox(d, key=f"chk_{d}")]
            
        if dims_selecionadas:
            dim_principal = dims_selecionadas[0]
            col_meses = [c for c in df_raw.columns if any(m in c for m in ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'])]
            df = df_raw.copy()
            for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            periodo_meses = col_meses[-lp_val:]
            chaves = ['EMPRESA'] + dims_selecionadas
            df_ag = df.groupby(chaves)[col_meses].sum().reset_index()
            df_ag['TOTAL_ACUMULADO'] = df_ag[periodo_meses].sum(axis=1).round(0)
            df_ag['MEDIA_LP'] = (df_ag[periodo_meses].sum(axis=1) / len(periodo_meses)).round(0)
            df_ag['MEDIA_CP'] = (df_ag[col_meses[-cp_val:]].sum(axis=1) / cp_val).round(0)
            
            # Cálculo da Curva ABC por Cliente
            df_ag = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)
            df_ag['CUM_SUM'] = df_ag['TOTAL_ACUMULADO'].cumsum()
            total_geral = df_ag['TOTAL_ACUMULADO'].sum()
            df_ag['PCT_ACUM'] = df_ag['CUM_SUM'] / total_geral if total_geral > 0 else 0
            df_ag['CURVA'] = df_ag['PCT_ACUM'].apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))
            
            res = df_ag.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
            df_final = df_ag.sort_values(['CURVA', 'TOTAL_ACUMULADO'], ascending=[True, False])

            # --- DRILL-DOWN TÁTICO E EXPORTAÇÃO EXECUTIVA ---
            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#ccc;margin-top:20px;margin-bottom:10px;">🔬 DRILL-DOWN TÁTICO: ISOLAMENTO DE CARTEIRA</div>', unsafe_allow_html=True)
            repres = df_final.groupby(dim_principal)['TOTAL_ACUMULADO'].sum().sort_values(ascending=False)
            opcoes = ["TODOS OS SEGMENTOS"] + repres.index.tolist()
            if 'mem_f' not in st.session_state: st.session_state.mem_f = "TODOS OS SEGMENTOS"
            
            col_f, col_ex = st.columns([3, 2])
            with col_f:
                f_sel = st.selectbox("X", opcoes, index=opcoes.index(st.session_state.mem_f) if st.session_state.mem_f in opcoes else 0, label_visibility="collapsed", key="sel_f")
                st.session_state.mem_f = f_sel
            
            df_exib = df_final[df_final[dim_principal] == f_sel] if f_sel != "TODOS OS SEGMENTOS" else df_final
            colunas_view = ['CURVA'] + list(df_exib.columns[:-3]) + ['TOTAL_ACUMULADO', 'STATUS', 'META', 'AÇÃO']
            
            with col_ex:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_exib[colunas_view].to_excel(writer, index=False, sheet_name='MATRIZ_STAR')
                    workbook, worksheet = writer.book, writer.sheets['MATRIZ_STAR']
                    
                    # FORMATOS EXCEL EXECUTIVOS
                    header_fmt = workbook.add_format({
                        'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#002060',
                        'border': 1, 'border_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True
                    })
                    base_fmt = workbook.add_format({'valign': 'vcenter', 'align': 'left', 'border': 1, 'border_color': '#D9D9D9'})
                    num_fmt = workbook.add_format({'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': '#D9D9D9'})
                    wrap_fmt = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left', 'border': 1, 'border_color': '#D9D9D9'})
                    bold_lbl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap': True})

                    fmt_queda = workbook.add_format({'font_color': '#FF0000', 'bold': True, 'valign': 'vcenter', 'border': 1})
                    fmt_queda_ac = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True, 'valign': 'vcenter', 'border': 1})
                    fmt_cresc = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': True, 'valign': 'vcenter', 'border': 1})
                    fmt_estav = workbook.add_format({'bg_color': '#DDEBF7', 'font_color': '#0070C0', 'bold': True, 'valign': 'vcenter', 'border': 1})

                    for col_num, value in enumerate(colunas_view):
                        worksheet.write(0, col_num, value, header_fmt)

                    acao_idx = colunas_view.index('AÇÃO')
                    status_idx = colunas_view.index('STATUS')
                    
                    for r_idx, (idx, row) in enumerate(df_exib.iterrows()):
                        s_val = str(row['STATUS'])
                        t_fmt = base_fmt
                        if "QUEDA ACENTUADA" in s_val: t_fmt = fmt_queda_ac
                        elif "🔴 QUEDA" in s_val: t_fmt = fmt_queda
                        elif "CRESCIMENTO" in s_val: t_fmt = fmt_cresc
                        elif "ESTÁVEL" in s_val: t_fmt = fmt_estav
                        
                        for c_idx, col_name in enumerate(colunas_view):
                            val = row[col_name]
                            if c_idx == status_idx: worksheet.write(r_idx + 1, c_idx, val, t_fmt)
                            elif c_idx == acao_idx:
                                parts = str(val).split('\n')
                                rich = []
                                for p in parts:
                                    if ':' in p:
                                        lbl, cont = p.split(':', 1)
                                        rich.extend([bold_lbl, lbl + ':', wrap_fmt, cont + '\n'])
                                if rich: worksheet.write_rich_string(r_idx + 1, acao_idx, *rich, wrap_fmt)
                                else: worksheet.write(r_idx + 1, c_idx, val, wrap_fmt)
                            elif isinstance(val, (int, float)): worksheet.write(r_idx + 1, c_idx, int(val), num_fmt)
                            else: worksheet.write(r_idx + 1, c_idx, val, base_fmt)

                    worksheet.set_column(0, 0, 8) # Curva
                    worksheet.set_column(1, 1, 45) # Empresa
                    worksheet.set_column(acao_idx, acao_idx, 75) 
                    worksheet.set_default_row(65)

                st.download_button(f"📥 EXPORTAR {f_sel.upper()}", output.getvalue(), f"Giri_Matriz_STAR_{f_sel}.xlsx")

            st.dataframe(df_exib[colunas_view].style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

# --- DASHBOARD ---
elif st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">GIRI | ARCHITECTURE</h1>', unsafe_allow_html=True)
    if st.button("ACESSAR MATRIZ STAR", use_container_width=True):
        st.session_state.pagina_ativa = 'Matriz'; st.rerun()
