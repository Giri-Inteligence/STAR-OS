import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math
import xlsxwriter
from io import BytesIO

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    [data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; }
    
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 13px !important;
        padding: 10px 5px !important;
        white-space: nowrap !important;
    }
    
    div[data-testid="stDataFrame"] td {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        min-width: 300px;
        vertical-align: middle !important;
    }

    .stTextInput input, .stNumberInput input { height: 35px !important; font-size: 13px !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def get_working_days(start, end):
    if start > end: return 0
    days = pd.date_range(start, end)
    return len(days[days.dayofweek < 5])

def engine_star(row, lp, cp):
    if cp == 0: 
        return "⚫ INATIVO", 0, (
            "OBJETIVO: Diagnóstico de Churn e Reconexão.\n"
            "AÇÃO: Reestabelecer contato sem viés de venda.\n"
            "ORIENTAÇÃO: Identifique o motivo real da parada. Valide se a dor ainda existe."
        )
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, (
            "OBJETIVO: Contenção de Perda e Defesa de Share.\n"
            "AÇÃO: Investigar entrada de concorrência ou falha de serviço.\n"
            "ORIENTAÇÃO: Foque no negócio dele. Entenda onde ele perde margem e apresente solução."
        )
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, (
            "OBJETIVO: Estabilização de Giro.\n"
            "AÇÃO: Identificar se a queda é sazonal ou substituição de mix.\n"
            "ORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas e manter o custo."
        )
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), (
            "OBJETIVO: Expansão de Share e Upsell.\n"
            "AÇÃO: Analisar mix de clientes similares e elevar Ticket Médio.\n"
            "ORIENTAÇÃO: Recomende itens complementares explicando o ganho de margem para ele."
        )
    return "🔵 ESTÁVEL", int(lp * 1.05), (
        "OBJETIVO: Manutenção e Blindagem.\n"
        "AÇÃO: Prevenir inércia e validar satisfação.\n"
        "ORIENTAÇÃO: Confirme se os objetivos dele estão sendo atingidos e prospecte novos projetos."
    )

# --- INICIALIZAÇÃO NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = 'Dashboard'

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()

# --- TELAS ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.title("Giri Strategic Hub")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-card"><h4>📍 Matriz STAR (Clientes)</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR MATRIZ STAR"): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
    with c2:
        st.markdown('<div class="main-card"><h4>📊 Desempenho (Vendedores)</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR DESEMPENHO"): st.session_state.pagina_ativa = 'Desempenho'; st.rerun()

elif st.session_state.pagina_ativa == 'Matriz':
    st.title("STAR-OS | SISTEMA DE GOVERNANÇA")
    with st.sidebar:
        st.markdown("---")
        lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

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
            
            st.subheader("Matriz de Decisão Tática")
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

elif st.session_state.pagina_ativa == 'Desempenho':
    with st.sidebar:
        st.markdown("---")
        nomes = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        vendedor = st.selectbox("CONSULTOR:", [v.strip().upper() for v in nomes.split('\n') if v.strip()])
    
    st.title(f"📊 DESEMPENHO: {vendedor}")
    
    hoje = datetime.now()
    p_dia = hoje.replace(day=1)
    u_dia = (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)
    d_totais = get_working_days(p_dia, u_dia)
    d_passados = get_working_days(p_dia, hoje)
    if hoje.weekday() < 5: d_passados = max(0, d_passados - 1)

    st.info(f"📅 Meta baseada em {d_passados} dias úteis de {d_totais}.")
    
    cols = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            n = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor}")
            m = st.number_input(f"Meta", min_value=0.0, step=1.0, key=f"m_{i}_{vendedor}")
            r = st.number_input(f"Realizado", min_value=0.0, step=1.0, key=f"r_{i}_{vendedor}")
            ind_list.append({"NOME": n, "META": m, "REALIZADO": r})

    res = []
    for it in ind_list:
        v_esp = math.ceil((it["META"] / d_totais) * d_passados) if d_totais > 0 else 0
        rota = (it["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if it["REALIZADO"] >= 0 else 0.0)
        res.append({"INDICADOR": it["NOME"].upper(), "META MENSAL": format_br(it["META"]), "ESPERADO": format_br(v_esp), "REALIZADO": format_br(it["REALIZADO"]), "STATUS": "🟢 NO RITMO" if rota >= 1.0 else "🚨 CRÍTICO"})
    st.table(pd.DataFrame(res))
