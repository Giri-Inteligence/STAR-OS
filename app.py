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
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | INTELLIGENCE")
    st.markdown("---")
    lp_val = st.number_input("Janela Longo Prazo (Meses)", value=12)
    cp_val = st.number_input("Janela Curto Prazo (Meses)", value=3)
    st.markdown("---")
    st.info("O sistema prioriza os meses mais recentes para o cálculo, ignorando excedentes.")

st.title("STAR-OS | ENGINE DE GOVERNANÇA")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Planilha de Faturamento", type=['xlsx'])
st.markdown('</div>', unsafe_allow_html=True)

def format_br(val):
    return f"{val:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 1. MAPEAMENTO INTELIGENTE DE COLUNAS MENSALISTAS
    # Filtra colunas que parecem meses e EXCLUI explicitamente colunas de 'TOTAL' vindas do cliente
    col_meses = [c for c in df.columns if any(m in c.upper() for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']) and 'TOTAL' not in c.upper()]
    
    for col in col_meses:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    if len(col_meses) >= cp_val:
        # 2. LÓGICA DE JANELA DESLIZANTE (PRIORIZAÇÃO DO RECENTE)
        # Curto Prazo = Média dos últimos 'cp_val' meses
        cols_cp = col_meses[-cp_val:]
        # Longo Prazo = Média dos 'lp_val' meses anteriores ao CP (ou o que houver disponível)
        cols_lp = col_meses[-(lp_val + cp_val):-cp_val]
        
        df['MEDIA_LP'] = (df[cols_lp].sum(axis=1) / len(cols_lp)).round(0).astype(int)
        df['MEDIA_CP'] = (df[cols_cp].sum(axis=1) / len(cols_cp)).round(0).astype(int)

        # 3. ANALISE TÁTICA E DIRETRIZ DE CAMPO
        def analise_star(row):
            lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
            if cp == 0: return "🔴 INATIVO", lp, "RECUPERAÇÃO: Agendar visita de reativação imediata."
            if cp > (lp * 1.15): return "🟢 CRESCIMENTO", int(cp * 1.10), "EXPANSÃO: Identificar novos itens para Upsell."
            if cp < (lp * 0.85): return "🟡 QUEDA", lp, "DEFESA: Investigar perda de share ou concorrência."
            return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Garantir rituais de atendimento."

        df['STATUS'], df['META'], df['AÇÃO'] = zip(*df.apply(analise_star, axis=1))

        # EXIBIÇÃO EXECUTIVA
        st.subheader("Matriz de Governança Acionável")
        df_view = df[['EMPRESA', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']].copy()
        
        st.dataframe(
            df_view.style.format({"MEDIA_LP": format_br, "MEDIA_CP": format_br, "META": format_br}),
            use_container_width=True
        )

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='STAR_DIAGNOSTICO')
        st.download_button("📥 BAIXAR PLANO DE AÇÃO", output.getvalue(), "Plano_STAR_Giri.xlsx")
    else:
        st.error("A planilha não possui meses suficientes para a análise solicitada.")
