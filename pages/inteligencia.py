import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

st.set_page_config(page_title="Giri | Inteligência de Carteira", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebarNav"]       { display:none; }
[data-testid="stAppViewContainer"] { background:#EDF1F7; }
[data-testid="stHeader"]           { background:transparent; }

.stSelectbox label, .stMultiSelect label, .stTextInput label {
    font-size:0.75rem !important; font-weight:700 !important;
    text-transform:uppercase !important; letter-spacing:1.2px !important;
    color:#1A2540 !important; display:block; text-align:center; margin-bottom:4px !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background:#1A2540 !important; border:1px solid #374151 !important;
    border-radius:8px !important; color:#FFFFFF !important;
}
[data-testid="stSelectbox"] svg, [data-testid="stMultiSelect"] svg { fill:#FFFFFF !important; }
[data-baseweb="tag"] { background:#C00000 !important; border-radius:6px !important; }
[data-baseweb="tag"] span { color:#FFFFFF !important; font-weight:700 !important; }
[data-baseweb="tag"] button svg { fill:#FFFFFF !important; }
[data-baseweb="menu"]   { background:#1A2540 !important; }
[data-baseweb="option"] { background:#1A2540 !important; color:#FFFFFF !important; }
[data-baseweb="option"]:hover { background:#2D3F6B !important; }
[data-testid="stTextInput"] > div > div > input {
    background:#1A2540 !important; color:#FFFFFF !important;
    border:1px solid #374151 !important; border-radius:8px !important;
}

.giri-header-int {
    background:linear-gradient(120deg,#071F12 0%,#0F4023 45%,#1A6B3A 80%,#22874A 100%);
    border-radius:18px; padding:30px 38px; margin-bottom:28px;
    box-shadow:0 12px 48px rgba(7,31,18,0.45),0 2px 8px rgba(34,135,74,0.20);
    display:flex; align-items:center; gap:18px;
}
.giri-header-dot { width:48px; height:48px; background:rgba(255,255,255,0.13); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
.giri-header-int h1 { color:#FFFFFF; font-size:1.45rem; font-weight:800; letter-spacing:1.2px; margin:0 0 3px 0; }
.giri-header-int p  { color:rgba(255,255,255,0.60); font-size:0.80rem; margin:0; letter-spacing:0.5px; }

.section-title { font-size:0.95rem; font-weight:800; text-transform:uppercase; letter-spacing:2px; color:#071F12; margin:32px 0 14px 0; padding-bottom:8px; border-bottom:2px solid #1A6B3A; }

.kpi-wrap { background:#FFFFFF; border-radius:14px; padding:14px 22px 12px 22px; box-shadow:0 4px 24px rgba(7,31,18,0.10),0 1px 4px rgba(0,0,0,0.04); position:relative; overflow:hidden; text-align:center; }
.kpi-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:4px; border-radius:14px 14px 0 0; }
.kpi-wrap.green::before { background:linear-gradient(90deg,#0F4023,#1A6B3A,#22874A); }
.kpi-wrap.dark::before  { background:linear-gradient(90deg,#071F12,#0F4023,#1A6B3A); }
.kpi-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:8px; }
.kpi-val { font-size:1.65rem; font-weight:800; line-height:1; margin-bottom:5px; color:#071F12; }
.kpi-sub { font-size:0.72rem; color:#4B5568; line-height:1.4; }

.erosao-bloco { background:#FFFFFF; border-radius:14px; box-shadow:0 4px 24px rgba(7,31,18,0.10),0 1px 4px rgba(0,0,0,0.04); overflow:hidden; }
.erosao-bloco-title { background:linear-gradient(90deg,#071F12 0%,#145A32 55%,#1E8449 100%); color:#FFFFFF; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; padding:12px 20px; text-align:center; }
.eros-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.85rem; }
.eros-table th { background:linear-gradient(90deg,#EAF5EE,#F4FBF6); color:#071F12; font-weight:700; padding:9px 16px; font-size:0.70rem; text-transform:uppercase; letter-spacing:0.6px; border-bottom:1px solid #C8E6D0; }
.eros-table th.left { text-align:left; } .eros-table th.center { text-align:center; }
.eros-table td { padding:10px 16px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; }
.eros-table td.left { text-align:left; }
.eros-table tr:last-child td { border-bottom:none; background:#F4FBF6; font-weight:800; color:#071F12; }
.eros-table tr:hover td { background:#F4FBF6; }

.faixa-badge { font-weight:800; border-radius:8px; padding:4px 0; font-size:0.83rem; display:inline-block; width:175px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.12); }
.nivel-badge { font-weight:700; border-radius:6px; padding:3px 0; font-size:0.78rem; display:inline-block; width:95px; text-align:center; }
.star-badge  { font-weight:800; border-radius:8px; padding:2px 0; font-size:0.72rem; display:inline-block; width:115px; text-align:center; }

.ctx-bar { background:#FFFFFF; border-radius:10px; padding:10px 18px; margin-bottom:10px; box-shadow:0 2px 10px rgba(7,31,18,0.08); display:flex; align-items:center; gap:28px; flex-wrap:wrap; }
.ctx-item { display:flex; align-items:center; gap:8px; }
.ctx-lbl  { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; color:#145A32; }
.ctx-val  { font-size:0.78rem; font-weight:700; color:#1A2540; }
.ctx-sep  { width:1px; height:20px; background:#C8E6D0; }
.top10-label { font-size:0.72rem; font-weight:700; color:#145A32; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }

.prio-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 4px 24px rgba(7,31,18,0.10),0 1px 4px rgba(0,0,0,0.04); overflow:auto; }
.prio-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.70rem; }
.prio-table th { background:linear-gradient(90deg,#071F12 0%,#145A32 60%,#1A6B3A 100%); color:#FFFFFF; font-weight:700; padding:7px 9px; text-align:center; letter-spacing:0.4px; font-size:0.62rem; text-transform:uppercase; white-space:nowrap; vertical-align:middle; }
.prio-table td { padding:5px 9px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; vertical-align:middle; font-size:0.70rem; }
.prio-table td.left { text-align:left; }
.prio-table tr:last-child td { border-bottom:none; }
.prio-table tr:hover td { background:#F4FBF6; }

.filtros-fila-wrap { background:#FFFFFF; border-radius:14px; padding:18px 24px 14px 24px; box-shadow:0 2px 12px rgba(7,31,18,0.08); margin-bottom:16px; }
.filtros-fila-title { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#145A32; margin-bottom:14px; border-bottom:1px solid #C8E6D0; padding-bottom:8px; }

.raio-header { background:linear-gradient(120deg,#071F12 0%,#0F4023 50%,#1A6B3A 100%); border-radius:16px; padding:24px 30px; box-shadow:0 8px 36px rgba(7,31,18,0.35),0 2px 8px rgba(34,135,74,0.15); margin-bottom:20px; }
.raio-nome { color:#FFFFFF; font-size:1.25rem; font-weight:800; letter-spacing:0.8px; margin-bottom:10px; }
.raio-meta { display:flex; gap:16px; flex-wrap:wrap; align-items:center; }
.raio-tag  { font-size:0.80rem; font-weight:600; color:rgba(255,255,255,0.75); }
.raio-tag strong { color:#FFFFFF; }

.raio-kpi-wrap { background:#FFFFFF; border-radius:12px; padding:14px 18px 12px 18px; box-shadow:0 3px 16px rgba(7,31,18,0.10); position:relative; overflow:hidden; text-align:center; }
.raio-kpi-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0; background:linear-gradient(90deg,#0F4023,#22874A); }
.raio-kpi-lbl { font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:#4B5568; margin-bottom:6px; }
.raio-kpi-val { font-size:1.45rem; font-weight:800; color:#071F12; line-height:1; margin-bottom:4px; }
.raio-kpi-sub { font-size:0.68rem; color:#4B5568; }

.chart-wrap { background:#FFFFFF; border-radius:14px; padding:18px 20px 10px 20px; box-shadow:0 3px 16px rgba(7,31,18,0.08); }
.chart-lbl  { font-size:0.70rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#071F12; text-align:center; margin-bottom:6px; }

.hip-section { background:#FFFFFF; border-radius:14px; padding:22px 26px; box-shadow:0 3px 16px rgba(7,31,18,0.08); }
.hip-section-titulo { font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#071F12; margin-bottom:16px; padding-bottom:10px; border-bottom:2px solid #C8E6D0; }
.hip-list { list-style:none; padding:0; margin:0; }
.hip-list li { display:flex; align-items:flex-start; gap:14px; padding:13px 0; border-bottom:1px solid #F0F4F8; font-size:0.88rem; color:#1A2540; line-height:1.45; }
.hip-list li:last-child { border-bottom:none; padding-bottom:0; }
.hip-bullet { width:11px; height:11px; min-width:11px; background:#C00000; border-radius:50%; margin-top:5px; flex-shrink:0; box-shadow:0 0 0 3px rgba(192,0,0,0.12); }

.missao-card { background:#FFFFFF; border-radius:14px; box-shadow:0 3px 16px rgba(7,31,18,0.08); overflow:hidden; }
.missao-card-header { background:linear-gradient(90deg,#071F12 0%,#145A32 100%); padding:12px 22px; }
.missao-card-header-txt { color:#FFFFFF; font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; }
.missao-objetivo { background:#F4FBF6; border-left:4px solid #1A6B3A; padding:16px 22px; }
.missao-obj-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:6px; }
.missao-obj-txt { font-size:0.90rem; color:#071F12; line-height:1.55; font-weight:500; }
.missao-callout { background:#071F12; padding:16px 22px; }
.missao-call-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.55); margin-bottom:6px; }
.missao-call-txt { font-size:0.93rem; color:#FFFFFF; line-height:1.5; font-weight:600; }
.missao-metrics { display:flex; border-bottom:1px solid #E5EAF2; }
.missao-metric { flex:1; padding:14px 22px; border-right:1px solid #E5EAF2; }
.missao-metric:last-child { border-right:none; }
.missao-metric-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:5px; }
.missao-metric-val { font-size:0.88rem; color:#1A2540; font-weight:600; line-height:1.4; }
.missao-sucesso { display:flex; align-items:flex-start; gap:14px; padding:14px 22px; border-bottom:1px solid #E5EAF2; background:#FAFFFE; }
.missao-suc-ico { width:26px; height:26px; min-width:26px; background:#1A6B3A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:0.85rem; font-weight:800; margin-top:1px; flex-shrink:0; }
.missao-suc-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:4px; }
.missao-suc-txt { font-size:0.85rem; color:#1A2540; line-height:1.45; }
.missao-escala { display:flex; align-items:flex-start; gap:14px; padding:14px 22px; background:#FFF8F8; }
.missao-esc-ico { width:26px; height:26px; min-width:26px; background:#C00000; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:0.90rem; font-weight:800; margin-top:1px; flex-shrink:0; }
.missao-esc-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#C00000; margin-bottom:4px; }
.missao-esc-txt { font-size:0.85rem; color:#1A2540; line-height:1.45; }

.abordagem-bloco { background:linear-gradient(135deg,#EAF5EE,#F4FBF6); border-radius:12px; padding:18px 22px; border-left:4px solid #1A6B3A; }
.abordagem-lbl { font-size:0.68rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:8px; }
.abordagem-txt { font-size:0.88rem; color:#071F12; font-style:italic; line-height:1.6; }

/* ── DIAGNÓSTICO INTERATIVO ── */
.diag-intro { background:#FFFFFF; border-radius:14px; padding:20px 24px; box-shadow:0 3px 16px rgba(7,31,18,0.08); margin-bottom:16px; border-left:4px solid #1A6B3A; }
.diag-intro-txt { font-size:0.88rem; color:#1A2540; line-height:1.5; }

.diag-historico { background:#F4FBF6; border-radius:10px; padding:14px 18px; margin-bottom:14px; }
.diag-historico-titulo { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:10px; }
.diag-hist-item { display:flex; gap:10px; margin-bottom:6px; font-size:0.82rem; color:#1A2540; padding-bottom:6px; border-bottom:1px solid #E5EAF2; }
.diag-hist-item:last-child { border-bottom:none; margin-bottom:0; padding-bottom:0; }
.diag-hist-p { color:#4B5568; flex:1; }
.diag-hist-r { font-weight:700; color:#071F12; }

.diag-pergunta-card { background:#FFFFFF; border-radius:14px; padding:24px 26px; box-shadow:0 4px 20px rgba(7,31,18,0.10); border-top:4px solid #1A6B3A; margin-bottom:16px; }
.diag-step { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:10px; }
.diag-pergunta-txt { font-size:1.0rem; font-weight:600; color:#071F12; line-height:1.5; margin-bottom:0; }

.stButton > button {
    background:#FFFFFF !important;
    border:1.5px solid #C8E6D0 !important;
    border-radius:10px !important;
    color:#071F12 !important;
    font-size:0.85rem !important;
    font-weight:600 !important;
    padding:10px 16px !important;
    width:100% !important;
    text-align:left !important;
    transition:all 0.15s !important;
}
.stButton > button:hover {
    background:#F4FBF6 !important;
    border-color:#1A6B3A !important;
    color:#071F12 !important;
}

.diag-resultado { background:#FFFFFF; border-radius:14px; overflow:hidden; box-shadow:0 4px 24px rgba(7,31,18,0.12); }
.diag-res-header { background:linear-gradient(90deg,#071F12,#145A32); padding:14px 22px; }
.diag-res-header-txt { color:#FFFFFF; font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; }
.diag-res-nome { background:#F4FBF6; padding:18px 22px; border-bottom:1px solid #E5EAF2; }
.diag-res-nome-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:6px; }
.diag-res-nome-val { font-size:1.15rem; font-weight:800; color:#071F12; }
.diag-res-acao { padding:16px 22px; border-bottom:1px solid #E5EAF2; }
.diag-res-acao-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:6px; }
.diag-res-acao-txt { font-size:0.90rem; color:#1A2540; line-height:1.5; }
.diag-res-prazo { padding:14px 22px; border-bottom:1px solid #E5EAF2; background:#FAFFFE; }
.diag-res-prazo-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:5px; }
.diag-res-prazo-val { font-size:0.92rem; font-weight:700; color:#071F12; }
.diag-res-escala { padding:14px 22px; background:#FFF8F8; display:flex; align-items:flex-start; gap:14px; }
.diag-res-escala-ico { width:26px; height:26px; min-width:26px; background:#C00000; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:0.90rem; font-weight:800; flex-shrink:0; }
.diag-res-escala-lbl { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#C00000; margin-bottom:4px; }
.diag-res-escala-txt { font-size:0.85rem; color:#1A2540; line-height:1.4; }
.diag-res-ok { padding:14px 22px; background:#FAFFFE; display:flex; align-items:center; gap:12px; }
.diag-res-ok-ico { width:26px; height:26px; min-width:26px; background:#1A6B3A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:0.85rem; font-weight:800; flex-shrink:0; }
.diag-res-ok-txt { font-size:0.85rem; color:#1A2540; font-weight:600; }

.diag-caminho { background:#F4FBF6; border-radius:10px; padding:14px 18px; margin-top:14px; }
.diag-caminho-titulo { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────
STATUS_CSS = {
    'QUEDA ACENTUADA':       'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 6px;white-space:nowrap;display:inline-block;font-size:0.68rem;',
    'QUEDA':                 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 6px;white-space:nowrap;display:inline-block;font-size:0.68rem;',
    'CRESCIMENTO':           'color:#375623;font-weight:700;',
    'ESTAVEL':               'color:#0070C0;font-weight:700;',
    'INATIVO':               'color:#6B7280;font-weight:700;',
}

FAIXAS_EROSAO = [
    ('EROSÃO STAR 8 A 10', 'CRÍTICO',    '#C00000', '#FFFFFF', lambda s: s >= 8),
    ('EROSÃO STAR 6 A 7',  'ALTO RISCO', '#FFC7CE', '#C00000', lambda s: 6 <= s <= 7),
    ('EROSÃO STAR 4 A 5',  'ATENÇÃO',    '#FFEB9C', '#7A4F00', lambda s: 4 <= s <= 5),
    ('EROSÃO STAR 1 A 3',  'BAIXA',      '#C6EFCE', '#375623', lambda s: s <= 3),
]

NIVEL_MAP = {
    'CRITICO':    lambda s: s >= 8,
    'ALTO RISCO': lambda s: 6 <= s <= 7,
    'ATENCAO':    lambda s: 4 <= s <= 5,
    'BAIXA':      lambda s: s <= 3,
}

HIPOTESES = {
    'QUEDA ACENTUADA':       ['Perda parcial ou total de share para concorrente', 'Retração do mercado ou queda de demanda final', 'Estoque elevado no cliente', 'Problema comercial: preço, prazo, entrega ou atendimento', 'Mudança interna no cliente — gestor, mix ou operação', 'Sazonalidade pontual', 'Causa ainda não identificada'],
    'QUEDA':                 ['Redução gradual de frequência de compra', 'Redução de mix comprado', 'Sinal inicial de diversificação de fornecedores', 'Ajuste de estoque pontual', 'Ponto comercial sensível emergindo', 'Risco de evolução para Queda Acentuada'],
    'ESTAVEL':               ['Conta protegida e vínculo preservado', 'Risco oculto não identificado nos números', 'Satisfação sensível com ponto de melhoria', 'Oportunidade de expansão de mix não explorada', 'Pressão concorrencial em andamento silencioso', 'Erosão relacional sem reflexo ainda no volume'],
    'CRESCIMENTO':           ['Crescimento recorrente por aumento real de demanda', 'Crescimento pontual — não repetível', 'Expansão de mix com novos itens', 'Falha temporária de concorrente', 'Oportunidade estratégica de conta', 'Crescimento vulnerável à retomada da concorrência'],
    'CRESCIMENTO ACENTUADO': ['Crescimento recorrente por aumento real de demanda', 'Expansão operacional do cliente', 'Falha de concorrente — janela de oportunidade', 'Oportunidade estratégica — possível contrato maior', 'Crescimento pontual superestimado', 'Crescimento vulnerável — concorrência retornará'],
    'INATIVO':               ['Inativo recuperável — demanda ainda existe', 'Estoque elevado temporariamente', 'Ruptura comercial: preço, condição ou atendimento', 'Perda estrutural — concorrente consolidado', 'Mudança operacional ou de segmento', 'Relacionamento enfraquecido ao longo do tempo', 'Inativo sem potencial real de retomada'],
}

MISSAO = {
    'QUEDA ACENTUADA': {'objetivo': 'Diagnosticar a causa da queda e tentar recuperar volume prioritário no menor prazo possível.', 'missao': 'A missão não é vender imediatamente. A missão é entender a causa da queda.', 'reavaliacao': '7 dias após o primeiro contato', 'sucesso': 'Retomada parcial, causa identificada ou plano de recuperação definido.', 'escala': 'O cliente citar concorrente como causa da queda; a queda for superior a 30%; não houver avanço concreto após 7 dias.', 'abordagem': '"Percebemos uma mudança no comportamento de compras dos últimos meses e gostaríamos de entender melhor o contexto da operação antes de pensar em qualquer ação comercial."'},
    'QUEDA':           {'objetivo': 'Detectar e corrigir erosão silenciosa antes que o cliente evolua para Queda Acentuada.', 'missao': 'Entender o que começou a mudar. Investigar frequência, mix, share, giro e qualidade relacional.', 'reavaliacao': '15 dias após o contato', 'sucesso': 'Cliente estabilizou, causa identificada ou plano preventivo definido.', 'escala': 'A queda aumentar no próximo ciclo; o cliente mencionar outro fornecedor; um problema comercial for identificado.', 'abordagem': '"Percebemos uma pequena redução no volume recente. Houve alguma mudança no movimento, no giro ou na necessidade de compra?"'},
    'ESTAVEL':         {'objetivo': 'Blindar a conta, validar a qualidade do vínculo e impedir erosão futura.', 'missao': 'Validar se a estabilidade é real ou apenas aparente. Identificar riscos ocultos e oportunidades incrementais.', 'reavaliacao': '30 dias', 'sucesso': 'Vínculo preservado, risco oculto descartado, cliente mantido no patamar.', 'escala': 'O cliente mencionar concorrente ou sinalizar insatisfação; houver redução de mix ou frequência no próximo ciclo.', 'abordagem': '"O volume atual de compras continua adequado para a operação de vocês? Existe algum ponto que possamos melhorar?"'},
    'CRESCIMENTO':     {'objetivo': 'Consolidar o avanço, proteger a conta e transformar o crescimento em novo patamar sustentável.', 'missao': 'Descobrir o que gerou o crescimento e avaliar se é recorrente, pontual, vulnerável ou expansível.', 'reavaliacao': '30 dias', 'sucesso': 'Cliente mantém novo patamar, amplia mix ou confirma recorrência.', 'escala': 'O crescimento indicar oportunidade estratégica maior; houver risco concreto de retomada pela concorrência.', 'abordagem': '"O que explica o aumento recente no volume de compra? Esse novo volume tende a se manter?"'},
    'CRESCIMENTO ACENTUADO': {'objetivo': 'Consolidar o avanço com urgência, proteger a conta e identificar oportunidade estratégica.', 'missao': 'Entender o motor do crescimento acentuado e blindar a conta antes que a concorrência reaja.', 'reavaliacao': '15 a 30 dias', 'sucesso': 'Cliente mantém patamar, confirma recorrência, oportunidade consolidada.', 'escala': 'O crescimento indicar possibilidade de contrato ou volume maior; houver sinal de retomada da concorrência.', 'abordagem': '"Percebemos um crescimento expressivo nos últimos meses. O que está puxando esse aumento e como podemos garantir continuidade?"'},
    'INATIVO':         {'objetivo': 'Validar possibilidade real de recuperação antes de qualquer ação comercial.', 'missao': 'Descobrir se existe possibilidade concreta de retomada. Não ofertar produto na primeira interação.', 'reavaliacao': '15 a 30 dias', 'sucesso': 'Cliente demonstra intenção real de retomada.', 'escala': 'O cliente for Curva A estratégico; houver sinal claro de recuperabilidade com obstáculo comercial identificado; o relacionamento estiver rompido por causa comercial corrigível.', 'abordagem': '"O que levou à interrupção das compras? A demanda relacionada aos nossos produtos continua existindo?"'},
}

PRAZOS = {
    'QUEDA ACENTUADA':       {'A': '24 a 48 horas', 'B': 'até 5 dias úteis', 'C': 'até 10 dias úteis'},
    'QUEDA':                 {'A': 'até 3 dias úteis', 'B': 'até 7 dias úteis', 'C': 'ciclo mensal'},
    'ESTAVEL':               {'A': 'dentro do ciclo mensal', 'B': 'ciclo mensal', 'C': 'gestão padronizada'},
    'CRESCIMENTO':           {'A': 'dentro do ciclo mensal', 'B': 'ciclo mensal', 'C': 'gestão padronizada'},
    'CRESCIMENTO ACENTUADO': {'A': 'até 5 dias úteis', 'B': 'até 10 dias úteis', 'C': 'ciclo mensal'},
    'INATIVO':               {'A': 'imediato — até 48 horas', 'B': 'até 10 dias úteis', 'C': 'análise de recuperabilidade'},
}


# ── ÁRVORE ADAPTATIVA ────────────────────────────────────────────────────
def _d(nome, acao, pa, pb, pc, escalar=False):
    return {'tipo': 'diagnostico', 'nome': nome, 'acao': acao,
            'prazo': {'A': pa, 'B': pb, 'C': pc}, 'escalar': escalar}


def _q(texto, *opcoes):
    return {'tipo': 'pergunta', 'texto': texto,
            'opcoes': [{'texto': t, 'proximo': p} for t, p in opcoes]}


ARVORE = {

    # ── QUEDA ACENTUADA ───────────────────────────────────────────────────
    'QUEDA ACENTUADA': {
        'A': _q(
            "Percebemos uma redução relevante no volume recente e gostaríamos de entender melhor o contexto atual da operação de vocês. O movimento da empresa mudou nos últimos meses?",
            ("Sim, o movimento caiu",
             _q("Essa redução está relacionada ao mercado como um todo, à operação interna ou especificamente a essa categoria?",
                ("Ao mercado como um todo",
                 _q("Vocês acreditam que essa retração é temporária ou tende a continuar?",
                    ("Temporária — esperamos recuperação",
                     _d("Retração temporária / Sazonalidade",
                        "Ajustar expectativa de volume, manter contato ativo e reavaliar no próximo ciclo.",
                        "15 dias", "30 dias", "Próximo ciclo")),
                    ("Tende a continuar",
                     _d("Retração estrutural",
                        "Redefinir mix, ajustar meta e monitorar recuperação do mercado.",
                        "15 dias", "30 dias", "Próximo ciclo")))),
                ("Especificamente nessa categoria",
                 _q("Essa categoria perdeu giro ou parte da demanda passou para outro fornecedor?",
                    ("Perdeu giro — demanda caiu",
                     _d("Redução de demanda",
                        "Revisar mix, identificar categorias com giro e propor reposicionamento.",
                        "7 dias", "15 dias", "Próximo ciclo")),
                    ("Passou para outro fornecedor",
                     _d("Perda para concorrente",
                        "Levantar itens perdidos, revisar proposta comercial e acionar gestor.",
                        "7 dias", "15 dias", "Próximo contato", True)))))),
            ("Não, o movimento continua normal",
             _q("Parte dessa demanda passou a ser atendida por outro fornecedor?",
                ("Sim",
                 _q("O principal fator foi preço, prazo, atendimento, mix ou disponibilidade?",
                    ("Preço ou prazo",
                     _d("Problema comercial",
                        "Avaliar proposta com contrapartida de volume e acionar gestor.",
                        "7 dias", "15 dias", "Próximo contato", True)),
                    ("Atendimento ou logística",
                     _d("Problema operacional",
                        "Acionar gestor imediatamente e corrigir falha antes de nova oferta.",
                        "48 horas", "5 dias úteis", "Próximo contato", True)),
                    ("Mix ou disponibilidade",
                     _d("Perda para concorrente",
                        "Revisar portfólio, levantar itens perdidos e acionar gestor.",
                        "7 dias", "15 dias", "Próximo contato", True)))),
                ("Não identificado",
                 _q("Existe algum ponto da nossa operação dificultando as compras?",
                    ("Sim, existe ponto claro",
                     _d("Problema operacional",
                        "Identificar e corrigir o ponto crítico antes de retomar abordagem comercial.",
                        "48 horas", "5 dias úteis", "Próximo contato", True)),
                    ("Não percebo problema",
                     _d("Erosão relacional",
                        "Reposicionar conversa, aumentar frequência de contato e validar qualidade do vínculo.",
                        "15 dias", "30 dias", "Próximo ciclo"))))))),
        'B': _q(
            "Percebemos uma queda relevante nas compras recentes. Houve alguma mudança importante na demanda ou na operação?",
            ("Sim, a demanda ou o movimento caiu",
             _q("Essa queda está relacionada ao mercado ou à operação interna?",
                ("Ao mercado",
                 _d("Retração de demanda",
                    "Manter contato ativo e reavaliar quando o mercado mostrar sinais de recuperação.",
                    "15 dias", "30 dias", "Próximo ciclo")),
                ("À operação interna",
                 _d("Mudança operacional",
                    "Mapear mudança interna e identificar novo decisor se necessário.",
                    "15 dias", "30 dias", "Próximo ciclo")))),
            ("Não, passamos a comprar de outro fornecedor",
             _q("O principal fator foi preço, atendimento ou disponibilidade?",
                ("Preço",
                 _d("Problema comercial",
                    "Avaliar proposta e acionar gestor se a conta justificar.",
                    "15 dias", "30 dias", "Próximo contato")),
                ("Atendimento ou disponibilidade",
                 _d("Problema operacional",
                    "Identificar falha e corrigir antes de retomar oferta.",
                    "15 dias", "30 dias", "Próximo contato")))),
            ("Não consigo identificar o motivo",
             _d("Erosão relacional",
                "Reaproximar relacionamento antes de qualquer ação comercial.",
                "15 dias", "30 dias", "Próximo ciclo"))),
        'C': _q(
            "Existe algum motivo principal para a redução recente das compras?",
            ("Estoque alto",
             _d("Estoque elevado",
                "Aguardar giro do estoque. Agendar contato em 15 dias.",
                "15 dias", "30 dias", "Próximo ciclo")),
            ("Compramos de outro fornecedor",
             _d("Perda para concorrente",
                "Registrar e monitorar. Escalonar apenas se houver potencial relevante.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("A demanda caiu",
             _d("Redução de demanda",
                "Monitorar mercado e reavaliar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Problema com nossa empresa",
             _d("Problema comercial",
                "Identificar ponto específico e avaliar se vale ação imediata.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo"))),
    },

    # ── QUEDA ─────────────────────────────────────────────────────────────
    'QUEDA': {
        'A': _q(
            "Percebemos uma pequena redução no volume recente e gostaríamos de entender se houve alguma mudança no comportamento da operação ou da demanda.",
            ("Sim, houve mudança",
             _q("A mudança está mais relacionada ao giro, à frequência ou ao mix?",
                ("Frequência de compra",
                 _q("Vocês passaram a trabalhar com estoques maiores ou o ciclo de reposição mudou?",
                    ("Estoques maiores",
                     _d("Estoque elevado",
                        "Não forçar pedido. Agendar retorno após o prazo de giro.",
                        "15 dias", "30 dias", "Próximo ciclo")),
                    ("Ciclo de reposição mudou",
                     _d("Mudança operacional",
                        "Ajustar cadência de contato ao novo ciclo do cliente.",
                        "15 dias", "30 dias", "Próximo ciclo")))),
                ("Mix comprado",
                 _q("Alguma linha específica perdeu relevância ou foi substituída?",
                    ("Sim, uma linha específica",
                     _d("Redução de mix",
                        "Revisar categorias e levantar oportunidades complementares.",
                        "7 dias", "15 dias", "Próximo ciclo")),
                    ("Pode ter entrada de concorrente",
                     _d("Perda inicial de share",
                        "Investigar itens deslocados, reforçar relacionamento e monitorar.",
                        "7 dias", "15 dias", "Próximo ciclo", True)))),
                ("Não sei identificar",
                 _d("Erosão silenciosa",
                    "Aprofundar investigação no próximo contato. Validar qualidade do vínculo.",
                    "7 dias", "15 dias", "Próximo ciclo")))),
            ("Não identificamos mudança clara",
             _q("Existe algum fornecedor tentando ganhar mais espaço nessa categoria?",
                ("Sim",
                 _d("Pressão concorrencial",
                    "Reforçar relacionamento, revisar posicionamento e monitorar share.",
                    "7 dias", "15 dias", "Próximo ciclo", True)),
                ("Não identificado",
                 _d("Erosão relacional",
                    "Reposicionar conversa e validar qualidade do vínculo no próximo contato.",
                    "15 dias", "30 dias", "Próximo ciclo"))))),
        'B': _q(
            "Percebemos uma redução leve nas compras recentes. Houve alguma mudança importante?",
            ("Sim, o giro ou a frequência caiu",
             _q("A causa parece ser estoque alto, mudança de mix ou pressão de concorrente?",
                ("Estoque alto",
                 _d("Estoque elevado",
                    "Aguardar giro. Retornar em 15 a 30 dias.",
                    "15 dias", "30 dias", "Próximo ciclo")),
                ("Mudança de mix",
                 _d("Redução de mix",
                    "Revisar categorias e identificar oportunidade de reposicionamento.",
                    "15 dias", "30 dias", "Próximo ciclo")),
                ("Pressão de concorrente",
                 _d("Perda inicial de share",
                    "Investigar itens deslocados e reforçar relacionamento.",
                    "15 dias", "30 dias", "Próximo ciclo")))),
            ("Não sei identificar o motivo",
             _d("Erosão relacional",
                "Reaproximar relacionamento e validar vínculo no próximo contato.",
                "15 dias", "30 dias", "Próximo ciclo"))),
        'C': _q(
            "Existe algum motivo específico para a redução recente das compras?",
            ("Estoque alto",
             _d("Estoque elevado",
                "Aguardar giro e retornar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Outro fornecedor",
             _d("Perda inicial de share",
                "Registrar e monitorar.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Não identificado",
             _d("Erosão relacional",
                "Monitorar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo"))),
    },

    # ── ESTÁVEL ───────────────────────────────────────────────────────────
    'ESTAVEL': {
        'A': _q(
            "O volume atual continua adequado para a operação de vocês ou existe algum ponto que possa afetar isso nos próximos meses?",
            ("Existe possível risco",
             _q("Esse risco está mais relacionado ao mercado, à operação de vocês ou ao relacionamento com fornecedores?",
                ("Relacionamento com fornecedores",
                 _q("Existe algum ponto nosso que deveríamos melhorar para continuarmos evoluindo juntos?",
                    ("Sim, existe ponto específico",
                     _d("Satisfação sensível",
                        "Corrigir atrito identificado antes que se transforme em queda.",
                        "7 dias", "15 dias", "Próximo ciclo", True)),
                    ("Não há ponto claro",
                     _d("Erosão relacional",
                        "Reposicionar conversa, aumentar proximidade e validar confiança.",
                        "15 dias", "30 dias", "Próximo ciclo")))),
                ("Mercado ou operação interna",
                 _d("Conta vulnerável",
                    "Registrar alerta e antecipar plano preventivo. Monitorar com atenção.",
                    "15 dias", "30 dias", "Próximo ciclo", True)))),
            ("Não existe risco — está estável",
             _q("Existe espaço para ampliarmos alguma linha, categoria ou frequência?",
                ("Sim, há oportunidade",
                 _d("Oportunidade incremental",
                    "Mapear linha complementar e propor teste controlado.",
                    "7 dias", "15 dias", "Próximo ciclo")),
                ("Não neste momento",
                 _d("Conta protegida",
                    "Manter ciclo de acompanhamento mensal e preservar vínculo.",
                    "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))))),
        'B': _q(
            "O volume atual continua adequado ou existe algo que possa mudar nos próximos meses?",
            ("Existe risco",
             _q("Esse risco envolve concorrência, operação interna ou relacionamento?",
                ("Concorrência",
                 _d("Pressão concorrencial",
                    "Reforçar relacionamento e monitorar share.",
                    "15 dias", "30 dias", "Próximo ciclo")),
                ("Operação ou relacionamento",
                 _d("Conta vulnerável",
                    "Registrar alerta e reavaliar em 30 dias.",
                    "15 dias", "30 dias", "Próximo ciclo")))),
            ("Está bem — sem mudanças previstas",
             _d("Conta protegida",
                "Manter ciclo mensal de acompanhamento.",
                "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))),
        'C': _q(
            "As compras continuam acontecendo normalmente?",
            ("Sim, está normal",
             _d("Conta protegida",
                "Manutenção padronizada. Monitorar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Há mudanças previstas",
             _d("Conta vulnerável",
                "Registrar e monitorar com atenção.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo"))),
    },

    # ── CRESCIMENTO ───────────────────────────────────────────────────────
    'CRESCIMENTO': {
        'A': _q(
            "Percebemos aumento recente nas compras e gostaríamos de entender melhor o que está impulsionando esse crescimento.",
            ("Aumento real de demanda",
             _q("Vocês acreditam que esse crescimento tende a continuar?",
                ("Sim, tende a se manter",
                 _q("Existe espaço para ampliarmos mix, frequência ou categorias?",
                    ("Sim, há espaço",
                     _d("Oportunidade estratégica",
                        "Consolidar novo patamar, ajustar metas e planejar expansão.",
                        "7 dias", "15 dias", "Próximo ciclo")),
                    ("Não neste momento",
                     _d("Crescimento recorrente",
                        "Consolidar novo patamar e acompanhar recorrência.",
                        "Ciclo mensal", "Ciclo mensal", "Próximo ciclo")))),
                ("Não, foi pontual",
                 _d("Crescimento pontual",
                    "Registrar evento e não inflar expectativa futura.",
                    "Ciclo mensal", "Ciclo mensal", "Próximo ciclo")))),
            ("Falha de concorrente",
             _q("Existe risco do concorrente recuperar esse espaço?",
                ("Sim, pode voltar",
                 _d("Crescimento vulnerável",
                    "Blindar relacionamento, revisar condições e garantir abastecimento.",
                    "7 dias", "15 dias", "Próximo ciclo", True)),
                ("Não, ganhamos a conta",
                 _d("Crescimento recorrente",
                    "Consolidar novo patamar e acompanhar recorrência.",
                    "Ciclo mensal", "Ciclo mensal", "Próximo ciclo")))),
            ("Compra pontual ou extraordinária",
             _d("Crescimento pontual",
                "Registrar evento e não inflar expectativa futura.",
                "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))),
        'B': _q(
            "O aumento recente tende a continuar ou foi uma situação pontual?",
            ("Tende a continuar",
             _q("O crescimento veio de aumento de demanda ou de falha do concorrente?",
                ("Aumento de demanda",
                 _d("Crescimento recorrente",
                    "Acompanhar novo patamar e ajustar cadência.",
                    "Ciclo mensal", "Ciclo mensal", "Próximo ciclo")),
                ("Falha do concorrente",
                 _d("Crescimento vulnerável",
                    "Blindar relacionamento antes que o concorrente retorne.",
                    "15 dias", "30 dias", "Próximo ciclo")))),
            ("Foi pontual",
             _d("Crescimento pontual",
                "Registrar e não inflar expectativa futura.",
                "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))),
        'C': _q(
            "O aumento das compras tende a continuar?",
            ("Sim",
             _d("Crescimento recorrente",
                "Monitorar recorrência no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Não, foi pontual",
             _d("Crescimento pontual",
                "Registrar e acompanhar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo"))),
    },

    # ── CRESCIMENTO ACENTUADO ─────────────────────────────────────────────
    'CRESCIMENTO ACENTUADO': {
        'A': _q(
            "O crescimento recente foi bastante expressivo. Gostaríamos de entender melhor o que mudou na operação ou na demanda de vocês.",
            ("Expansão da empresa — novas unidades ou demanda maior",
             _q("Essa expansão é estrutural ou pode ser temporária?",
                ("É estrutural — tende a continuar",
                 _q("Existe espaço para construirmos um plano mais estratégico para acompanhar esse crescimento?",
                    ("Sim, temos interesse",
                     _d("Oportunidade estratégica",
                        "Acionar gestor, construir plano dedicado e revisar metas e abastecimento.",
                        "48 horas", "5 dias úteis", "Ciclo mensal", True)),
                    ("Ainda não, vamos ver",
                     _d("Crescimento recorrente",
                        "Consolidar novo patamar e monitorar evolução.",
                        "7 dias", "15 dias", "Próximo ciclo")))),
                ("Pode ser temporária",
                 _d("Crescimento vulnerável",
                    "Blindar relacionamento e monitorar recorrência antes de ajustar metas.",
                    "7 dias", "15 dias", "Próximo ciclo")))),
            ("Falha de concorrente — janela de oportunidade",
             _d("Crescimento vulnerável",
                "Blindar relacionamento e garantir abastecimento antes que o concorrente retorne.",
                "48 horas", "5 dias úteis", "Próximo ciclo", True)),
            ("Compra extraordinária ou antecipação de estoque",
             _d("Crescimento pontual",
                "Ajustar expectativa e monitorar recorrência no próximo ciclo.",
                "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))),
        'B': _q(
            "O crescimento recente tende a continuar ou foi um movimento específico?",
            ("Tende a continuar — há expansão",
             _q("Existe risco de perda para concorrente?",
                ("Sim",
                 _d("Crescimento vulnerável",
                    "Blindar relacionamento antes que o concorrente reaja.",
                    "7 dias", "15 dias", "Próximo ciclo")),
                ("Não",
                 _d("Crescimento recorrente",
                    "Consolidar novo patamar e avaliar potencial de evolução para Curva A.",
                    "Ciclo mensal", "Ciclo mensal", "Próximo ciclo")))),
            ("Foi um movimento específico",
             _d("Crescimento pontual",
                "Registrar e não inflar expectativa futura.",
                "Ciclo mensal", "Ciclo mensal", "Próximo ciclo"))),
        'C': _q(
            "O aumento recente das compras deve continuar?",
            ("Sim, deve continuar",
             _d("Crescimento recorrente",
                "Monitorar recorrência no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo")),
            ("Não, foi pontual",
             _d("Crescimento pontual",
                "Registrar e acompanhar no próximo ciclo.",
                "Próximo ciclo", "Próximo ciclo", "Próximo ciclo"))),
    },

    # ── INATIVO ───────────────────────────────────────────────────────────
    'INATIVO': {
        'A': _q(
            "Percebemos interrupção nas compras e gostaríamos de entender o que mudou na operação ou no relacionamento nos últimos meses.",
            ("Mudamos de fornecedor",
             _q("O principal fator dessa mudança foi preço, atendimento, disponibilidade ou relacionamento?",
                ("Preço ou condição comercial",
                 _d("Inativo recuperável",
                    "Avaliar proposta de retomada e acionar gestor para definir condição.",
                    "48 horas", "10 dias úteis", "Análise de recuperabilidade", True)),
                ("Atendimento ou disponibilidade",
                 _d("Inativo recuperável",
                    "Identificar falha, corrigir e reaproximar antes de ofertar.",
                    "48 horas", "10 dias úteis", "Análise de recuperabilidade", True)),
                ("Relacionamento",
                 _q("Existe abertura para retomarmos essa conversa e reconstruirmos essa parceria?",
                    ("Sim, há abertura",
                     _d("Inativo recuperável",
                        "Reaproximar antes de vender. Construir plano de retomada gradual.",
                        "48 horas", "10 dias úteis", "Análise de recuperabilidade")),
                    ("Não há abertura",
                     _d("Perda estrutural",
                        "Reduzir prioridade operacional. Manter monitoramento leve.",
                        "Próximo trimestre", "Próximo trimestre", "Baixa prioridade")))))),
            ("A demanda acabou ou mudou",
             _q("Essa redução é temporária ou estrutural?",
                ("Temporária",
                 _d("Inativo recuperável",
                    "Aguardar recuperação da demanda e manter contato leve.",
                    "15 dias", "30 dias", "Análise de recuperabilidade")),
                ("Estrutural",
                 _d("Perda estrutural",
                    "Reduzir prioridade operacional e encerrar ciclo ativo.",
                    "Próximo trimestre", "Próximo trimestre", "Baixa prioridade")))),
            ("Questão interna nossa",
             _d("Mudança operacional",
                "Mapear mudança, identificar novo decisor e reapresentar portfólio.",
                "7 dias", "15 dias", "Análise de recuperabilidade"))),
        'B': _q(
            "O que levou à interrupção das compras nos últimos meses?",
            ("Passamos para outro fornecedor",
             _q("O fator principal foi preço ou atendimento?",
                ("Preço",
                 _d("Inativo recuperável",
                    "Avaliar possibilidade de proposta e validar recuperabilidade.",
                    "7 dias", "10 dias úteis", "Análise de recuperabilidade")),
                ("Atendimento",
                 _d("Inativo recuperável",
                    "Corrigir falha antes de retomar oferta.",
                    "7 dias", "10 dias úteis", "Análise de recuperabilidade")))),
            ("A demanda acabou",
             _d("Perda estrutural",
                "Reduzir prioridade e manter monitoramento leve.",
                "Próximo trimestre", "Próximo trimestre", "Baixa prioridade")),
            ("Mudança interna nossa",
             _d("Mudança operacional",
                "Mapear mudança e avaliar se ainda há potencial de retomada.",
                "15 dias", "30 dias", "Análise de recuperabilidade"))),
        'C': _q(
            "Ainda existe demanda para essa categoria?",
            ("Sim, a demanda existe",
             _d("Inativo recuperável",
                "Validar possibilidade de retomada. Contato leve sem pressão comercial.",
                "Próximo ciclo", "Próximo ciclo", "Baixa prioridade")),
            ("Não, a demanda acabou",
             _d("Perda estrutural",
                "Encerrar ciclo ativo. Monitoramento mínimo.",
                "Baixa prioridade", "Baixa prioridade", "Baixa prioridade"))),
    },
}


# ── FUNÇÕES ───────────────────────────────────────────────────────────────
def calcular_erosao_star(lp, cp):
    try: lp_v, cp_v = float(lp), float(cp)
    except: return 1
    if cp_v <= 0: return 10
    if lp_v <= 0: return 1
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
    if n >= 8:   return '#C00000', '#FFFFFF', 'CRÍTICO'
    elif n >= 6: return '#FFC7CE', '#C00000', 'ALTO RISCO'
    elif n >= 4: return '#FFEB9C', '#7A4F00', 'ATENÇÃO'
    else:        return '#C6EFCE', '#375623', 'BAIXA EROSÃO'


def get_prazo(status, curva):
    return PRAZOS.get(str(status).strip().upper(), {}).get(str(curva).strip().upper(), 'a definir')


def calcular_prioridade(curva, status, erosao, risco):
    c = str(curva).strip().upper()
    s = str(status).strip().upper()
    e = int(erosao); r = float(risco or 0)
    cp = {'A': 25, 'B': 15, 'C': 5}.get(c, 5)
    rp = 15 if r > 20000 else 12 if r > 10000 else 9 if r > 5000 else 6 if r > 1000 else 3 if r > 0 else 0
    p1 = cp + rp
    p2 = 40 if e >= 8 else 32 if e >= 6 else 22 if e >= 4 else 12 if e >= 2 else 5
    p3 = {'QUEDA ACENTUADA': 20, 'INATIVO': 16, 'QUEDA': 14, 'ESTAVEL': 8, 'CRESCIMENTO': 4, 'CRESCIMENTO ACENTUADO': 2}.get(s, 5)
    t = p1 + p2 + p3
    if t >= 70:   return 'PRIORIDADE MÁXIMA',  '#C00000', '#FFFFFF', t
    elif t >= 50: return 'PRIORIDADE ALTA',     '#D44000', '#FFFFFF', t
    elif t >= 30: return 'PRIORIDADE MÉDIA',    '#0056b3', '#FFFFFF', t
    elif t >= 15: return 'PRIORIDADE SELETIVA', '#4B5568', '#FFFFFF', t
    else:         return 'GESTÃO PADRÃO',        '#6B7280', '#FFFFFF', t


def score_ranking(curva, status, erosao, risco):
    c = str(curva).strip().upper(); s = str(status).strip().upper()
    e = int(erosao); r = float(risco or 0)
    cp = {'A': 250, 'B': 150, 'C': 50}.get(c, 50)
    rp = 150 if r > 20000 else 120 if r > 10000 else 90 if r > 5000 else 60 if r > 1000 else 30 if r > 0 else 0
    p1 = cp + rp
    p2 = 400 if e >= 8 else 320 if e >= 6 else 220 if e >= 4 else 120 if e >= 2 else 50
    p3 = {'QUEDA ACENTUADA': 200, 'INATIVO': 160, 'QUEDA': 140, 'ESTAVEL': 80, 'CRESCIMENTO': 40, 'CRESCIMENTO ACENTUADO': 20}.get(s, 50)
    return p1 + p2 + p3


def fmt_num(v):
    try: return f"{int(float(v)):,}".replace(',', '.')
    except: return '0'


def find_col(df, *kw):
    for c in df.columns:
        if all(k in c for k in kw): return c
    return None


def get_arvore_node(status, curva):
    s = str(status).strip().upper()
    c = str(curva).strip().upper()
    tree = ARVORE.get(s, {})
    return tree.get(c, tree.get('B', None))


# ── INTERFACE ─────────────────────────────────────────────────────────────
st.page_link("app.py", label="← Voltar ao Dashboard STAR")

st.markdown("""
<div class="giri-header-int">
  <div class="giri-header-dot">&#9650;</div>
  <div>
    <h1>GIRI | INTELIGÊNCIA DE CARTEIRA</h1>
    <p>PRIORIZAÇÃO OPERACIONAL — ÍNDICE DE EROSÃO STAR — CAMADA 2</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:0.85rem;color:#4B5568;margin-bottom:6px;'>Faça upload da Matriz STAR gerada pelo dashboard (XLSX ou CSV)</p>", unsafe_allow_html=True)
uploaded = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

if not uploaded:
    st.stop()

try:
    df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Erro ao ler arquivo: {e}"); st.stop()

df.columns = [str(c).strip().upper() for c in df.columns]
col_cli  = find_col(df, 'CLIENTE');  col_vend = find_col(df, 'VENDEDOR')
col_curv = find_col(df, 'CURVA');    col_cid  = find_col(df, 'CIDADE')
col_mlp  = find_col(df, 'MEDIA', 'LP'); col_mcp = find_col(df, 'MEDIA', 'CP')
col_sta  = find_col(df, 'STATUS')
meses_cols = [c for c in df.columns if re.match(r'^[A-Z]{3}/\d{2}$', c)]

if not all([col_cli, col_mlp, col_mcp, col_sta]):
    st.error("Arquivo não reconhecido. Faça o download da Matriz STAR pelo dashboard e suba esse arquivo aqui."); st.stop()

df['_EROSAO'] = df.apply(lambda r: calcular_erosao_star(r.get(col_mlp,0), r.get(col_mcp,0)), axis=1)
df['_RISCO']  = df.apply(lambda r: max(0.0, float(r.get(col_mlp,0) or 0) - float(r.get(col_mcp,0) or 0)), axis=1)
df['_SCORE']  = df.apply(lambda r: score_ranking(r.get(col_curv,'C') if col_curv else 'C', r.get(col_sta,''), r['_EROSAO'], r['_RISCO']), axis=1)
df_sorted = df.sort_values('_SCORE', ascending=False).reset_index(drop=True)

st.markdown("<div class='section-title'>FILTROS</div>", unsafe_allow_html=True)
vends   = sorted(df[col_vend].dropna().astype(str).unique().tolist()) if col_vend else []
cidades = sorted(df[col_cid].dropna().astype(str).unique().tolist())  if col_cid  else []
c1, c2, c3 = st.columns(3)
with c1: sel_v = st.selectbox("VENDEDOR", ['Todos'] + vends)
with c2:
    if cidades: sel_cid = st.selectbox("CIDADE", ['Todas'] + cidades)
    else:
        sel_cid = 'Todas'; st.selectbox("CIDADE", ['Todas'], disabled=True)
with c3: sel_curva = st.multiselect("CURVA", ['A','B','C'], default=['A','B','C'])

df_f = df_sorted.copy()
if sel_v != 'Todos' and col_vend:  df_f = df_f[df_f[col_vend].astype(str) == sel_v]
if sel_cid != 'Todas' and col_cid: df_f = df_f[df_f[col_cid].astype(str) == sel_cid]
if sel_curva and col_curv:         df_f = df_f[df_f[col_curv].astype(str).str.upper().isin([c.upper() for c in sel_curva])]

n_total = len(df_f); risco_t = df_f['_RISCO'].sum()

st.markdown("<div class='section-title'>VISÃO GERAL — PRIORIZAÇÃO</div>", unsafe_allow_html=True)
k1, k2 = st.columns(2)
with k1: st.markdown(f"<div class='kpi-wrap green'><div class='kpi-lbl'>CLIENTES NA SELEÇÃO</div><div class='kpi-val'>{n_total}</div><div class='kpi-sub'>na fila de priorização</div></div>", unsafe_allow_html=True)
with k2: st.markdown(f"<div class='kpi-wrap dark'><div class='kpi-lbl'>RECEITA EM RISCO</div><div class='kpi-val'>{fmt_num(risco_t)}</div><div class='kpi-sub'>diferença LP vs CP acumulada</div></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
rows_eros = ""
for fl, nl, bg, fg, fn in FAIXAS_EROSAO:
    n_f = int(df_f[df_f['_EROSAO'].apply(fn)].shape[0])
    pct_f = round(n_f / n_total * 100, 1) if n_total > 0 else 0.0
    rows_eros += f"<tr><td class='left'><span class='faixa-badge' style='background:{bg};color:{fg};'>{fl}</span></td><td><span class='nivel-badge' style='background:{bg};color:{fg};'>{nl}</span></td><td><strong>{n_f}</strong></td><td><strong>{pct_f}%</strong></td></tr>"
rows_eros += f"<tr><td class='left' colspan='2'><strong>TOTAL</strong></td><td><strong>{n_total}</strong></td><td><strong>100%</strong></td></tr>"
st.markdown(f"<div class='erosao-bloco'><div class='erosao-bloco-title'>ÍNDICE DE EROSÃO STAR</div><table class='eros-table'><thead><tr><th class='left'>FAIXA</th><th class='center'>NÍVEL</th><th class='center'>CLIENTES</th><th class='center'>%</th></tr></thead><tbody>{rows_eros}</tbody></table></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>FILA OPERACIONAL DE PRIORIDADE</div>", unsafe_allow_html=True)
st.markdown("<div class='filtros-fila-wrap'><div class='filtros-fila-title'>FILTRAR FILA</div>", unsafe_allow_html=True)
fa, fb, fc, fd = st.columns(4)
with fa: busca   = st.text_input("POR CLIENTE", placeholder="Digite o nome...")
with fb: sel_sta = st.selectbox("POR STATUS", ['Todos os status','QUEDA ACENTUADA','QUEDA','ESTAVEL','CRESCIMENTO','CRESCIMENTO ACENTUADO','INATIVO'])
with fc: sel_ind = st.selectbox("POR ÍNDICE DE EROSÃO STAR", ['Todos','EROSÃO STAR 8 A 10','EROSÃO STAR 6 A 7','EROSÃO STAR 4 A 5','EROSÃO STAR 1 A 3'])
with fd: sel_niv = st.selectbox("POR NÍVEL", ['Todos','CRITICO','ALTO RISCO','ATENCAO','BAIXA'])
st.markdown("</div>", unsafe_allow_html=True)

df_fila = df_f.copy()
if busca.strip():                df_fila = df_fila[df_fila[col_cli].astype(str).str.upper().str.contains(busca.strip().upper(), na=False)]
if sel_sta != 'Todos os status': df_fila = df_fila[df_fila[col_sta].astype(str).str.upper() == sel_sta]
if '8 A 10' in sel_ind:          df_fila = df_fila[df_fila['_EROSAO'] >= 8]
elif '6 A 7' in sel_ind:         df_fila = df_fila[df_fila['_EROSAO'].between(6, 7)]
elif '4 A 5' in sel_ind:         df_fila = df_fila[df_fila['_EROSAO'].between(4, 5)]
elif '1 A 3' in sel_ind:         df_fila = df_fila[df_fila['_EROSAO'] <= 3]
if sel_niv != 'Todos' and sel_niv in NIVEL_MAP:
    df_fila = df_fila[df_fila['_EROSAO'].apply(NIVEL_MAP[sel_niv])]

df_top10 = df_fila.head(10); n_fila = len(df_fila)
ctx_vend  = sel_v if sel_v != 'Todos' else (' + '.join(vends) if vends else 'Todos')
ctx_curva = ' + '.join(sorted(sel_curva)) if sel_curva else 'Nenhuma'
ctx_cid   = sel_cid if sel_cid != 'Todas' else 'Todas'

st.markdown(f"<div class='ctx-bar'><div class='ctx-item'><span class='ctx-lbl'>VENDEDOR</span><span class='ctx-val'>{ctx_vend}</span></div><div class='ctx-sep'></div><div class='ctx-item'><span class='ctx-lbl'>CURVA</span><span class='ctx-val'>{ctx_curva}</span></div><div class='ctx-sep'></div><div class='ctx-item'><span class='ctx-lbl'>CIDADE</span><span class='ctx-val'>{ctx_cid}</span></div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='top10-label'>EXIBINDO TOP 10 DE {n_fila} CLIENTES PRIORIZADOS</div>", unsafe_allow_html=True)

if not df_top10.empty:
    rows_html = ""
    for i, (_, r) in enumerate(df_top10.iterrows(), 1):
        en = int(r['_EROSAO']); ebg, efg, _ = erosao_display(en)
        sta = str(r.get(col_sta,'')).strip().upper()
        scss = STATUS_CSS.get(sta, 'color:#1A2540;font-weight:600;')
        nome = str(r.get(col_cli,''))
        p_lbl, p_bg, p_fg, _ = calcular_prioridade(r.get(col_curv,'C') if col_curv else 'C', sta, en, r['_RISCO'])
        rows_html += (f"<tr><td><strong>#{i}</strong></td><td class='left'><strong>{nome}</strong></td>"
            f"<td><span style='{scss}'>{sta}</span></td>"
            f"<td><span class='star-badge' style='background:{ebg};color:{efg};'>EROSÃO STAR {en}</span></td>"
            f"<td><span style='background:{p_bg};color:{p_fg};font-weight:700;border-radius:6px;padding:2px 8px;font-size:0.68rem;white-space:nowrap;display:inline-block;'>{p_lbl}</span></td>"
            f"<td>{fmt_num(r.get(col_mlp,0))}</td><td>{fmt_num(r.get(col_mcp,0))}</td>"
            f"<td style='color:#C00000;font-weight:700;'>{fmt_num(r['_RISCO'])}</td></tr>")
    st.markdown(f"<div class='prio-wrap'><table class='prio-table'><thead><tr><th>#</th><th>CLIENTE</th><th>STATUS</th><th>ÍNDICE EROSÃO</th><th>PRIORIDADE</th><th>MÉDIA LP</th><th>MÉDIA CP</th><th>RISCO</th></tr></thead><tbody>{rows_html}</tbody></table></div>", unsafe_allow_html=True)
else:
    st.info("Nenhum cliente encontrado para os filtros selecionados.")

# ════════════════════════════════════════════════════════════════════════
# RAIO-X
# ════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>RAIO-X DO CLIENTE</div>", unsafe_allow_html=True)

if df_fila.empty:
    st.info("Aplique os filtros acima para visualizar clientes disponíveis para o Raio-X."); st.stop()

nomes_lista = ['Selecione um cliente...'] + df_fila[col_cli].astype(str).tolist()
sel_cliente = st.selectbox("SELECIONAR CLIENTE", nomes_lista)
if sel_cliente == 'Selecione um cliente...': st.stop()

row    = df_fila[df_fila[col_cli].astype(str) == sel_cliente].iloc[0]
r_nome = str(row.get(col_cli,''))
r_vend = str(row.get(col_vend,'')) if col_vend else '—'
r_curv = str(row.get(col_curv,'')) if col_curv else '—'
r_sta  = str(row.get(col_sta,'')).strip().upper()
r_mlp  = float(row.get(col_mlp,0) or 0); r_mcp = float(row.get(col_mcp,0) or 0)
r_eros = int(row['_EROSAO']); r_risco = float(row['_RISCO'])
r_diff = round(((r_mlp - r_mcp) / r_mlp * 100), 1) if r_mlp > 0 else 0.0

ebg, efg, elbl              = erosao_display(r_eros)
p_lbl, p_bg, p_fg, p_score = calcular_prioridade(r_curv, r_sta, r_eros, r_risco)
sta_css                     = STATUS_CSS.get(r_sta, '')
prazo_dinamico              = get_prazo(r_sta, r_curv)

st.markdown(f"""
<div class='raio-header'>
  <div class='raio-nome'>{r_nome}</div>
  <div class='raio-meta'>
    <div class='raio-tag'>Vendedor: <strong>{r_vend}</strong></div>
    <div class='raio-tag'>Curva: <strong>{r_curv}</strong></div>
    <div class='raio-tag'><span style='{sta_css}'>{r_sta}</span></div>
    <div class='raio-tag'><span style='background:{ebg};color:{efg};font-weight:800;border-radius:8px;padding:3px 12px;font-size:0.85rem;'>EROSÃO STAR {r_eros}</span></div>
    <div class='raio-tag'><span style='background:{p_bg};color:{p_fg};font-weight:700;border-radius:6px;padding:3px 12px;font-size:0.80rem;'>{p_lbl}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

rk1, rk2, rk3, rk4 = st.columns(4)
with rk1: st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>ÍNDICE DE EROSÃO STAR</div><div class='raio-kpi-val'><span style='background:{ebg};color:{efg};border-radius:8px;padding:2px 14px;'>STAR {r_eros}</span></div><div class='raio-kpi-sub'>{elbl}</div></div>", unsafe_allow_html=True)
with rk2: st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>MÉDIA LP</div><div class='raio-kpi-val'>{fmt_num(r_mlp)}</div><div class='raio-kpi-sub'>referência histórica</div></div>", unsafe_allow_html=True)
with rk3:
    cor_cp = '#C00000' if r_mcp < r_mlp * 0.98 else '#1A6B3A'
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>MÉDIA CP</div><div class='raio-kpi-val' style='color:{cor_cp};'>{fmt_num(r_mcp)}</div><div class='raio-kpi-sub'>comportamento recente</div></div>", unsafe_allow_html=True)
with rk4:
    sinal = f"▼ {r_diff}% abaixo da média" if r_diff > 0 else f"▲ {abs(r_diff)}% acima da média"
    cor_r = '#C00000' if r_diff > 0 else '#1A6B3A'
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>RECEITA EM RISCO</div><div class='raio-kpi-val' style='color:{cor_r};'>{fmt_num(r_risco)}</div><div class='raio-kpi-sub'>{sinal}</div></div>", unsafe_allow_html=True)

if meses_cols:
    valores_meses = [float(row.get(m,0) or 0) for m in meses_cols]
    cores_barras  = ['#C00000' if v < r_mlp*0.98 else '#1A6B3A' for v in valores_meses]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=meses_cols, y=valores_meses, marker_color=cores_barras,
        text=[fmt_num(v) for v in valores_meses], textposition='outside',
        textfont=dict(size=10, color='#1A2540')))
    if r_mlp > 0:
        fig.add_hline(y=r_mlp, line_dash='dash', line_color='#145A32', line_width=2,
            annotation_text=f'Média LP: {fmt_num(r_mlp)}',
            annotation_font_color='#145A32', annotation_font_size=11)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=250,
        margin=dict(t=30,b=10,l=10,r=10), showlegend=False,
        yaxis=dict(showgrid=True, gridcolor='#E5EAF2', tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=11, color='#1A2540', family='Arial')))
    st.markdown("<div style='margin-top:16px;'><div class='chart-wrap'><div class='chart-lbl'>HISTÓRICO MENSAL DE COMPRAS</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div></div>", unsafe_allow_html=True)

hips = HIPOTESES.get(r_sta, HIPOTESES.get('ESTAVEL', []))
miss = MISSAO.get(r_sta, MISSAO.get('ESTAVEL', {}))

st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
items_hip = "".join([f"<li><div class='hip-bullet'></div>{h}</li>" for h in hips])
st.markdown(f"<div class='hip-section'><div class='hip-section-titulo'>HIPÓTESES INICIAIS</div><ul class='hip-list'>{items_hip}</ul></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
st.markdown(f"""
<div class='missao-card'>
  <div class='missao-card-header'><div class='missao-card-header-txt'>MISSÃO DO CONTATO</div></div>
  <div class='missao-objetivo'><div class='missao-obj-lbl'>OBJETIVO DO CONTATO</div><div class='missao-obj-txt'>{miss.get('objetivo','—')}</div></div>
  <div class='missao-callout'><div class='missao-call-lbl'>SUA MISSÃO</div><div class='missao-call-txt'>{miss.get('missao','—')}</div></div>
  <div class='missao-metrics'>
    <div class='missao-metric'><div class='missao-metric-lbl'>PRAZO</div><div class='missao-metric-val'>{prazo_dinamico}</div></div>
    <div class='missao-metric'><div class='missao-metric-lbl'>REAVALIAÇÃO</div><div class='missao-metric-val'>{miss.get('reavaliacao','—')}</div></div>
  </div>
  <div class='missao-sucesso'><div class='missao-suc-ico'>&#10003;</div><div><div class='missao-suc-lbl'>CRITÉRIO DE SUCESSO</div><div class='missao-suc-txt'>{miss.get('sucesso','—')}</div></div></div>
  <div class='missao-escala'><div class='missao-esc-ico'>!</div><div><div class='missao-esc-lbl'>ACIONE O GESTOR SE</div><div class='missao-esc-txt'>{miss.get('escala','—')}</div></div></div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

abord = miss.get('abordagem','')
if abord:
    st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='abordagem-bloco'><div class='abordagem-lbl'>LINHA DE ABORDAGEM SUGERIDA</div><div class='abordagem-txt'>{abord}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# DIAGNÓSTICO INTERATIVO
# ════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>DIAGNÓSTICO INTERATIVO</div>", unsafe_allow_html=True)

st.markdown("""
<div class='diag-intro'>
  <div class='diag-intro-txt'>
    Use esta seção <strong>após a ligação</strong> com o cliente. Registre as respostas que ele deu
    e o sistema chegará ao diagnóstico com a ação prescrita e o prazo correspondente.
  </div>
</div>
""", unsafe_allow_html=True)

# Session state por cliente
chave = f"diag_{sel_cliente.replace(' ','_')}"
if st.session_state.get('diag_cliente_ativo') != sel_cliente:
    st.session_state['diag_cliente_ativo'] = sel_cliente
    st.session_state[chave + '_node']    = get_arvore_node(r_sta, r_curv)
    st.session_state[chave + '_hist']    = []

node    = st.session_state.get(chave + '_node')
historico = st.session_state.get(chave + '_hist', [])

if node is None:
    st.info("Árvore de diagnóstico não disponível para esta combinação de status e curva.")
    st.stop()

# Exibe histórico
if historico:
    hist_html = "".join([
        f"<div class='diag-hist-item'>"
        f"<div class='diag-hist-p'>{h['p']}</div>"
        f"<div class='diag-hist-r'>→ {h['r']}</div>"
        f"</div>"
        for h in historico
    ])
    st.markdown(f"<div class='diag-historico'><div class='diag-historico-titulo'>CAMINHO PERCORRIDO</div>{hist_html}</div>", unsafe_allow_html=True)

# Nó atual
if node['tipo'] == 'pergunta':
    step = len(historico) + 1
    st.markdown(
        f"<div class='diag-pergunta-card'>"
        f"<div class='diag-step'>PERGUNTA {step}</div>"
        f"<div class='diag-pergunta-txt'>{node['texto']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )
    for i, opcao in enumerate(node['opcoes']):
        if st.button(opcao['texto'], key=f"{chave}_opt_{step}_{i}"):
            historico.append({'p': node['texto'], 'r': opcao['texto']})
            st.session_state[chave + '_hist'] = historico
            st.session_state[chave + '_node'] = opcao['proximo']
            st.rerun()

elif node['tipo'] == 'diagnostico':
    prazo_diag = node['prazo'].get(r_curv.upper(), node['prazo'].get('B', '—'))
    escalar    = node.get('escalar', False)

    escala_html = (
        f"<div class='diag-res-escala'>"
        f"<div class='diag-res-escala-ico'>!</div>"
        f"<div><div class='diag-res-escala-lbl'>ACIONE O GESTOR</div>"
        f"<div class='diag-res-escala-txt'>Este diagnóstico requer escalonamento imediato.</div></div>"
        f"</div>"
    ) if escalar else (
        f"<div class='diag-res-ok'>"
        f"<div class='diag-res-ok-ico'>&#10003;</div>"
        f"<div class='diag-res-ok-txt'>Gestão direta pelo vendedor — sem necessidade de escalonar.</div>"
        f"</div>"
    )

    st.markdown(f"""
<div class='diag-resultado'>
  <div class='diag-res-header'><div class='diag-res-header-txt'>DIAGNÓSTICO CONCLUÍDO</div></div>
  <div class='diag-res-nome'>
    <div class='diag-res-nome-lbl'>DIAGNÓSTICO</div>
    <div class='diag-res-nome-val'>{node['nome']}</div>
  </div>
  <div class='diag-res-acao'>
    <div class='diag-res-acao-lbl'>AÇÃO PRESCRITA</div>
    <div class='diag-res-acao-txt'>{node['acao']}</div>
  </div>
  <div class='diag-res-prazo'>
    <div class='diag-res-prazo-lbl'>PRAZO — CURVA {r_curv}</div>
    <div class='diag-res-prazo-val'>{prazo_diag}</div>
  </div>
  {escala_html}
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'>", unsafe_allow_html=True)
    if st.button("↺ Reiniciar diagnóstico", key=f"{chave}_restart"):
        st.session_state[chave + '_node'] = get_arvore_node(r_sta, r_curv)
        st.session_state[chave + '_hist'] = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
