import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

# DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    st.subheader("📅 JANELAS DE GOVERNANÇA")
    lp_val = st.number_input("Média Longo Prazo (Meses)", value=12, min_value=1)
    cp_val = st.number_input("Média Curto Prazo (Meses)", value=3, min_value=1)
    st.markdown("---")
    st.warning("Postura Crítica: Ações baseadas estritamente em desvios de média móvel.")

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
st.markdown('</div>', unsafe_allow_html=True)

def format_br(val):
    try: return f"{int(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    all_cols = df_raw.columns.tolist()
    
    # Identifica colunas de meses (Ignora colunas que o cliente já somou como 'TOTAL')
    col_meses = [c for c in all_cols if any(m in c.upper() for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c.upper()]
    # Colunas de Dimensão (Texto)
    col_dimensoes = [c for c in all_cols if c not in col_meses and c != 'EMPRESA']

    with st.sidebar:
        st.subheader("📂 ANÁLISE MULTIDIMENSIONAL")
        dims_selecionadas = st.multiselect("Selecione as chaves de governança (Vendedor, Segmento, Cidade...)", col_gestao if 'col_gestao' in locals() else col_dimensoes)
        st.info("O sistema cruzará as informações para gerar a visão de performance.")

    if not dims_selecionadas:
        st.error("Selecione ao menos uma dimensão na barra lateral para processar a matriz.")
    else:
        # Limpeza e Cálculo
        df = df_raw.copy()
        for col in col_meses:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Janelas Deslizantes
        cols_cp = col_meses[-cp_val:]
        cols_lp = col_meses[-(lp_val + cp_val):-cp_val]
        
        # Agrupamento Dinâmico por Múltiplas Dimensões
        chaves = ['EMPRESA'] + dims_selecionadas
        df_agrupado = df.groupby(chaves)[col_meses].sum().reset_index()

        df_agrupado['MEDIA_LP'] = (df_agrupado[cols_lp].sum(axis=1) / len(cols_lp)).round(0)
        df_agrupado['MEDIA_CP'] = (df_agrupado[cols_cp].sum(axis=1) / len(cols_cp)).round(0)

        # MOTOR DE STATUS STAR
        def engine_star(row):
            lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
            if cp == 0: return "⚫ INATIVO", lp, "RECUPERAÇÃO: Sem compra há 90 dias. Visita imediata e diagnóstico de Churn."
            if cp < (lp * 0.85): return "🔴 QUEDA", lp, "DEFESA: Perda de share. Investigar concorrência ou falha logística."
            if cp > (lp * 1.15): return "🟢 CRESCIMENTO", int(cp * 1.10), "EXPANSÃO: Tração positiva. Aplicar Cross-sell imediato."
            return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Blindagem de conta e rituais de fidelização."

        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*df_agrupado.apply(engine_star, axis=1))

        # EXIBIÇÃO FINAL
        exibir = chaves + ['MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader("Matriz de Decisão Tática")
        st.dataframe(
            df_agrupado[exibir].sort_values('MEDIA_LP', ascending=False).style.format({
                "MEDIA_LP": format_br, "MEDIA_CP": format_br, "META": format_br
            }), 
            use_container_width=True
        )

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_agrupado[exibir].to_excel(writer, index=False, sheet_name='STAR_GOVERNANCA')
        st.download_button("📥 EXPORTAR PLANO DE TRABALHO", output.getvalue(), "Plano_Trabalho_Giri.xlsx")
