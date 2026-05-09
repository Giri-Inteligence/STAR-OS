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
    border-radius: 18px;
    padding: 30px 38px;
    margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(0,18,51,0.32);
    display: flex;
    align-items: center;
    gap: 18px;
}
.giri-header-dot {
    width: 48px; height: 48px;
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.giri-header h1 {
    color: #FFFFFF;
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 0 0 3px 0;
}
.giri-header p {
    color: rgba(255,255,255,0.55);
    font-size: 0.80rem;
    margin: 0;
    letter-spacing: 0.5px;
}
.section-title {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #6B7A99;
    margin: 28px 0 12px 0;
    padding-left: 2px;
}
.kpi-wrap {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 22px 16px 22px;
    box-shadow: 0 2px 18px rgba(0,0,0,0.07);
    height: 100%;
    position: relative;
    overflow: hidden;
}
.kpi-wrap::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 14px 14px 0 0;
}
.kpi-wrap.blue::before  { background: linear-gradient(90deg,#0056b3,#00A3E0); }
.kpi-wrap.red::before   { background: linear-gradient(90deg,#C00000,#FF6B6B); }
.kpi-wrap.green::before { background: linear-gradient(90deg,#1A6B2A,#52C471); }
.kpi-wrap.gold::before  { background: linear-gradient(90deg,#9E6A00,#F4C430); }
.kpi-lbl {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #8A93A2;
    margin-bottom: 10px;
}
.kpi-val {
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 7px;
    color: #0D1B2A;
}
.kpi-val.blue  { color: #0056b3; }
.kpi-val.red   { color: #C00000; }
.kpi-val.green { color: #1A6B2A; }
.kpi-val.gold  { color: #9E6A00; }
.kpi-sub {
    font-size: 0.73rem;
    color: #B0BAC9;
    line-height: 1.4;
}
.chart-wrap {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 22px 10px 22px;
    box-shadow: 0 2px 18px rgba(0,0,0,0.07);
}
.chart-lbl {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #8A93A2;
    margin-bottom: 2px;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #001233 0%, #003087 50%, #0056b3 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 15px 28px !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    width: 100% !important;
    box-shadow: 0 6px 24px rgba(0,18,51,0.35) !important;
}
.stDownloadButton > button:hover { opacity: 0.88 !important; }
</style>
""", unsafe_allow_html=True)


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
    larguras = {
        'CURVA': 7, clie_col: 30, vend_col: 22,
        'TOTAL LP': 13, 'MEDIA LP': 13, 'MEDIA CP': 13,
        'STATUS': 24, 'META': 12, 'ACAO': 88,
    }
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


def kpi(lbl, val, sub, color):
    return f"""
    <div class="kpi-wrap {color}">
        <div class="kpi-lbl">{lbl}</div>
        <div class="kpi-val {color}">{val}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


STATUS_ORDER = ['CRESCIMENTO ACENTUADO', 'CRESCIMENTO', 'ESTAVEL', 'QUEDA', 'QUEDA ACENTUADA', 'INATIVO']
STATUS_COLORS = {
    'CRESCIMENTO ACENTUADO': '#1A6B2A',
    'CRESCIMENTO':           '#52C471',
    'ESTAVEL':               '#0070C0',
    'QUEDA':                 '#FF6B6B',
    'QUEDA ACENTUADA':       '#C00000',
    'INATIVO':               '#9CA3AF',
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
    df_raw = (
        pd.read_excel(uploaded_file)
        if uploaded_file.name.endswith('xlsx')
        else pd.read_csv(uploaded_file)
    )
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [c for c in cols if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))]
    clie_col  = next((c for c in cols if any(x in c for x in ("CLIENTE","NOME","RAZAO"))), cols[0])
    vend_col  = next((c for c in cols if any(x in c for x in ("VENDEDOR","REP"))), cols[1] if len(cols) > 1 else cols[0])
    cida_col  = next((c for c in cols if any(x in c for x in ("CIDADE","MUNICIPIO","LOCALIDADE","REGIAO"))), None)

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

    total       = len(df)
    curva_a     = len(df[df['CURVA'] == 'A'])
    pct_a       = curva_a / total * 100 if total > 0 else 0
    rec_tot     = df['TOTAL LP'].sum()
    risco_mask  = df['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO'])
    rec_risco   = df.loc[risco_mask, 'TOTAL LP'].sum()
    pct_risco   = rec_risco / rec_tot * 100 if rec_tot > 0 else 0
    queda_mask  = df['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA'])
    potencial   = max(0, (df.loc[queda_mask, 'META'] - df.loc[queda_mask, 'MEDIA CP']).sum())

    st.markdown('<div class="section-title">VISAO GERAL DA CARTEIRA</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi("Total de Clientes", f"{total}", f"Curva A: {curva_a} clientes ({pct_a:.0f}%)", "blue"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi("Receita Total LP", f"R$ {rec_tot:,.0f}", "Faturamento acumulado do periodo", "blue"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi("Receita em Risco", f"R$ {rec_risco:,.0f}", f"{pct_risco:.0f}% da receita total da carteira", "red"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi("Potencial de Recuperacao", f"R$ {potencial:,.0f}", "Gap META vs MEDIA CP nos clientes em queda", "green"), unsafe_allow_html=True)

    st.markdown('<div class="section-title">DIAGNOSTICO DE CARTEIRA</div>', unsafe_allow_html=True)
    g1, g2 = st.columns([3, 2])

    with g1:
        status_counts = df['STATUS'].value_counts()
        labels = [s for s in STATUS_ORDER if s in status_counts.index]
        values = [status_counts[s] for s in labels]
        colors = [STATUS_COLORS[s] for s in labels]
        pcts   = [v / total * 100 if total > 0 else 0 for v in values]
        fig1 = go.Figure(go.Bar(
            x=values, y=labels, orientation='h',
            marker_color=colors,
            text=[f"  {v} ({p:.0f}%)" for v, p in zip(values, pcts)],
            textposition='outside',
            textfont=dict(size=11, family='Arial', color='#374151'),
        ))
        fig1.update_layout(
            margin=dict(l=0, r=90, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
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
            labels=cv_labels, values=cv_values,
            hole=0.58,
            marker=dict(colors=cv_colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='label+percent',
            textfont=dict(size=13, family='Arial', color='#FFFFFF'),
            insidetextorientation='radial',
        ))
        fig2.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            height=260, showlegend=False,
        )
        st.markdown('<div class="chart-wrap"><div class="chart-lbl">DISTRIBUICAO POR CURVA ABC</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    if sel_vend == "Todos":
        st.markdown('<div class="section-title">PERFORMANCE POR VENDEDOR</div>', unsafe_allow_html=True)
        rows = []
        for v in sorted(df[vend_col].dropna().astype(str).unique()):
            dv = df[df[vend_col].astype(str) == v]
            rows.append({
                'VENDEDOR':      v,
                'CLIENTES':      len(dv),
                'CURVA A':       len(dv[dv['CURVA'] == 'A']),
                'RECEITA TOTAL': dv['TOTAL LP'].sum(),
                'EM RISCO':      len(dv[dv['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO'])]),
                'CRESCIMENTO':   len(dv[dv['STATUS'].isin(['CRESCIMENTO', 'CRESCIMENTO ACENTUADO'])]),
                'INATIVOS':      len(dv[dv['STATUS'] == 'INATIVO']),
            })
        df_vend = pd.DataFrame(rows).sort_values('RECEITA TOTAL', ascending=False)
        st.dataframe(
            df_vend.style.format({'RECEITA TOTAL': 'R$ {:,.0f}'}),
            use_container_width=True, hide_index=True
        )

    st.markdown('<div class="section-title">CARTEIRA DE CLIENTES</div>', unsafe_allow_html=True)
    cols_display = ['CURVA', clie_col, vend_col] + extra + ['TOTAL LP', 'MEDIA LP', 'MEDIA CP', 'STATUS', 'META']
    df_disp = df[cols_display].copy()

    def colorir(val):
        return {
            'QUEDA ACENTUADA':       'background-color:#FFC7CE;color:#C00000;font-weight:bold',
            'QUEDA':                 'color:#C00000;font-weight:bold',
            'CRESCIMENTO ACENTUADO': 'background-color:#C6EFCE;color:#375623;font-weight:bold',
            'CRESCIMENTO':           'color:#375623;font-weight:bold',
            'ESTAVEL':               'color:#0070C0;font-weight:bold',
            'INATIVO':               'color:#6B7280;font-weight:bold',
        }.get(val, '')

    styled = (
        df_disp.style
        .map(colorir, subset=['STATUS'])
        .format({'TOTAL LP': '{:,.0f}', 'MEDIA LP': '{:,.0f}', 'MEDIA CP': '{:,.0f}', 'META': '{:,.0f}'})
    )
    st.dataframe(styled, use_container_width=True, height=500)
