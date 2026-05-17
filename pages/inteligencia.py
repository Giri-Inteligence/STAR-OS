import streamlit as st
import pandas as pd

st.set_page_config(page_title="Giri | Inteligencia de Carteira", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebarNav"]      { display:none; }
[data-testid="stAppViewContainer"]{ background:#EDF1F7; }
[data-testid="stHeader"]          { background:transparent; }

/* ── HEADER ── */
.giri-header-int {
    background:linear-gradient(120deg,#071F12 0%,#0F4023 45%,#1A6B3A 80%,#22874A 100%);
    border-radius:18px; padding:30px 38px; margin-bottom:28px;
    box-shadow:0 12px 48px rgba(7,31,18,0.45), 0 2px 8px rgba(34,135,74,0.20);
    display:flex; align-items:center; gap:18px;
}
.giri-header-dot {
    width:48px; height:48px;
    background:rgba(255,255,255,0.13);
    border-radius:12px; display:flex; align-items:center;
    justify-content:center; font-size:22px; flex-shrink:0;
    box-shadow:inset 0 1px 0 rgba(255,255,255,0.2);
}
.giri-header-int h1 { color:#FFFFFF; font-size:1.45rem; font-weight:800; letter-spacing:1.2px; margin:0 0 3px 0; }
.giri-header-int p  { color:rgba(255,255,255,0.60); font-size:0.80rem; margin:0; letter-spacing:0.5px; }

/* ── SECTION TITLE ── */
.section-title {
    font-size:0.95rem; font-weight:800; text-transform:uppercase;
    letter-spacing:2px; color:#071F12;
    margin:32px 0 14px 0; padding-bottom:8px;
    border-bottom:2px solid #1A6B3A;
}

/* ── KPI ── */
.kpi-wrap {
    background:#FFFFFF; border-radius:14px;
    padding:14px 22px 12px 22px;
    box-shadow:0 4px 24px rgba(7,31,18,0.10), 0 1px 4px rgba(0,0,0,0.04);
    position:relative; overflow:hidden; text-align:center;
}
.kpi-wrap::before {
    content:""; position:absolute; top:0; left:0; right:0;
    height:4px; border-radius:14px 14px 0 0;
}
.kpi-wrap.green::before { background:linear-gradient(90deg,#0F4023,#1A6B3A,#22874A); }
.kpi-wrap.dark::before  { background:linear-gradient(90deg,#071F12,#0F4023,#1A6B3A); }
.kpi-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:8px; }
.kpi-val { font-size:1.65rem; font-weight:800; line-height:1; margin-bottom:5px; color:#071F12; }
.kpi-sub { font-size:0.72rem; color:#4B5568; line-height:1.4; }

/* ── BLOCO EROSÃO ── */
.erosao-bloco {
    background:#FFFFFF; border-radius:14px;
    box-shadow:0 4px 24px rgba(7,31,18,0.10), 0 1px 4px rgba(0,0,0,0.04);
    overflow:hidden;
}
.erosao-bloco-title {
    background:linear-gradient(90deg,#071F12 0%,#145A32 55%,#1E8449 100%);
    color:#FFFFFF; font-size:0.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.5px;
    padding:12px 20px; text-align:center;
}
.eros-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.eros-table th {
    background:linear-gradient(90deg,#EAF5EE,#F4FBF6);
    color:#071F12; font-weight:700; padding:9px 16px;
    font-size:0.70rem; text-transform:uppercase; letter-spacing:0.6px;
    border-bottom:1px solid #C8E6D0;
}
.eros-table th.left { text-align:left; }
.eros-table th.center { text-align:center; }
.eros-table td { padding:10px 16px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; }
.eros-table td.left { text-align:left; }
.eros-table tr:last-child td { border-bottom:none; background:#F4FBF6; font-weight:800; color:#071F12; }
.eros-table tr:hover td { background:#F4FBF6; }

/* ── BADGES LARGURA FIXA ── */
.faixa-badge {
    font-weight:800; border-radius:8px; padding:4px 0;
    font-size:0.83rem; display:inline-block;
    width:170px; text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.12);
}
.nivel-badge {
    font-weight:700; border-radius:6px; padding:3px 0;
    font-size:0.78rem; display:inline-block;
    width:95px; text-align:center;
}
.star-badge {
    font-weight:800; border-radius:8px; padding:3px 0;
    font-size:0.85rem; display:inline-block;
    width:130px; text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.10);
}

/* ── FILA OPERACIONAL ── */
.prio-wrap {
    background:#FFFFFF; border-radius:14px;
    box-shadow:0 4px 24px rgba(7,31,18,0.10), 0 1px 4px rgba(0,0,0,0.04);
    overflow:auto; max-height:640px;
}
.prio-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.83rem; }
.prio-table th {
    background:linear-gradient(90deg,#071F12 0%,#145A32 60%,#1A6B3A 100%);
    color:#FFFFFF; font-weight:700; padding:10px 12px;
    text-align:center; letter-spacing:0.6px;
    font-size:0.70rem; text-transform:uppercase;
    white-space:nowrap; vertical-align:middle;
}
.prio-table td {
    padding:9px 12px; text-align:center;
    color:#1A2540; border-bottom:1px solid #E5EAF2;
    font-weight:500; vertical-align:middle;
}
.prio-table td.left { text-align:left; }
.prio-table tr:last-child td { border-bottom:none; }
.prio-table tr:hover td { background:#F4FBF6; }

/* ── BOTAO VOLTAR ── */
.voltar-link a {
    font-size:0.80rem; font-weight:600;
    color:#145A32 !important; text-decoration:none;
}
</style>
""", unsafe_allow_html=True)

STATUS_CSS = {
    'QUEDA ACENTUADA':       'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 8px;white-space:nowrap;display:inline-block;',
    'QUEDA':                 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 8px;white-space:nowrap;display:inline-block;',
    'CRESCIMENTO':           'color:#375623;font-weight:700;',
    'ESTAVEL':               'color:#0070C0;font-weight:700;',
    'INATIVO':               'color:#6B7280;font-weight:700;',
}

ACAO_MAP = {
    'QUEDA ACENTUADA':       'Diagnostico — contato em ate 48h',
    'QUEDA':                 'Acao preventiva — contato em 5 dias uteis',
    'INATIVO':               'Validar recuperabilidade antes de ofertar',
    'ESTAVEL':               'Blindagem relacional — ciclo mensal',
    'CRESCIMENTO':           'Consolidacao — entender driver e proteger conta',
    'CRESCIMENTO ACENTUADO': 'Consolidacao urgente — crescimento atrai concorrencia',
}

FAIXAS_EROSAO = [
    ('EROSAO STAR 8 A 10', 'CRITICO',    '#C00000', '#FFFFFF', lambda s: s >= 8),
    ('EROSAO STAR 6 A 7',  'ALTO RISCO', '#FFC7CE', '#C00000', lambda s: 6 <= s <= 7),
    ('EROSAO STAR 4 A 5',  'ATENCAO',    '#FFEB9C', '#7A4F00', lambda s: 4 <= s <= 5),
    ('EROSAO STAR 1 A 3',  'BAIXA',      '#C6EFCE', '#375623', lambda s: s <= 3),
]


def calcular_erosao_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        return 1
    if cp_v <= 0:  return 10
    if lp_v <= 0:  return 1
    diff = ((lp_v - cp_v) / lp_v) * 100
    if diff <= 0:  return 1
    if diff <= 5:  return 1
    if diff <= 10: return 2
    if diff <= 15: return 3
    if diff <= 20: return 4
    if diff <= 30: return 5
    if diff <= 40: return 6
    if diff <= 50: return 7
    if diff <= 60: return 8
    if diff <= 70: return 9
    return 10


def erosao_display(n):
    if n >= 8:   return '#C00000', '#FFFFFF', 'CRITICO'
    elif n >= 6: return '#FFC7CE', '#C00000', 'ALTO RISCO'
    elif n >= 4: return '#FFEB9C', '#7A4F00', 'ATENCAO'
    else:        return '#C6EFCE', '#375623', 'BAIXA EROSAO'


def score_prioridade(curva, status, erosao, media_lp):
    cp = {'A': 300, 'B': 150, 'C': 50}.get(str(curva).strip().upper(), 30)
    sp = {
        'QUEDA ACENTUADA': 500, 'QUEDA': 350, 'INATIVO': 280,
        'ESTAVEL': 150, 'CRESCIMENTO': 80, 'CRESCIMENTO ACENTUADO': 50
    }.get(str(status).strip().upper(), 50)
    ep = int(erosao) * 20
    rp = min(float(media_lp or 0) / 100, 300)
    return cp + sp + ep + rp


def fmt_br(v):
    try:
        return 'R$ ' + f"{int(float(v)):,}".replace(',', '.')
    except:
        return 'R$ 0'


def find_col(df, *kw):
    for c in df.columns:
        if all(k in c for k in kw):
            return c
    return None


# ── BOTAO VOLTAR ─────────────────────────────────────────────────────────
st.page_link("app.py", label="← Voltar ao Dashboard STAR")

# ── HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="giri-header-int">
  <div class="giri-header-dot">&#9650;</div>
  <div>
    <h1>GIRI | INTELIGENCIA DE CARTEIRA</h1>
    <p>PRIORIZACAO OPERACIONAL — INDICE DE EROSAO STAR — CAMADA 2</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD ───────────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:0.85rem;color:#4B5568;margin-bottom:6px;'>"
    "Faca upload da Matriz STAR gerada pelo dashboard (XLSX ou CSV)"
    "</p>",
    unsafe_allow_html=True
)
uploaded = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

if not uploaded:
    st.stop()

try:
    df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Erro ao ler arquivo: {e}")
    st.stop()

df.columns = [str(c).strip().upper() for c in df.columns]

col_cli  = find_col(df, 'CLIENTE')
col_vend = find_col(df, 'VENDEDOR')
col_curv = find_col(df, 'CURVA')
col_mlp  = find_col(df, 'MEDIA', 'LP')
col_mcp  = find_col(df, 'MEDIA', 'CP')
col_sta  = find_col(df, 'STATUS')

if not all([col_cli, col_mlp, col_mcp, col_sta]):
    st.error("Arquivo nao reconhecido. Faca o download da Matriz STAR pelo dashboard e suba esse arquivo aqui.")
    st.stop()

# ── CALCULO ──────────────────────────────────────────────────────────────
df['_EROSAO'] = df.apply(lambda r: calcular_erosao_star(r.get(col_mlp, 0), r.get(col_mcp, 0)), axis=1)
df['_SCORE']  = df.apply(lambda r: score_prioridade(
    r.get(col_curv, 'C') if col_curv else 'C',
    r.get(col_sta, ''), r['_EROSAO'], r.get(col_mlp, 0)
), axis=1)
df['_RISCO']  = df.apply(lambda r: max(0.0, float(r.get(col_mlp, 0) or 0) - float(r.get(col_mcp, 0) or 0)), axis=1)
df_sorted = df.sort_values('_SCORE', ascending=False).reset_index(drop=True)

# ── FILTROS ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>FILTROS</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
vends = (['Todos'] + sorted(df[col_vend].dropna().astype(str).unique().tolist())) if col_vend else ['Todos']
with c1: sel_v = st.selectbox("VENDEDOR", vends)
with c2: sel_c = st.selectbox("CURVA", ['Todas', 'A', 'B', 'C'])
with c3: sel_e = st.selectbox("EROSAO STAR", ['Todos', 'EROSAO STAR 8 A 10  Critico', 'EROSAO STAR 6 A 7  Alto Risco', 'EROSAO STAR 4 A 5  Atencao', 'EROSAO STAR 1 A 3  Baixa'])

df_f = df_sorted.copy()
if sel_v != 'Todos' and col_vend:     df_f = df_f[df_f[col_vend].astype(str) == sel_v]
if sel_c != 'Todas' and col_curv:     df_f = df_f[df_f[col_curv].astype(str).str.upper() == sel_c]
if   '8 A 10' in sel_e: df_f = df_f[df_f['_EROSAO'] >= 8]
elif '6 A 7'  in sel_e: df_f = df_f[df_f['_EROSAO'].between(6, 7)]
elif '4 A 5'  in sel_e: df_f = df_f[df_f['_EROSAO'].between(4, 5)]
elif '1 A 3'  in sel_e: df_f = df_f[df_f['_EROSAO'] <= 3]

n_total = len(df_f)
risco_t = df_f['_RISCO'].sum()

# ── VISAO GERAL ──────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>VISAO GERAL — PRIORIZACAO</div>", unsafe_allow_html=True)

# Linha 1 — dois KPIs lado a lado
k1, k2 = st.columns(2)
with k1:
    st.markdown(
        f"<div class='kpi-wrap green'>"
        f"<div class='kpi-lbl'>CLIENTES NA SELECAO</div>"
        f"<div class='kpi-val'>{n_total}</div>"
        f"<div class='kpi-sub'>na fila de priorizacao</div>"
        f"</div>", unsafe_allow_html=True
    )
with k2:
    st.markdown(
        f"<div class='kpi-wrap dark'>"
        f"<div class='kpi-lbl'>RECEITA EM RISCO</div>"
        f"<div class='kpi-val'>{fmt_br(risco_t)}</div>"
        f"<div class='kpi-sub'>diferenca LP vs CP acumulada</div>"
        f"</div>", unsafe_allow_html=True
    )

# Linha 2 — bloco erosão largura total
st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
rows_eros = ""
for faixa_lbl, nivel_lbl, bg, fg, fn in FAIXAS_EROSAO:
    n_f   = int(df_f[df_f['_EROSAO'].apply(fn)].shape[0])
    pct_f = round(n_f / n_total * 100, 1) if n_total > 0 else 0.0
    rows_eros += (
        f"<tr>"
        f"<td class='left'>"
        f"<span class='faixa-badge' style='background:{bg};color:{fg};'>{faixa_lbl}</span>"
        f"</td>"
        f"<td>"
        f"<span class='nivel-badge' style='background:{bg};color:{fg};'>{nivel_lbl}</span>"
        f"</td>"
        f"<td><strong>{n_f}</strong></td>"
        f"<td><strong>{pct_f}%</strong></td>"
        f"</tr>"
    )
rows_eros += (
    f"<tr><td class='left' colspan='2'><strong>TOTAL</strong></td>"
    f"<td><strong>{n_total}</strong></td>"
    f"<td><strong>100%</strong></td></tr>"
)
st.markdown(
    f"<div class='erosao-bloco'>"
    f"<div class='erosao-bloco-title'>INDICE DE EROSAO STAR</div>"
    f"<table class='eros-table'>"
    f"<thead><tr>"
    f"<th class='left'>FAIXA</th>"
    f"<th class='center'>NIVEL</th>"
    f"<th class='center'>CLIENTES</th>"
    f"<th class='center'>%</th>"
    f"</tr></thead>"
    f"<tbody>{rows_eros}</tbody>"
    f"</table></div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ── FILA OPERACIONAL ─────────────────────────────────────────────────────
st.markdown("<div class='section-title'>FILA OPERACIONAL DE PRIORIDADE</div>", unsafe_allow_html=True)

if not df_f.empty:
    rows_html = ""
    for i, (_, r) in enumerate(df_f.iterrows(), 1):
        en             = int(r['_EROSAO'])
        ebg, efg, elbl = erosao_display(en)
        sta            = str(r.get(col_sta, '')).strip().upper()
        scss           = STATUS_CSS.get(sta, 'color:#1A2540;font-weight:600;')
        curv           = str(r.get(col_curv, '')) if col_curv else ''
        nome           = str(r.get(col_cli, ''))
        vend           = str(r.get(col_vend, '')) if col_vend else ''
        mlp            = fmt_br(r.get(col_mlp, 0))
        mcp            = fmt_br(r.get(col_mcp, 0))
        risk           = fmt_br(r['_RISCO'])
        acao           = ACAO_MAP.get(sta, 'Monitorar')
        rows_html += (
            f"<tr>"
            f"<td><strong>#{i}</strong></td>"
            f"<td class='left'><strong>{nome}</strong></td>"
            f"<td>{vend}</td>"
            f"<td><strong>{curv}</strong></td>"
            f"<td><span style='{scss}'>{sta}</span></td>"
            f"<td><span class='star-badge' style='background:{ebg};color:{efg};'>"
            f"EROSAO STAR {en}</span></td>"
            f"<td><span class='nivel-badge' style='background:{ebg};color:{efg};'>"
            f"{elbl}</span></td>"
            f"<td>{mlp}</td><td>{mcp}</td>"
            f"<td style='color:#C00000;font-weight:700;'>{risk}</td>"
            f"<td class='left' style='font-size:0.78rem;color:#4B5568;'>{acao}</td>"
            f"</tr>"
        )
    st.markdown(
        f"<div class='prio-wrap'><table class='prio-table'>"
        f"<thead><tr>"
        f"<th>#</th><th>CLIENTE</th><th>VENDEDOR</th><th>CURVA</th><th>STATUS</th>"
        f"<th>INDICE EROSAO</th><th>NIVEL</th><th>MEDIA LP</th><th>MEDIA CP</th>"
        f"<th>RISCO</th><th>ACAO PRESCRITA</th>"
        f"</tr></thead>"
        f"<tbody>{rows_html}</tbody></table></div>",
        unsafe_allow_html=True
    )
else:
    st.info("Nenhum cliente encontrado para os filtros selecionados.")
