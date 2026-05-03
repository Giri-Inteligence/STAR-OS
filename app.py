import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

# 1. CONFIGURAÇÃO E DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
    cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

st.title("STAR-OS | SISTEMA DE GOVERNANÇA")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
st.markdown('</div>', unsafe_allow_html=True)

def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "-"
        return f"{int(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp, cp):
    # LÓGICA DE STATUS: ORIENTAÇÃO METODOLÓGICA (MÉTODO STAR)
    if cp == 0: 
        return "⚫ INATIVO", 0, (
            "OBJETIVO: Diagnóstico de Churn e Reconexão. "
            "AÇÃO: Reestabelecer contato sem viés de venda. "
            "ORIENTAÇÃO: Identifique o motivo real da parada. Valide se a dor que resolvíamos ainda existe ou se ele tem novas prioridades."
        )
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, (
            "OBJETIVO: Contenção de Perda e Defesa de Share. "
            "AÇÃO: Investigar entrada de concorrência ou falha de serviço. "
            "ORIENTAÇÃO: Foque no negócio dele. Entenda onde a operação do cliente está perdendo margem e apresente-se para recuperar esse fôlego."
        )
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, (
            "OBJETIVO: Estabilização de Giro. "
            "AÇÃO: Identificar se a queda é sazonal ou substituição de mix. "
            "ORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas e manter o custo operacional sob controle."
        )
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), (
            "OBJETIVO: Expansão de Share e Upsell. "
            "AÇÃO: Analisar mix de clientes similares e elevar Ticket Médio. "
            "ORIENTAÇÃO: Recomende itens complementares explicando como isso ajuda o cliente a atrair novos consumidores ou melhorar a margem."
        )
    return "🔵 ESTÁVEL", int(lp * 1.05), (
        "OBJETIVO: Manutenção e Blindagem. "
        "AÇÃO: Prevenir inércia e validar satisfação. "
        "ORIENTAÇÃO: Confirme se os objetivos de curto prazo dele estão sendo atingidos. Prospecte necessidades futuras para novos projetos."
    )

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

            header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#001220', 'border': 1, 'align': 'center'})
            num_fmt = workbook.add_format({'num_format': '#,##0', 'align': 'center'})
            left_fmt = workbook.add_format({'align': 'left'})
            
            fmt_queda = workbook.add_format({'font_color': '#C00000', 'bold': True, 'align': 'left'})
            fmt_queda_ac = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True, 'align': 'left'})
            fmt_cresc = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': True, 'align': 'left'})

            for col_num, value in enumerate(colunas_exibicao):
                worksheet.write(0, col_num, value, header_fmt)
                if value == 'STATUS':
                    worksheet.set_column(col_num, col_num, 20, left_fmt)
                    worksheet.conditional_format(1, col_num, len(df_final), col_num, {'type': 'text', 'criteria': 'containing', 'value': 'QUEDA ACENTUADA', 'format': fmt_queda_ac})
                    worksheet.conditional_format(1, col_num, len(df_final), col_num, {'type': 'text', 'criteria': 'containing', 'value': 'QUEDA', 'format': fmt_queda})
                    worksheet.conditional_format(1, col_num, len(df_final), col_num, {'type': 'text', 'criteria': 'containing', 'value': 'CRESCIMENTO', 'format': fmt_cresc})
                elif value in ['AÇÃO', 'EMPRESA'] + dims_selecionadas:
                    worksheet.set_column(col_num, col_num, 50, left_fmt)
                else:
                    worksheet.set_column(col_num, col_num, 15, num_fmt)

        st.download_button("📥 EXPORTAR PLANO EXECUTIVO GIRI", output.getvalue(), "Plano_STAR_Giri.xlsx")
