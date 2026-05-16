import streamlit as st
import pandas as pd
import html as htmllib
from io import BytesIO
import xlsxwriter
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Giri | STAR", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #EDF1F7; }
[data-testid="stHeader"] { background: transparent; }
.giri-header { background: linear-gradient(120deg, #001233 0%, #003087 55%, #0056b3 100%); border-radius: 18px; padding: 30px 38px; margin-bottom: 28px; box-shadow: 0 10px 40px rgba(0,18,51,0.32); display: flex; align-items: center; gap: 18px; }
.giri-header-dot { width: 48px; height: 48px; background: rgba(255,255,255,0.15); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
.giri-header h1 { color:#FFFFFF; font-size:1.45rem; font-weight:800; letter-spacing:1.2px; margin:0 0 3px 0; }
.giri-header p  { color:rgba(255,255,255,0.65); font-size:0.80rem; margin:0; letter-spacing:0.5px; }
.section-title { font-size:0.95rem; font-weight:800; text-transform:uppercase; letter-spacing:2px; color:#1A2540; margin:32px 0 14px 0; padding-bottom:8px; border-bottom:2px solid #D1D9E6; }
.kpi-wrap { background:#FFFFFF; border-radius:14px; padding:20px 22px 16px 22px; box-shadow:0 2px 18px rgba(0,0,0,0.07); height:100%; position:relative; overflow:hidden; text-align:center; }
.kpi-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:4px; border-radius:14px 14px 0 0; }
.kpi-wrap.blue::before { background:linear-gradient(90deg,#0056b3,#00A3E0); }
.kpi-wrap.red::before  { background:linear-gradient(90deg,#C00000,#FF6B6B); }
.kpi-wrap.dark::before { background:linear-gradient(90deg,#1A2540,#3A4A6B); }
.kpi-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:10px; }
.kpi-val { font-size:1.85rem; font-weight:800; line-height:1; margin-bottom:7px; color:#0D1B2A; }
.kpi-val.red { color:#C00000; }
.kpi-sub { font-size:0.74rem; color:#4B5568; line-height:1.4; }
.kpi-breakdown { font-size:0.74rem; color:#4B5568; margin-top:8px; font-weight:600; }
.kpi-breakdown span { margin:0 4px; }
.ind-wrap { background:#FFFFFF; border-radius:14px; padding:18px 22px; box-shadow:0 2px 18px rgba(0,0,0,0.07); text-align:center; position:relative; overflow:hidden; }
.ind-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:4px; border-radius:14px 14px 0 0; background:linear-gradient(90deg,#001845,#0056b3); }
.ind-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:8px; }
.ind-val { font-size:1.5rem; font-weight:800; color:#0D1B2A; margin-bottom:5px; }
.ind-sub { font-size:0.74rem; color:#4B5568; }
.chart-wrap { background:#FFFFFF; border-radius:14px; padding:20px 22px 10px 22px; box-shadow:0 2px 18px rgba(0,0,0,0.07); }
.chart-lbl { font-size:1.0rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; color:#1A2540; text-align:center; margin-bottom:8px; }
.ana-wrap { background:#FFFFFF; border-radius:14px; padding:20px 24px; box-shadow:0 2px 18px rgba(0,0,0,0.07); }
.ana-title { font-size:0.80rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#1A2540; margin-bottom:14px; text-align:center; }
.ana-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.ana-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:10px 10px; text-align:center; font-size:0.70rem; text-transform:uppercase; letter-spacing:0.6px; white-space:normal; line-height:1.4; vertical-align:middle; }
.ana-table td { padding:10px 10px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; font-size:0.85rem; vertical-align:middle; }
.ana-table td.left { text-align:left; }
.ana-table tr:last-child td { border-bottom:none; }
.ana-table tr:hover td { background:#F5F7FB; }
.ana-table tr.total-row td { background:#EEF2FF; font-weight:800; color:#001845; border-top:2px solid #1A2540; }
.rec-ativo   { background:#C6EFCE; color:#375623; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-atencao { background:#FFEB9C; color:#7A4F00; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-risco   { background:#FFC7CE; color:#7A0000; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-critico { background:#C00000; color:#FFFFFF; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.briefing-wrap { background:#FFFFFF; border-radius:16px; padding:28px 32px; box-shadow:0 4px 24px rgba(0,0,0,0.10); border-left:6px solid #001845; }
.briefing-status { display:flex; align-items:center; gap:12px; margin-bottom:16px; }
.briefing-badge { font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; padding:5px 16px; border-radius:20px; }
.badge-critico { background:#C00000; color:#FFFFFF; }
.badge-atencao { background:#FFEB9C; color:#7A4F00; }
.badge-estavel { background:#C6EFCE; color:#375623; }
.briefing-titulo { font-size:1.15rem; font-weight:800; color:#0D1B2A; }
.briefing-texto { font-size:0.90rem; color:#2D3748; line-height:1.7; margin:12px 0 18px 0; }
.briefing-prioridades { border-top:1px solid #E5EAF2; padding-top:14px; }
.briefing-prioridades-titulo { font-size:0.68rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; color:#6B7A99; margin-bottom:10px; }
.prioridade-item { display:flex; align-items:flex-start; gap:10px; margin-bottom:8px; }
.prioridade-num { background:#001845; color:#FFFFFF; border-radius:50%; width:22px; height:22px; display:flex; align-items:center; justify-content:center; font-size:0.72rem; font-weight:800; flex-shrink:0; margin-top:1px; }
.prioridade-texto { font-size:0.87rem; color:#2D3748; font-weight:500; }
.missao-card { background:#FFFFFF; border-radius:16px; padding:24px 28px; box-shadow:0 4px 24px rgba(0,0,0,0.10); height:100%; }
.missao-card.critica { border-top:5px solid #C00000; }
.missao-card.urgente { border-top:5px solid #E07000; }
.missao-card.atencao { border-top:5px solid #B09000; }
.missao-badge { font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; padding:4px 14px; border-radius:20px; display:inline-block; margin-bottom:12px; }
.missao-badge.critica { background:#FFC7CE; color:#C00000; }
.missao-badge.urgente { background:#FFE0B2; color:#E07000; }
.missao-badge.atencao { background:#FFEB9C; color:#7A4F00; }
.missao-titulo { font-size:1.05rem; font-weight:800; color:#0D1B2A; margin-bottom:6px; }
.missao-contexto { font-size:0.85rem; color:#4B5568; margin-bottom:18px; line-height:1.5; }
.missao-steps { margin-bottom:18px; }
.missao-step { display:flex; align-items:flex-start; gap:12px; margin-bottom:12px; }
.step-num { border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:800; flex-shrink:0; margin-top:1px; color:#FFFFFF; }
.step-num.critica { background:#C00000; }
.step-num.urgente { background:#E07000; }
.step-num.atencao { background:#B09000; }
.step-titulo { font-size:0.87rem; font-weight:700; color:#0D1B2A; margin-bottom:2px; }
.step-desc { font-size:0.82rem; color:#4B5568; line-height:1.5; }
.missao-footer { border-top:2px solid #E5EAF2; padding-top:14px; }
.missao-footer-titulo { font-size:0.68rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; color:#6B7A99; margin-bottom:10px; }
.vend-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.vend-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:10px 10px; text-align:center; letter-spacing:0.6px; font-size:0.70rem; text-transform:uppercase; white-space:normal; line-height:1.4; vertical-align:middle; }
.vend-table td { padding:10px 12px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; vertical-align:middle; }
.vend-table td.left { text-align:left; font-weight:600; }
.vend-table tr:last-child td { border-bottom:none; }
.vend-table tr:hover td { background:#F5F7FB; }
.vend-table tr.total-row td { background:#EEF2FF; font-weight:800; color:#001845; border-top:2px solid #1A2540; }
.vend-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:auto; }
.cart-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.cart-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:11px 14px; text-align:center; letter-spacing:0.8px; font-size:0.72rem; text-transform:uppercase; }
.cart-table td { padding:10px 14px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; }
.cart-table td.left { text-align:left; }
.cart-table tr:last-child td { border-bottom:none; }
.cart-table tr:hover td { background:#F5F7FB; }
.cart-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:auto; max-height:520px; }
.stDownloadButton > button { background:linear-gradient(135deg,#1A5C2A 0%,#2E8B47 100%) !important; color:#FFFFFF !important; border:none !important; border-radius:12px !important; padding:15px 28px !important; font-size:0.88rem !important; font-weight:800 !important; letter-spacing:1px !important; width:100% !important; box-shadow:0 6px 24px rgba(26,92,42,0.40) !important; }
.stDownloadButton > button:hover { opacity:0.88 !important; }
</style>
""", unsafe_allow_html=True)


def fmt_br(v):
    return f"{int(v):,}".replace(",", ".")

def var_html(pct):
    if pct is None: return '<span style="color:#9CA3AF">--</span>'
    c = "#1A6B2A" if pct >= 0 else "#C00000"
    s = "+" if pct >= 0 else ""
    return f'<span style="color:{c};font-weight:700">{s}{pct:.1f}%</span>'

def curva_label_fmt(sel):
    if not sel: return "NENHUMA"
    if set(sel) == {'A','B','C'}: return "TODA A CARTEIRA"
    if len(sel) == 1: return f"CURVA {sel[0]}"
    return "CURVAS " + " + ".join(sorted(sel))

def curva_short(sel):
    if not sel: return ""
    if set(sel) == {'A','B','C'}: return "TOTAL"
    return "+".join(sorted(sel))

def engine_star(lp, cp):
    try: lp_v, cp_v = float(lp), float(cp)
    except: lp_v, cp_v = 0.0, 0.0
    txt_ina  = "OBJETIVO: Diagnostico de causa\nPRE-CONTATO: Revisar ultimo pedido. Identificar o que parou de ser comprado e em que momento.\nCONTATO: Contato de diagnostico. Entender o motivo da inatividade sem pressao de venda.\nORIENTACAO: Nao ofertar produto na primeira interacao. Primeiro entender o que aconteceu. Registrar motivo antes de qualquer acao de reconquista."
    txt_q_ac = "OBJETIVO: Recuperacao emergencial\nPRE-CONTATO: Revisar historico completo do cliente. Identificar exatamente quais produtos cairam, em que momento e qual era o volume anterior. Calcular o gap entre a media historica e o momento atual.\nCONTATO: Priorizar visita presencial ou ligacao direta - nao mensagem. Abrir diagnostico sem pressao. Entender se houve mudanca interna no cliente, problema de relacionamento ou entrada de concorrente.\nORIENTACAO: Este cliente esta em risco de perda. O objetivo da primeira interacao nao e vender - e entender. Registrar causa com precisao. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    txt_q    = "OBJETIVO: Estabilizacao\nPRE-CONTATO: Revisar historico de mix. Identificar quais produtos reduziram ou desapareceram nos ultimos 3 meses.\nCONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudanca operacional, financeira ou troca de fornecedor.\nORIENTACAO: Registrar causa identificada. Se houver abertura, propor recomposicao de mix com base no historico anterior."
    txt_est  = "OBJETIVO: Blindagem e crescimento incremental\nPRE-CONTATO: Revisar mix atual. Mapear categorias que o cliente nao compra mas que sao compativeis com seu perfil.\nCONTATO: Manter frequencia de relacionamento. Explorar oportunidade de expansao de mix.\nORIENTACAO: Cliente estavel nao e cliente seguro. Monitorar frequencia de pedidos e introduzir novos itens gradualmente."
    txt_cre  = "OBJETIVO: Consolidacao\nPRE-CONTATO: Identificar o driver do crescimento. Avaliar se e sazonalidade ou mudanca estrutural no cliente.\nCONTATO: Reforcar relacionamento. Garantir abastecimento e antecipar demanda dos proximos periodos.\nORIENTACAO: Proteger o cliente. Momento de crescimento e o de maior risco de abordagem pelo concorrente."
    txt_ca   = "OBJETIVO: Consolidacao e protecao\nPRE-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar esse volume ou se e pontual. Verificar se ha mix ainda nao explorado.\nCONTATO: Reforcar presenca. Garantir que o abastecimento esta adequado ao novo patamar de compra. Antecipar pedidos futuros.\nORIENTACAO: Crescimento acentuado atrai concorrencia. Este e o momento de maior risco de abordagem externa. Aumentar frequencia de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."
    if cp_v <= 0:         return "INATIVO", 0, txt_ina
    if lp_v <= 0:         return "ESTAVEL", int(cp_v*1.05), txt_est
    if cp_v < lp_v*0.90: return "QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < lp_v*0.98: return "QUEDA", int(lp_v), txt_q
    if cp_v > lp_v*1.10: return "CRESCIMENTO ACENTUADO", int(cp_v*1.05), txt_ca
    if cp_v > lp_v*1.02: return "CRESCIMENTO", int(cp_v*1.05), txt_cre
    return "ESTAVEL", int(lp_v*1.05), txt_est

def get_tab_names(vendors):
    fm = {}
    for v in vendors:
        p = str(v).strip().split(); f = p[0] if p else str(v)
        fm.setdefault(f, []).append(v)
    r = {}
    for f, vl in fm.items():
        if len(vl)==1: r[vl[0]] = f[:31]
        else:
            for v in vl:
                p = str(v).strip().split()
                r[v] = (f+" "+(p[1][0] if len(p)>1 else str(v)[-1]))[:31]
    return r

def get_excel_formats(wb):
    b = {'font_name':'Arial','border':1}
    return {
        'hdr':   wb.add_format({**b,'bold':True,'bg_color':'#002060','font_color':'#FFFFFF','align':'center','valign':'vcenter','text_wrap':True}),
        'txt':   wb.add_format({**b,'valign':'vcenter','align':'left','text_wrap':True}),
        'num':   wb.add_format({**b,'num_format':'#,##0','valign':'vcenter','align':'center'}),
        'total': wb.add_format({**b,'num_format':'#,##0','bg_color':'#D9D9D9','bold':True,'font_color':'#000000','valign':'vcenter','align':'center'}),
        'qa':    wb.add_format({**b,'bg_color':'#FFC7CE','font_color':'#C00000','bold':True,'valign':'vcenter','align':'center'}),
        'q':     wb.add_format({**b,'font_color':'#C00000','bold':True,'valign':'vcenter','align':'center'}),
        'ca':    wb.add_format({**b,'bg_color':'#C6EFCE','font_color':'#375623','bold':True,'valign':'vcenter','align':'center'}),
        'c':     wb.add_format({**b,'font_color':'#375623','bold':True,'valign':'vcenter','align':'center'}),
        'e':     wb.add_format({**b,'font_color':'#0070C0','bold':True,'valign':'vcenter','align':'center'}),
        'i':     wb.add_format({**b,'font_color':'#000000','bold':True,'valign':'vcenter','align':'center'}),
    }

def write_sheet(ws, df, fo, cc, vc, mc, fmts):
    larg = {'CURVA':7,cc:30,vc:22,'TOTAL LP':13,'MEDIA LP':13,'MEDIA CP':13,'STATUS':24,'META':12,'ACAO':88}
    ws.set_default_row(125); ws.set_row(0,40)
    sf = {'QUEDA ACENTUADA':fmts['qa'],'QUEDA':fmts['q'],'CRESCIMENTO ACENTUADO':fmts['ca'],'CRESCIMENTO':fmts['c'],'ESTAVEL':fmts['e'],'INATIVO':fmts['i']}
    for i,col in enumerate(fo):
        ws.write(0,i,col,fmts['hdr']); ws.set_column(i,i,larg.get(col,8))
    for ri,row in df.iterrows():
        xl=ri+1
        for ci,cn in enumerate(fo):
            v=row[cn]
            if cn=='STATUS': ws.write_string(xl,ci,str(v),sf.get(str(v),fmts['txt']))
            elif cn=='TOTAL LP': ws.write_number(xl,ci,int(v),fmts['total'])
            elif cn in('MEDIA LP','MEDIA CP','META') or cn in mc: ws.write_number(xl,ci,int(v),fmts['num'])
            else: ws.write_string(xl,ci,str(v),fmts['txt'])

def gerar_excel(df_raw,fo,cc,vc,mc):
    buf=BytesIO(); vends=sorted(df_raw[vc].dropna().astype(str).unique().tolist()); tn=get_tab_names(vends)
    with pd.ExcelWriter(buf,engine='xlsxwriter') as w:
        wb=w.book; fmts=get_excel_formats(wb)
        df_raw[fo].to_excel(w,index=False,sheet_name='GERAL')
        write_sheet(w.sheets['GERAL'],df_raw.reset_index(drop=True),fo,cc,vc,mc,fmts)
        for vend in vends:
            dv=df_raw[df_raw[vc].astype(str)==vend].reset_index(drop=True)
            tab=tn[vend]; dv[fo].to_excel(w,index=False,sheet_name=tab)
            write_sheet(w.sheets[tab],dv,fo,cc,vc,mc,fmts)
    return buf.getvalue()

STATUS_ORDER  = ['CRESCIMENTO ACENTUADO','CRESCIMENTO','ESTAVEL','QUEDA','QUEDA ACENTUADA','INATIVO']
STATUS_COLORS = {'CRESCIMENTO ACENTUADO':'#1A6B2A','CRESCIMENTO':'#52C471','ESTAVEL':'#0070C0','QUEDA':'#FF6B6B','QUEDA ACENTUADA':'#C00000','INATIVO':'#9CA3AF'}
STATUS_CSS    = {'QUEDA ACENTUADA':'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 8px;','QUEDA':'color:#C00000;font-weight:700;','CRESCIMENTO ACENTUADO':'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 8px;','CRESCIMENTO':'color:#375623;font-weight:700;','ESTAVEL':'color:#0070C0;font-weight:700;','INATIVO':'color:#6B7280;font-weight:700;'}

st.markdown("""
<div class="giri-header">
    <div class="giri-header-dot">&#9733;</div>
    <div><h1>GIRI | SISTEMA DE GOVERNANCA STAR</h1>
    <p>PAINEL DE GOVERNANCA COMERCIAL &#8212; GESTAO DE CARTEIRA B2B</p></div>
</div>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Faca upload da base (XLSX ou CSV)", type=['xlsx','csv'])

if uploaded_file:
    def detectar_header(file):
        kw = ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ")
        for h in range(6):
            try:
                dt = pd.read_excel(file, header=h, nrows=3)
                if any(any(m in str(c).upper() for m in kw) for c in dt.columns): return h
            except: pass
        return 0

    fn = uploaded_file.name
    if fn.endswith('xlsx'):
        hr = detectar_header(uploaded_file); uploaded_file.seek(0)
        df_raw = pd.read_excel(uploaded_file, header=hr)
    else:
        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')

    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [c for c in cols if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))]
    clie_col  = next((c for c in cols if any(x in c for x in ("CLIENTE","NOME","RAZAO"))), cols[0])
    vend_col  = next((c for c in cols if any(x in c for x in ("VENDEDOR","REP"))), cols[1] if len(cols)>1 else cols[0])
    cida_col  = next((c for c in cols if any(x in c for x in ("CIDADE","MUNICIPIO","LOCALIDADE","REGIAO"))), None)

    for c in meses_col:
        df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)

    df_raw = df_raw.dropna(subset=meses_col, how='all').reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].notna()].reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].astype(str).str.strip()!=''].reset_index(drop=True)

    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MEDIA LP'] = df_raw[meses_col].mean(axis=1).astype(int)
    df_raw['MEDIA CP'] = df_raw[meses_col[-3:]].mean(axis=1).astype(int)

    curva_detectada = False
    import re

    if 'CURVA' in cols:
        vals = df_raw['CURVA'].astype(str).str.upper().str.strip()
        if vals.isin(['A','B','C']).sum() > 0:
            df_raw['CURVA'] = vals.where(vals.isin(['A','B','C']), other=pd.NA).ffill().fillna('C')
            curva_detectada = True

    if not curva_detectada:
        for col in cols:
            col_vals = df_raw[col].astype(str).str.upper().str.strip()
            if col_vals.str.match(r'^CURVA\s*[ABC]$').any():
                curva_series = col_vals.where(col_vals.str.match(r'^CURVA\s*[ABC]$'), other=pd.NA)
                curva_series = curva_series.ffill()
                df_raw['CURVA'] = curva_series.str.replace(r'^CURVA\s*', '', regex=True).str.strip()
                df_raw['CURVA'] = df_raw['CURVA'].where(df_raw['CURVA'].isin(['A','B','C']), 'C')
                curva_detectada = True
                break

    if not curva_detectada:
        df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
        cp2 = df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()
        df_raw['CURVA'] = cp2.apply(lambda x: 'A' if x<=0.80 else('B' if x<=0.95 else 'C'))
    else:
        df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)

    res = df_raw.apply(lambda r: engine_star(r['MEDIA LP'],r['MEDIA CP']), axis=1)
    df_raw['STATUS'],df_raw['META'],df_raw['ACAO'] = zip(*res)

    def calc_rec(row):
        for i in range(len(meses_col)-1,-1,-1):
            if row[meses_col[i]]>0: return len(meses_col)-1-i
        return len(meses_col)
    df_raw['MESES_SEM_COMPRA'] = df_raw.apply(calc_rec, axis=1)

    extra = [cida_col] if cida_col else []
    fo = ['CURVA',clie_col,vend_col]+extra+meses_col+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META','ACAO']

# ── FILTROS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">FILTROS</div>', unsafe_allow_html=True)
    fc = st.columns([2,2,2,2])

    LBL = '<p style="font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#4B5568;margin:0 0 4px 0;">{}</p>'

    with fc[0]:
        st.markdown(LBL.format("VENDEDOR"), unsafe_allow_html=True)
        vendedores = ["Todos"]+sorted(df_raw[vend_col].dropna().astype(str).unique().tolist())
        sel_vend = st.selectbox("Vendedor", vendedores, label_visibility="collapsed")

    with fc[1]:
        st.markdown(LBL.format("CIDADE"), unsafe_allow_html=True)
        if cida_col:
            cidades = ["Todas"]+sorted(df_raw[cida_col].dropna().astype(str).unique().tolist())
            sel_cida = st.selectbox("Cidade", cidades, label_visibility="collapsed")
        else:
            sel_cida = "Todas"
            st.caption("Coluna de cidade nao encontrada.")

    with fc[2]:
        st.markdown(LBL.format("CURVA"), unsafe_allow_html=True)
        curvas_disponiveis = sorted(df_raw['CURVA'].unique().tolist())
        sel_curvas = st.multiselect("Curva", options=curvas_disponiveis,
            default=curvas_disponiveis, placeholder="Selecione...",
            label_visibility="collapsed")
        if not sel_curvas: sel_curvas = curvas_disponiveis

    with fc[3]:
        st.markdown(LBL.format("&nbsp;"), unsafe_allow_html=True)
        eb = gerar_excel(df_raw,fo,clie_col,vend_col,meses_col)
        st.download_button(label="BAIXAR PLANILHA STAR", data=eb,
            file_name="Matriz_STAR_Giri.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # ── APLICAR FILTROS ───────────────────────────────────────────────────────
    df = df_raw.copy()
    if sel_vend != "Todos": df = df[df[vend_col].astype(str)==sel_vend]
    if cida_col and sel_cida != "Todas": df = df[df[cida_col].astype(str)==sel_cida]

    n_a_total = len(df[df['CURVA']=='A'])
    n_b_total = len(df[df['CURVA']=='B'])
    n_c_total = len(df[df['CURVA']=='C'])

    df_sel  = df[df['CURVA'].isin(sel_curvas)]
    clabel  = curva_label_fmt(sel_curvas)
    cshort  = curva_short(sel_curvas)

    ultimo_mes = meses_col[-1]; penultimo = meses_col[-2] if len(meses_col)>1 else meses_col[-1]
    last3 = meses_col[-3:] if len(meses_col)>=3 else meses_col

    total       = len(df_sel)
    rec_ult     = df_sel[ultimo_mes].sum()
    rec_pen     = df_sel[penultimo].sum()
    var_rec     = (rec_ult-rec_pen)/rec_pen*100 if rec_pen>0 else 0
    meta_total  = df_sel['META'].sum()
    meta_a      = df[df['CURVA']=='A']['META'].sum()
    meta_b      = df[df['CURVA']=='B']['META'].sum()
    meta_c      = df[df['CURVA']=='C']['META'].sum()
    risco_mask  = df_sel['STATUS'].isin(['QUEDA','QUEDA ACENTUADA','INATIVO'])
    risco_val   = df_sel.loc[risco_mask,'MEDIA LP'].sum()
    n_risco     = risco_mask.sum()
    ticket_ult  = df_sel[ultimo_mes].mean() if total>0 else 0
    ticket_pen  = df_sel[penultimo].mean() if total>0 else 0
    var_ticket  = (ticket_ult-ticket_pen)/ticket_pen*100 if ticket_pen>0 else 0
    saude_mask  = df_sel['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO','ESTAVEL'])
    n_saudaveis = saude_mask.sum()
    idx_saude   = n_saudaveis/total*100 if total>0 else 0
    saude_color = "#1A6B2A" if idx_saude>=70 else("#B07D00" if idx_saude>=50 else "#C00000")
    n_qa  = len(df_sel[df_sel['STATUS']=='QUEDA ACENTUADA'])
    n_q   = len(df_sel[df_sel['STATUS']=='QUEDA'])
    n_in  = len(df_sel[df_sel['MESES_SEM_COMPRA']>=3])
    fat_trend = all(df_sel[last3[i]].sum()<=df_sel[last3[i-1]].sum() for i in range(1,len(last3))) if len(last3)>=2 else False
    contexto  = sel_vend if sel_vend!="Todos" else "TODA A CARTEIRA"

    # ── DIAGNOSTICO ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">DIAGNOSTICO COMERCIAL</div>', unsafe_allow_html=True)
    score=0
    if n_qa>0: score+=3
    if n_in>0: score+=2
    if var_rec<-20: score+=2
    if n_q>0: score+=1
    if idx_saude<50: score+=2
    elif idx_saude<70: score+=1
    if score>=5: sit_label,sit_badge,sit_cor="CRITICO","badge-critico","#C00000"
    elif score>=2: sit_label,sit_badge,sit_cor="ATENCAO","badge-atencao","#B09000"
    else: sit_label,sit_badge,sit_cor="ESTAVEL","badge-estavel","#375623"

    frases=[]
    if n_qa>0: frases.append(f"{n_qa} cliente(s) em queda acentuada ({clabel}), com media mensal de R$ {fmt_br(df_sel[df_sel['STATUS']=='QUEDA ACENTUADA']['MEDIA LP'].sum())}.")
    if n_q>0:  frases.append(f"{n_q} cliente(s) em queda — compras abaixo da media historica.")
    if abs(var_rec)>5:
        dir2="caiu" if var_rec<0 else "cresceu"
        frases.append(f"A receita ({clabel}) {dir2} {abs(var_rec):.0f}% em relacao ao mes anterior ({penultimo} para {ultimo_mes}).")
    if n_in>0: frases.append(f"{n_in} cliente(s) sem compra ha mais de 90 dias. Recuperacao urgente necessaria.")
    if fat_trend and len(last3)>=3: frases.append(f"Faturamento em queda consecutiva nos 3 ultimos meses.")
    if idx_saude<50: frases.append(f"Apenas {idx_saude:.0f}% dos clientes selecionados estao em situacao saudavel.")
    if not frases: frases.append(f"Carteira ({clabel}) com {idx_saude:.0f}% dos clientes em crescimento ou estaveis.")

    prios=[]
    if n_qa>0: prios.append(f"Contatar imediatamente os {n_qa} cliente(s) em queda acentuada. Diagnostico antes de qualquer oferta.")
    if n_in>0: prios.append(f"Recuperar os {n_in} cliente(s) inativos ha mais de 90 dias. Risco de perda definitiva.")
    if n_q>0:  prios.append(f"Investigar queda nos {n_q} cliente(s). Entender mix e historico.")
    if not prios: prios.append("Manter frequencia de contato. Blindar os clientes em crescimento.")
    prios=prios[:3]
    prios_html="".join([f'<div class="prioridade-item"><div class="prioridade-num">{i+1}</div><div class="prioridade-texto">{p}</div></div>' for i,p in enumerate(prios)])

    st.markdown(f"""
    <div class="briefing-wrap" style="border-left-color:{sit_cor}">
        <div class="briefing-status">
            <span class="briefing-badge {sit_badge}">{sit_label}</span>
            <span class="briefing-titulo">Diagnostico — {htmllib.escape(contexto)} | {htmllib.escape(clabel)}</span>
        </div>
        <div class="briefing-texto">{" ".join(frases)}</div>
        <div class="briefing-prioridades">
            <div class="briefing-prioridades-titulo">Prioridades de acao</div>
            {prios_html}
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    missoes=[]
    if n_qa>0:
        val_risco=df_sel[df_sel['STATUS']=='QUEDA ACENTUADA']['MEDIA LP'].sum()
        missoes.append({'tipo':'critica','titulo':f'{n_qa} Cliente(s) em Queda Acentuada ({clabel})','contexto':f'Esses clientes tinham media mensal de R$ {fmt_br(val_risco)} e estao comprando mais de 10% abaixo do historico.','passos':[('Prepare-se antes de ligar','Abra o historico de cada cliente. Veja o que ele comprava e quanto valia por mes.'),('Entre em contato sem ofertar produto','O objetivo e entender, nao vender. O que mudou? O que parou de precisar?'),('Registre e agende o proximo passo','Anote o motivo e defina proxima acao com data.')],'key':'missao_qa'})
    if n_in>0:
        missoes.append({'tipo':'critica','titulo':f'{n_in} Cliente(s) Inativo(s) — Mais de 90 Dias','contexto':'Clientes que representavam receita relevante e nao compram ha mais de 3 meses.','passos':[('Revise o ultimo pedido','Qual foi o ultimo produto? Quando foi? Qual era o valor?'),('Faca contato de diagnostico sem pressao','Nao ligue para vender. Ligue para entender.'),('Defina o potencial de reconquista','Recuperavel, perdido ou a monitorar. Registre e agende.')],'key':'missao_in'})
    if n_q>0 and len(missoes)<3:
        missoes.append({'tipo':'urgente','titulo':f'{n_q} Cliente(s) em Queda','contexto':'Compras abaixo da media historica. Janela de intervencao aberta.','passos':[('Compare o mix atual com o historico','Quais produtos reduziram?'),('Contato de manutencao','Ha produto que ele compra de outro fornecedor?'),('Monitore o proximo mes','Se cair mais de 10%, escale para protocolo de queda acentuada.')],'key':'missao_q'})
    if not missoes:
        missoes.append({'tipo':'atencao','titulo':f'Manter e Expandir — {clabel}','contexto':f'Carteira em situacao saudavel com {idx_saude:.0f}% dos clientes em crescimento ou estaveis.','passos':[('Mantenha frequencia de contato','Clientes em crescimento sao os mais visados pela concorrencia.'),('Explore expansao de mix','Identifique categorias que o cliente nao compra.'),('Monitore mensalmente','Qualquer queda acima de 10% deve virar acao imediata.')],'key':'missao_ok'})

    card_cols = st.columns(len(missoes)) if len(missoes)>1 else [st.container()]
    for idx,(missao,col) in enumerate(zip(missoes,card_cols)):
        with col:
            tipo=missao['tipo']
            steps_html="".join([f'<div class="missao-step"><div class="step-num {tipo}">{si+1}</div><div class="step-content"><div class="step-titulo">{st_t}</div><div class="step-desc">{st_d}</div></div></div>' for si,(st_t,st_d) in enumerate(missao['passos'])])
            st.markdown(f"""<div class="missao-card {tipo}">
                <span class="missao-badge {tipo}">{tipo.upper()}</span>
                <div class="missao-titulo">{missao['titulo']}</div>
                <div class="missao-contexto">{missao['contexto']}</div>
                <div class="missao-steps">{steps_html}</div>
                <div class="missao-footer"><div class="missao-footer-titulo">Registrar proximo passo</div></div>
            </div>""", unsafe_allow_html=True)
            st.text_input("Proximo passo:", placeholder="Descreva a acao...", key=f"ps_{missao['key']}_{idx}", label_visibility="collapsed")
            st.date_input("Data:", value=date.today(), key=f"dt_{missao['key']}_{idx}", format="DD/MM/YYYY", label_visibility="collapsed")

    # ── CARDS KPI ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">VISAO GERAL DA CARTEIRA</div>', unsafe_allow_html=True)
    k1,k2,k3,k4=st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-wrap blue">
            <div class="kpi-lbl">COMPOSICAO DA CARTEIRA</div>
            <div class="kpi-val">{fmt_br(total)}</div>
            <div class="kpi-breakdown">
                <span style="color:{'#0056b3' if 'A' in sel_curvas else '#B0BAC9'}">A: {n_a_total}</span> |
                <span style="color:{'#0056b3' if 'B' in sel_curvas else '#B0BAC9'}">B: {n_b_total}</span> |
                <span style="color:{'#0056b3' if 'C' in sel_curvas else '#B0BAC9'}">C: {n_c_total}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-wrap blue">
            <div class="kpi-lbl">RECEITA {htmllib.escape(clabel)} &mdash; {ultimo_mes}</div>
            <div class="kpi-val">R$ {fmt_br(rec_ult)}</div>
            <div class="kpi-sub">vs {penultimo}: {var_html(var_rec)}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-wrap dark">
            <div class="kpi-lbl">META DO MES</div>
            <div class="kpi-val">R$ {fmt_br(meta_total)}</div>
            <div class="kpi-breakdown"><span>A: R$ {fmt_br(meta_a)}</span><br>
            <span>B: R$ {fmt_br(meta_b)}</span> | <span>C: R$ {fmt_br(meta_c)}</span></div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-wrap red">
            <div class="kpi-lbl">RECEITA EM RISCO &mdash; {htmllib.escape(clabel)}</div>
            <div class="kpi-val red">R$ {fmt_br(risco_val)}</div>
            <div class="kpi-sub">{n_risco} clientes em queda ou inativos</div>
        </div>""", unsafe_allow_html=True)

    # ── INDICADORES ────────────────────────────────────────────────────────────
    st.markdown(f'<div class="section-title">INDICADORES — {htmllib.escape(clabel)}</div>', unsafe_allow_html=True)
    i1,i2=st.columns(2)
    with i1:
        st.markdown(f"""<div class="ind-wrap">
            <div class="ind-lbl">TICKET MEDIO &mdash; {ultimo_mes}</div>
            <div class="ind-val">R$ {fmt_br(ticket_ult)}</div>
            <div class="ind-sub">vs {penultimo}: {var_html(var_ticket)}</div>
        </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(f"""<div class="ind-wrap">
            <div class="ind-lbl">INDICE DE SAUDE &mdash; {htmllib.escape(clabel)}</div>
            <div class="ind-val" style="color:{saude_color}">{idx_saude:.0f}%</div>
            <div class="ind-sub">{n_saudaveis} de {total} clientes em crescimento ou estaveis</div>
        </div>""", unsafe_allow_html=True)

    # ── ANALISE DETALHADA UNIFICADA ───────────────────────────────────────────
    # CORRECAO 1: tabela unificada com CLIENTES TOTAIS + COMPRARAM NO MES
    st.markdown(f'<div class="section-title">ANALISE DETALHADA — {htmllib.escape(clabel)}</div>', unsafe_allow_html=True)

    prev_fat    = None
    prev_ticket = None
    rows_unified = ""
    for i, mes in enumerate(last3):
        compraram = int((df_sel[mes] > 0).sum())
        fat = df_sel[mes].sum()
        tk  = fat / compraram if compraram > 0 else 0

        vf_html = var_html(None) if i==0 else var_html((fat-prev_fat)/prev_fat*100 if prev_fat and prev_fat>0 else None)
        vt_html = var_html(None) if i==0 else var_html((tk-prev_ticket)/prev_ticket*100 if prev_ticket and prev_ticket>0 else None)

        rows_unified += f"""<tr>
            <td><strong>{mes}</strong></td>
            <td>{total}</td>
            <td>{compraram}</td>
            <td>R$ {fmt_br(fat)}</td>
            <td>{vf_html}</td>
            <td>R$ {fmt_br(tk)}</td>
            <td>{vt_html}</td>
        </tr>"""
        prev_fat = fat; prev_ticket = tk

    st.markdown(f"""<div class="ana-wrap">
        <div class="ana-title">FATURAMENTO E TICKET MEDIO — {htmllib.escape(clabel)} — ULTIMOS 3 MESES</div>
        <table class="ana-table">
            <thead><tr>
                <th>MES</th>
                <th>CLIENTES TOTAIS</th>
                <th>COMPRARAM NO MES</th>
                <th>FATURAMENTO</th>
                <th>VAR. FAT.</th>
                <th>TICKET MEDIO</th>
                <th>VAR. TICKET</th>
            </tr></thead>
            <tbody>{rows_unified}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)

    # ── RECENCIA ──────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    l0=f"Comprou em {meses_col[-1]}"; l1=f"Ultimo pedido em {meses_col[-2]}" if len(meses_col)>1 else "Ha 1 mes"
    l2=f"Ultimo pedido em {meses_col[-3]}" if len(meses_col)>2 else "Ha 2 meses"
    l3p=f"Sem compra desde {meses_col[-4]} ou antes" if len(meses_col)>3 else "Ha 3+ meses"
    faixas_rec=[(l0,'<span class="rec-ativo">Ativo recente</span>',0),(l1,'<span class="rec-atencao">Atencao</span>',1),(l2,'<span class="rec-risco">Risco alto</span>',2),(l3p,'<span class="rec-critico">Inativo critico</span>',99)]
    rr=""
    for crit,badge,mr in faixas_rec:
        cnt=int((df_sel['MESES_SEM_COMPRA']>=3).sum()) if mr==99 else int((df_sel['MESES_SEM_COMPRA']==mr).sum())
        pct=cnt/total*100 if total>0 else 0
        rr+=f"<tr><td>{badge}</td><td style='text-align:left'>{crit}</td><td>{cnt}</td><td>{pct:.0f}%</td></tr>"
    st.markdown(f"""<div class="ana-wrap"><div class="ana-title">RECENCIA DE COMPRA &mdash; {htmllib.escape(clabel)}</div>
        <table class="ana-table"><thead><tr><th>CLASSIFICACAO</th><th style="text-align:left">CRITERIO</th><th>CLIENTES</th><th>%</th></tr></thead>
        <tbody>{rr}</tbody></table></div>""", unsafe_allow_html=True)

    # ── GRAFICOS ──────────────────────────────────────────────────────────────
    # CORRECAO 3: titulo dinamico + texto nao cortado
    st.markdown('<div class="section-title">DIAGNOSTICO DE CARTEIRA</div>', unsafe_allow_html=True)
    g1,g2=st.columns([3,2])
    with g1:
        sc=df_sel['STATUS'].value_counts(); lb=[s for s in STATUS_ORDER if s in sc.index]
        vl=[sc[s] for s in lb]; co=[STATUS_COLORS[s] for s in lb]; pc=[v/total*100 if total>0 else 0 for v in vl]
        fig1=go.Figure(go.Bar(
            x=vl, y=lb, orientation='h', marker_color=co,
            text=[f"  {v} ({p:.0f}%)" for v,p in zip(vl,pc)],
            textposition='outside',
            textfont=dict(size=12, family='Arial', color='#1A2540'),
            cliponaxis=False
        ))
        fig1.update_layout(
            margin=dict(l=0,r=160,t=10,b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(tickfont=dict(size=12,family='Arial',color='#1A2540'), autorange='reversed'),
            height=260, showlegend=False
        )
        titulo_grafico = f"DISTRIBUICAO POR STATUS &mdash; {htmllib.escape(clabel)}"
        st.markdown(f'<div class="chart-wrap"><div class="chart-lbl">{titulo_grafico}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        cc2=df_sel['CURVA'].value_counts(); cvl=['A','B','C']; cvv=[cc2.get(c,0) for c in cvl]
        fig2=go.Figure(go.Pie(labels=cvl,values=cvv,hole=0.58,marker=dict(colors=['#001845','#0056b3','#4A90C4'],line=dict(color='#FFFFFF',width=2)),textinfo='label+percent',textfont=dict(size=13,family='Arial',color=['#FFFFFF','#FFFFFF','#1A2540']),insidetextorientation='radial'))
        fig2.update_layout(margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor='rgba(0,0,0,0)',height=260,showlegend=False)
        st.markdown('<div class="chart-wrap"><div class="chart-lbl">DISTRIBUICAO POR CURVA ABC</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2,use_container_width=True,config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── PERFORMANCE POR VENDEDOR ──────────────────────────────────────────────
    # CORRECAO 2: nova estrutura + labels dinamicos + linha TOTAL GERAL
    if sel_vend=="Todos":
        st.markdown('<div class="section-title">PERFORMANCE POR VENDEDOR</div>', unsafe_allow_html=True)

        rv = []
        for v in sorted(df_sel[vend_col].dropna().astype(str).unique()):
            dv_todos = df[df[vend_col].astype(str)==v]
            dv_sel   = df_sel[df_sel[vend_col].astype(str)==v]
            rv.append({
                'VENDEDOR':          v,
                'CLIENTES TOTAL':    len(dv_todos),
                f'CLIENTES {cshort}': len(dv_sel),
                f'RECEITA {cshort}':  dv_sel['TOTAL LP'].sum(),
                f'QDA. ACENTUADA {cshort}': len(dv_sel[dv_sel['STATUS']=='QUEDA ACENTUADA']),
                f'QUEDA {cshort}':    len(dv_sel[dv_sel['STATUS']=='QUEDA']),
                f'CRESCIMENTO {cshort}': len(dv_sel[dv_sel['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO'])]),
                f'INATIVOS {cshort}': len(dv_sel[dv_sel['STATUS']=='INATIVO']),
            })

        cv2 = list(rv[0].keys())
        receita_col = f'RECEITA {cshort}'

        # Linha de total geral
        total_row = {'VENDEDOR': 'TOTAL GERAL'}
        for k in cv2:
            if k != 'VENDEDOR':
                total_row[k] = sum(r[k] for r in rv)

        # Render header
        hh = "".join([f"<th>{c}</th>" for c in cv2])

        # Render linhas de vendedor
        rh = ""
        for r in rv:
            rh += "<tr>"
            for k in cv2:
                v_val = r[k]
                if k == 'VENDEDOR':
                    rh += f"<td class='left'>{htmllib.escape(str(v_val))}</td>"
                elif k == receita_col:
                    rh += f"<td>R$ {fmt_br(v_val)}</td>"
                else:
                    rh += f"<td>{v_val}</td>"
            rh += "</tr>"

        # Render linha TOTAL GERAL
        rh += "<tr class='total-row'>"
        for k in cv2:
            v_val = total_row[k]
            if k == 'VENDEDOR':
                rh += f"<td class='left'>{v_val}</td>"
            elif k == receita_col:
                rh += f"<td>R$ {fmt_br(v_val)}</td>"
            else:
                rh += f"<td>{v_val}</td>"
        rh += "</tr>"

        st.markdown(f"""<div class="vend-wrap">
            <table class="vend-table"><thead><tr>{hh}</tr></thead><tbody>{rh}</tbody></table>
        </div>""", unsafe_allow_html=True)

    # ── CARTEIRA DE CLIENTES ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">CARTEIRA DE CLIENTES</div>', unsafe_allow_html=True)
    cd=['CURVA',clie_col,vend_col]+extra+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META']
    dd=df_sel[cd].copy().reset_index(drop=True)
    hc="".join([f"<th>{c}</th>" for c in cd]); rc=""
    for _,row in dd.iterrows():
        cells=""
        for cn in cd:
            v=row[cn]; ac=' class="left"' if cn==clie_col else ''
            if cn=='STATUS': s=str(v); css=STATUS_CSS.get(s,''); cells+=f'<td><span style="{css}">{s}</span></td>'
            elif cn in('TOTAL LP','MEDIA LP','MEDIA CP','META'): cells+=f'<td{ac}>{fmt_br(v)}</td>'
            else: cells+=f'<td{ac}>{htmllib.escape(str(v))}</td>'
        rc+=f"<tr>{cells}</tr>"
    st.markdown(f"""<div class="cart-wrap"><table class="cart-table"><thead><tr>{hc}</tr></thead><tbody>{rc}</tbody></table></div>""", unsafe_allow_html=True)
