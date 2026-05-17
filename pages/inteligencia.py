import streamlit as st
import pandas as pd

st.set_page_config(page_title="Giri | Inteligencia de Carteira", layout="wide")

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
.kpi-wrap.blue::before  { background:linear-gradient(90deg,#0056b3,#00A3E0); }
.kpi-wrap.red::before   { background:linear-gradient(90deg,#C00000,#FF6B6B); }
.kpi-wrap.dark::before  { background:linear-gradient(90deg,#1A2540,#3A4A6B); }
.kpi-wrap.amber::before { background:linear-gradient(90deg,#D44000,#FF8C42); }
.kpi-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:10px; }
.kpi-val { font-size:1.85rem; font-weight:800; line-height:1; margin-bottom:7px; color:#0D1B2A; }
.kpi-val.red   { color:#C00000; }
.kpi-val.amber { color:#D44000; }
.kpi-sub { font-size:0.74rem; color:#4B5568; line-height:1.4; }
.prio-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:auto; max-height:640px; }
.prio-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.83rem; }
.prio-table th { background:#1A2540; color:#FFFFFF; font-weight:700; padding:10px 12px; text-align:center; letter-spacing:0.6px; font-size:0.70rem; text-transform:uppercase; white-space:nowrap; vertical-align:middle; }
.prio-table td { padding:9px 12px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; vertical-align:middle; }
.prio-table td.left { text-align:left; }
.prio-table tr:last-child td { border-bottom:none; }
.prio-table tr:hover td { background:#F5F7FB; }
.erosao-dist { background:#FFFFFF; border-radius:14px; padding:20px 24px; box-shadow:0 2px 18px rgba(0,0,0,0.07); }
.erosao-dist-title { font-size:0.80rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#1A2540; margin-bottom:16px; text-align:center; }
.hbc-row { display:flex; align-items:center; gap:10px; padding:5px 0; }
.hbc-lbl { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; color:#1A2540; width:130px; flex-shrink:0; text-align:right; padding-right:8px; }
.hbc-track { flex:1; height:18px; background:#EDF1F7; border-radius:4px; overflow:hidden; }
.hbc-fill { height:100%; border-radius:4px; }
.hbc-cnt { font-size:10px; font-weight:700; color:#4B5568; width:60px; flex-shrink:0; padding-left:6px; }
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
    'CRESCIMENTO':           'Consolidacao — entender driver e proteger',
    'CRESCIMENTO ACENTUADO': 'Consolidacao urgente — crescimento atrai concorrencia',
}

EROSAO_CORES = {
    'baixa':     ('#C6EFCE', '#375623'),
    'atencao':   ('#FFEB9C', '#7A4F00'),
    'alto':      ('#FFC7CE', '#C00000'),
    'critico':   ('#C00000', '#FFFFFF'),
}


def calcular_erosao_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        return 1
    if cp_v <= 0:
        return 10
    if lp_v <= 0:
        return 1
    diff = ((lp_v - cp_v) / lp_v) * 100
    if diff <= 0:   return 1
    if diff <= 5:   return 1
    if diff <= 10:  return 2
    if diff <= 15:  return 3
    if diff <= 20:  return 4
    if diff <= 30:  return 5
    if diff <= 40:  return 6
    if diff <= 50:  return 7
    if diff <= 60:  return 8
    if diff <= 70:  return 9
    return 10


def erosao_display(n):
    if n <= 3:
        bg, fg = EROSAO_CORES['baixa']
        return bg, fg, 'BAIXA EROSAO'
    elif n <= 5:
        bg, fg = EROSAO_CORES['atencao']
        return bg, fg, 'ATENCAO'
    elif n <= 7:
        bg, fg = EROSAO_CORES['alto']
        return bg, fg, 'ALTO RISCO'
    else:
        bg, fg = EROSAO_CORES['critico']
        return bg, fg, 'CRITICO'


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


# ── HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="giri-header">
  <div class="giri-header-dot">&#9733;</div>
  <div>
    <h1>GIRI | INTELIGENCIA DE CARTEIRA</h1>
    <p>PRIORIZACAO OPERACIONAL — INDICE DE EROSAO STAR — CAMADA 2</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD ───────────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:0.85rem;color:#4B5568;margin-bottom:6px;'>Faca upload da base (XLSX ou CSV)</p>",
    unsafe_allow_html=True
)
uploaded = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

if not uploaded:
    st.stop()

try:
    if uploaded.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
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
    st.error(
        "Arquivo nao reconhecido. "
        "Verifique se as colunas CLIENTE, MEDIA LP, MEDIA CP e STATUS estao presentes."
    )
    st.stop()

# ── CALCULO ──────────────────────────────────────────────────────────────
df['_EROSAO'] = df.apply(
    lambda r: calcular_erosao_star(r.get(col_mlp, 0), r.get(col_mcp, 0)), axis=1
)
df['_SCORE'] = df.apply(
    lambda r: score_prioridade(
        r.get(col_curv, 'C') if col_curv else 'C',
        r.get(col_sta, ''),
        r['_EROSAO'],
        r.get(col_mlp, 0)
    ), axis=1
)
df['_RISCO'] = df.apply(
    lambda r: max(0.0, float(r.get(col_mlp, 0) or 0) - float(r.get(col_mcp, 0) or 0)),
    axis=1
)
df_sorted = df.sort_values('_SCORE', ascending=False).reset_index(drop=True)

# ── FILTROS ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>FILTROS</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

vends = ['Todos'] + sorted(df[col_vend].dropna().astype(str).unique().tolist()) if col_vend else ['Todos']
with c1:
    sel_v = st.selectbox("VENDEDOR", vends)
with c2:
    sel_c = st.selectbox("CURVA", ['Todas', 'A', 'B', 'C'])
with c3:
    sel_e = st.selectbox(
        "EROSAO STAR",
        ['Todos', 'STAR 1-3  Baixa Erosao', 'STAR 4-5  Atencao', 'STAR 6-7  Alto Risco', 'STAR 8-10  Critico']
    )

df_f = df_sorted.copy()
if sel_v != 'Todos' and col_vend:
    df_f = df_f[df_f[col_vend].astype(str) == sel_v]
if sel_c != 'Todas' and col_curv:
    df_f = df_f[df_f[col_curv].astype(str).str.upper() == sel_c]
if 'STAR 1-3'  in sel_e: df_f = df_f[df_f['_EROSAO'] <= 3]
elif 'STAR 4-5'  in sel_e: df_f = df_f[df_f['_EROSAO'].between(4, 5)]
elif 'STAR 6-7'  in sel_e: df_f = df_f[df_f['_EROSAO'].between(6, 7)]
elif 'STAR 8-10' in sel_e: df_f = df_f[df_f['_EROSAO'] >= 8]

# ── KPIs ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>VISAO GERAL — PRIORIZACAO</div>", unsafe_allow_html=True)

n_total  = len(df_f)
n_crit   = int((df_f['_EROSAO'] >= 8).sum())
n_alto   = int(df_f['_EROSAO'].between(6, 7).sum())
risco_t  = df_f['_RISCO'].sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        f"<div class='kpi-wrap blue'>"
        f"<div class='kpi-lbl'>CLIENTES NA SELECAO</div>"
        f"<div class='kpi-val'>{n_total}</div>"
        f"<div class='kpi-sub'>na fila de priorizacao</div>"
        f"</div>", unsafe_allow_html=True
    )
with k2:
    st.markdown(
        f"<div class='kpi-wrap red'>"
        f"<div class='kpi-lbl'>EROSAO CRITICA — STAR 8 A 10</div>"
        f"<div class='kpi-val red'>{n_crit}</div>"
        f"<div class='kpi-sub'>clientes em estado critico</div>"
        f"</div>", unsafe_allow_html=True
    )
with k3:
    st.markdown(
        f"<div class='kpi-wrap amber'>"
        f"<div class='kpi-lbl'>ALTO RISCO — STAR 6 A 7</div>"
        f"<div class='kpi-val amber'>{n_alto}</div>"
        f"<div class='kpi-sub'>clientes em alto risco</div>"
        f"</div>", unsafe_allow_html=True
    )
with k4:
    st.markdown(
        f"<div class='kpi-wrap dark'>"
        f"<div class='kpi-lbl'>RECEITA EM RISCO</div>"
        f"<div class='kpi-val'>{fmt_br(risco_t)}</div>"
        f"<div class='kpi-sub'>diferenca LP vs CP acumulada</div>"
        f"</div>", unsafe_allow_html=True
    )

# ── DISTRIBUICAO POR EROSAO ───────────────────────────────────────────────
st.markdown("<div class='section-title'>DISTRIBUICAO POR INDICE DE EROSAO STAR</div>", unsafe_allow_html=True)

faixas = [
    ('STAR 1-3  Baixa Erosao',  df_f['_EROSAO'] <= 3,           '#C6EFCE', '#375623'),
    ('STAR 4-5  Atencao',       df_f['_EROSAO'].between(4, 5),  '#FFEB9C', '#7A4F00'),
    ('STAR 6-7  Alto Risco',    df_f['_EROSAO'].between(6, 7),  '#FFC7CE', '#C00000'),
    ('STAR 8-10  Critico',      df_f['_EROSAO'] >= 8,           '#C00000', '#FFFFFF'),
]

col_dist, col_esp = st.columns([1, 1])
with col_dist:
    st.markdown("<div class='erosao-dist'><div class='erosao-dist-title'>CLIENTES POR FAIXA DE EROSAO</div>", unsafe_allow_html=True)
    max_n = max((df_f[mask].shape[0] for _, mask, _, _ in faixas), default=1)
    for lbl, mask, bg, fg in faixas:
        n   = int(df_f[mask].shape[0])
        pct = round(n / n_total * 100, 1) if n_total > 0 else 0
        bar = int((n / max(max_n, 1)) * 100)
        st.markdown(
            f"<div class='hbc-row'>"
            f"<div class='hbc-lbl'>{lbl}</div>"
            f"<div class='hbc-track'><div class='hbc-fill' style='width:{bar}%;background:{bg};'></div></div>"
            f"<div class='hbc-cnt'>{n} ({pct}%)</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ── FILA OPERACIONAL ─────────────────────────────────────────────────────
st.markdown(
    f"<div class='section-title'>FILA OPERACIONAL DE PRIORIDADE</div>",
    unsafe_allow_html=True
)

if not df_f.empty:
    rows_html = ""
    for i, (_, r) in enumerate(df_f.iterrows(), 1):
        en         = int(r['_EROSAO'])
        ebg, efg, elbl = erosao_display(en)
        sta        = str(r.get(col_sta, '')).strip().upper()
        scss       = STATUS_CSS.get(sta, 'color:#1A2540;font-weight:600;')
        curv       = str(r.get(col_curv, '')) if col_curv else ''
        nome       = str(r.get(col_cli, ''))
        vend       = str(r.get(col_vend, '')) if col_vend else ''
        mlp        = fmt_br(r.get(col_mlp, 0))
        mcp        = fmt_br(r.get(col_mcp, 0))
        risk       = fmt_br(r['_RISCO'])
        acao       = ACAO_MAP.get(sta, 'Monitorar')

        rows_html += (
            f"<tr>"
            f"<td><strong>#{i}</strong></td>"
            f"<td class='left'><strong>{nome}</strong></td>"
            f"<td>{vend}</td>"
            f"<td><strong>{curv}</strong></td>"
            f"<td><span style='{scss}'>{sta}</span></td>"
            f"<td><span style='background:{ebg};color:{efg};font-weight:800;border-radius:8px;"
            f"padding:3px 12px;font-size:0.88rem;display:inline-block;'>STAR {en}</span></td>"
            f"<td><span style='background:{ebg};color:{efg};font-weight:700;border-radius:6px;"
            f"padding:2px 8px;font-size:0.78rem;display:inline-block;'>{elbl}</span></td>"
            f"<td>{mlp}</td>"
            f"<td>{mcp}</td>"
            f"<td style='color:#C00000;font-weight:700;'>{risk}</td>"
            f"<td class='left' style='font-size:0.78rem;color:#4B5568;'>{acao}</td>"
            f"</tr>"
        )

    st.markdown(
        f"<div class='prio-wrap'><table class='prio-table'>"
        f"<thead><tr>"
        f"<th>#</th><th>CLIENTE</th><th>VENDEDOR</th><th>CURVA</th><th>STATUS</th>"
        f"<th>INDICE STAR</th><th>NIVEL</th><th>MEDIA LP</th><th>MEDIA CP</th>"
        f"<th>RISCO</th><th>ACAO PRESCRITA</th>"
        f"</tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        f"</table></div>",
        unsafe_allow_html=True
    )
else:
    st.info("Nenhum cliente encontrado para os filtros selecionados.")
