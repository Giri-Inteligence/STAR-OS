import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter
import plotly.graph_objects as go
import html as htmllib  # <-- ADICIONADO: escape de caracteres HTML

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
.cli-badge { display: inline-block; font-size: 0.70rem; font-weight: 700; padding: 2px 10px; border-radius: 6px; margin-bottom: 10px; }
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
    sign  = "+" if pct >= 0 else ""
    return f'<span style="color:{color};font-weight:700">{sign}{pct:.1f}%</span>'


def recencia_label(meses_atras):
    if meses_atras == 0:
        return '<span class="rec-ativo">0-30 dias</span>', '0-30 dias'
    elif meses_atras == 1:
        return '<span class="rec-atencao">31-60 dias</span>', '31-60 dias'
    elif meses_atras == 2:
        return '<span class="rec-risco">61-90 dias</span>', '61-90 dias'
    else:
        return '<span class="rec-critico">Acima de 90 dias</span>', 'Acima de 90 dias'


STATUS_ORDER = ['CRESCIMENTO ACENTUADO', 'CRESCIMENTO', 'ESTAVEL', 'QUEDA', 'QUEDA ACENTUADA', 'INATIVO']
STATUS_COLORS = {
    'CRESCIMENTO ACENTUADO': '#1A6B2A', 'CRESCIMENTO': '#52C471',
    'ESTAVEL': '#0070C0', 'QUEDA': '#FF6B6B',
    'QUEDA ACENTUADA': '#C00000', 'INATIVO': '#9CA3AF',
}
STATUS_CSS = {
    'QUEDA ACENTUADA':       'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 8px;',
    'QUEDA':                 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 8px;',
    'CRESCIMENTO':           'color:#375623;font-weight:700;',
    'ESTAVEL':               'color:#0070C0;font-weight:700;',
    'INATIVO':               'color:#6B7280;font-weight:700;',
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
    clie_col  = next((c for c in cols if any(x in c for x in ("CLIENTE","NOME","RAZAO"))), cols[0])
    vend_col  = next((c for c in cols if any(x in c for x in ("VENDEDOR","REP"))), cols[1] if len(cols) > 1 else cols[0])
    cida_col  = next((c for c in cols if any(x in c for x in ("CIDADE","MUNICIPIO","LOCALIDADE","REGIAO"))), None)

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

    # RECENCIA: meses atras desde ultima compra > 0
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
    penultimo  = meses_col[-2] if len(meses_col) > 1 else meses_col[-1]
    last3      = meses_col[-3:] if len(meses_col) >= 3 else meses_col

    total    = len(df)
    n_a      = len(df[df['CURVA'] == 'A'])
    n_b      = len(df[df['CURVA'] == 'B'])
    n_c      = len(df[df['CURVA'] == 'C'])
    df_a     = df[df['CURVA'] == 'A']
    rec_a_ult   = df_a[ultimo_mes].sum()
    rec_a_pen   = df_a[penultimo].sum()
    var_rec_a   = (rec_a_ult - rec_a_pen) / rec_a_pen * 100 if rec_a_pen > 0 else 0
    meta_total  = df['META'].sum()
    meta_a      = df[df['CURVA'] == 'A']['META'].sum()
    meta_b      = df[df['CURVA'] == 'B']['META'].sum()
    meta_c      = df[df['CURVA'] == 'C']['META'].sum()
    risco_mask  = (df['CURVA'] == 'A') & (df['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO']))
    risco_a     = df.loc[risco_mask, 'MEDIA LP'].sum()
    n_risco_a   = risco_mask.sum()
    ticket_ult  = df_a[ultimo_mes].mean() if n_a > 0 else 0
    ticket_pen  = df_a[penultimo].mean()  if n_a > 0 else 0
    var_ticket  = (ticket_ult - ticket_pen) / ticket_pen * 100 if ticket_pen > 0 else 0
    saude_mask  = (df['CURVA'] == 'A') & (df['STATUS'].isin(['CRESCIMENTO', 'CRESCIMENTO ACENTUADO', 'ESTAVEL']))
    n_saudaveis = saude_mask.sum()
    idx_saude   = n_saudaveis / n_a * 100 if n_a > 0 else 0
    saude_color = "#1A6B2A" if idx_saude >= 70 else ("#F4A500" if idx_saude >= 50 else "#C00000")

    # ── CARDS ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">VISAO GERAL DA CARTEIRA</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-wrap blue">
            <div class="kpi-lbl">COMPOSICAO DA CARTEIRA</div>
            <div class="kpi-val blue">{fmt_br(total)}</div>
            <div class="kpi-breakdown"><span>A: {n_a}</span> | <span>B: {n_b}</span> | <span>C: {n_c}</span></div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-wrap blue">
            <div class="kpi-lbl">RECEITA CURVA A &mdash; {ultimo_mes}</div>
            <div class="kpi-val blue">R$ {fmt_br(rec_a_ult)}</div>
            <div class="kpi-sub">vs {penultimo}: {var_html(var_rec_a)}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-wrap gold">
            <div class="kpi-lbl">META DO MES</div>
            <div class="kpi-val gold">R$ {fmt_br(meta_total)}</div>
            <div class="kpi-breakdown"><span>A: R$ {fmt_br(meta_a)}</span><br>
            <span>B: R$ {fmt_br(meta_b)}</span> | <span>C: R$ {fmt_br(meta_c)}</span></div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-wrap red">
            <div class="kpi-lbl">RECEITA EM RISCO &mdash; CURVA A</div>
            <div class="kpi-val red">R$ {fmt_br(risco_a)}</div>
            <div class="kpi-sub">{n_risco_a} clientes A em queda ou inativos</div>
        </div>""", unsafe_allow_html=True)

    # ── INDICADORES CURVA A ────────────────────────────────────────────────────
    st.markdown('<div class="section-title">INDICADORES CURVA A</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown(f"""<div class="ind-wrap">
            <div class="ind-lbl">TICKET MEDIO CURVA A &mdash; {ultimo_mes}</div>
            <div class="ind-val">R$ {fmt_br(ticket_ult)}</div>
            <div class="ind-sub">vs {penultimo}: {var_html(var_ticket)}</div>
        </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(f"""<div class="ind-wrap
