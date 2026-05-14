import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter
import plotly.graph_objects as go

st.set_page_config(page_title="Giri | STAR", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #EDF1F7; }
[data-testid="stHeader"] { background: transparent; }
.giri-header {
    background: linear-gradient(120deg, #001233 0%, #003087 55%, #0056b3 100%);
    border-radius: 18px; padding: 30px 38px; margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(0,18,51,0.32);
    display: flex; align-items: center; gap: 18px;
}
.giri-header-dot {
    width: 48px; height: 48px; background: rgba(255,255,255,0.15);
    border-radius: 12px; display: flex; align-items: center;
    justify-content: center; font-size: 22px; flex-shrink: 0;
}
.giri-header h1 { color: #FFFFFF; font-size: 1.45rem; font-weight: 800; letter-spacing: 1.2px; margin: 0 0 3px 0; }
.giri-header p  { color: rgba(255,255,255,0.55); font-size: 0.80rem; margin: 0; letter-spacing: 0.5px; }
.section-title  { font-size: 0.68rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: #6B7A99; margin: 28px 0 12px 0; padding-left: 2px; }
.kpi-wrap { background: #FFFFFF; border-radius: 14px; padding: 20px 22px 16px 22px; box-shadow: 0 2px 18px rgba(0,0,0,0.07); height: 100%; position: relative; overflow: hidden; text-align: center; }
.kpi-wrap::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 14px 14px 0 0; }
.kpi-wrap.blue::before  { background: linear-gradient(90deg,#0056b3,#00A3E0); }
.kpi-wrap.red::before   { background: linear-gradient(90deg,#C00000,#FF6B6B); }
.kpi-wrap.green::before { background: linear-gradient(90deg,#1A6B2A,#52C471); }
.kpi-wrap.gold::before  { background: linear-gradient(90deg,#9E6A00,#F4C430); }
.kpi-lbl { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: #8A93A2; margin-bottom: 10px; }
.kpi-val { font-size: 1.85rem; font-weight: 800; line-height: 1; margin-bottom: 7px; color: #0D1B2A; }
.kpi-val.blue  { color: #0056b3; }
.kpi-val.red   { color: #C00000; }
.kpi-val.green { color: #1A6B2A; }
.kpi-val.gold  { color: #9E6A00; }
.kpi-sub { font-size: 0.73rem; color: #B0BAC9; line-height: 1.4; }
.kpi-breakdown { font-size: 0.72rem; color: #6B7A99; margin-top: 8px; font-weight: 600; }
.kpi-breakdown span { margin: 0 4px; }
.ind-wrap { background: #FFFFFF; border-radius: 14px; padding: 18px 22px; box-shadow: 0 2px 18px rgba(0,0,0,0.07); text-align: center; position: relative; overflow: hidden; }
.ind-wrap::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 14px 14px 0 0; background: linear-gradient(90deg,#001845,#0056b3); }
.ind-lbl { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: #8A93A2; margin-bottom: 8px; }
.ind-val { font-size: 1.5rem; font-weight: 800; color: #0D1B2A; margin-bottom: 5px; }
.ind-sub { font-size: 0.72rem; color: #B0BAC9; }
.chart-wrap { background: #FFFFFF; border-radius: 14px; padding: 20px 22px 10px 22px; box-shadow: 0 2px 18px rgba(0,0,0,0.07); }
.chart-lbl { font-size: 1.0rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; color: #1A2540; text-align: center; margin-bottom: 8px; }
.vend-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.88rem; }
.vend-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:12px 16px; text-align:center; letter-spacing:0.8px; font-size:0.75rem; text-transform:uppercase; }
.vend-table td { padding:12px 16px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; }
.vend-table tr:last-child td { border-bottom:none; }
.vend-table tr:hover td { background:#F5F7FB; }
.vend-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:hidden; }
.cart-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.cart-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:11px 14px; text-align:center; letter-spacing:0.8px; font-size:0.72rem; text-transform:uppercase; }
.cart-table td { padding:10px 14px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; }
.cart-table td.left { text-align:left; }
.cart-table tr:last-child td { border-bottom:none; }
.cart-table tr:hover td { background:#F5F7FB; }
.cart-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:auto; max-height:520px; }
.stDownloadButton > button {
    background: linear-gradient(135deg, #001233 0%, #003087 50%, #0056b3 100%) !important;
    color: #FFFFFF !important; border: none !important; border-radius: 12px !important;
    padding: 15px 28px !important; font-size: 0.88rem !important; font-weight: 800 !important;
    letter-spacing: 1px !important; width: 100% !important;
    box-shadow: 0 6px 24px rgba(0,18,51,0.35) !important;
}
.stDownloadButton > button:hover { opacity: 0.88 !important; }
</style>
""", unsafe_allow_html=True)


def fmt_br(value):
    return f"{int(value):,}".replace(",", ".")


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


def get_tab_names(vendors):
    first_map = {}
    for v in vendors:
        parts = str(v).strip().split()
        first = parts[0] if parts else str(v)
        first_map.setdefault(first, []).append(v)
    result = {}
    for first, vlist in first_map.items():
        if len(vlist) == 1:
            result[vlist[0]] = first[:31]
        else:
            for v in vlist:
                parts = str(v).strip().split()
                suffix = parts[1][0] if len(parts) > 1 else str(v)[-1]
                result[v] = (first + " " + suffix)[:31]
    return result


def get_excel_formats(wb):
    base = {'font_name': 'Arial', 'border': 1}
    return {
        'hdr':   wb.add_format({**base, 'bold': True, 'bg_color': '#002060', 'font_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True}),
        'txt':   wb.add_format({**base, 'valign': 'vcenter', 'align': 'left', 'text_wrap': True}),
        'num':   wb.add_format({**base, 'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center'}),
        'total': wb.add_format({**base, 'num_format': '#,##0', 'bg_color': '#D9D9D9', 'bold': True, 'font_color': '#000000', 'valign': 'vcenter', 'align': 'center'}),
        'qa':    wb.add_format({**base, 'bg_color': '#FFC7CE', 'font_color': '#C00000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'q':     wb.add_format({**base, 'font_color': '#C00000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'ca':    wb.add_format({**base, 'bg_color': '#C6EFCE', 'font_color': '#375623', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'c':     wb.add_format({**base, 'font_color': '#375623', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'e':     wb.add_format({**base, 'font_color': '#0070C0', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'i':     wb.add_format({**base, 'font_color': '#000000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
    }


def write_sheet(ws, df, final_ordem, clie_col, vend_col, meses_col, fmts):
    larguras = {'CURVA': 7, clie_col: 30, vend_col: 22, 'TOTAL LP': 13, 'MEDIA LP': 13, 'MEDIA CP': 13, 'STATUS': 24, 'META': 12, 'ACAO': 88}
    ws.set_default_row(125)
    ws.set_row(0, 40)
    status_fmt = {
        'QUEDA ACENTUADA': fmts['qa'], 'QUEDA': fmts['q'],
        'CRESCIMENTO ACENTUADO': fmts['ca'], 'CRESCIMENTO': fmts['c'],
        'ESTAVEL': fmts['e'], 'INATIVO': fmts['i'],
    }
    for i, col in enumerate(final_ordem):
        ws.write(0, i, col, fmts['hdr'])
        ws.set_column(i, i, larguras.get(col, 8))
    for r_idx, row in df.iterrows():
        xl_r = r_idx + 1
        for c_idx, col_n in enumerate(final_ordem):
            val = row[col_n]
            if col_n == 'STATUS':
                s = str(val)
                ws.write_string(xl_r, c_idx, s, status_fmt.get(s, fmts['txt']))
            elif col_n == 'TOTAL LP':
                ws.write_number(xl_r, c_idx, int(val), fmts['total'])
            elif col_n in ('MEDIA LP', 'MEDIA CP', 'META') or col_n in meses_col:
                ws.write_number(xl_r, c_idx, int(val), fmts['num'])
            else:
                ws.write_string(xl_r, c_idx, str(val), fmts['txt'])


def gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col):
    buffer = BytesIO()
    vendors = sorted(df_raw[vend_col].dropna().astype(str).unique().tolist())
