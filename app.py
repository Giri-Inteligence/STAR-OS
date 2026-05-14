import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter
import plotly.graph_objects as go
import html as htmllib

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
.ana-wrap { background: #FFFFFF; border-radius: 14px; padding: 20px 24px; box-shadow: 0 2px 18px rgba(0,0,0,0.07); }
.ana-title { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.3px; color: #1A2540; margin-bottom: 14px; text-align: center; }
.ana-table { width: 100%; border-collapse: collapse; font-family: Arial; font-size: 0.83rem; }
.ana-table th { background: #1A2540; color: #FFFFFF; font-weight: 700; padding: 9px 14px; text-align: center; font-size: 0.70rem; text-transform: uppercase; letter-spacing: 0.8px; }
.ana-table td { padding: 9px 14px; text-align: center; color: #1A2540; border-bottom: 1px solid #E5EAF2; font-weight: 500; }
.ana-table tr:last-child td { border-bottom: none; }
.ana-table tr:hover td { background: #F5F7FB; }
.rec-ativo   { background: #C6EFCE; color: #375623; font-weight: 700; border-radius: 6px; padding: 2px 10px; }
.rec-atencao { background: #FFEB9C; color: #9C6500; font-weight: 700; border-radius: 6px; padding: 2px 10px; }
.rec-risco   { background: #FFC7CE; color: #9C0006; font-weight: 700; border-radius: 6px; padding: 2px 10px; }
.rec-critico { background: #C00000; color: #FFFFFF; font-weight: 700; border-radius: 6px; padding: 2px 10px; }
.cli-list-wrap { background: #FFFFFF; border-radius: 14px; padding: 20px 24px; box-shadow: 0 2px 18px rgba(0,0,0,0.07); }
.cli-list-title { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.3px; color: #1A2540; margin-bottom: 14px; }
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
    
    txt_ina = "OBJETIVO: Diagnostico de causa\nPRE-CONTATO: Revisar ultimo pedido. Identificar o que parou de ser comprado e em que momento.\nCONTATO: Contato de diagnostico. Entender o motivo da inatividade sem pressao de venda.\nORIENTACAO: Nao ofertar produto na primeira interacao. Primeiro entender o que aconteceu. Registrar motivo antes de qualquer acao de reconquista."
    txt_q_ac = "OBJETIVO: Recuperacao emergencial\nPRE-CONTATO: Revisar historico completo do cliente. Identificar exatamente quais produtos cairam, em que momento e qual era o volume anterior. Calcular o gap entre a media historica e o momento atual.\nCONTATO: Priorizar visita presencial ou ligacao direta - nao mensagem. Abrir diagnostico sem pressao. Entender se houve mudanca interna no cliente, problema de relacionamento ou entrada de concorrente.\nORIENTACAO: Este cliente esta em risco de perda. O objetivo da primeira interacao nao e vender - e entender. Registrar causa com precisao. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    txt_q = "OBJETIVO: Estabilizacao\nPRE-CONTATO: Revisar historico de mix. Identificar quais produtos reduziram ou desapareceram nos ultimos 3 meses.\nCONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudanca operacional, financeira ou troca de fornecedor.\nORIENTACAO: Registrar causa identificada. Se houver abertura, propor recomposicao de mix com base no historico anterior."
    txt_est = "OBJETIVO: Blindagem e crescimento incremental\nPRE-CONTATO: Revisar mix atual. Mapear categorias que o cliente nao compra mas que sao compativeis com seu perfil.\nCONTATO: Manter frequencia de relacionamento. Explorar oportunidade de expansao de mix.\nORIENTACAO: Cliente estavel nao e cliente seguro. Monitorar frequencia de pedidos e introduzir novos itens gradualmente."
    txt_cre = "OBJETIVO: Consolidacao\nPRE-CONTATO: Identificar o driver do crescimento. Avaliar se e sazonalidade ou mudanca estrutural no cliente.\nCONTATO: Reforcar relacionamento. Garantir abastecimento e antecipar demanda dos proximos periodos.\nORIENTACAO: Proteger o cliente. Momento de crescimento e o de maior risco de abordagem pelo concorrente."
    txt_cre_ac = "OBJETIVO: Consolidacao e protecao\nPRE-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar esse volume ou se e pontual. Verificar se ha mix ainda nao explorado.\nCONTATO: Reforcar presenca. Garantir que o abastecimento esta adequado ao novo patamar de compra. Antecipar pedidos futuros.\nORIENTACAO: Crescimento acentuado atrai concorrencia. Este e o momento de maior risco de abordagem externa. Aumentar frequencia de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."
    
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
        'hdr': wb.add_format({**base, 'bold': True, 'bg_color': '#002060', 'font_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True}),
        'txt': wb.add_format({**base, 'valign': 'vcenter', 'align': 'left', 'text_wrap': True}),
        'num': wb.add_format({**base, 'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center'}),
        'total': wb.add_format({**base, 'num_format': '#,##0', 'bg_color': '#D9D9D9', 'bold': True, 'font_color': '#000000', 'valign': 'vcenter', 'align': 'center'}),
        'qa': wb.add_format({**base, 'bg_color': '#FFC7CE', 'font_color': '#C00000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'q': wb.add_format({**base, 'font_color': '#C00000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'ca': wb.add_format({**base, 'bg_color': '#C6EFCE', 'font_color': '#375623', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'c': wb.add_format({**base, 'font_color': '#375623', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'e': wb.add_format({**base, 'font_color': '#0070C0', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
        'i': wb.add_format({**base, 'font_color': '#000000', 'bold': True, 'valign': 'vcenter', 'align': 'center'}),
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
    tab_names = get_tab_names(vendors)
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        wb = writer.book
        fmts = get_excel_formats(wb)
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='GERAL')
        write_sheet(writer.sheets['GERAL'], df_raw.reset_index(drop=True), final_ordem, clie_col, vend_col, meses_col, fmts)
        for vendor in vendors:
            df_v = df_raw[df_raw[vend_col].astype(str) == vendor].reset_index(drop=True)
            tab = tab_names[vendor]
            df_v[final_ordem].to_excel(writer, index=False, sheet_name=tab)
            write_sheet(writer.sheets[tab], df_v, final_ordem, clie_col, vend_col, meses_col, fmts)
    return buffer.getvalue()


def var_html(pct):
    if pct is None:
        return '<span style="color:#B0BAC9">--</span>'
    color = "#1A6B2A" if pct >= 0 else "#C00000"
    sign = "+" if pct >= 0 else ""
    return f'<span style="color:{color};font-weight:700">{sign}{pct:.1f}%</span>'


STATUS_ORDER = ['CRESCIMENTO ACENTUADO', 'CRESCIMENTO', 'ESTAVEL', 'QUEDA', 'QUEDA ACENTUADA', 'INATIVO']
STATUS_COLORS = {
    'CRESCIMENTO ACENTUADO': '#1A6B2A', 'CRESCIMENTO': '#52C471',
    'ESTAVEL': '#0070C0', 'QUEDA': '#FF6B6B',
    'QUEDA ACENTUADA': '#C00000', 'INATIVO': '#9CA3AF',
}
STATUS_CSS = {
    'QUEDA ACENTUADA': 'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 8px;',
    'QUEDA': 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 8px;',
    'CRESCIMENTO': 'color:#375623;font-weight:700;',
    'ESTAVEL': 'color:#0070C0;font-weight:700;',
    'INATIVO': 'color:#6B7280;font-weight:700;',
}

st.markdown("""
<div class="giri-header">
    <div class="giri-header-dot">&#9733;</div>
    <div>
        <h1>GIRI | SISTEMA DE GOVERNANCA STAR</h1>
        <p>PAINEL DE GOVERNANCA COMERCIAL &#8212; GESTAO DE CARTEIRA B2B</p>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Faca upload da base (XLSX ou CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    def detectar_header(file):
        keywords = ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ")
        for h in range(6):
            try:
                df_test = pd.read_excel(file, header=h, nrows=3)
                cols = [str(c).strip().upper() for c in df_test.columns]
                if any(any(m in c for m in keywords) for c in cols):
                    return h
            except:
                pass
        return 0

    file_name = uploaded_file.name
    if file_name.endswith('xlsx'):
        header_row = detectar_header(uploaded_file)
        uploaded_file.seek(0)
        df_raw = pd.read_excel(uploaded_file, header=header_row)
    else:
        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')

    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [c for c in cols if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))]
    clie_col = next((c for c in cols if any(x in c for x in ("CLIENTE","NOME","RAZAO"))), cols[0])
    vend_col = next((c for c in cols if any(x in c for x in ("VENDEDOR","REP"))), cols[1] if len(cols) > 1 else cols[0])
    cida_col = next((c for c in cols if any(x in c for x in ("CIDADE","MUNICIPIO","LOCALIDADE","REGIAO"))), None)

    for c in meses_col:
        df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)

    df_raw = df_raw.dropna(subset=meses_col, how='all').reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].notna()].reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].astype(str).str.strip() != ''].reset_index(drop=True)

    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MEDIA LP'] = df_raw[meses_col].mean(axis=1).astype(int)
    df_raw['MEDIA CP'] = df_raw[meses_col[-3:]].mean(axis=1).astype(int)
    df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)

    cumsum_pct = df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()
    df_raw['CURVA'] = cumsum_pct.apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))

    res = df_raw.apply(lambda r: engine_star(r['MEDIA LP'], r['MEDIA CP']), axis=1)
    df_raw['STATUS'], df_raw['META'], df_raw['ACAO'] = zip(*res)

    def calc_recencia(row):
        for i in range(len(meses_col) - 1, -1, -1):
            if row[meses_col[i]] > 0:
                return len(meses_col) - 1 - i
        return len(meses_col)
    df_raw['MESES_SEM_COMPRA'] = df_raw.apply(calc_recencia, axis=1)

    extra = [cida_col] if cida_col else []
    final_ordem = ['CURVA', clie_col, vend_col] + extra + meses_col + ['TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'STATUS', 'META', 'ACAO']

    st.markdown('<div class="section-title">FILTROS</div>', unsafe_allow_html=True)
    fc = st.columns([2, 2, 2])
    with fc[0]:
        vendedores = ["Todos"] + sorted(df_raw[vend_col].dropna().astype(str).unique().tolist())
        sel_vend = st.selectbox("Vendedor", vendedores)
    with fc[1]:
        if cida_col:
            cidades = ["Todas"] + sorted(df_raw[cida_col].dropna().astype(str).unique().tolist())
            sel_cida = st.selectbox("Cidade", cidades)
        else:
            sel_cida = "Todas"
            st.caption("Coluna de cidade nao encontrada.")
    with fc[2]:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        excel_bytes = gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col)
        st.download_button(
            label="BAIXAR PLANILHA STAR",
            data=excel_bytes,
            file_name="Matriz_STAR_Giri.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    df = df_raw.copy()
    if sel_vend != "Todos":
        df = df[df[vend_col].astype(str) == sel_vend]
    if cida_col and sel_cida != "Todas":
        df = df[df[cida_col].astype(str) == sel_cida]

    ultimo_mes = meses_col[-1]
    penultimo = meses_col[-2] if len(meses_col) > 1 else meses_col[-1]
    last3 = meses_col[-3:] if len(meses_col) >= 3 else meses_col

    total = len(df)
    n_a = len(df[df['CURVA'] == 'A'])
    n_b = len(df[df['CURVA'] == 'B'])
    n_c = len(df[df['CURVA'] == 'C'])
    df_a = df[df['CURVA'] == 'A']
    rec_a_ult = df_a[ultimo_mes].sum()
    rec_a_pen = df_a[penultimo].sum()
    var_rec_a = (rec_a_ult - rec_a_pen) / rec_a_pen * 100 if rec_a_pen > 0 else 0
    meta_total = df['META'].sum()
    meta_a = df[df['CURVA'] == 'A']['META'].sum()
    meta_b = df[df['CURVA'] == 'B']['META'].sum()
    meta_c = df[df['CURVA'] == 'C']['META'].sum()
    risco_mask = (df['CURVA'] == 'A') & (df['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO']))
    risco_a = df.loc[risco_mask, 'MEDIA LP'].sum()
    n_risco_a = risco_mask.sum()
    ticket_ult = df_a[ultimo_mes].mean() if n_a > 0 else 0
    ticket_pen = df_a[penultimo].mean() if n_a > 0 else 0
    var_ticket = (ticket_ult - ticket_pen) / ticket_pen * 100 if ticket_pen > 0 else 0
    saude_mask = (df['CURVA'] == 'A') & (df['STATUS'].isin(['CRESCIMENTO', 'CRESCIMENTO ACENTUADO', 'ESTAVEL']))
    n_saudaveis = saude_mask.sum()
    idx_saude = n_saudaveis / n_a * 100 if n_a > 0 else 0
    saude_color = "#1A6B2A" if idx_saude >= 70 else ("#F4A500" if idx_saude >= 50 else "#C00000")

    st.markdown('<div class="section-title">VISAO GERAL DA CARTEIRA</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-wrap blue"><div class="kpi-lbl">COMPOSICAO DA CARTEIRA</div><div class="kpi-val blue">{fmt_br(total)}</div><div class="kpi-breakdown"><span>A: {n_a}</span> | <span>B: {n_b}</span> | <span>C: {n_c}</span></div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-wrap blue"><div class="kpi-lbl">RECEITA CURVA A &mdash; {ultimo_mes}</div><div class="kpi-val blue">R$ {fmt_br(rec_a_ult)}</div><div class="kpi-sub">vs {penultimo}: {var_html(var_rec_a)}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-wrap gold"><div class="kpi-lbl">META DO MES</div><div class="kpi-val gold">R$ {fmt_br(meta_total)}</div><div class="kpi-breakdown"><span>A: R$ {fmt_br(meta_a)}</span><br><span>B: R$ {fmt_br(meta_b)}</span> | <span>C: R$ {fmt_br(meta_c)}</span></div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-wrap red"><div class="kpi-lbl">RECEITA EM RISCO &mdash; CURVA A</div><div class="kpi-val red">R$ {fmt_br(risco_a)}</div><div class="kpi-sub">{n_risco_a} clientes A em queda ou inativos</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">INDICADORES CURVA A</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown(f'<div class="ind-wrap"><div class="ind-lbl">TICKET MEDIO CURVA A &mdash; {ultimo_mes}</div><div class="ind-val">R$ {fmt_br(ticket_ult)}</div><div class="ind-sub">vs {penultimo}: {var_html(var_ticket)}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="ind-wrap"><div class="ind-lbl">INDICE DE SAUDE &mdash; CURVA A</div><div class="ind-val" style="color:{saude_color}">{idx_saude:.0f}%</div><div class="ind-sub">{n_saudaveis} de {n_a} clientes A em crescimento ou estaveis</div></div>', unsafe_allow_html=True)

    # ANALISE DETALHADA CURVA A
    st.markdown('<div class="section-title">ANALISE DETALHADA CURVA A</div>', unsafe_allow_html=True)
    col_fat, col_ticket = st.columns(2)

    with col_fat:
        fat_rows = ""
        for i, mes in enumerate(last3):
            fat = df_a[mes].sum()
            if i == 0:
                var_pct = None
            else:
                prev = df_a[last3[i-1]].sum()
                var_pct = (fat - prev) / prev * 100 if prev > 0 else None
            fat_rows += f"<tr><td>{mes}</td><td>R$ {fmt_br(fat)}</td><td>{var_html(var_pct)}</td></tr>"
        st.markdown(f'<div class="ana-wrap"><div class="ana-title">FATURAMENTO CURVA A &mdash; ULTIMOS 3 MESES</div><table class="ana-table"><thead><tr><th>MES</th><th>FATURAMENTO</th><th>VARIACAO</th></tr></thead><tbody>{fat_rows}</tbody></table></div>', unsafe_allow_html=True)

    with col_ticket:
        tick_rows = ""
        for mes in last3:
            ativos = int((df_a[mes] > 0).sum())
            fat = df_a[mes].sum()
            ticket = fat / ativos if ativos > 0 else 0
            tick_rows += f"<tr><td>{mes}</td><td>{ativos}</td><td>R$ {fmt_br(fat)}</td><td>R$ {fmt_br(ticket)}</td></tr>"
        st.markdown(f'<div class="ana-wrap"><div class="ana-title">TICKET MEDIO CURVA A &mdash; ULTIMOS 3 MESES</div><table class="ana-table"><thead><tr><th>MES</th><th>CLIENTES ATIVOS</th><th>FATURAMENTO</th><th>TICKET MEDIO</th></tr></thead><tbody>{tick_rows}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    rec_col, lista_col = st.columns([1, 2])

    with rec_col:
        faixas = [
            ('0-30 dias', '<span class="rec-ativo">Ativo recente</span>', 0),
            ('31-60 dias', '<span class="rec-atencao">Atencao</span>', 1),
            ('61-90 dias', '<span class="rec-risco">Risco alto</span>', 2),
            ('Acima de 90 dias', '<span class="rec-critico">Inativo critico</span>', 99),
        ]
        rec_rows = ""
        for faixa, badge, meses_ref in faixas:
            if meses_ref == 99:
                count = int((df_a['MESES_SEM_COMPRA'] >= 3).sum())
            else:
                count = int((df_a['MESES_SEM_COMPRA'] == meses_ref).sum())
            pct = count / n_a * 100 if n_a > 0 else 0
            rec_rows += f"<tr><td>{badge}</td><td>{faixa}</td><td>{count}</td><td>{pct:.0f}%</td></tr>"
        st.markdown(f'<div class="ana-wrap"><div class="ana-title">RECENCIA DE COMPRA &mdash; CURVA A</div><table class="ana-table"><thead><tr><th>CLASSIFICACAO</th><th>FAIXA</th><th>CLIENTES</th><th>%</th></tr></thead><tbody>{rec_rows}</tbody></table></div>', unsafe_allow_html=True)

    with lista_col:
        faixas_lista = [
            ('Ativo recente', 'rec-ativo', '#375623', df_a[df_a['MESES_SEM_COMPRA'] == 0]),
            ('Atencao', 'rec-atencao', '#9C6500', df_a[df_a['MESES_SEM_COMPRA'] == 1]),
            ('Risco alto', 'rec-risco', '#9C0006', df_a[df_a['MESES_SEM_COMPRA'] == 2]),
            ('Inativo critico', 'rec-critico', '#FFFFFF', df_a[df_a['MESES_SEM_COMPRA'] >= 3]),
        ]
        lista_html = ""
        for label, css_class, txt_color, subset in faixas_lista:
            if len(subset) == 0:
                continue
            nomes = ""
            for _, row in subset.iterrows():
                nomes += f'<tr><td class="left">{htmllib.escape(str(row[clie_col]))}</td><td>{htmllib.escape(str(row[vend_col]))}</td><td>R$ {fmt_br(row[ultimo_mes])}</td></tr>'
            lista_html += f'<div style="margin-bottom:12px"><span class="{css_class}" style="font-size:0.72rem;font-weight:800;padding:3px 12px;border-radius:6px;display:inline-block;margin-bottom:8px">{label} ({len(subset)})</span><table class="ana-table"><thead><tr><th style="text-align:left">CLIENTE</th><th>VENDEDOR</th><th>{ultimo_mes}</th></tr></thead><tbody>{nomes}</tbody></table></div>'
        st.markdown(f'<div class="cli-list-wrap"><div class="ana-title">CLIENTES CURVA A POR RECENCIA DE COMPRA</div>{lista_html}</div>', unsafe_allow_html=True)

    # GRAFICOS
    st.markdown('<div class="section-title">DIAGNOSTICO DE CARTEIRA</div>', unsafe_allow_html=True)
    g1, g2 = st.columns([3, 2])
    with g1:
        status_counts = df['STATUS'].value_counts()
        labels = [s for s in STATUS_ORDER if s in status_counts.index]
        values = [status_counts[s] for s in labels]
        colors = [STATUS_COLORS[s] for s in labels]
        pcts = [v / total * 100 if total > 0 else 0 for v in values]
        fig1 = go.Figure(go.Bar(
            x=values, y=labels, orientation='h', marker_color=colors,
            text=[f"  {v} ({p:.0f}%)" for v, p in zip(values, pcts)],
            textposition='outside', textfont=dict(size=11, family='Arial', color='#374151'),
        ))
        fig1.update_layout(
            margin=dict(l=0, r=90, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(tickfont=dict(size=11, family='Arial', color='#374151'), autorange='reversed'),
            height=260, showlegend=False,
        )
        st.markdown('<div class="chart-wrap"><div class="chart-lbl">DISTRIBUICAO POR STATUS</div>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        curva_counts = df['CURVA'].value_counts()
        cv_labels = ['A', 'B', 'C']
        cv_values = [curva_counts.get(c, 0) for c in cv_labels]
        cv_colors = ['#001845', '#0056b3', '#7EB8F7']
        fig2 = go.Figure(go.Pie(
            labels=cv_labels, values=cv_values, hole=0.58,
            marker=dict(colors=cv_colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='label+percent', textfont=dict(size=13, family='Arial', color='#FFFFFF'),
            insidetextorientation='radial',
        ))
        fig2.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', height=260, showlegend=False,
        )
        st.markdown('<div class="chart-wrap"><div class="chart-lbl">DISTRIBUICAO POR CURVA ABC</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # PERFORMANCE POR VENDEDOR
    if sel_vend == "Todos":
        st.markdown('<div class="section-title">PERFORMANCE POR VENDEDOR</div>', unsafe_allow_html=True)
        rows = []
        for v in sorted(df[vend_col].dropna().astype(str).unique()):
            dv = df[df[vend_col].astype(str) == v]
            rows.append({
                'VENDEDOR': v,
                'CLIENTES': str(len(dv)),
                'CURVA A': str(len(dv[dv['CURVA'] == 'A'])),
                'RECEITA TOTAL': f"R$ {fmt_br(dv['TOTAL LP'].sum())}",
                'EM RISCO': str(len(dv[dv['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO'])])),
                'CRESCIMENTO': str(len(dv[dv['STATUS'].isin(['CRESCIMENTO', 'CRESCIMENTO ACENTUADO'])])),
                'INATIVOS': str(len(dv[dv['STATUS'] == 'INATIVO'])),
            })
        cols_vend = ['VENDEDOR', 'CLIENTES', 'CURVA A', 'RECEITA TOTAL', 'EM RISCO', 'CRESCIMENTO', 'INATIVOS']
        header_html = "".join([f"<th>{c}</th>" for c in cols_vend])
        rows_html = ""
        for r in rows:
            cells = "".join([f"<td>{r[c]}</td>" for c in cols_vend])
            rows_html += f"<tr>{cells}</tr>"
        st.markdown(f'<div class="vend-wrap"><table class="vend-table"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)

    # CARTEIRA DE CLIENTES
    st.markdown('<div class="section-title">CARTEIRA DE CLIENTES</div>', unsafe_allow_html=True)
    cols_display = ['CURVA', clie_col, vend_col] + extra + ['TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'STATUS', 'META']
    df_disp = df[cols_display].copy().reset_index(drop=True)

    header_cart = "".join([f"<th>{c}</th>" for c in cols_display])
    rows_cart = ""
    for _, row in df_disp.iterrows():
        cells = ""
        for col_n in cols_display:
            val = row[col_n]
            align_class = ' class="left"' if col_n == clie_col else ''
            if col_n == 'STATUS':
                s = str(val)
                css = STATUS_CSS.get(s, '')
                cells += f'<td><span style="{css}">{s}</span></td>'
            elif col_n in ('TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'META'):
                cells += f'<td{align_class}>{fmt_br(val)}</td>'
            else:
                escaped_val = htmllib.escape(str(val)) if col_n == clie_col else str(val)
                cells += f'<td{align_class}>{escaped_val}</td>'
        rows_cart += f"<tr>{cells}</tr>"

    st.markdown(f'<div class="cart-wrap"><table class="cart-table"><thead><tr>{header_cart}</tr></thead><tbody>{rows_cart}</tbody></table></div>', unsafe_allow_html=True)
