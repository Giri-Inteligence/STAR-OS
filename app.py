import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO
from streamlit_option_menu import option_menu

# CONFIGURAÇÃO DE DESIGN EXECUTIVO
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

# CSS PARA GLASSMORPHISM E ESTÉTICA NAVY
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003358 100%);
        color: #ffffff;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# MENU LATERAL
with st.sidebar:
    st.markdown("### GIRI | INTELIGENCE")
    selected = option_menu(
        menu_title="STAR-OS Hub",
        options=["Diagnóstico STAR", "Cadência (Em breve)", "Funil (Em breve)"],
        icons=["activity", "clock", "funnel"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "transparent"},
            "nav-link": {"color": "white", "--hover-color": "#004080"},
            "nav-link-selected": {"background-color": "#003358"},
        }
    )

if selected == "Diagnóstico STAR":
    st.title("SISTEMA TÁTICO DE AÇÃO E RESULTADOS")
    
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lp_months = st.number_input("Meses Longo Prazo (LP)", value=12)
        with col2:
            cp_months = st.number_input("Meses Curto Prazo (CP)", value=3)
        
        uploaded_file = st.file_uploader("Upload da Planilha Bruta (Excel/CSV)", type=['xlsx', 'csv'])
        st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        
        st.write("Mapeamento de Colunas:")
        cols = df.columns.tolist()
        vendedor_col = st.selectbox("Vendedor", cols)
        cliente_col = st.selectbox("Cliente", cols)
        data_col = st.selectbox("Data", cols)
        valor_col = st.selectbox("Valor de Venda", cols)
        cidade_col = st.selectbox("Cidade (Opcional - Ex: Tortelli)", ["Nenhum"] + cols)

        if st.button("PROCESSAR STAR-OS"):
            # LÓGICA DE ENGENHARIA STAR
            df[data_col] = pd.to_datetime(df[data_col])
            
            # Agrupamento e Médias
            resumo = df.groupby([vendedor_col, cliente_col]).agg({valor_col: 'sum'}).reset_index()
            resumo['LP'] = resumo[valor_col] / lp_months
            resumo['CP'] = resumo[valor_col] / cp_months # Simplificação para o MVP
            
            # MATRIZ DE STATUS (REGRAS DE GOVERNANÇA)
            def check_status(row):
                if row['CP'] == 0: return "INATIVO"
                if row['CP'] > (row['LP'] * 1.15): return "CRESCIMENTO"
                if row['CP'] < (row['LP'] * 0.85): return "QUEDA"
                return "ESTÁVEL"
            
            resumo['STATUS'] = resumo.apply(check_status, axis=1)
            resumo['META'] = resumo.apply(lambda x: x['LP'] if x['STATUS'] in ["QUEDA", "INATIVO"] else x['CP'], axis=1)
            
            # ORDENAÇÃO POR LP DESCENDENTE
            resumo = resumo.sort_values(by='LP', ascending=False)
            
            st.success("Diagnóstico concluído com sucesso!")
            st.dataframe(resumo)

            # EXPORTAÇÃO EXECUTIVA
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Aba Geral
                resumo.to_excel(writer, index=False, sheet_name='GERAL')
                workbook = writer.book
                header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D3D3D3'})
                
                # Formatação das abas
                for sheet in writer.sheets.values():
                    for col_num, value in enumerate(resumo.columns.values):
                        sheet.write(0, col_num, value.upper(), header_format)

                # Abas por Vendedor
                for vendedor in resumo[vendedor_col].unique():
                    v_df = resumo[resumo[vendedor_col] == vendedor]
                    v_df.to_excel(writer, index=False, sheet_name=str(vendedor)[:31])

            st.download_button("BAIXAR PLANILHA STAR FORMATADA", output.getvalue(), "Planilha_STAR_Giri.xlsx")
