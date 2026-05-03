import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.title("STAR-OS | ENGINE DE GOVERNANÇA UNIVERSAL")
st.markdown("### Arquitetura de Sistemas Comerciais B2B")

uploaded_file = st.file_uploader("Upload da Planilha (Bruta ou Consolidada)", type=['xlsx', 'csv'])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    cols = df.columns.tolist()
    
    with st.sidebar:
        st.header("⚙️ Configuração de Dimensões")
        st.info("Selecione quais colunas representam suas chaves de gestão.")
        
        # Seletores dinâmicos baseados nas colunas reais da planilha
        dim_vendedor = st.selectbox("Coluna de Vendedor (Opcional)", ["Nenhum"] + cols)
        dim_segmento = st.selectbox("Coluna de Segmento (Opcional)", ["Nenhum"] + cols)
        dim_cidade = st.selectbox("Coluna de Cidade/Região (Opcional)", ["Nenhum"] + cols)
        
        st.header("📅 Parâmetros STAR")
        lp_val = st.number_input("Meses Longo Prazo", value=12)
        cp_val = st.number_input("Meses Curto Prazo", value=3)

    # Identificação Automática de Períodos (Lógica para Planilha Tamoyo e similares)
    # Procura colunas que pareçam meses ou anos
    colunas_valor = [c for c in cols if any(m in c.upper() for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ', '2024', '2025', '2026'])]
    
    if colunas_valor:
        st.success(f"Detectadas {len(colunas_valor)} colunas de faturamento mensal.")
        
        # Mapeamento de chaves ativas
        chaves_gestao = []
        if dim_vendedor != "Nenhum": chaves_gestao.append(dim_vendedor)
        if dim_segmento != "Nenhum": chaves_gestao.append(dim_segmento)
        if dim_cidade != "Nenhum": chaves_gestao.append(dim_cidade)
        
        if not chaves_gestao:
            st.warning("Selecione ao menos uma dimensão (Vendedor, Segmento ou Cidade) no menu lateral.")
        else:
            # Cálculos de Engenharia Comercial
            # CP: Últimos 3 meses detectados | LP: Todos os meses detectados (ajustado pelo parâmetro)
            df['MEDIA_LP'] = df[colunas_valor].sum(axis=1) / lp_val
            df['MEDIA_CP'] = df[colunas_valor[-3:]].sum(axis=1) / cp_val
            
            def check_status(row):
                if row['MEDIA_CP'] == 0: return "INATIVO"
                if row['MEDIA_CP'] > (row['MEDIA_LP'] * 1.15): return "CRESCIMENTO"
                if row['MEDIA_CP'] < (row['MEDIA_LP'] * 0.85): return "QUEDA"
                return "ESTÁVEL"
            
            df['STATUS'] = df.apply(check_status, axis=1)
            
            # Dashboard Executivo
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total de Clientes Analisados", len(df))
            with col_b:
                st.metric("Clientes em Queda/Inativos", len(df[df['STATUS'].isin(['QUEDA', 'INATIVO'])]))
            
            st.dataframe(df[chaves_gestao + ['MEDIA_LP', 'MEDIA_CP', 'STATUS']].sort_values('MEDIA_LP', ascending=False))

            # Motor de Exportação Inteligente
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='BASE_STAR')
                
                # Cria abas para a primeira chave de gestão selecionada
                chave_principal = chaves_gestao[0]
                for valor in df[chave_principal].unique():
                    aba_df = df[df[chave_principal] == valor]
                    aba_df.to_excel(writer, index=False, sheet_name=str(valor)[:31])
            
            st.download_button("BAIXAR DIAGNÓSTICO FORMATADO", output.getvalue(), "STAR_OS_Relatorio.xlsx")
