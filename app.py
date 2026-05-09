import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

st.set_page_config(page_title="Giri | Sistema STAR", layout="wide")

def engine_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        lp_v, cp_v = 0.0, 0.0

    txt_ina = (
        "OBJETIVO: Diagnostico de causa\n"
        "PRE-CONTATO: Revisar ultimo pedido. Identificar o que parou de ser comprado e em que momento.\n"
        "CONTATO: Contato de diagnostico. Entender o motivo da inatividade sem pressao de venda.\n"
        "ORIENTACAO: Nao ofertar produto na primeira interacao. Primeiro entender o que aconteceu. "
        "Registrar motivo antes de qualquer acao de reconquista."
    )
    txt_q_ac = (
        "OBJETIVO: Recuperacao emergencial\n"
        "PRE-CONTATO: Revisar historico completo do cliente. Identificar exatamente quais produtos cairam, "
        "em que momento e qual era o volume anterior. Calcular o gap entre a media historica e o momento atual.\n"
        "CONTATO: Priorizar visita presencial ou ligacao direta - nao mensagem. Abrir diagnostico sem pressao. "
        "Entender se houve mudanca interna no cliente, problema de relacionamento ou entrada de concorrente.\n"
        "ORIENTACAO: Este cliente esta em risco de perda. O objetivo da primeira interacao nao e vender - e entender. "
        "Registrar causa com precisao. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    )
    txt_q = (
        "OBJETIVO: Estabilizacao\n"
        "PRE-CONTATO: Revisar historico de mix. Identificar quais produtos reduziram ou desapareceram nos ultimos 3 meses.\n"
        "CONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudanca operacional, financeira ou troca de fornecedor.\n"
        "ORIENTACAO: Registrar causa identificada. Se houver abertura, propor recomposicao de mix com base no historico anterior."
    )
    txt_est = (
        "OBJETIVO: Blindagem e crescimento incremental\n"
        "PRE-CONTATO: Revisar mix atual. Mapear categorias que o cliente nao compra mas que sao compativeis com seu perfil.\n"
        "CONTATO: Manter frequencia de relacionamento. Explorar oportunidade de expansao de mix.\n"
        "ORIENTACAO: Cliente estavel nao e cliente seguro. Monitorar frequencia de pedidos e introduzir novos itens gradualmente."
    )
    txt_cre = (
        "OBJETIVO: Consolidacao\n"
        "PRE-CONTATO: Identificar o driver do crescimento. Avaliar se e sazonalidade ou mudanca estrutural no cliente.\n"
        "CONTATO: Reforcar relacionamento. Garantir abastecimento e antecipar demanda dos proximos periodos.\n"
        "ORIENTACAO: Proteger o cliente. Momento de crescimento e o de maior risco de abordagem pelo concorrente."
    )
    txt_cre_ac = (
        "OBJETIVO: Consolidacao e protecao\n"
        "PRE-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar "
        "esse volume ou se e pontual. Verificar se ha mix ainda nao explorado.\n"
        "CONTATO: Reforcar presenca. Garantir que o abastecimento esta adequado ao novo patamar de compra. Antecipar pedidos futuros.\n"
        "ORIENTACAO: Crescimento acentuado atrai concorrencia. Este e o momento de maior risco de abordagem externa. "
        "Aumentar frequencia de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."
    )

    if cp_v <= 0:
        return "INATIVO", 0, txt_ina
    if lp_v <= 0:
        return "ESTAVEL", int(cp_v * 1.05), txt_est
    if cp_v < (lp_v * 0.85):
        return "QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < (lp_v * 0.98):
        return "QUEDA", int(lp_v), txt_q
    if cp_v > (lp_v * 1.20):
        return "CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_cre_ac
    if cp_v > (lp_v * 1.05):
        return "CRESCIMENTO", int(cp_v * 1.05), txt_cre
    return "ESTAVEL", int(lp_v * 1.05), txt_est


def gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='STAR')
        wb = writer.book
        ws = writer.sheets['STAR']

        hdr = wb.add_format({
            'bold': True, 'bg_color': '#002060', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'text_wrap': True, 'font_name': 'Arial'
        })
        txt = wb.add_format({
            'valign': 'vcenter', 'align': 'left', 'border': 1,
            'text_wrap': True, 'font_name': 'Arial'
        })
        num = wb.add_format({
            'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center',
            'border': 1, 'font_name': 'Arial'
        })
        total_f = wb.add_format({
            'num_format': '#,##0', 'bg_color': '#D9D9D9', 'bold': True,
            'font_color': '#000000', 'valign': 'vcenter', 'align': 'center',
            'border': 1, 'font_name': 'Arial'
        })
        fmt_qa = wb.add_format({
            'bg_color': '#FFC7CE', 'font_color': '#C00000', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        fmt_q = wb.add_format({
            'font_color': '#C00000', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        fmt_ca = wb.add_format({
            'bg_color': '#C6EFCE', 'font_color': '#375623', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        fmt_c = wb.add_format({
            'font_color': '#375623', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        fmt_e = wb.add_format({
            'font_color': '#0070C0', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        fmt_i = wb.add_format({
            'font_color': '#000000', 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })

        ws.set_default_row(95)
        ws.set_row(0, 40)

        larguras = {
            'CURVA': 7, clie_col: 30, vend_col: 22,
            'TOTAL LP': 13, 'MEDIA LP': 13, 'MEDIA CP': 13,
            'STATUS': 24, 'META': 12, 'ACAO': 88,
        }

        for i, col in enumerate(final_ordem):
            ws.write(0, i, col, hdr)
            ws.set_column(i, i, larguras.get(col, 8))

        for r_idx, row in df_raw.iterrows():
            xl_r = r_idx + 1
            for c_idx, col_n in enumerate(final_ordem):
                val = row[col_n]
                if col_n == 'STATUS':
                    s = str(val)
                    if s == 'QUEDA ACENTUADA':         f = fmt_qa
                    elif s == 'QUEDA':                 f = fmt_q
                    elif s == 'CRESCIMENTO ACENTUADO': f = fmt_ca
                    elif s == 'CRESCIMENTO':           f = fmt_c
                    elif s == 'ESTAVEL':               f = fmt_e
                    else:                              f = fmt_i
                    ws.write_string(xl_r, c_idx, s, f)
                elif col_n == 'TOTAL LP':
                    ws.write_number(xl_r, c_idx, int(val), total_f)
                elif col_n in ('MEDIA LP', 'MEDIA CP', 'META') or col_n in meses_col:
                    ws.write_number(xl_r, c_idx, int(val), num)
                else:
                    ws.write_string(xl_r, c_idx, str(val), txt)

    return buffer.getvalue()


st.markdown("## GIRI | SISTEMA DE GOVERNANCA STAR")
st.markdown("---")

uploaded_file = st.file_uploader("Faca upload da base (XLSX ou CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    df_raw = (
        pd.read_excel(uploaded_file)
        if uploaded_file.name.endswith('xlsx')
        else pd.read_csv(uploaded_file)
    )
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [
        c for c in cols
        if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))
    ]
    clie_col = next((c for c in cols if "CLIENTE" in c or "NOME" in c or "RAZAO" in c), cols[0])
    vend_col = next((c for c in cols if "VENDEDOR" in c or "REP" in c), cols[1] if len(cols) > 1 else cols[0])

    for c in meses_col:
        df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)

    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MEDIA LP'] = df_raw[meses_col].mean(axis=1).astype(int)
    df_raw['MEDIA CP'] = df_raw[meses_col[-3:]].mean(axis=1).astype(int)
    df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)

    cumsum_pct = df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()
    df_raw['CURVA'] = cumsum_pct.apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))

    res = df_raw.apply(lambda r: engine_star(r['MEDIA LP'], r['MEDIA CP']), axis=1)
    df_raw['STATUS'], df_raw['META'], df_raw['ACAO'] = zip(*res)

    final_ordem = (
        ['CURVA', clie_col, vend_col]
        + meses_col
        + ['TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'STATUS', 'META', 'ACAO']
    )

    st.markdown("### MATRIZ STAR - VISUALIZACAO")

    cols_display = ['CURVA', clie_col, vend_col, 'TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'STATUS', 'META']
    df_display = df_raw[cols_display].copy()

    def colorir_status(val):
        cores = {
            'QUEDA ACENTUADA':       'background-color:#FFC7CE; color:#C00000; font-weight:bold',
            'QUEDA':                 'color:#C00000; font-weight:bold',
            'CRESCIMENTO ACENTUADO': 'background-color:#C6EFCE; color:#375623; font-weight:bold',
            'CRESCIMENTO':           'color:#375623; font-weight:bold',
            'ESTAVEL':               'color:#0070C0; font-weight:bold',
            'INATIVO':               'color:#000000; font-weight:bold',
        }
        return cores.get(val, '')

    styled = (
        df_display.style
        .map(colorir_status, subset=['STATUS'])
        .format({
            'TOTAL LP': '{:,.0f}',
            'MEDIA LP': '{:,.0f}',
            'MEDIA CP': '{:,.0f}',
            'META':     '{:,.0f}',
        })
    )

    st.dataframe(styled, use_container_width=True, height=520)

    st.markdown("### DISTRIBUICAO POR STATUS")
    dist = df_raw['STATUS'].value_counts().reset_index()
    dist.columns = ['STATUS', 'CLIENTES']
    st.dataframe(dist, use_container_width=False, hide_index=True)

    st.markdown("---")
    excel_bytes = gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col)

    st.download_button(
        label="BAIXAR PLANILHA STAR",
        data=excel_bytes,
        file_name="Matriz_STAR_Giri.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
