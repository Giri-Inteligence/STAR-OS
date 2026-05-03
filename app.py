import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO
from datetime import datetime

# 1. CONFIGURAÇÃO E DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def get_working_days(start_date, end_date):
    days = pd.date_range(start_date, end_date)
    return len(days[days.dayofweek < 5])

def engine_star(row, lp, cp):
    if cp == 0: 
        return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo da parada e valide se a dor ainda existe."
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Contenção de Perda.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele. Entenda onde ele perde margem."
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, "OBJETIVO: Estabilização de Giro.\nAÇÃO: Identificar queda sazonal ou troca de mix.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas e manter o custo."
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão de Share.\nAÇÃO: Elevar Ticket Médio via Mix.\nORIENTAÇÃO: Recomende itens complementares explicando o ganho de margem."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Manutenção e Blindagem.\nAÇÃO: Prevenir inércia.\nORIENTAÇÃO: Confirme se os objetivos dele estão sendo atingidos e prospecte novos projetos."

# --- INTERFACE DE NAVEGAÇÃO ---
st.sidebar.markdown("## GIRI | ARCHITECTURE")
menu = st.sidebar.radio("CENTRO DE COMANDO", ["Dashboard Inicial", "Matriz STAR (Clientes)", "Desempenho (Vendedores)"])

# 1. TELA: DASHBOARD INICIAL
if menu == "Dashboard Inicial":
    st.title("Giri Strategic Hub")
    st.markdown("### Bem-vindo, William. Escolha a ferramenta de governança para hoje:")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("📍 Matriz STAR")
        st.write("Análise tática de faturamento por cliente. Foco em churn, recuperação e expansão de share.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("📊 Desempenho Individual")
        st.write("Governança semanal de ritmo e tendência. Foco em atingimento de metas e desvio de rota.")
        st.markdown('</div>', unsafe_allow_html=True)

# 2. TELA: MATRIZ STAR
elif menu == "Matriz STAR (Clientes)":
    st.title("Matriz STAR-OS | Gestão de Carteira")
    with st.sidebar:
        st.markdown("---")
        lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)
    
    uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        cols = [str(c).upper() for c in df_raw.columns]
        df_raw.columns = cols
        
        focos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
        dimensoes = [c for c in cols if any(f in c for f in focos)]
        dims_sel = st.multiselect("Chaves de Governança", dimensoes, default=dimensoes[0] if dimensoes else [])
        
        if dims_sel:
            col_meses = [c for c in cols if any(m in c for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c]
            df = df_raw.copy()
            for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            df_agrupado = df.groupby(['EMPRESA'] + dims_sel)[col_meses].sum().reset_index()
            df_agrupado['TOTAL_ACUMULADO'] = df_agrupado[col_meses].sum(axis=1).round(0)
            df_agrupado['MEDIA_LP'] = (df_agrupado[col_meses[-(lp_val+cp_val):-cp_val]].sum(axis=1) / lp_val).round(0)
            df_agrupado['MEDIA_CP'] = (df_agrupado[col_meses[-cp_val:]].sum(axis=1) / cp_val).round(0)
            
            res = df_agrupado.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
            df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res)
            
            df_final = df_agrupado.sort_values('TOTAL_ACUMULADO', ascending=False)
            st.dataframe(df_final.style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

# 3. TELA: DESEMPENHO INDIVIDUAL (V30)
elif menu == "Desempenho (Vendedores)":
    st.title("Governança de Performance | STAR-OS")
    
    # Bloco de Tempo Automático
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1)
    if hoje.month == 12: ultimo_dia = hoje.replace(day=31)
    else: ultimo_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    
    d_uteis_totais = get_working_days(primeiro_dia, ultimo_dia)
    d_uteis_hoje = get_working_days(primeiro_dia, hoje)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 1. CONFIGURAÇÃO DA RÉGUA COMERCIAL")
    col_v, col_t = st.columns([2, 1])
    vendedor_nome = col_v.text_input("Nome do Vendedor", placeholder="Digite o nome do consultor...")
    col_t.metric("Dias Úteis (Mês / Hoje)", f"{d_uteis_totais} / {d_uteis_hoje}")
    
    ind_list = []
    st.write("Defina os 5 indicadores estratégicos e suas metas:")
    c1, c2, c3, c4, c5 = st.columns(5)
    cols_ind = [c1, c2, c3, c4, c5]
    
    for i, col in enumerate(cols_ind):
        with col:
            nome_i = st.text_input(f"Indicador {i+1}", value=f"IND {i+1}", key=f"n_{i}")
            meta_i = st.number_input(f"Meta {i+1}", min_value=0.01, key=f"m_{i}")
            real_i = st.number_input(f"Realizado {i+1}", min_value=0.0, key=f"r_{i}")
            ind_list.append({"NOME": nome_i, "META": meta_i, "REALIZADO": real_i})
    st.markdown('</div>', unsafe_allow_html=True)

    if vendedor_nome:
        st.markdown(f"### 2. ANÁLISE DE ROTA: {vendedor_nome.upper()}")
        resultados = []
        for item in ind_list:
            v_esperado = (item["META"] / d_uteis_totais) * d_uteis_hoje
            percentual_rota = (item["REALIZADO"] / v_esperado) if v_esperado > 0 else 0
            tendencia_final = (item["REALIZADO"] / d_uteis_hoje) * d_uteis_totais if d_uteis_hoje > 0 else 0
            
            if percentual_rota >= 1.0: status = "🟢 NO RITMO"
            elif percentual_rota >= 0.85: status = "🟡 ATENÇÃO"
            else: status = "🚨 CRÍTICO"
            
            resultados.append({
                "INDICADOR": item["NOME"],
                "META MENSAL": item["META"],
                "ESPERADO HOJE": round(v_esperado, 2),
                "REALIZADO": item["REALIZADO"],
                "ROTA": f"{round(percentual_rota * 100, 1)}%",
                "TENDÊNCIA": round(tendencia_final, 2),
                "STATUS": status
            })
        st.table(pd.DataFrame(resultados))
