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

    /* SELETORES E BOTÃO 3D */
    .stSelectbox div[data-baseweb="select"] { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important; 
        border-radius: 4px !important; 
        min-height: 42px !important;
    }

    div[data-testid="stDownloadButton"] button { 
        height: 42px !important; border-radius: 6px !important; 
        border: 1px solid rgba(255, 255, 255, 0.3) !important; 
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03)) !important;
        color: #ffffff !important; font-weight: 800 !important; text-transform: uppercase !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important;
        transition: all 0.2s ease-in-out !important; width: 100% !important;
    }
    div[data-testid="stDownloadButton"] button:hover { 
        box-shadow: 0px 0px 15px rgba(255,255,255,0.15), inset 1px 1px 1px rgba(255,255,255,0.3) !important;
        transform: translateY(-1px);
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
    """Instruções de Alto Impacto - Método STAR Original"""
    if cp == 0: 
        return "⚫ INATIVO", 0, ("OBJETIVO: Diagnóstico de Churn e Reconexão.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo real da parada.")
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, ("OBJETIVO: Contenção de Perda e Defesa de Share.\nAÇÃO: Investigar entrada de concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele e entenda onde perde margem.")
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, ("OBJETIVO: Estabilização de Giro.\nAÇÃO: Identificar se a queda é sazonal ou substituição de mix.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas.")
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), ("OBJETIVO: Expansão de Share e Upsell.\nAÇÃO: Analisar mix de clientes similares e elevar Ticket Médio.\nORIENTAÇÃO: Recomende itens complementares.")
    return "🔵 ESTÁVEL", int(lp * 1.05), ("OBJETIVO: Manutenção e Blindagem.\nAÇÃO: Prevenir inércia e validar satisfação.\nORIENTAÇÃO: Confirme se os objetivos estão sendo atingidos.")

