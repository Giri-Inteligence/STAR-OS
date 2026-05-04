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
    .tool-card:hover { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); }
    h4 { text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.9rem; margin-bottom: 8px; color: #ffffff; font-weight: 700; }
    .tool-card p { color: rgba(255, 255, 255, 0.4); font-size: 0.7rem; line-height: 1.2; margin: 0; }

    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .vendedor-destaque { text-align: center; text-transform: uppercase; letter-spacing: 3px; color: #ffffff; margin-bottom: 5px; font-weight: 700; font-size: 1.4rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }

    .stTextInput input { height: 40px !important; text-align: center !important; background-color: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 4px !important; color: #ffffff !important; }
    
    div[data-testid="column"] div.stButton { margin-top: -126px; z-index: 10; position: relative; }
    div[data-testid="column"] div.stButton button { height: 110px !important; width: 100% !important; background: transparent !important; border: none !important; color: transparent !important; box-shadow: none !important; }
    div[data-testid="column"] div.stButton button:hover { background: rgba(255, 255, 255, 0.05) !important; border-radius: 4px !important; }

    div[data-testid="stTable"] table { width: 100% !important; }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { text-align: center !important; vertical-align: middle !important; font-size: 13px !important; color: #ffffff !important; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; word-wrap: break-word !important; min-width: 150px; vertical-align: middle !important; }
    
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 800; }
    div[data-testid="stMetricLabel"] p { font-size: 0.8rem !important; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.6); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES GLOBAIS ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def parse_int(val):
    try:
        limpo = str(val).replace(".", "").replace(",", "")
        return int(limpo) if limpo else 0
    except: return 0

def get_business_days(start, end):
    holidays = ['2026-01-01', '2026-05-01', '2026-09-07', '2026-10-12', '2026-11-02', '2026-11-15', '2026-12-25']
    days = pd.date_range(start, end)
    return len([d for d in days if d.weekday() < 5 and d.strftime('%Y-%m-%d') not in holidays])

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

# --- LÓGICA TEMPORAL ---
hoje = datetime.now()
p_dia = hoje.replace(day=1)
u_dia = (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)
d_totais = get_business_days(p_dia, u_dia)
d_passados = get_business_days(p_dia, hoje)
if hoje.weekday() < 5 and hoje.strftime('%Y-%m-%d') not in ['2026-05-01']:
    d_passados = max(0, d_passados - 1)

# --- NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'

with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()

    if st.session_state.pagina_ativa == 'Matriz':
        lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

    if st.session_state.pagina_ativa == 'Desempenho':
        nomes_input = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        lista_vendedores = [v.strip().upper() for v in nomes_input.split('\n') if v.strip()]
        vendedor_selecionado = st.selectbox("SELECIONAR CONSULTOR:", lista_vendedores)

# --- TELA 1: DASHBOARD ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">DASHBOARD ESTRATÉGICO</h1>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div class="tool-card"><h4>MATRIZ STAR</h4><p>Diagnóstico de Carteira e Governança de Churn</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_star", use_container_width=True): 
            st.session_state.pagina_ativa = 'Matriz'
            st.rerun()
    with cols[1]:
        st.markdown('<div class="tool-card"><h4>MATRIZ DE DESEMPENHO</h4><p>Gestão de Ritmo e Eficiência Individual</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_desempenho", use_container_width=True): 
            st.session_state.pagina_ativa = 'Desempenho'
            st.rerun()
    with cols[2]:
        st.markdown('<div class="tool-card"><h4>ARQUITETURA COMERCIAL</h4><p>Estruturação de Processos e Playbooks</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_arch", use_container_width=True): pass
    with cols[3]:
        st.markdown('<div class="tool-card"><h4>PIPELINE PREDICTOR</h4><p>Previsibilidade de Receita B2B</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_pipe", use_container_width=True): pass

# --- TELA 2: MATRIZ STAR ---
elif st.session_state.pagina_ativa == 'Matriz':
    st.markdown('<div class="title-center">MATRIZ STAR</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        cols = [str(c).upper() for c in df_raw.columns]
        df_raw.columns = cols 

        focos_permitidos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
        dimensoes_reais = [c for c in cols if any(f in c for f in focos_permitidos)]

        with st.sidebar:
            st.subheader("📂 CHAVES DE GOVERNANÇA")
            dims_selecionadas = [d for d in dimensoes_reais if st.checkbox(d, key=f"chk_{d}")]

        if dims_selecionadas or not dimensoes_reais:
            col_meses = [c for c in cols if any(m in c for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c]
            df = df_raw.copy()
            for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            chaves = ['EMPRESA'] + dims_selecionadas
            df_agrupado = df.groupby(chaves)[col_meses].sum().reset_index()

            df_agrupado['TOTAL_ACUMULADO'] = df_agrupado[col_meses].sum(axis=1).round(0)
            df_agrupado['MEDIA_LP'] = (df_agrupado[col_meses[-(lp_val+cp_val):-cp_val]].sum(axis=1) / lp_val).round(0)
            df_agrupado['MEDIA_CP'] = (df_agrupado[col_meses[-cp_val:]].sum(axis=1) / cp_val).round(0)

            res = df_agrupado.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
            df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res)

            df_final = df_agrupado.sort_values('TOTAL_ACUMULADO', ascending=False)
            colunas_exibicao = chaves + col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
            
            # --- CAMADA ANALÍTICA: PARETO E SAÚDE DA BASE ---
            st.markdown('<div class="subtitle-center" style="text-align: left; margin-top: 30px; margin-bottom: 5px;">DIAGNÓSTICO ESTRUTURAL DA CARTEIRA</div>', unsafe_allow_html=True)
            
            total_clientes = len(df_final)
            if total_clientes > 0:
                status_pct = (df_final['STATUS'].value_counts() / total_clientes * 100).round(1)
                
                cresc = status_pct.get('🟢 CRESCIMENTO', 0.0)
                estav = status_pct.get('🔵 ESTÁVEL', 0.0)
                queda = status_pct.get('🔴 QUEDA', 0.0)
                queda_ac = status_pct.get('🚨 QUEDA ACENTUADA', 0.0)
                inativo = status_pct.get('⚫ INATIVO', 0.0)
                risco_total = (queda + queda_ac + inativo).round(1)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("EXPANSÃO (CRESCIMENTO)", f"{cresc}%")
                c2.metric("BLINDAGEM (ESTÁVEL)", f"{estav}%")
                c3.metric("CONTENÇÃO (QUEDA)", f"{(queda + queda_ac).round(1)}%")
                c4.metric("CHURN (INATIVO)", f"{inativo}%")

                if dims_selecionadas:
                    dim_principal = dims_selecionadas[0]
                    st.markdown(f'<div class="subtitle-center" style="text-align: left; margin-top: 30px; margin-bottom: 10px;">ANÁLISE DE PARETO E SAÚDE POR {dim_principal.upper()}</div>', unsafe_allow_html=True)
                    
                    df_pareto = df_final.groupby(dim_principal)['TOTAL_ACUMULADO'].sum().reset_index()
                    df_pareto = df_pareto.sort_values('TOTAL_ACUMULADO', ascending=False)
                    df_pareto['CUM_PCT'] = df_pareto['TOTAL_ACUMULADO'].cumsum() / df_pareto['TOTAL_ACUMULADO'].sum()
                    
                    def assign_curve(pct):
                        if pct <= 0.80: return "CURVA A (80% DA RECEITA)"
                        elif pct <= 0.95: return "CURVA B (15% DA RECEITA)"
                        else: return "CURVA C (5% DA RECEITA)"
                        
                    df_pareto['CURVA'] = df_pareto['CUM_PCT'].apply(assign_curve)
                    
                    resumo_dim = df_final.groupby([dim_principal, 'STATUS']).size().unstack(fill_value=0)
                    resumo_dim['TOTAL_CONTAS'] = resumo_dim.sum(axis=1)
                    
                    df_pareto = df_pareto.merge(resumo_dim, on=dim_principal, how='left')
                    
                    st.markdown('<div style="margin-top: 15px; margin-bottom: 25px; font-size: 0.95rem; line-height: 1.5; color: #e0e0e0; background: rgba(255,255,255,0.05); padding: 20px; border-left: 3px solid #001f3f;">', unsafe_allow_html=True)
                    st.markdown("**LAUDO DE DISTRIBUIÇÃO E TRAÇÃO:**")
                    
                    for curva in ["CURVA A (80% DA RECEITA)", "CURVA B (15% DA RECEITA)", "CURVA C (5% DA RECEITA)"]:
                        df_c = df_pareto[df_pareto['CURVA'] == curva]
                        if not df_c.empty:
                            st.markdown(f"<br>**{curva}**", unsafe_allow_html=True)
                            for _, row in df_c.iterrows():
                                tot = row['TOTAL_CONTAS']
                                faturamento = row['TOTAL_ACUMULADO']
                                
                                cresc_val = row.get('🟢 CRESCIMENTO', 0)
                                estav_val = row.get('🔵 ESTÁVEL', 0)
                                queda_val = row.get('🔴 QUEDA', 0) + row.get('🚨 QUEDA ACENTUADA', 0)
                                inat_val = row.get('⚫ INATIVO', 0)
                                
                                p_cresc = round((cresc_val / tot * 100), 1) if tot > 0 else 0
                                p_estav = round((estav_val / tot * 100), 1) if tot > 0 else 0
                                p_queda = round((queda_val / tot * 100), 1) if tot > 0 else 0
                                p_inat = round((inat_val / tot * 100), 1) if tot > 0 else 0
                                
                                fat_str = format_br(faturamento)
                                st.markdown(f"- **{row[dim_principal]}** (Receita Acumulada: R$ {fat_str}) <br> &nbsp;&nbsp;&nbsp; Crescimento: {p_cresc}% | Queda: {p_queda}% | Inativo: {p_inat}% | Estável: {p_estav}%", unsafe_allow_html=True)
                                
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="subtitle-center" style="text-align: left; margin-top: 30px; margin-bottom: 10px;">MATRIZ DE DECISÃO TÁTICA BASE</div>', unsafe_allow_html=True)
            st.dataframe(df_final[colunas_exibicao].style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final[colunas_exibicao].to_excel(writer, index=False, sheet_name='MATRIZ_STAR')
                workbook, worksheet = writer.book, writer.sheets['MATRIZ_STAR']

                header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#001220', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                num_fmt = workbook.add_format({'num_format': '#,##0', 'align': 'center', 'valign': 'vcenter'})
                wrap_fmt = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left'})
                bold_part = workbook.add_format({'bold': True, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})

                fmt_queda = workbook.add_format({'font_color': '#C00000', 'bold': True, 'align': 'left', 'valign': 'vcenter'})
                fmt_queda_ac = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True, 'align': 'left', 'valign': 'vcenter'})
                fmt_cresc = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': True, 'align': 'left', 'valign': 'vcenter'})

                for col_num, value in enumerate(colunas_exibicao):
                    worksheet.write(0, col_num, value, header_fmt)

                acao_idx = colunas_exibicao.index('AÇÃO')
                status_idx = colunas_exibicao.index('STATUS')

                for row_num, row_data in enumerate(df_final[colunas_exibicao].values):
                    for col_num, cell_value in enumerate(row_data):
                        if col_num == acao_idx:
                            parts = cell_value.split('\n')
                            rich_text = []
                            for p in parts:
                                if ':' in p:
                                    label, content = p.split(':', 1)
                                    rich_text.extend([bold_part, label + ':', wrap_fmt, content + '\n'])
                            worksheet.write_rich_string(row_num + 1, col_num, *rich_text, wrap_fmt)
                        else:
                            fmt = num_fmt if isinstance(cell_value, (int, float)) else wrap_fmt
                            worksheet.write(row_num + 1, col_num, cell_value, fmt)

                worksheet.set_column(acao_idx, acao_idx, 60)
                worksheet.set_column(0, acao_idx-1, 20)
                
                worksheet.conditional_format(1, status_idx, len(df_final), status_idx, {'type': 'text', 'criteria': 'containing', 'value': 'QUEDA ACENTUADA', 'format': fmt_queda_ac})
                worksheet.conditional_format(1, status_idx, len(df_final), status_idx, {'type': 'text', 'criteria': 'containing', 'value': 'QUEDA', 'format': fmt_queda})
                worksheet.conditional_format(1, status_idx, len(df_final), status_idx, {'type': 'text', 'criteria': 'containing', 'value': 'CRESCIMENTO', 'format': fmt_cresc})

            st.download_button("📥 EXPORTAR PLANO EXECUTIVO", output.getvalue(), "Plano_STAR_Giri.xlsx")

# --- TELA 3: MATRIZ DE DESEMPENHO ---
elif st.session_state.pagina_ativa == 'Desempenho':
    meses_br = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    
    st.markdown('<div class="title-center">MATRIZ DE DESEMPENHO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="vendedor-destaque">{vendedor_selecionado}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle-center">COMPETÊNCIA: {meses_br[hoje.month].upper()} / {hoje.year}</div>', unsafe_allow_html=True)
    
    st.info(f"📅 Meta baseada em **{d_passados}** dias úteis passados de **{d_totais}**.")

    cols_in = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]

    for i, col in enumerate(cols_in):
        with col:
            st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor_selecionado}")
            m_raw = st.text_input(f"Meta", value="", key=f"m_{i}_{vendedor_selecionado}")
            r_raw = st.text_input(f"Realizado", value="", key=f"r_{i}_{vendedor_selecionado}")
            ind_list.append({"NOME": sugestoes[i], "META": parse_int(m_raw), "REALIZADO": parse_int(r_raw)})

    res = []
    for it in ind_list:
        v_esp = math.ceil((it["META"] / d_totais) * d_passados) if d_totais > 0 else 0
        rota = (it["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if it["REALIZADO"] >= 0 else 0.0)
        tend = math.ceil((it["REALIZADO"] / d_passados) * d_totais) if d_passados > 0 else it["REALIZADO"]
        status = "-" if it["META"] == 0 else ("🟢 NO RITMO" if (v_esp == 0) or rota >= 1.0 else "🚨 CRÍTICO")
        eficiencia = "-" if v_esp == 0 else f"{round(rota * 100, 1)}%"
        res.append({"INDICADOR": it["NOME"], "META MENSAL": format_br(it["META"]), "ESPERADO": format_br(v_esp), "REALIZADO": format_br(it["REALIZADO"]), "EFICIÊNCIA (ROTA)": eficiencia, "PROJEÇÃO FINAL": format_br(tend), "STATUS": status})
    st.table(pd.DataFrame(res))
