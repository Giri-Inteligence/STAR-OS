import streamlit as st
import pandas as pd
import html as htmllib
from io import BytesIO
import xlsxwriter
import plotly.graph_objects as go
import streamlit.components.v1 as components
from datetime import date

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as rlc
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

st.set_page_config(page_title="Giri | STAR", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background:#EDF1F7; }
[data-testid="stHeader"] { background:transparent; }
.giri-header { background:linear-gradient(120deg,#001233 0%,#003087 55%,#0056b3 100%); border-radius:18px; padding:30px 38px; margin-bottom:28px; box-shadow:0 10px 40px rgba(0,18,51,0.32); display:flex; align-items:center; gap:18px; }
.giri-header-dot { width:48px; height:48px; background:rgba(255,255,255,0.15); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
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
.ana-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:10px; text-align:center; font-size:0.70rem; text-transform:uppercase; letter-spacing:0.6px; white-space:normal; line-height:1.4; vertical-align:middle; }
.ana-table td { padding:10px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; font-size:0.85rem; vertical-align:middle; }
.ana-table td.left { text-align:left; }
.ana-table tr:last-child td { border-bottom:none; }
.ana-table tr:hover td { background:#F5F7FB; }
.rec-ativo   { background:#C6EFCE; color:#375623; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-atencao { background:#FFEB9C; color:#7A4F00; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-risco   { background:#FFC7CE; color:#7A0000; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.rec-critico { background:#C00000; color:#FFFFFF; font-weight:700; border-radius:6px; padding:3px 10px; font-size:0.82rem; }
.vend-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.vend-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:10px; text-align:center; letter-spacing:0.6px; font-size:0.70rem; text-transform:uppercase; white-space:normal; line-height:1.4; vertical-align:middle; }
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

/* BAR CHART */
.hbc { background:#FFFFFF; border-radius:14px; padding:20px 22px; box-shadow:0 2px 18px rgba(0,0,0,0.07); }
.hbc-title { font-size:0.85rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#1A2540; text-align:center; margin-bottom:16px; }
.hbc-row { display:flex; align-items:center; gap:10px; padding:6px 6px; border-radius:6px; border-left:3px solid transparent; margin-bottom:3px; }
.hbc-lbl { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; color:#1A2540; width:155px; flex-shrink:0; text-align:right; padding-right:6px; }
.hbc-track { flex:1; height:18px; background:#EDF1F7; border-radius:4px; overflow:hidden; min-width:50px; }
.hbc-fill { height:100%; border-radius:4px; }
.hbc-cnt { font-size:10px; font-weight:700; color:#4B5568; width:72px; flex-shrink:0; text-align:left; padding-left:6px; white-space:nowrap; }

/* BOTOES DOWNLOAD */
[data-testid="stMarkdownContainer"]:has(.dlg) ~ [data-testid="stDownloadButton"] button {
    background:linear-gradient(135deg,#1A5C2A 0%,#2E8B47 100%) !important;
    color:#FFFFFF !important; border:none !important; border-radius:12px !important;
    height:46px !important; font-size:0.82rem !important; font-weight:800 !important;
    letter-spacing:0.8px !important; width:100% !important; white-space:nowrap !important;
    box-shadow:0 4px 16px rgba(26,92,42,0.35) !important; opacity:1 !important;
}
[data-testid="stMarkdownContainer"]:has(.dlg) ~ [data-testid="stDownloadButton"] button:hover {
    filter:brightness(0.86) !important; opacity:1 !important;
}
[data-testid="stMarkdownContainer"]:has(.dlb) ~ [data-testid="stDownloadButton"] button {
    background:linear-gradient(135deg,#001845 0%,#003087 50%,#0056b3 100%) !important;
    color:#FFFFFF !important; border:none !important; border-radius:12px !important;
    height:46px !important; font-size:0.82rem !important; font-weight:800 !important;
    letter-spacing:0.8px !important; width:100% !important; white-space:nowrap !important;
    box-shadow:0 4px 16px rgba(0,18,51,0.35) !important; opacity:1 !important;
}
[data-testid="stMarkdownContainer"]:has(.dlb) ~ [data-testid="stDownloadButton"] button:hover {
    filter:brightness(0.86) !important; opacity:1 !important;
}

/* COMPRESSOR ESPACAMENTO BOTOES G2 */
[data-testid="stMarkdownContainer"]:has(span[id^="sa_"]) {
    height:0 !important; overflow:hidden !important;
    margin:0 !important; padding:0 !important; min-height:0 !important;
}
[data-testid="stMarkdownContainer"]:has(span[id^="sa_"]) + [data-testid="stButton"] {
    margin:0 0 2px 0 !important; padding:0 !important;
}
</style>
""", unsafe_allow_html=True)

STATUS_ORDER   = ['CRESCIMENTO ACENTUADO','CRESCIMENTO','ESTAVEL','QUEDA','QUEDA ACENTUADA','INATIVO']
STATUS_BTN_COR = {'CRESCIMENTO ACENTUADO':'#1A6B2A','CRESCIMENTO':'#2E8B57','ESTAVEL':'#0056b3','QUEDA':'#D44000','QUEDA ACENTUADA':'#C00000','INATIVO':'#6B7280'}
STATUS_CSS     = {
    'QUEDA ACENTUADA':       'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 8px;',
    'QUEDA':                 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 8px;',
    'CRESCIMENTO':           'color:#375623;font-weight:700;',
    'ESTAVEL':               'color:#0070C0;font-weight:700;',
    'INATIVO':               'color:#6B7280;font-weight:700;',
}

if 'status_filtro' not in st.session_state:
    st.session_state.status_filtro = None
if 'scroll_needed' not in st.session_state:
    st.session_state.scroll_needed = False


def fmt_br(v):
    try: return f"{int(v):,}".replace(",", ".")
    except: return "0"

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
    txt_ina  = "OBJETIVO: Diagnostico de causa\nPRE-CONTATO: Revisar ultimo pedido.\nCONTATO: Contato de diagnostico sem pressao.\nORIENTACAO: Nao ofertar produto na primeira interacao."
    txt_q_ac = "OBJETIVO: Recuperacao emergencial\nPRE-CONTATO: Revisar historico completo.\nCONTATO: Priorizar visita ou ligacao direta.\nORIENTACAO: Objetivo e entender, nao vender."
    txt_q    = "OBJETIVO: Estabilizacao\nPRE-CONTATO: Revisar historico de mix.\nCONTATO: Diagnosticar contexto atual.\nORIENTACAO: Registrar causa e propor recomposicao de mix."
    txt_est  = "OBJETIVO: Blindagem e crescimento incremental\nPRE-CONTATO: Revisar mix. Mapear categorias nao compradas.\nCONTATO: Manter frequencia. Explorar expansao.\nORIENTACAO: Cliente estavel nao e cliente seguro."
    txt_cre  = "OBJETIVO: Consolidacao\nPRE-CONTATO: Identificar driver do crescimento.\nCONTATO: Reforcar relacionamento.\nORIENTACAO: Proteger o cliente."
    txt_ca   = "OBJETIVO: Consolidacao e protecao\nPRE-CONTATO: Identificar produtos que puxaram crescimento.\nCONTATO: Reforcar presenca.\nORIENTACAO: Crescimento acentuado atrai concorrencia."
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
        if len(vl) == 1: r[vl[0]] = f[:31]
        else:
            for v in vl:
                p = str(v).strip().split()
                r[v] = (f + " " + (p[1][0] if len(p) > 1 else str(v)[-1]))[:31]
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
    sf2 = {'QUEDA ACENTUADA':fmts['qa'],'QUEDA':fmts['q'],'CRESCIMENTO ACENTUADO':fmts['ca'],'CRESCIMENTO':fmts['c'],'ESTAVEL':fmts['e'],'INATIVO':fmts['i']}
    for i,col in enumerate(fo):
        ws.write(0,i,col,fmts['hdr']); ws.set_column(i,i,larg.get(col,8))
    for ri,row in df.iterrows():
        xl = ri+1
        for ci,cn in enumerate(fo):
            v = row[cn]
            if cn=='STATUS': ws.write_string(xl,ci,str(v),sf2.get(str(v),fmts['txt']))
            elif cn=='TOTAL LP': ws.write_number(xl,ci,int(v),fmts['total'])
            elif cn in('MEDIA LP','MEDIA CP','META') or cn in mc: ws.write_number(xl,ci,int(v),fmts['num'])
            else: ws.write_string(xl,ci,str(v),fmts['txt'])

def gerar_excel(df_raw,fo,cc,vc,mc):
    buf = BytesIO()
    vends = sorted(df_raw[vc].dropna().astype(str).unique().tolist())
    tn = get_tab_names(vends)
    with pd.ExcelWriter(buf,engine='xlsxwriter') as w:
        wb = w.book; fmts = get_excel_formats(wb)
        df_raw[fo].to_excel(w,index=False,sheet_name='GERAL')
        write_sheet(w.sheets['GERAL'],df_raw.reset_index(drop=True),fo,cc,vc,mc,fmts)
        for vend in vends:
            dv = df_raw[df_raw[vc].astype(str)==vend].reset_index(drop=True)
            tab = tn[vend]; dv[fo].to_excel(w,index=False,sheet_name=tab)
            write_sheet(w.sheets[tab],dv,fo,cc,vc,mc,fmts)
    return buf.getvalue()


def gerar_pdf(df_sel,df_full,col_config,filters,metrics):
    if not REPORTLAB_OK: return None
    buf = BytesIO()
    clie_col=col_config['clie']; vend_col=col_config['vend']; meses_col=col_config['meses']
    last3=col_config['last3']; ultimo=col_config['ultimo']; penultimo=col_config['penultimo']; extra=col_config['extra']
    clabel=filters['clabel']; cshort=filters['cshort']; contexto=filters['contexto']; sel_vend=filters['vend']
    total=metrics['total']; n_a=metrics['n_a']; n_b=metrics['n_b']; n_c=metrics['n_c']
    rec_ult=metrics['rec_ult']; var_rec=metrics['var_rec']; meta_total=metrics['meta_total']
    risco_val=metrics['risco_val']; n_risco=metrics['n_risco']; ticket_ult=metrics['ticket_ult']
    buyers_ult=metrics['buyers_ult']; idx_saude=metrics['idx_saude']; n_saud=metrics['n_saudaveis']
    today_str=date.today().strftime('%d/%m/%Y')
    PAGE_W,PAGE_H=A4; MARGIN=2.0*cm; CW=PAGE_W-2*MARGIN
    NAVY=rlc.Color(0/255,18/255,51/255); BLUE=rlc.Color(0/255,86/255,179/255)
    RED=rlc.Color(192/255,0/255,0/255); GRN=rlc.Color(26/255,107/255,42/255)
    GRN2=rlc.Color(46/255,139/255,87/255); ORG=rlc.Color(212/255,64/255,0/255)
    GRAY=rlc.Color(75/255,85/255,104/255); LGRAY=rlc.Color(237/255,241/255,247/255)
    LGRAY2=rlc.Color(248/255,249/255,252/255); W=rlc.white
    SC_MAP={'QUEDA ACENTUADA':RED,'QUEDA':ORG,'CRESCIMENTO ACENTUADO':GRN,'CRESCIMENTO':GRN2,'ESTAVEL':BLUE,'INATIVO':GRAY}

    def ps(name,**kw):
        d=dict(fontName='Helvetica',fontSize=9,textColor=rlc.Color(26/255,37/255,64/255),leading=13,spaceAfter=0)
        d.update(kw); return ParagraphStyle(name,**d)

    S={'ct':ps('ct',fontName='Helvetica-Bold',fontSize=22,textColor=W,alignment=TA_CENTER,leading=28),
       'cs':ps('cs',fontSize=11,textColor=rlc.Color(0.72,0.80,0.95),alignment=TA_CENTER,leading=16),
       'cf':ps('cf',fontName='Helvetica-Bold',fontSize=10,textColor=rlc.Color(0.80,0.86,0.96),alignment=TA_CENTER,leading=14),
       'cd':ps('cd',fontSize=8,textColor=rlc.Color(0.60,0.70,0.85),alignment=TA_CENTER),
       'h2':ps('h2',fontName='Helvetica-Bold',fontSize=13,textColor=NAVY,spaceBefore=14,spaceAfter=6),
       'kl':ps('kl',fontName='Helvetica-Bold',fontSize=7,textColor=GRAY,alignment=TA_CENTER,leading=10),
       'kv':ps('kv',fontName='Helvetica-Bold',fontSize=15,textColor=NAVY,alignment=TA_CENTER,leading=20),
       'ks':ps('ks',fontSize=7,textColor=GRAY,alignment=TA_CENTER,leading=10),
       'th':ps('th',fontName='Helvetica-Bold',fontSize=8,textColor=W,alignment=TA_CENTER,leading=10),
       'td':ps('td',fontSize=8,alignment=TA_CENTER,leading=10),
       'tdl':ps('tdl',fontSize=8,alignment=TA_LEFT,leading=10),
       'tdls':ps('tdls',fontSize=7,alignment=TA_LEFT,leading=9),
       'tds':ps('tds',fontSize=7,alignment=TA_CENTER,leading=9)}

    def hr_line():
        return Table([['']],colWidths=[CW],rowHeights=[2],
            style=TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))

    def kpi_box(lbl,val,sub=''):
        data=[[Paragraph(lbl,S['kl'])],[Paragraph(val,S['kv'])],[Paragraph(sub,S['ks']) if sub else Spacer(1,0)]]
        return Table(data,colWidths=[CW/4-0.15*cm],rowHeights=[0.6*cm,1.0*cm,0.5*cm],
            style=TableStyle([('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),4),
                              ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))

    story=[]
    capa=Table([[Paragraph('GIRI',S['ct'])],[Spacer(1,0.3*cm)],
        [Paragraph('SISTEMA DE GOVERNANCA STAR',S['cs'])],[Spacer(1,0.5*cm)],
        [Paragraph('RELATORIO DE CARTEIRA COMERCIAL',S['cs'])],[Spacer(1,1.5*cm)],
        [Paragraph(f'Contexto: {contexto}',S['cf'])],[Paragraph(f'Selecao: {clabel}',S['cf'])],
        [Spacer(1,0.6*cm)],[Paragraph(f'Gerado em {today_str}',S['cd'])]],colWidths=[CW])
    capa.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
        ('TOPPADDING',(0,0),(0,0),3.5*cm),('BOTTOMPADDING',(0,-1),(-1,-1),3.5*cm),
        ('LEFTPADDING',(0,0),(-1,-1),1.5*cm),('RIGHTPADDING',(0,0),(-1,-1),1.5*cm)]))
    story.append(capa); story.append(PageBreak())

    story.append(Paragraph('VISAO EXECUTIVA',S['h2'])); story.append(hr_line()); story.append(Spacer(1,0.3*cm))
    var_txt=f"+{var_rec:.1f}%" if var_rec>=0 else f"{var_rec:.1f}%"
    kpi_row=[[kpi_box('CLIENTES NA SELECAO',str(total),f'A:{n_a}  B:{n_b}  C:{n_c}'),
              kpi_box(f'RECEITA {clabel[:12]}',f'R$ {fmt_br(rec_ult)}',f'vs {penultimo}: {var_txt}'),
              kpi_box('META DO MES',f'R$ {fmt_br(meta_total)}',''),
              kpi_box('RECEITA EM RISCO',f'R$ {fmt_br(risco_val)}',f'{n_risco} clientes em queda')]]
    kpi_t=Table(kpi_row,colWidths=[CW/4]*4,rowHeights=[2.4*cm])
    kpi_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRAY2),
        ('LINEABOVE',(0,0),(0,0),3,BLUE),('LINEABOVE',(1,0),(1,0),3,BLUE),
        ('LINEABOVE',(2,0),(2,0),3,NAVY),('LINEABOVE',(3,0),(3,0),3,RED),
        ('BOX',(0,0),(0,0),0.5,BLUE),('BOX',(1,0),(1,0),0.5,BLUE),
        ('BOX',(2,0),(2,0),0.5,NAVY),('BOX',(3,0),(3,0),0.5,RED),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    story.append(kpi_t); story.append(Spacer(1,0.3*cm))

    saude_col=GRN if idx_saude>=70 else (rlc.Color(0.69,0.49,0) if idx_saude>=50 else RED)
    ind_row=[[
        Table([[Paragraph('TICKET MEDIO — COMPRADORES ATIVOS',S['kl'])],
               [Paragraph(f'R$ {fmt_br(ticket_ult)}',S['kv'])],
               [Paragraph(f'{buyers_ult} clientes compraram em {ultimo}',S['ks'])]],
              colWidths=[CW/2-0.1*cm],
              style=TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRAY2),('LINEABOVE',(0,0),(-1,0),3,BLUE),
                                ('BOX',(0,0),(-1,-1),0.5,BLUE),('TOPPADDING',(0,0),(-1,-1),8),
                                ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)])),
        Table([[Paragraph(f'INDICE DE SAUDE — {clabel[:14]}',S['kl'])],
               [Paragraph(f'{idx_saude:.0f}%',ps('sv',fontName='Helvetica-Bold',fontSize=15,textColor=saude_col,alignment=TA_CENTER,leading=20))],
               [Paragraph(f'{n_saud} de {total} clientes saudaveis',S['ks'])]],
              colWidths=[CW/2-0.1*cm],
              style=TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRAY2),('LINEABOVE',(0,0),(-1,0),3,BLUE),
                                ('BOX',(0,0),(-1,-1),0.5,BLUE),('TOPPADDING',(0,0),(-1,-1),8),
                                ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)])),
    ]]
    ind_t=Table(ind_row,colWidths=[CW/2,CW/2],rowHeights=[2.0*cm])
    ind_t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
                               ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)]))
    story.append(ind_t); story.append(Spacer(1,0.5*cm))

    story.append(Paragraph('DISTRIBUICAO POR STATUS',S['h2'])); story.append(hr_line()); story.append(Spacer(1,0.2*cm))
    sc_pdf=df_sel['STATUS'].value_counts()
    st_data=[[Paragraph('STATUS',S['th']),Paragraph('CLIENTES',S['th']),Paragraph('%',S['th']),Paragraph('VOLUME MEDIO (R$)',S['th'])]]
    for stat in STATUS_ORDER:
        if stat in sc_pdf.index:
            cnt=sc_pdf[stat]; pct=cnt/total*100 if total>0 else 0
            vol=df_sel[df_sel['STATUS']==stat]['MEDIA LP'].sum(); sc3=SC_MAP.get(stat,GRAY)
            st_data.append([Paragraph(stat,ps(f'sp{stat}',fontName='Helvetica-Bold',fontSize=8,textColor=sc3,alignment=TA_LEFT,leading=10)),
                Paragraph(str(cnt),S['td']),Paragraph(f'{pct:.0f}%',S['td']),Paragraph(f'R$ {fmt_br(vol)}',S['td'])])
    st_t=Table(st_data,colWidths=[CW*0.45,CW*0.15,CW*0.15,CW*0.25])
    st_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[W,LGRAY2]),
        ('GRID',(0,0),(-1,-1),0.3,rlc.Color(0.85,0.87,0.90)),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
    story.append(st_t); story.append(Spacer(1,0.4*cm))

    story.append(Paragraph('RECENCIA DE COMPRA',S['h2'])); story.append(hr_line()); story.append(Spacer(1,0.2*cm))
    l0=f"Comprou em {meses_col[-1]}"; l1=f"Ultimo pedido em {meses_col[-2]}" if len(meses_col)>1 else "Ha 1 mes"
    l2=f"Ultimo pedido em {meses_col[-3]}" if len(meses_col)>2 else "Ha 2 meses"
    l3p=f"Sem compra desde {meses_col[-4]} ou antes" if len(meses_col)>3 else "Ha 3+ meses"
    rec_data=[[Paragraph('CLASSIFICACAO',S['th']),Paragraph('CRITERIO',S['th']),Paragraph('CLIENTES',S['th']),Paragraph('%',S['th'])]]
    for crit,badge,cor,mr in [(l0,'Ativo recente',GRN2,0),(l1,'Atencao',rlc.Color(0.7,0.5,0),1),(l2,'Risco alto',ORG,2),(l3p,'Inativo critico',RED,99)]:
        cnt=int((df_sel['MESES_SEM_COMPRA']>=3).sum()) if mr==99 else int((df_sel['MESES_SEM_COMPRA']==mr).sum())
        pct=cnt/total*100 if total>0 else 0
        rec_data.append([Paragraph(badge,ps(f'rp{mr}',fontName='Helvetica-Bold',fontSize=8,textColor=cor,alignment=TA_CENTER,leading=10)),
            Paragraph(crit,S['tdl']),Paragraph(str(cnt),S['td']),Paragraph(f'{pct:.0f}%',S['td'])])
    rec_t=Table(rec_data,colWidths=[CW*0.20,CW*0.50,CW*0.15,CW*0.15])
    rec_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[W,LGRAY2]),
        ('GRID',(0,0),(-1,-1),0.3,rlc.Color(0.85,0.87,0.90)),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
    story.append(rec_t); story.append(Spacer(1,0.4*cm))

    story.append(Paragraph('ANALISE DETALHADA — ULTIMOS 3 MESES',S['h2'])); story.append(hr_line()); story.append(Spacer(1,0.2*cm))
    ana_data=[[Paragraph('MES',S['th']),Paragraph('CLIENTES TOTAIS',S['th']),Paragraph('COMPRARAM',S['th']),
        Paragraph('FATURAMENTO (R$)',S['th']),Paragraph('VAR. FAT.',S['th']),
        Paragraph('TICKET MEDIO (R$)',S['th']),Paragraph('VAR. TICKET',S['th'])]]
    pf2=None; pt2=None
    for i,mes in enumerate(last3):
        comp=int((df_sel[mes]>0).sum()); fat=df_sel[mes].sum(); tk=fat/comp if comp>0 else 0
        vf=None if i==0 else ((fat-pf2)/pf2*100 if pf2 and pf2>0 else None)
        vt=None if i==0 else ((tk-pt2)/pt2*100 if pt2 and pt2>0 else None)
        def vs(v): return '--' if v is None else (f'+{v:.1f}%' if v>=0 else f'{v:.1f}%')
        def vc2(v): return GRAY if v is None else (GRN if v>=0 else RED)
        ana_data.append([Paragraph(f'<b>{mes}</b>',S['td']),Paragraph(str(total),S['td']),
            Paragraph(str(comp),S['td']),Paragraph(f'R$ {fmt_br(fat)}',S['td']),
            Paragraph(vs(vf),ps(f'vf{i}',fontName='Helvetica-Bold',fontSize=8,textColor=vc2(vf),alignment=TA_CENTER,leading=10)),
            Paragraph(f'R$ {fmt_br(tk)}',S['td']),
            Paragraph(vs(vt),ps(f'vt{i}',fontName='Helvetica-Bold',fontSize=8,textColor=vc2(vt),alignment=TA_CENTER,leading=10))])
        pf2=fat; pt2=tk
    ana_t=Table(ana_data,colWidths=[CW*0.10,CW*0.14,CW*0.11,CW*0.18,CW*0.12,CW*0.18,CW*0.17])
    ana_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[W,LGRAY2]),
        ('GRID',(0,0),(-1,-1),0.3,rlc.Color(0.85,0.87,0.90)),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
    story.append(ana_t); story.append(PageBreak())

    story.append(Paragraph(f'CARTEIRA DE CLIENTES — {clabel}',S['h2'])); story.append(hr_line()); story.append(Spacer(1,0.2*cm))
    cd_pdf=['CURVA',clie_col,vend_col]+extra+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META']
    hdrs=['CRV','CLIENTE','VENDEDOR']+[c[:6] for c in extra]+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META']
    cart_data=[[Paragraph(h,S['th']) for h in hdrs]]
    for _,row in df_sel[cd_pdf].iterrows():
        row_data=[]
        for cn in cd_pdf:
            v=row[cn]
            if cn=='STATUS':
                sc4=SC_MAP.get(str(v),GRAY)
                row_data.append(Paragraph(str(v),ps(f'sp2{v}',fontName='Helvetica-Bold',fontSize=7,textColor=sc4,alignment=TA_CENTER,leading=9)))
            elif cn in('TOTAL LP','MEDIA LP','MEDIA CP','META'): row_data.append(Paragraph(fmt_br(v),S['tds']))
            elif cn==clie_col: row_data.append(Paragraph(str(v)[:32],S['tdls']))
            else: row_data.append(Paragraph(str(v)[:14],S['tds']))
        cart_data.append(row_data)
    n_e=len(extra)
    cw2=[CW*0.04,CW*0.24,CW*0.12,CW*0.10,CW*0.09,CW*0.09,CW*0.18,CW*0.08] if n_e==0 \
        else [CW*0.04,CW*0.20,CW*0.11,CW*0.08,CW*0.10,CW*0.09,CW*0.09,CW*0.18,CW*0.07]
    tw=sum(cw2); cw2=[w*CW/tw for w in cw2]
    cart_t=Table(cart_data,colWidths=cw2,repeatRows=1)
    cart_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[W,LGRAY2]),
        ('GRID',(0,0),(-1,-1),0.3,rlc.Color(0.85,0.87,0.90)),('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]))
    story.append(cart_t)

    if sel_vend=="Todos":
        story.append(PageBreak()); story.append(Paragraph('PERFORMANCE POR VENDEDOR',S['h2']))
        story.append(hr_line()); story.append(Spacer(1,0.2*cm))
        vh=['VENDEDOR','TOTAL','SEL.','RECEITA','QDA. ACENT.','QUEDA','CRESC.','INATIVOS']
        vd=[[Paragraph(h,S['th']) for h in vh]]
        for v in sorted(df_sel[vend_col].dropna().astype(str).unique()):
            dt=df_full[df_full[vend_col].astype(str)==v]; ds=df_sel[df_sel[vend_col].astype(str)==v]
            vd.append([Paragraph(str(v)[:22],S['tdl']),Paragraph(str(len(dt)),S['td']),Paragraph(str(len(ds)),S['td']),
                Paragraph(f"R$ {fmt_br(ds['TOTAL LP'].sum())}",S['td']),
                Paragraph(str(len(ds[ds['STATUS']=='QUEDA ACENTUADA'])),ps('qa3',fontName='Helvetica-Bold',fontSize=8,textColor=RED,alignment=TA_CENTER,leading=10)),
                Paragraph(str(len(ds[ds['STATUS']=='QUEDA'])),ps('q3',fontName='Helvetica-Bold',fontSize=8,textColor=ORG,alignment=TA_CENTER,leading=10)),
                Paragraph(str(len(ds[ds['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO'])])),ps('c3',fontName='Helvetica-Bold',fontSize=8,textColor=GRN,alignment=TA_CENTER,leading=10)),
                Paragraph(str(len(ds[ds['STATUS']=='INATIVO'])),ps('i3',fontName='Helvetica-Bold',fontSize=8,textColor=GRAY,alignment=TA_CENTER,leading=10))])
        vd.append([Paragraph('TOTAL GERAL',ps('tg',fontName='Helvetica-Bold',fontSize=8,textColor=NAVY,alignment=TA_LEFT,leading=10)),
            Paragraph(str(len(df_full)),S['td']),Paragraph(str(total),S['td']),
            Paragraph(f"R$ {fmt_br(df_sel['TOTAL LP'].sum())}",S['td']),
            Paragraph(str(len(df_sel[df_sel['STATUS']=='QUEDA ACENTUADA'])),ps('qa4',fontName='Helvetica-Bold',fontSize=8,textColor=RED,alignment=TA_CENTER,leading=10)),
            Paragraph(str(len(df_sel[df_sel['STATUS']=='QUEDA'])),ps('q4',fontName='Helvetica-Bold',fontSize=8,textColor=ORG,alignment=TA_CENTER,leading=10)),
            Paragraph(str(len(df_sel[df_sel['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO'])])),ps('c4',fontName='Helvetica-Bold',fontSize=8,textColor=GRN,alignment=TA_CENTER,leading=10)),
            Paragraph(str(len(df_sel[df_sel['STATUS']=='INATIVO'])),ps('i4',fontName='Helvetica-Bold',fontSize=8,textColor=GRAY,alignment=TA_CENTER,leading=10))])
        vw=[CW*0.22,CW*0.07,CW*0.07,CW*0.20,CW*0.11,CW*0.09,CW*0.09,CW*0.10]
        vt2=Table(vd,colWidths=vw,repeatRows=1)
        vt2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-2),[W,LGRAY2]),
            ('BACKGROUND',(0,-1),(-1,-1),LGRAY),('LINEABOVE',(0,-1),(-1,-1),1.5,NAVY),
            ('GRID',(0,0),(-1,-1),0.3,rlc.Color(0.85,0.87,0.90)),('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
        story.append(vt2)

    def footer(canvas,doc):
        canvas.saveState(); canvas.setFont('Helvetica',7); canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN,1.2*cm,f'GIRI | Sistema de Governanca STAR  |  {clabel}  |  {today_str}')
        canvas.drawRightString(PAGE_W-MARGIN,1.2*cm,f'Pagina {doc.page}'); canvas.restoreState()

    SimpleDocTemplate(buf,pagesize=A4,topMargin=2*cm,bottomMargin=2*cm,
        leftMargin=MARGIN,rightMargin=MARGIN).build(story,onFirstPage=footer,onLaterPages=footer)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
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
                dt = pd.read_excel(file,header=h,nrows=3)
                if any(any(m in str(c).upper() for m in kw) for c in dt.columns): return h
            except: pass
        return 0

    fn = uploaded_file.name
    if fn.endswith('xlsx'):
        hr = detectar_header(uploaded_file); uploaded_file.seek(0)
        df_raw = pd.read_excel(uploaded_file,header=hr)
    else:
        df_raw = pd.read_csv(uploaded_file,sep=None,engine='python')

    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [c for c in cols if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))]
    clie_col  = next((c for c in cols if any(x in c for x in ("CLIENTE","NOME","RAZAO"))), cols[0])
    vend_col  = next((c for c in cols if any(x in c for x in ("VENDEDOR","REP"))), cols[1] if len(cols)>1 else cols[0])
    cida_col  = next((c for c in cols if any(x in c for x in ("CIDADE","MUNICIPIO","LOCALIDADE","REGIAO"))), None)

    for c in meses_col:
        df_raw[c] = pd.to_numeric(df_raw[c],errors='coerce').fillna(0)
    df_raw = df_raw.dropna(subset=meses_col,how='all').reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].notna()].reset_index(drop=True)
    df_raw = df_raw[df_raw[clie_col].astype(str).str.strip()!=''].reset_index(drop=True)

    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MEDIA LP'] = df_raw[meses_col].mean(axis=1).astype(int)
    df_raw['MEDIA CP'] = df_raw[meses_col[-3:]].mean(axis=1).astype(int)

    import re
    curva_detectada = False
    if 'CURVA' in cols:
        vals = df_raw['CURVA'].astype(str).str.upper().str.strip()
        if vals.isin(['A','B','C']).sum()>0:
            df_raw['CURVA'] = vals.where(vals.isin(['A','B','C']),other=pd.NA).ffill().fillna('C')
            curva_detectada = True
    if not curva_detectada:
        for col in cols:
            col_vals = df_raw[col].astype(str).str.upper().str.strip()
            if col_vals.str.match(r'^CURVA\s*[ABC]$').any():
                cs2 = col_vals.where(col_vals.str.match(r'^CURVA\s*[ABC]$'),other=pd.NA).ffill()
                df_raw['CURVA'] = cs2.str.replace(r'^CURVA\s*','',regex=True).str.strip()
                df_raw['CURVA'] = df_raw['CURVA'].where(df_raw['CURVA'].isin(['A','B','C']),'C')
                curva_detectada = True; break
    if not curva_detectada:
        df_raw = df_raw.sort_values('TOTAL LP',ascending=False).reset_index(drop=True)
        cp2 = df_raw['TOTAL LP'].cumsum()/df_raw['TOTAL LP'].sum()
        df_raw['CURVA'] = cp2.apply(lambda x: 'A' if x<=0.80 else ('B' if x<=0.95 else 'C'))
    else:
        df_raw = df_raw.sort_values('TOTAL LP',ascending=False).reset_index(drop=True)

    res = df_raw.apply(lambda r: engine_star(r['MEDIA LP'],r['MEDIA CP']),axis=1)
    df_raw['STATUS'],df_raw['META'],df_raw['ACAO'] = zip(*res)

    def calc_rec(row):
        for i in range(len(meses_col)-1,-1,-1):
            if row[meses_col[i]]>0: return len(meses_col)-1-i
        return len(meses_col)
    df_raw['MESES_SEM_COMPRA'] = df_raw.apply(calc_rec,axis=1)

    extra = [cida_col] if cida_col else []
    fo = ['CURVA',clie_col,vend_col]+extra+meses_col+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META','ACAO']

    # ── FILTROS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">FILTROS</div>', unsafe_allow_html=True)
    fc = st.columns([2,2,2,2,2])
    LBL = '<p style="font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#4B5568;margin:0 0 4px 0;">{}</p>'

    with fc[0]:
        st.markdown(LBL.format("VENDEDOR"), unsafe_allow_html=True)
        vendedores = ["Todos"]+sorted(df_raw[vend_col].dropna().astype(str).unique().tolist())
        sel_vend = st.selectbox("Vendedor",vendedores,label_visibility="collapsed")
    with fc[1]:
        st.markdown(LBL.format("CIDADE"), unsafe_allow_html=True)
        if cida_col:
            cidades = ["Todas"]+sorted(df_raw[cida_col].dropna().astype(str).unique().tolist())
            sel_cida = st.selectbox("Cidade",cidades,label_visibility="collapsed")
        else:
            sel_cida = "Todas"; st.caption("Cidade nao encontrada.")
    with fc[2]:
        st.markdown(LBL.format("CURVA"), unsafe_allow_html=True)
        curvas_disp = sorted(df_raw['CURVA'].unique().tolist())
        sel_curvas = st.multiselect("Curva",options=curvas_disp,default=curvas_disp,
            placeholder="Selecione...",label_visibility="collapsed")
        if not sel_curvas: sel_curvas = curvas_disp
    with fc[3]:
        st.markdown(LBL.format("&nbsp;"), unsafe_allow_html=True)
        eb = gerar_excel(df_raw,fo,clie_col,vend_col,meses_col)
        st.markdown('<span class="dlg"></span>', unsafe_allow_html=True)
        st.download_button(label="BAIXAR STAR",data=eb,
            file_name="Matriz_STAR_Giri.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with fc[4]:
        st.markdown(LBL.format("&nbsp;"), unsafe_allow_html=True)
        pdf_container = st.container()

    # ── METRICAS ──────────────────────────────────────────────────────────────
    df = df_raw.copy()
    if sel_vend!="Todos": df = df[df[vend_col].astype(str)==sel_vend]
    if cida_col and sel_cida!="Todas": df = df[df[cida_col].astype(str)==sel_cida]

    n_a_total=len(df[df['CURVA']=='A']); n_b_total=len(df[df['CURVA']=='B']); n_c_total=len(df[df['CURVA']=='C'])
    df_sel=df[df['CURVA'].isin(sel_curvas)]; clabel=curva_label_fmt(sel_curvas); cshort=curva_short(sel_curvas)
    ultimo_mes=meses_col[-1]; penultimo=meses_col[-2] if len(meses_col)>1 else meses_col[-1]
    last3=meses_col[-3:] if len(meses_col)>=3 else meses_col
    total=len(df_sel); rec_ult=df_sel[ultimo_mes].sum(); rec_pen=df_sel[penultimo].sum()
    var_rec=(rec_ult-rec_pen)/rec_pen*100 if rec_pen>0 else 0
    meta_total=df_sel['META'].sum()
    meta_a=df[df['CURVA']=='A']['META'].sum(); meta_b=df[df['CURVA']=='B']['META'].sum(); meta_c=df[df['CURVA']=='C']['META'].sum()
    risco_mask=df_sel['STATUS'].isin(['QUEDA','QUEDA ACENTUADA','INATIVO'])
    risco_val=df_sel.loc[risco_mask,'MEDIA LP'].sum(); n_risco=risco_mask.sum()
    saude_mask=df_sel['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO','ESTAVEL'])
    n_saudaveis=saude_mask.sum(); idx_saude=n_saudaveis/total*100 if total>0 else 0
    saude_color="#1A6B2A" if idx_saude>=70 else ("#B07D00" if idx_saude>=50 else "#C00000")
    buyers_ult=(df_sel[ultimo_mes]>0).sum(); ticket_ult=df_sel[ultimo_mes].sum()/buyers_ult if buyers_ult>0 else 0
    buyers_pen=(df_sel[penultimo]>0).sum(); ticket_pen=df_sel[penultimo].sum()/buyers_pen if buyers_pen>0 else 0
    var_ticket=(ticket_ult-ticket_pen)/ticket_pen*100 if ticket_pen>0 else 0
    contexto=sel_vend if sel_vend!="Todos" else "TODA A CARTEIRA"

    # ── PDF ───────────────────────────────────────────────────────────────────
    if REPORTLAB_OK:
        col_config={'clie':clie_col,'vend':vend_col,'cida':cida_col,'meses':meses_col,
                    'last3':last3,'ultimo':ultimo_mes,'penultimo':penultimo,'extra':extra}
        filters_pdf={'clabel':clabel,'cshort':cshort,'contexto':contexto,'vend':sel_vend,'curvas':sel_curvas}
        metrics_pdf={'total':total,'n_a':n_a_total,'n_b':n_b_total,'n_c':n_c_total,
                     'rec_ult':rec_ult,'var_rec':var_rec,'meta_total':meta_total,
                     'risco_val':risco_val,'n_risco':n_risco,'ticket_ult':ticket_ult,
                     'buyers_ult':buyers_ult,'idx_saude':idx_saude,'n_saudaveis':n_saudaveis}
        pdf_bytes=gerar_pdf(df_sel,df,col_config,filters_pdf,metrics_pdf)
        nome_pdf=f"STAR_{contexto.replace(' ','_')}_{clabel.replace(' ','_').replace('+','')}.pdf"
        with pdf_container:
            st.markdown('<span class="dlb"></span>', unsafe_allow_html=True)
            st.download_button(label="BAIXAR RELATORIO PDF",data=pdf_bytes,file_name=nome_pdf,mime="application/pdf")
    else:
        with pdf_container: st.caption("Instale reportlab para PDF")

    # ── KPI CARDS ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">VISAO GERAL DA CARTEIRA</div>', unsafe_allow_html=True)
    k1,k2,k3,k4=st.columns(4)
    with k1: st.markdown(f'<div class="kpi-wrap blue"><div class="kpi-lbl">COMPOSICAO DA CARTEIRA</div><div class="kpi-val">{fmt_br(total)}</div><div class="kpi-breakdown"><span style="color:{"#0056b3" if "A" in sel_curvas else "#B0BAC9"}">A: {n_a_total}</span> | <span style="color:{"#0056b3" if "B" in sel_curvas else "#B0BAC9"}">B: {n_b_total}</span> | <span style="color:{"#0056b3" if "C" in sel_curvas else "#B0BAC9"}">C: {n_c_total}</span></div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-wrap blue"><div class="kpi-lbl">RECEITA {htmllib.escape(clabel)} &mdash; {ultimo_mes}</div><div class="kpi-val">R$ {fmt_br(rec_ult)}</div><div class="kpi-sub">vs {penultimo}: {var_html(var_rec)}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-wrap dark"><div class="kpi-lbl">META DO MES</div><div class="kpi-val">R$ {fmt_br(meta_total)}</div><div class="kpi-breakdown"><span>A: R$ {fmt_br(meta_a)}</span><br><span>B: R$ {fmt_br(meta_b)}</span> | <span>C: R$ {fmt_br(meta_c)}</span></div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-wrap red"><div class="kpi-lbl">RECEITA EM RISCO &mdash; {htmllib.escape(clabel)}</div><div class="kpi-val red">R$ {fmt_br(risco_val)}</div><div class="kpi-sub">{n_risco} clientes em queda ou inativos</div></div>', unsafe_allow_html=True)

    # ── INDICADORES ───────────────────────────────────────────────────────────
    st.markdown(f'<div class="section-title">INDICADORES — {htmllib.escape(clabel)}</div>', unsafe_allow_html=True)
    i1,i2=st.columns(2)
    with i1: st.markdown(f'<div class="ind-wrap"><div class="ind-lbl">TICKET MEDIO — {ultimo_mes} (COMPRADORES ATIVOS)</div><div class="ind-val">R$ {fmt_br(ticket_ult)}</div><div class="ind-sub">vs {penultimo}: {var_html(var_ticket)}</div></div>', unsafe_allow_html=True)
    with i2: st.markdown(f'<div class="ind-wrap"><div class="ind-lbl">INDICE DE SAUDE &mdash; {htmllib.escape(clabel)}</div><div class="ind-val" style="color:{saude_color}">{idx_saude:.0f}%</div><div class="ind-sub">{n_saudaveis} de {total} clientes em crescimento ou estaveis</div></div>', unsafe_allow_html=True)

    # ── ANALISE DETALHADA ─────────────────────────────────────────────────────
    st.markdown(f'<div class="section-title">ANALISE DETALHADA — {htmllib.escape(clabel)}</div>', unsafe_allow_html=True)
    prev_fat=None; prev_ticket=None; rows_unified=""
    for i,mes in enumerate(last3):
        compraram=int((df_sel[mes]>0).sum()); fat=df_sel[mes].sum(); tk=fat/compraram if compraram>0 else 0
        vf_html=var_html(None) if i==0 else var_html((fat-prev_fat)/prev_fat*100 if prev_fat and prev_fat>0 else None)
        vt_html=var_html(None) if i==0 else var_html((tk-prev_ticket)/prev_ticket*100 if prev_ticket and prev_ticket>0 else None)
        rows_unified+=("<tr>"+f"<td><strong>{mes}</strong></td>"+f"<td>{total}</td>"+f"<td>{compraram}</td>"+f"<td>R$ {fmt_br(fat)}</td>"+f"<td>{vf_html}</td>"+f"<td>R$ {fmt_br(tk)}</td>"+f"<td>{vt_html}</td>"+"</tr>")
        prev_fat=fat; prev_ticket=tk
    st.markdown('<div class="ana-wrap">'+f'<div class="ana-title">FATURAMENTO E TICKET MEDIO — {htmllib.escape(clabel)} — ULTIMOS 3 MESES</div>'+'<table class="ana-table"><thead><tr><th>MES</th><th>CLIENTES TOTAIS</th><th>COMPRARAM NO MES</th><th>FATURAMENTO</th><th>VAR. FAT.</th><th>TICKET MEDIO</th><th>VAR. TICKET</th></tr></thead><tbody>'+rows_unified+'</tbody></table></div>', unsafe_allow_html=True)

    # ── RECENCIA ──────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    l0=f"Comprou em {meses_col[-1]}"; l1=f"Ultimo pedido em {meses_col[-2]}" if len(meses_col)>1 else "Ha 1 mes"
    l2=f"Ultimo pedido em {meses_col[-3]}" if len(meses_col)>2 else "Ha 2 meses"
    l3p=f"Sem compra desde {meses_col[-4]} ou antes" if len(meses_col)>3 else "Ha 3+ meses"
    rr=""
    for crit,badge,mr in [(l0,'<span class="rec-ativo">Ativo recente</span>',0),(l1,'<span class="rec-atencao">Atencao</span>',1),(l2,'<span class="rec-risco">Risco alto</span>',2),(l3p,'<span class="rec-critico">Inativo critico</span>',99)]:
        cnt=int((df_sel['MESES_SEM_COMPRA']>=3).sum()) if mr==99 else int((df_sel['MESES_SEM_COMPRA']==mr).sum())
        pct=cnt/total*100 if total>0 else 0
        rr+=f"<tr><td>{badge}</td><td style='text-align:left'>{crit}</td><td>{cnt}</td><td>{pct:.0f}%</td></tr>"
    st.markdown(f'<div class="ana-wrap"><div class="ana-title">RECENCIA DE COMPRA &mdash; {htmllib.escape(clabel)}</div><table class="ana-table"><thead><tr><th>CLASSIFICACAO</th><th style="text-align:left">CRITERIO</th><th>CLIENTES</th><th>%</th></tr></thead><tbody>'+rr+'</tbody></table></div>', unsafe_allow_html=True)

    # ── DIAGNOSTICO DE CARTEIRA ───────────────────────────────────────────────
    st.markdown('<div class="section-title">DIAGNOSTICO DE CARTEIRA</div>', unsafe_allow_html=True)

    sc=df_sel['STATUS'].value_counts()
    status_presentes=[s for s in STATUS_ORDER if s in df_sel['STATUS'].values]
    cur_filter=st.session_state.status_filtro or ''
    max_count=max([sc.get(s,0) for s in status_presentes]) if status_presentes else 1

    g1,g2,g3=st.columns([5,1,3])

    with g1:
        titulo=htmllib.escape(f"DISTRIBUICAO POR STATUS — {clabel}")
        rows_bar=""
        for status in status_presentes:
            cor=STATUS_BTN_COR.get(status,'#555'); count=sc.get(status,0)
            pct=count/total*100 if total>0 else 0; bar_w=count/max_count*100
            is_active=cur_filter==status
            row_bg=cor+'14' if is_active else 'transparent'
            border_c=cor if is_active else 'transparent'
            rows_bar+=(f'<div class="hbc-row" style="background:{row_bg};border-left-color:{border_c};">'
                f'<div class="hbc-lbl">{htmllib.escape(status)}</div>'
                f'<div class="hbc-track"><div class="hbc-fill" style="width:{bar_w:.1f}%;background:{cor};"></div></div>'
                f'<span class="hbc-cnt">{count} ({pct:.0f}%)</span></div>')
        st.markdown('<div class="hbc">'+f'<p class="hbc-title">{titulo}</p>'+rows_bar+'</div>', unsafe_allow_html=True)

    with g2:
        st.markdown('<div style="height:52px;"></div>', unsafe_allow_html=True)
        for status in status_presentes:
            cor=STATUS_BTN_COR.get(status,'#555')
            is_active=st.session_state.status_filtro==status
            bg=cor if is_active else 'transparent'; txt='#FFFFFF' if is_active else cor
            safe=status.replace(' ','_'); lbl='LIMPAR' if is_active else 'VER'
            st.markdown(
                f'<style>[data-testid="stMarkdownContainer"]:has(#sa_{safe}) + [data-testid="stButton"] button {{'
                f'background:{bg}!important;color:{txt}!important;border:2px solid {cor}!important;'
                f'border-radius:5px!important;height:28px!important;font-size:8px!important;'
                f'font-weight:800!important;width:100%!important;padding:0 4px!important;'
                f'text-transform:uppercase!important;letter-spacing:0.5px!important;'
                f'box-shadow:0 2px 5px rgba(0,0,0,0.12)!important;white-space:nowrap!important;}}'
                f'[data-testid="stMarkdownContainer"]:has(#sa_{safe}) + [data-testid="stButton"] button:hover{{'
                f'filter:brightness(0.88)!important;opacity:1!important;}}'
                f'</style><span id="sa_{safe}"></span>',
                unsafe_allow_html=True)
            if st.button(lbl, key=f'sfb_{safe}'):
                st.session_state.status_filtro=None if is_active else status
                st.session_state.scroll_needed=True
                st.rerun()

        st.markdown('<hr style="margin:4px 0;border:none;border-top:1px solid #D1D9E6;">', unsafe_allow_html=True)
        is_todos=st.session_state.status_filtro is None
        bg_t='#4B5568' if is_todos else 'transparent'; txt_t='#FFFFFF' if is_todos else '#4B5568'; lbl_t='LIMPAR' if is_todos else 'TODOS'
        st.markdown(
            f'<style>[data-testid="stMarkdownContainer"]:has(#sa_todos) + [data-testid="stButton"] button {{'
            f'background:{bg_t}!important;color:{txt_t}!important;border:2px solid #4B5568!important;'
            f'border-radius:5px!important;height:28px!important;font-size:8px!important;'
            f'font-weight:800!important;width:100%!important;padding:0 4px!important;'
            f'text-transform:uppercase!important;letter-spacing:0.5px!important;'
            f'box-shadow:0 2px 5px rgba(0,0,0,0.12)!important;}}'
            f'[data-testid="stMarkdownContainer"]:has(#sa_todos) + [data-testid="stButton"] button:hover{{'
            f'filter:brightness(0.88)!important;opacity:1!important;}}'
            f'</style><span id="sa_todos"></span>',
            unsafe_allow_html=True)
        if st.button(lbl_t, key='sfb_todos'):
            st.session_state.status_filtro=None
            st.session_state.scroll_needed=True
            st.rerun()

    with g3:
        cc2=df_sel['CURVA'].value_counts(); cvl=['A','B','C']; cvv=[cc2.get(c,0) for c in cvl]
        fig2=go.Figure(go.Pie(labels=cvl,values=cvv,hole=0.58,
            marker=dict(colors=['#001845','#0056b3','#4A90C4'],line=dict(color='#FFFFFF',width=2)),
            textinfo='label+percent',textfont=dict(size=13,family='Arial',color=['#FFFFFF','#FFFFFF','#1A2540']),
            insidetextorientation='radial'))
        fig2.update_layout(margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor='rgba(0,0,0,0)',height=320,showlegend=False)
        st.markdown('<div class="chart-wrap"><div class="chart-lbl">DISTRIBUICAO POR CURVA ABC</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2,use_container_width=True,config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── PERFORMANCE POR VENDEDOR ──────────────────────────────────────────────
    if sel_vend=="Todos":
        st.markdown('<div class="section-title">PERFORMANCE POR VENDEDOR</div>', unsafe_allow_html=True)
        rv=[]
        for v in sorted(df_sel[vend_col].dropna().astype(str).unique()):
            dv_t=df[df[vend_col].astype(str)==v]; dv_s=df_sel[df_sel[vend_col].astype(str)==v]
            rv.append({'VENDEDOR':v,'CLIENTES TOTAL':len(dv_t),f'CLIENTES {cshort}':len(dv_s),
                f'RECEITA {cshort}':dv_s['TOTAL LP'].sum(),
                f'QDA. ACENTUADA {cshort}':len(dv_s[dv_s['STATUS']=='QUEDA ACENTUADA']),
                f'QUEDA {cshort}':len(dv_s[dv_s['STATUS']=='QUEDA']),
                f'CRESCIMENTO {cshort}':len(dv_s[dv_s['STATUS'].isin(['CRESCIMENTO','CRESCIMENTO ACENTUADO'])]),
                f'INATIVOS {cshort}':len(dv_s[dv_s['STATUS']=='INATIVO'])})
        cv2=list(rv[0].keys()); rcol=f'RECEITA {cshort}'
        total_row={'VENDEDOR':'TOTAL GERAL'}
        for k in cv2:
            if k!='VENDEDOR': total_row[k]=sum(r[k] for r in rv)
        hh="".join([f"<th>{c}</th>" for c in cv2]); rh=""
        for r in rv:
            rh+="<tr>"+"".join([f"<td class='left'>{htmllib.escape(str(r[k]))}</td>" if k=='VENDEDOR' else (f"<td>R$ {fmt_br(r[k])}</td>" if k==rcol else f"<td>{r[k]}</td>") for k in cv2])+"</tr>"
        rh+="<tr class='total-row'>"+"".join([f"<td class='left'>{total_row[k]}</td>" if k=='VENDEDOR' else (f"<td>R$ {fmt_br(total_row[k])}</td>" if k==rcol else f"<td>{total_row[k]}</td>") for k in cv2])+"</tr>"
        st.markdown(f'<div class="vend-wrap"><table class="vend-table"><thead><tr>{hh}</tr></thead><tbody>{rh}</tbody></table></div>', unsafe_allow_html=True)

    # ── CARTEIRA DE CLIENTES ──────────────────────────────────────────────────
    st.markdown('<div id="carteira-anchor" style="scroll-margin-top:20px;"></div>', unsafe_allow_html=True)
    filtro_ativo=st.session_state.status_filtro
    if filtro_ativo:
        cor_ativo=STATUS_BTN_COR.get(filtro_ativo,'#555')
        st.markdown(f'<div class="section-title">CARTEIRA DE CLIENTES &mdash; <span style="color:{cor_ativo}">{htmllib.escape(filtro_ativo)}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-title">CARTEIRA DE CLIENTES</div>', unsafe_allow_html=True)

    cd=['CURVA',clie_col,vend_col]+extra+['TOTAL LP','MEDIA LP','MEDIA CP','STATUS','META']
    dd=df_sel[df_sel['STATUS']==filtro_ativo].copy() if filtro_ativo else df_sel.copy()
    dd=dd[cd].reset_index(drop=True)
    hc="".join([f"<th>{c}</th>" for c in cd]); rc=""
    for _,row in dd.iterrows():
        cells=""
        for cn in cd:
            v=row[cn]; ac=' class="left"' if cn==clie_col else ''
            if cn=='STATUS': s=str(v); css5=STATUS_CSS.get(s,''); cells+=f'<td><span style="{css5}">{s}</span></td>'
            elif cn in('TOTAL LP','MEDIA LP','MEDIA CP','META'): cells+=f'<td{ac}>{fmt_br(v)}</td>'
            else: cells+=f'<td{ac}>{htmllib.escape(str(v))}</td>'
        rc+=f"<tr>{cells}</tr>"
    st.markdown(f'<div class="cart-wrap"><table class="cart-table"><thead><tr>{hc}</tr></thead><tbody>{rc}</tbody></table></div>', unsafe_allow_html=True)

    # ── SCROLL AUTOMATICO ─────────────────────────────────────────────────────
    if st.session_state.get('scroll_needed', False):
        components.html("""
        <script>
        setTimeout(function() {
            try {
                var el = window.parent.document.getElementById('carteira-anchor');
                if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
            } catch(e) {}
        }, 400);
        </script>
        """, height=0)
        st.session_state.scroll_needed = False