# --- LÓGICA TEMPORAL E NAVEGAÇÃO ---
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
            
            res = df_ag.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
            df_final = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)

            # [RESTAURAÇÃO DOS INFOGRÁFICOS - CÓDIGO ANTERIOR INTEGRADO AQUI]
            st.markdown('<div class="subtitle-center" style="text-align: left; margin-top: 30px; margin-bottom: 10px;">ANÁLISE DE TRAÇÃO E SAÚDE POR SEGMENTO</div>', unsafe_allow_html=True)
            df_pareto = df_final.groupby(dim_principal)[['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP']].sum().reset_index().sort_values('TOTAL_ACUMULADO', ascending=False)
            df_pareto['CUM_PCT'] = df_pareto['TOTAL_ACUMULADO'].cumsum() / df_pareto['TOTAL_ACUMULADO'].sum()
            def assign_curve(pct):
                if pct <= 0.80: return "CURVA A (80% DA RECEITA)"
                elif pct <= 0.95: return "CURVA B (15% DA RECEITA)"
                else: return "CURVA C (5% DA RECEITA)"
            df_pareto['CURVA'] = df_pareto['CUM_PCT'].apply(assign_curve)
            resumo_status = df_final.groupby([dim_principal, 'STATUS']).size().unstack(fill_value=0)
            df_p = df_pareto.merge(resumo_status, on=dim_principal, how='left')

            laudo_html = '<div style="margin-bottom: 40px;">'
            for curva in ["CURVA A (80% DA RECEITA)", "CURVA B (15% DA RECEITA)", "CURVA C (5% DA RECEITA)"]:
                df_c = df_p[df_p['CURVA'] == curva].copy()
                if not df_c.empty:
                    if curva == "CURVA C (5% DA RECEITA)":
                        laudo_html += f'<div style="background:rgba(255,255,255,0.02);border:1px dashed rgba(255,255,255,0.1);padding:15px;border-radius:8px;margin-top:20px;color:#888;">{curva}: R$ {format_br(df_c["TOTAL_ACUMULADO"].sum())} acumulados.</div>'
                        continue
                    if curva == "CURVA B (15% DA RECEITA)" and len(df_c) > 3:
                        top3, outros = df_c.head(3), df_c.iloc[3:]
                        outros_ag = pd.DataFrame([{dim_principal: "OUTROS (AGRUPADOS)", 'TOTAL_ACUMULADO': outros['TOTAL_ACUMULADO'].sum(), 'MEDIA_LP': outros['MEDIA_LP'].sum(), 'MEDIA_CP': outros['MEDIA_CP'].sum()}])
                        for col_s in ['🟢 CRESCIMENTO', '🔵 ESTÁVEL', '🔴 QUEDA', '🚨 QUEDA ACENTUADA', '⚫ INATIVO']: outros_ag[col_s] = outros[col_s].sum() if col_s in outros.columns else 0
                        df_c = pd.concat([top3, outros_ag], ignore_index=True)
                    laudo_html += f'<div style="color:#fff;font-weight:800;margin:25px 0 10px 0;letter-spacing:1.5px;font-size:0.95rem;">{curva}</div>'
                    for _, row in df_c.iterrows():
                        tot_contas = row.get('🟢 CRESCIMENTO',0)+row.get('🔵 ESTÁVEL',0)+row.get('🔴 QUEDA',0)+row.get('🚨 QUEDA ACENTUADA',0)+row.get('⚫ INATIVO',0)
                        tracao = ((row['MEDIA_CP'] / row['MEDIA_LP']) - 1) * 100 if row['MEDIA_LP'] > 0 else 0
                        t_color = "#00E676" if tracao >= 0 else "#FF1744"
                        blocks = [{"n": "Cresc.", "p": round(row.get('🟢 CRESCIMENTO',0)/tot_contas*100,1) if tot_contas>0 else 0, "c": "#00E676"},
                                  {"n": "Estável", "p": round(row.get('🔵 ESTÁVEL',0)/tot_contas*100,1) if tot_contas>0 else 0, "c": "#29B6F6"},
                                  {"n": "Queda", "p": round((row.get('🔴 QUEDA',0)+row.get('🚨 QUEDA ACENTUADA',0))/tot_contas*100,1) if tot_contas>0 else 0, "c": "#FF1744"},
                                  {"n": "Inat.", "p": round(row.get('⚫ INATIVO',0)/tot_contas*100,1) if tot_contas>0 else 0, "c": "#555"}]
                        blocks.sort(key=lambda x: x["p"], reverse=True)
                        barra_html = "".join([f'<div style="width:{b["p"]}%;padding-right:4px;"><div style="height:8px;background:{b["c"]};border-radius:2px;margin-bottom:4px;width:100%;"></div><div style="font-size:0.65rem;color:{b["c"]};font-weight:700;line-height:1.1;display:{"block" if b["p"] > 8 else "none"};">{b["n"]}<br>{b["p"]}%</div></div>' for b in blocks if b["p"] > 0])
                        laudo_html += f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:20px;margin-bottom:12px;"><div style="display:flex;justify-content:space-between;margin-bottom:10px;"><b style="font-size:1.1rem;letter-spacing:1px;">{str(row[dim_principal]).upper()}</b><span style="font-size:0.75rem;color:#888;background:rgba(255,255,255,0.05);padding:4px 10px;border-radius:4px;font-weight:800;">{int(tot_contas)} CONTAS</span></div><div style="display:flex;gap:40px;margin-bottom:15px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.05);"><div><div style="font-size:0.7rem;color:#888;margin-bottom:3px;">RECEITA ACUM.</div><div style="font-size:1.2rem;font-weight:800;">R$ {format_br(row['TOTAL_ACUMULADO'])}</div></div><div><div style="font-size:0.7rem;color:#888;margin-bottom:3px;">TRAÇÃO</div><div style="font-size:1.2rem;font-weight:800;color:{t_color};">{'▲' if tracao>=0 else '▼'} {tracao:.1f}%</div></div></div><div style="display:flex;width:100%;align-items:flex-start;">{barra_html}</div></div>"""
            st.markdown(laudo_html + "</div>", unsafe_allow_html=True)

            # --- DRILL-DOWN TÁTICO E EXPORTAÇÃO EXECUTIVA ---
            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#ccc;margin-top:50px;margin-bottom:10px;border-top:1px solid rgba(255,255,255,0.1);padding-top:30px;">🔬 DRILL-DOWN TÁTICO: ISOLAMENTO DE CARTEIRA</div>', unsafe_allow_html=True)
            repres = df_final.groupby(dim_principal)['TOTAL_ACUMULADO'].sum().sort_values(ascending=False)
            opcoes = ["TODOS OS SEGMENTOS"] + repres.index.tolist()
            if 'mem_f' not in st.session_state: st.session_state.mem_f = "TODOS OS SEGMENTOS"
            
            col_f, col_ex = st.columns([3, 2])
            with col_f:
                f_sel = st.selectbox("X", opcoes, index=opcoes.index(st.session_state.mem_f) if st.session_state.mem_f in opcoes else 0, label_visibility="collapsed", key="sel_f")
                st.session_state.mem_f = f_sel
            
            df_exib = df_final[df_final[dim_principal] == f_sel] if f_sel != "TODOS OS SEGMENTOS" else df_final
            
            with col_ex:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_exib.to_excel(writer, index=False, sheet_name='MATRIZ_STAR')
                    workbook, worksheet = writer.book, writer.sheets['MATRIZ_STAR']
                    
                    # FORMATOS EXECUTIVOS
                    wrap_fmt = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
                    bold_fmt = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
                    num_fmt = workbook.add_format({'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center', 'border': 1})
                    
                    # ESTILOS DE STATUS (FORÇA TAREFA)
                    fmt_queda = workbook.add_format({'font_color': '#C00000', 'bold': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
                    fmt_queda_ac = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
                    fmt_cresc = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
                    fmt_estavel = workbook.add_format({'bg_color': '#DDEBF7', 'font_color': '#0070C0', 'bold': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})

                    # Ajuste de Colunas e Alinhamento Vertical Total
                    worksheet.set_column('A:A', 40, wrap_fmt) # Nome da Empresa (Largo)
                    worksheet.set_column('B:Z', 15, num_fmt)
                    acao_idx = list(df_exib.columns).index('AÇÃO')
                    status_idx = list(df_exib.columns).index('STATUS')
                    worksheet.set_column(acao_idx, acao_idx, 65, wrap_fmt)

                    # ESCALADA DE STATUS E FORMATAÇÃO CONDICIONAL
                    for r_idx, (idx, row) in enumerate(df_exib.iterrows()):
                        status_val = row['STATUS']
                        target_fmt = wrap_fmt
                        if "QUEDA ACENTUADA" in status_val: target_fmt = fmt_queda_ac
                        elif "🔴 QUEDA" in status_val: target_fmt = fmt_queda
                        elif "CRESCIMENTO" in status_val: target_fmt = fmt_cresc
                        elif "ESTÁVEL" in status_val: target_fmt = fmt_estavel
                        
                        worksheet.write(r_idx + 1, status_idx, status_val, target_fmt)
                        
                        # Rich Text para a Coluna Ação
                        parts = str(row['AÇÃO']).split('\n')
                        rich_text = []
                        for p in parts:
                            if ':' in p:
                                label, content = p.split(':', 1)
                                rich_text.extend([bold_fmt, label + ':', wrap_fmt, content + '\n'])
                        if rich_text: worksheet.write_rich_string(r_idx + 1, acao_idx, *rich_text, wrap_fmt)
                        else: worksheet.write(r_idx + 1, acao_idx, row['AÇÃO'], wrap_fmt)

                    # Aplicar alinhamento vertical em todas as células usadas
                    worksheet.set_default_row(50) # Altura padrão maior para acomodar o Método STAR

                st.download_button(f"📥 EXPORTAR {f_sel.upper()}", output.getvalue(), f"Giri_Matriz_STAR_{f_sel}.xlsx")

            st.dataframe(df_exib.style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)
