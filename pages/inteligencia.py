import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

st.set_page_config(page_title="Giri | Inteligencia de Carteira", layout="wide")

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

/* ── HEADER ── */
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

/* ── KPIs ── */
.kpi-wrap { background:#FFFFFF; border-radius:14px; padding:14px 22px 12px 22px; box-shadow:0 4px 24px rgba(7,31,18,0.10),0 1px 4px rgba(0,0,0,0.04); position:relative; overflow:hidden; text-align:center; }
.kpi-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:4px; border-radius:14px 14px 0 0; }
.kpi-wrap.green::before { background:linear-gradient(90deg,#0F4023,#1A6B3A,#22874A); }
.kpi-wrap.dark::before  { background:linear-gradient(90deg,#071F12,#0F4023,#1A6B3A); }
.kpi-lbl { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#4B5568; margin-bottom:8px; }
.kpi-val { font-size:1.65rem; font-weight:800; line-height:1; margin-bottom:5px; color:#071F12; }
.kpi-sub { font-size:0.72rem; color:#4B5568; line-height:1.4; }

/* ── EROSAO BLOCO ── */
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

/* ── BARRA CONTEXTO ── */
.ctx-bar { background:#FFFFFF; border-radius:10px; padding:10px 18px; margin-bottom:10px; box-shadow:0 2px 10px rgba(7,31,18,0.08); display:flex; align-items:center; gap:28px; flex-wrap:wrap; }
.ctx-item { display:flex; align-items:center; gap:8px; }
.ctx-lbl  { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; color:#145A32; }
.ctx-val  { font-size:0.78rem; font-weight:700; color:#1A2540; }
.ctx-sep  { width:1px; height:20px; background:#C8E6D0; }
.top10-label { font-size:0.72rem; font-weight:700; color:#145A32; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }

/* ── TABELA TOP 10 ── */
.prio-wrap { background:#FFFFFF; border-radius:14px; box-shadow:0 4px 24px rgba(7,31,18,0.10),0 1px 4px rgba(0,0,0,0.04); overflow:auto; }
.prio-table { width:100%; border-collapse:collapse; font-family:Arial; font-size:0.70rem; }
.prio-table th { background:linear-gradient(90deg,#071F12 0%,#145A32 60%,#1A6B3A 100%); color:#FFFFFF; font-weight:700; padding:7px 9px; text-align:center; letter-spacing:0.4px; font-size:0.62rem; text-transform:uppercase; white-space:nowrap; vertical-align:middle; }
.prio-table td { padding:5px 9px; text-align:center; color:#1A2540; border-bottom:1px solid #E5EAF2; font-weight:500; vertical-align:middle; font-size:0.70rem; }
.prio-table td.left { text-align:left; }
.prio-table tr:last-child td { border-bottom:none; }
.prio-table tr:hover td { background:#F4FBF6; }

.filtros-fila-wrap { background:#FFFFFF; border-radius:14px; padding:18px 24px 14px 24px; box-shadow:0 2px 12px rgba(7,31,18,0.08); margin-bottom:16px; }
.filtros-fila-title { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#145A32; margin-bottom:14px; border-bottom:1px solid #C8E6D0; padding-bottom:8px; }

/* ── RAIO-X HEADER ── */
.raio-header { background:linear-gradient(120deg,#071F12 0%,#0F4023 50%,#1A6B3A 100%); border-radius:16px; padding:24px 30px; box-shadow:0 8px 36px rgba(7,31,18,0.35),0 2px 8px rgba(34,135,74,0.15); margin-bottom:20px; }
.raio-nome { color:#FFFFFF; font-size:1.25rem; font-weight:800; letter-spacing:0.8px; margin-bottom:10px; }
.raio-meta { display:flex; gap:16px; flex-wrap:wrap; align-items:center; }
.raio-tag  { font-size:0.80rem; font-weight:600; color:rgba(255,255,255,0.75); }
.raio-tag strong { color:#FFFFFF; }

/* ── RAIO-X KPIs ── */
.raio-kpi-wrap { background:#FFFFFF; border-radius:12px; padding:14px 18px 12px 18px; box-shadow:0 3px 16px rgba(7,31,18,0.10); position:relative; overflow:hidden; text-align:center; }
.raio-kpi-wrap::before { content:""; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0; background:linear-gradient(90deg,#0F4023,#22874A); }
.raio-kpi-lbl { font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:#4B5568; margin-bottom:6px; }
.raio-kpi-val { font-size:1.45rem; font-weight:800; color:#071F12; line-height:1; margin-bottom:4px; }
.raio-kpi-sub { font-size:0.68rem; color:#4B5568; }

/* ── CHART ── */
.chart-wrap { background:#FFFFFF; border-radius:14px; padding:18px 20px 10px 20px; box-shadow:0 3px 16px rgba(7,31,18,0.08); }
.chart-lbl  { font-size:0.70rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#071F12; text-align:center; margin-bottom:6px; }

/* ── HIPOTESES — BULLETS VERMELHOS ── */
.hip-section {
    background:#FFFFFF; border-radius:14px;
    padding:22px 26px;
    box-shadow:0 3px 16px rgba(7,31,18,0.08);
}
.hip-section-titulo {
    font-size:0.72rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1.3px; color:#071F12;
    margin-bottom:16px; padding-bottom:10px;
    border-bottom:2px solid #C8E6D0;
}
.hip-list { list-style:none; padding:0; margin:0; }
.hip-list li {
    display:flex; align-items:flex-start; gap:14px;
    padding:13px 0; border-bottom:1px solid #F0F4F8;
    font-size:0.88rem; color:#1A2540; line-height:1.45;
}
.hip-list li:last-child { border-bottom:none; padding-bottom:0; }
.hip-bullet {
    width:11px; height:11px; min-width:11px;
    background:#C00000; border-radius:50%;
    margin-top:5px; flex-shrink:0;
    box-shadow:0 0 0 3px rgba(192,0,0,0.12);
}

/* ── MISSAO BRIEFING CARD ── */
.missao-card {
    background:#FFFFFF; border-radius:14px;
    box-shadow:0 3px 16px rgba(7,31,18,0.08);
    overflow:hidden;
}
.missao-card-header {
    background:linear-gradient(90deg,#071F12 0%,#145A32 100%);
    padding:12px 22px;
}
.missao-card-header-txt {
    color:#FFFFFF; font-size:0.72rem; font-weight:800;
    text-transform:uppercase; letter-spacing:1.5px;
}
.missao-objetivo {
    background:#F4FBF6; border-left:4px solid #1A6B3A;
    padding:16px 22px;
}
.missao-obj-lbl {
    font-size:0.62rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1px; color:#145A32; margin-bottom:6px;
}
.missao-obj-txt {
    font-size:0.90rem; color:#071F12; line-height:1.55; font-weight:500;
}
.missao-callout {
    background:#071F12; padding:16px 22px;
}
.missao-call-lbl {
    font-size:0.62rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1px; color:rgba(255,255,255,0.55); margin-bottom:6px;
}
.missao-call-txt {
    font-size:0.93rem; color:#FFFFFF; line-height:1.5; font-weight:600;
}
.missao-metrics {
    display:flex; border-bottom:1px solid #E5EAF2;
}
.missao-metric {
    flex:1; padding:14px 22px; border-right:1px solid #E5EAF2;
}
.missao-metric:last-child { border-right:none; }
.missao-metric-lbl {
    font-size:0.62rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1px; color:#145A32; margin-bottom:5px;
}
.missao-metric-val {
    font-size:0.88rem; color:#1A2540; font-weight:600; line-height:1.4;
}
.missao-sucesso {
    display:flex; align-items:flex-start; gap:14px;
    padding:14px 22px; border-bottom:1px solid #E5EAF2;
    background:#FAFFFE;
}
.missao-suc-ico {
    width:26px; height:26px; min-width:26px;
    background:#1A6B3A; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color:#FFFFFF; font-size:0.85rem; font-weight:800;
    margin-top:1px; flex-shrink:0;
}
.missao-suc-lbl {
    font-size:0.62rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1px; color:#145A32; margin-bottom:4px;
}
.missao-suc-txt { font-size:0.85rem; color:#1A2540; line-height:1.45; }
.missao-escala {
    display:flex; align-items:flex-start; gap:14px;
    padding:14px 22px; background:#FFF8F8;
}
.missao-esc-ico {
    width:26px; height:26px; min-width:26px;
    background:#C00000; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color:#FFFFFF; font-size:0.90rem; font-weight:800;
    margin-top:1px; flex-shrink:0;
}
.missao-esc-lbl {
    font-size:0.62rem; font-weight:800; text-transform:uppercase;
    letter-spacing:1px; color:#C00000; margin-bottom:4px;
}
.missao-esc-txt { font-size:0.85rem; color:#1A2540; line-height:1.45; }

/* ── PERGUNTAS ── */
.perg-section { background:#FFFFFF; border-radius:14px; padding:22px 26px; box-shadow:0 3px 16px rgba(7,31,18,0.08); }
.perg-section-titulo { font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:1.3px; color:#071F12; margin-bottom:16px; padding-bottom:10px; border-bottom:2px solid #C8E6D0; }
.perg-bloco { background:#F4FBF6; border-radius:10px; padding:14px 16px; margin-bottom:10px; }
.perg-bloco:last-child { margin-bottom:0; }
.perg-num   { font-size:0.65rem; font-weight:800; color:#145A32; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:5px; }
.perg-txt   { font-size:0.88rem; font-weight:600; color:#071F12; margin-bottom:10px; line-height:1.4; }
.opcao-pill { display:inline-block; background:#FFFFFF; border:1px solid #C8E6D0; border-radius:20px; padding:4px 14px; margin:3px 4px 3px 0; font-size:0.76rem; color:#145A32; font-weight:600; }

/* ── ABORDAGEM ── */
.abordagem-bloco { background:linear-gradient(135deg,#EAF5EE,#F4FBF6); border-radius:12px; padding:18px 22px; border-left:4px solid #1A6B3A; }
.abordagem-lbl { font-size:0.68rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#145A32; margin-bottom:8px; }
.abordagem-txt { font-size:0.88rem; color:#071F12; font-style:italic; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

STATUS_CSS = {
    'QUEDA ACENTUADA':       'background:#FFC7CE;color:#C00000;font-weight:700;border-radius:6px;padding:2px 6px;white-space:nowrap;display:inline-block;font-size:0.68rem;',
    'QUEDA':                 'color:#C00000;font-weight:700;',
    'CRESCIMENTO ACENTUADO': 'background:#C6EFCE;color:#375623;font-weight:700;border-radius:6px;padding:2px 6px;white-space:nowrap;display:inline-block;font-size:0.68rem;',
    'CRESCIMENTO':           'color:#375623;font-weight:700;',
    'ESTAVEL':               'color:#0070C0;font-weight:700;',
    'INATIVO':               'color:#6B7280;font-weight:700;',
}

FAIXAS_EROSAO = [
    ('EROSAO STAR 8 A 10', 'CRITICO',    '#C00000', '#FFFFFF', lambda s: s >= 8),
    ('EROSAO STAR 6 A 7',  'ALTO RISCO', '#FFC7CE', '#C00000', lambda s: 6 <= s <= 7),
    ('EROSAO STAR 4 A 5',  'ATENCAO',    '#FFEB9C', '#7A4F00', lambda s: 4 <= s <= 5),
    ('EROSAO STAR 1 A 3',  'BAIXA',      '#C6EFCE', '#375623', lambda s: s <= 3),
]

NIVEL_MAP = {
    'CRITICO':    lambda s: s >= 8,
    'ALTO RISCO': lambda s: 6 <= s <= 7,
    'ATENCAO':    lambda s: 4 <= s <= 5,
    'BAIXA':      lambda s: s <= 3,
}

HIPOTESES = {
    'QUEDA ACENTUADA': ['Perda parcial ou total de share para concorrente', 'Retracao do mercado ou queda de demanda final', 'Estoque elevado no cliente', 'Problema comercial: preco, prazo, entrega ou atendimento', 'Mudanca interna no cliente (gestor, mix, operacao)', 'Sazonalidade pontual', 'Causa ainda nao identificada'],
    'QUEDA':           ['Reducao gradual de frequencia de compra', 'Reducao de mix comprado', 'Sinal inicial de diversificacao de fornecedores', 'Ajuste de estoque pontual', 'Ponto comercial sensivel emergindo', 'Risco de evolucao para Queda Acentuada'],
    'ESTAVEL':         ['Conta protegida e vinculo preservado', 'Risco oculto nao identificado nos numeros', 'Satisfacao sensivel com ponto de melhoria', 'Oportunidade de expansao de mix nao explorada', 'Pressao concorrencial em andamento silencioso', 'Erosao relacional sem reflexo ainda no volume'],
    'CRESCIMENTO':     ['Crescimento recorrente por aumento real de demanda', 'Crescimento pontual — nao repetivel', 'Expansao de mix com novos itens', 'Falha temporaria de concorrente', 'Oportunidade estrategica de conta', 'Crescimento vulneravel a retomada da concorrencia'],
    'CRESCIMENTO ACENTUADO': ['Crescimento recorrente por aumento real de demanda', 'Expansao operacional do cliente', 'Falha de concorrente — janela de oportunidade', 'Oportunidade estrategica — possivel contrato maior', 'Crescimento pontual superestimado', 'Crescimento vulneravel — concorrencia retornara'],
    'INATIVO':         ['Inativo recuperavel — demanda ainda existe', 'Estoque elevado temporariamente', 'Ruptura comercial: preco, condicao ou atendimento', 'Perda estrutural — concorrente consolidado', 'Mudanca operacional ou de segmento', 'Relacionamento enfraquecido ao longo do tempo', 'Inativo sem potencial real de retomada'],
}

MISSAO = {
    'QUEDA ACENTUADA': {'objetivo': 'Diagnosticar a causa da queda e tentar recuperar volume prioritario no menor prazo possivel.', 'missao': 'A missao nao e vender imediatamente. A missao e entender a causa da queda.', 'prazo': '48 horas — Curva A', 'reavaliacao': '15 dias apos o primeiro contato', 'sucesso': 'Retomada parcial, causa identificada ou plano de recuperacao definido.', 'escala': 'Concorrente identificado, queda superior a 30%, sem avanco apos 15 dias.', 'abordagem': '"Percebemos uma mudanca no comportamento de compras dos ultimos meses e gostariamos de entender melhor o contexto da operacao antes de pensar em qualquer acao comercial."'},
    'QUEDA':           {'objetivo': 'Detectar e corrigir erosao silenciosa antes que o cliente evolua para Queda Acentuada.', 'missao': 'Entender o que comecou a mudar. Investigar frequencia, mix, share, giro e qualidade relacional.', 'prazo': '5 dias uteis — Curva A', 'reavaliacao': '15 a 30 dias apos o contato', 'sucesso': 'Cliente estabilizou, causa identificada ou plano preventivo definido.', 'escala': 'Queda aumenta, cliente cita concorrente, problema comercial aparece.', 'abordagem': '"Percebemos uma pequena reducao no volume recente. Houve alguma mudanca no movimento, no giro ou na necessidade de compra?"'},
    'ESTAVEL':         {'objetivo': 'Blindar a conta, validar qualidade do vinculo e impedir erosao futura.', 'missao': 'Validar se a estabilidade e real ou apenas aparente. Identificar riscos ocultos e oportunidades incrementais.', 'prazo': 'Ciclo mensal — Curva A', 'reavaliacao': '30 dias', 'sucesso': 'Vinculo preservado, risco oculto descartado, cliente mantido no patamar.', 'escala': 'Sinal de concorrencia, reclamacao, reducao de mix, relacao excessivamente transacional.', 'abordagem': '"O volume atual de compras continua adequado para a operacao de voces? Existe algum ponto que possamos melhorar?"'},
    'CRESCIMENTO':     {'objetivo': 'Consolidar o avanco, proteger a conta e transformar crescimento em novo patamar sustentavel.', 'missao': 'Descobrir o que gerou o crescimento e avaliar se e recorrente, pontual, vulneravel ou expansivel.', 'prazo': 'Ciclo mensal — Curva A', 'reavaliacao': '30 dias', 'sucesso': 'Cliente mantem novo patamar, amplia mix ou confirma recorrencia.', 'escala': 'Crescimento associado a oportunidade maior, crescimento vulneravel a concorrencia.', 'abordagem': '"O que explica o aumento recente no volume de compra? Esse novo volume tende a se manter?"'},
    'CRESCIMENTO ACENTUADO': {'objetivo': 'Consolidar o avanco com urgencia, proteger a conta e identificar oportunidade estrategica.', 'missao': 'Entender o motor do crescimento acentuado e blindar a conta antes que a concorrencia reaja.', 'prazo': '5 dias uteis — Curva A em Crescimento Acentuado', 'reavaliacao': '15 a 30 dias', 'sucesso': 'Cliente mantem patamar, confirma recorrencia, oportunidade consolidada.', 'escala': 'Expansao de unidade, possibilidade de contrato maior, crescimento vulneravel.', 'abordagem': '"Percebemos um crescimento expressivo nos ultimos meses. O que esta puxando esse aumento e como podemos garantir continuidade?"'},
    'INATIVO':         {'objetivo': 'Validar possibilidade real de recuperacao antes de qualquer acao comercial.', 'missao': 'Descobrir se existe possibilidade concreta de retomada. Nao ofertar produto na primeira interacao.', 'prazo': 'Curva A: imediato. Curva B: ate 10 dias uteis.', 'reavaliacao': '15 a 30 dias', 'sucesso': 'Cliente demonstra intencao real de retomada.', 'escala': 'Cliente estrategico, ruptura grave, concorrente dominante, potencial relevante.', 'abordagem': '"O que levou a interrupcao das compras? A demanda relacionada aos nossos produtos continua existindo?"'},
}

PERGUNTAS = {
    'QUEDA ACENTUADA': [
        {'p': 'Como esta o movimento da empresa nos ultimos meses?', 'o': ['Caiu claramente', 'Esta parecido com antes', 'Aumentou']},
        {'p': 'Os produtos que voces compram de nos continuam girando bem?', 'o': ['Giro caiu', 'Giro esta normal', 'Giro aumentou']},
        {'p': 'Voces passaram a comprar parte dessa demanda com outro fornecedor?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
        {'p': 'Existe algum ponto nosso dificultando a compra: preco, prazo, entrega, atendimento ou disponibilidade?', 'o': ['Sim, existe problema claro', 'Existe algum incomodo, mas nao e decisivo', 'Nao existe problema percebido']},
        {'p': 'Existe possibilidade de retomarmos parte do volume nos proximos dias ou semanas?', 'o': ['Alta possibilidade', 'Possibilidade media', 'Baixa possibilidade']},
    ],
    'QUEDA': [
        {'p': 'Percebemos uma pequena reducao no volume recente. Houve alguma mudanca no movimento, no giro ou na necessidade de compra?', 'o': ['Sim, houve reducao', 'Nao houve mudanca clara', 'Nao sei avaliar']},
        {'p': 'A frequencia de reposicao continua parecida com a de antes?', 'o': ['Reduziu', 'Esta parecida', 'Aumentou']},
        {'p': 'Algum produto ou categoria deixou de fazer sentido para voces neste momento?', 'o': ['Sim', 'Parcialmente', 'Nao']},
        {'p': 'Alguma parte da demanda passou a ser atendida por outro fornecedor ou outro tipo de produto?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
        {'p': 'O que precisariamos ajustar agora para manter o volume de compra em linha com o historico?', 'o': ['Condicao comercial', 'Mix ou produto', 'Frequencia ou atendimento', 'Nada neste momento']},
    ],
    'ESTAVEL': [
        {'p': 'O volume atual de compras continua adequado para a operacao de voces?', 'o': ['Sim, esta adequado', 'Parcialmente', 'Nao esta adequado']},
        {'p': 'Existe algum ponto que possa afetar as compras nos proximos meses?', 'o': ['Sim', 'Talvez', 'Nao identificado']},
        {'p': 'Hoje existe algum ponto nosso que deveria melhorar: atendimento, prazo, preco, entrega ou suporte?', 'o': ['Sim, existe ponto claro', 'Existe ponto leve', 'Nao ha ponto relevante']},
        {'p': 'Existe alguma linha ou produto que voces ainda nao compram conosco e que faria sentido avaliarmos?', 'o': ['Sim', 'Talvez', 'Nao neste momento']},
        {'p': 'Algum fornecedor tem tentado ocupar mais espaco nessa categoria?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
    ],
    'CRESCIMENTO': [
        {'p': 'O que explica o aumento recente no volume de compra?', 'o': ['Aumento real de demanda', 'Compra pontual', 'Mudanca de mix', 'Nao sei avaliar']},
        {'p': 'Esse novo volume tende a se manter nos proximos meses?', 'o': ['Sim, tende a se manter', 'Talvez', 'Nao, foi pontual']},
        {'p': 'O crescimento veio de produtos que voces ja compravam ou de novas linhas?', 'o': ['Produtos ja comprados', 'Novas linhas', 'Ambos']},
        {'p': 'Existe espaco para ampliarmos alguma linha, frequencia ou categoria?', 'o': ['Sim', 'Talvez', 'Nao neste momento']},
        {'p': 'Algum outro fornecedor esta tentando disputar esse aumento de demanda?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
    ],
    'CRESCIMENTO ACENTUADO': [
        {'p': 'O que explica o aumento expressivo no volume de compra?', 'o': ['Aumento real de demanda', 'Expansao operacional', 'Falha de concorrente', 'Nao sei avaliar']},
        {'p': 'Esse novo patamar de compra tende a se manter nos proximos meses?', 'o': ['Sim, tende a se manter', 'Talvez', 'Nao, foi pontual']},
        {'p': 'Existe espaco para ampliarmos ainda mais alguma linha ou categoria?', 'o': ['Sim', 'Talvez', 'Nao neste momento']},
        {'p': 'Algum concorrente esta tentando retomar esse espaco?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
        {'p': 'Existe possibilidade de formalizarmos um acordo ou condicao de maior volume?', 'o': ['Sim, ha interesse', 'Talvez', 'Nao neste momento']},
    ],
    'INATIVO': [
        {'p': 'O que levou a interrupcao das compras nos ultimos meses?', 'o': ['Mudanca operacional', 'Concorrencia', 'Estoque elevado', 'Problema comercial', 'Sem motivo claro']},
        {'p': 'A demanda relacionada aos nossos produtos continua existindo hoje?', 'o': ['Sim', 'Parcialmente', 'Nao']},
        {'p': 'Existe abertura para retomarmos conversa comercial sobre essa categoria?', 'o': ['Sim', 'Talvez', 'Nao']},
        {'p': 'Hoje essa demanda esta concentrada em outro fornecedor?', 'o': ['Sim', 'Parcialmente', 'Nao identificado']},
        {'p': 'O que precisaria acontecer para retomarmos essa parceria?', 'o': ['Ajuste comercial', 'Atendimento', 'Mix ou produto', 'Nada especifico', 'Nao ha interesse']},
    ],
}


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
    if n >= 8:   return '#C00000', '#FFFFFF', 'CRITICO'
    elif n >= 6: return '#FFC7CE', '#C00000', 'ALTO RISCO'
    elif n >= 4: return '#FFEB9C', '#7A4F00', 'ATENCAO'
    else:        return '#C6EFCE', '#375623', 'BAIXA EROSAO'


def sinal_prioridade(curva, status):
    c = str(curva).strip().upper()
    s = str(status).strip().upper()
    if c == 'A' and s in ['QUEDA ACENTUADA', 'QUEDA', 'INATIVO']:
        return 'PRIORIDADE MAXIMA', '#C00000', '#FFFFFF'
    elif c == 'A':
        return 'PRIORIDADE ALTA', '#D44000', '#FFFFFF'
    elif c == 'B' and s in ['QUEDA ACENTUADA', 'QUEDA']:
        return 'PRIORIDADE MEDIA', '#0056b3', '#FFFFFF'
    elif c == 'B':
        return 'PRIORIDADE SELETIVA', '#4B5568', '#FFFFFF'
    else:
        return 'GESTAO PADRAO', '#6B7280', '#FFFFFF'


def score_prioridade(curva, status, erosao, media_lp):
    cp = {'A': 300, 'B': 150, 'C': 50}.get(str(curva).strip().upper(), 30)
    sp = {'QUEDA ACENTUADA': 500, 'QUEDA': 350, 'INATIVO': 280, 'ESTAVEL': 150, 'CRESCIMENTO': 80, 'CRESCIMENTO ACENTUADO': 50}.get(str(status).strip().upper(), 50)
    ep = int(erosao) * 20
    rp = min(float(media_lp or 0) / 100, 300)
    return cp + sp + ep + rp


def fmt_num(v):
    try: return f"{int(float(v)):,}".replace(',', '.')
    except: return '0'


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
st.markdown("<p style='font-size:0.85rem;color:#4B5568;margin-bottom:6px;'>Faca upload da Matriz STAR gerada pelo dashboard (XLSX ou CSV)</p>", unsafe_allow_html=True)
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
col_cid  = find_col(df, 'CIDADE')
col_mlp  = find_col(df, 'MEDIA', 'LP')
col_mcp  = find_col(df, 'MEDIA', 'CP')
col_sta  = find_col(df, 'STATUS')
meses_cols = [c for c in df.columns if re.match(r'^[A-Z]{3}/\d{2}$', c)]

if not all([col_cli, col_mlp, col_mcp, col_sta]):
    st.error("Arquivo nao reconhecido. Faca o download da Matriz STAR pelo dashboard e suba esse arquivo aqui.")
    st.stop()

df['_EROSAO'] = df.apply(lambda r: calcular_erosao_star(r.get(col_mlp, 0), r.get(col_mcp, 0)), axis=1)
df['_SCORE']  = df.apply(lambda r: score_prioridade(
    r.get(col_curv, 'C') if col_curv else 'C',
    r.get(col_sta, ''), r['_EROSAO'], r.get(col_mlp, 0)), axis=1)
df['_RISCO']  = df.apply(lambda r: max(0.0, float(r.get(col_mlp, 0) or 0) - float(r.get(col_mcp, 0) or 0)), axis=1)
df_sorted = df.sort_values('_SCORE', ascending=False).reset_index(drop=True)

# ── FILTROS GERAIS ────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>FILTROS</div>", unsafe_allow_html=True)
vends   = sorted(df[col_vend].dropna().astype(str).unique().tolist()) if col_vend else []
cidades = sorted(df[col_cid].dropna().astype(str).unique().tolist())  if col_cid  else []
c1, c2, c3 = st.columns(3)
with c1: sel_v     = st.selectbox("VENDEDOR", ['Todos'] + vends)
with c2:
    if cidades: sel_cid = st.selectbox("CIDADE", ['Todas'] + cidades)
    else:
        sel_cid = 'Todas'
        st.selectbox("CIDADE", ['Todas'], disabled=True)
with c3: sel_curva = st.multiselect("CURVA", ['A','B','C'], default=['A','B','C'])

df_f = df_sorted.copy()
if sel_v != 'Todos' and col_vend:  df_f = df_f[df_f[col_vend].astype(str) == sel_v]
if sel_cid != 'Todas' and col_cid: df_f = df_f[df_f[col_cid].astype(str) == sel_cid]
if sel_curva and col_curv:         df_f = df_f[df_f[col_curv].astype(str).str.upper().isin([c.upper() for c in sel_curva])]

n_total = len(df_f)
risco_t = df_f['_RISCO'].sum()

# ── VISAO GERAL ──────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>VISAO GERAL — PRIORIZACAO</div>", unsafe_allow_html=True)
k1, k2 = st.columns(2)
with k1:
    st.markdown(f"<div class='kpi-wrap green'><div class='kpi-lbl'>CLIENTES NA SELECAO</div><div class='kpi-val'>{n_total}</div><div class='kpi-sub'>na fila de priorizacao</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-wrap dark'><div class='kpi-lbl'>RECEITA EM RISCO</div><div class='kpi-val'>{fmt_num(risco_t)}</div><div class='kpi-sub'>diferenca LP vs CP acumulada</div></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
rows_eros = ""
for fl, nl, bg, fg, fn in FAIXAS_EROSAO:
    n_f   = int(df_f[df_f['_EROSAO'].apply(fn)].shape[0])
    pct_f = round(n_f / n_total * 100, 1) if n_total > 0 else 0.0
    rows_eros += f"<tr><td class='left'><span class='faixa-badge' style='background:{bg};color:{fg};'>{fl}</span></td><td><span class='nivel-badge' style='background:{bg};color:{fg};'>{nl}</span></td><td><strong>{n_f}</strong></td><td><strong>{pct_f}%</strong></td></tr>"
rows_eros += f"<tr><td class='left' colspan='2'><strong>TOTAL</strong></td><td><strong>{n_total}</strong></td><td><strong>100%</strong></td></tr>"
st.markdown(f"<div class='erosao-bloco'><div class='erosao-bloco-title'>INDICE DE EROSAO STAR</div><table class='eros-table'><thead><tr><th class='left'>FAIXA</th><th class='center'>NIVEL</th><th class='center'>CLIENTES</th><th class='center'>%</th></tr></thead><tbody>{rows_eros}</tbody></table></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── FILA ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>FILA OPERACIONAL DE PRIORIDADE</div>", unsafe_allow_html=True)
st.markdown("<div class='filtros-fila-wrap'><div class='filtros-fila-title'>FILTRAR FILA</div>", unsafe_allow_html=True)
fa, fb, fc, fd = st.columns(4)
s_opts = ['Todos os status', 'QUEDA ACENTUADA', 'QUEDA', 'ESTAVEL', 'CRESCIMENTO', 'CRESCIMENTO ACENTUADO', 'INATIVO']
i_opts = ['Todos', 'EROSAO STAR 8 A 10', 'EROSAO STAR 6 A 7', 'EROSAO STAR 4 A 5', 'EROSAO STAR 1 A 3']
n_opts = ['Todos', 'CRITICO', 'ALTO RISCO', 'ATENCAO', 'BAIXA']
with fa: busca   = st.text_input("POR CLIENTE", placeholder="Digite o nome...")
with fb: sel_sta = st.selectbox("POR STATUS", s_opts)
with fc: sel_ind = st.selectbox("POR INDICE DE EROSAO STAR", i_opts)
with fd: sel_niv = st.selectbox("POR NIVEL", n_opts)
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

df_top10 = df_fila.head(10)
n_fila   = len(df_fila)

ctx_vend  = sel_v if sel_v != 'Todos' else (' + '.join(vends) if vends else 'Todos')
ctx_curva = ' + '.join(sorted(sel_curva)) if sel_curva else 'Nenhuma'
ctx_cid   = sel_cid if sel_cid != 'Todas' else 'Todas'

st.markdown(
    f"<div class='ctx-bar'>"
    f"<div class='ctx-item'><span class='ctx-lbl'>VENDEDOR</span><span class='ctx-val'>{ctx_vend}</span></div>"
    f"<div class='ctx-sep'></div>"
    f"<div class='ctx-item'><span class='ctx-lbl'>CURVA</span><span class='ctx-val'>{ctx_curva}</span></div>"
    f"<div class='ctx-sep'></div>"
    f"<div class='ctx-item'><span class='ctx-lbl'>CIDADE</span><span class='ctx-val'>{ctx_cid}</span></div>"
    f"</div>",
    unsafe_allow_html=True
)
st.markdown(f"<div class='top10-label'>EXIBINDO TOP 10 DE {n_fila} CLIENTES PRIORIZADOS</div>", unsafe_allow_html=True)

if not df_top10.empty:
    rows_html = ""
    for i, (_, r) in enumerate(df_top10.iterrows(), 1):
        en = int(r['_EROSAO']); ebg, efg, elbl = erosao_display(en)
        sta  = str(r.get(col_sta, '')).strip().upper()
        scss = STATUS_CSS.get(sta, 'color:#1A2540;font-weight:600;')
        nome = str(r.get(col_cli, ''))
        rows_html += (
            f"<tr><td><strong>#{i}</strong></td>"
            f"<td class='left'><strong>{nome}</strong></td>"
            f"<td><span style='{scss}'>{sta}</span></td>"
            f"<td><span class='star-badge' style='background:{ebg};color:{efg};'>EROSAO STAR {en}</span></td>"
            f"<td><span class='nivel-badge' style='background:{ebg};color:{efg};'>{elbl}</span></td>"
            f"<td>{fmt_num(r.get(col_mlp,0))}</td>"
            f"<td>{fmt_num(r.get(col_mcp,0))}</td>"
            f"<td style='color:#C00000;font-weight:700;'>{fmt_num(r['_RISCO'])}</td></tr>"
        )
    st.markdown(
        f"<div class='prio-wrap'><table class='prio-table'>"
        f"<thead><tr><th>#</th><th>CLIENTE</th><th>STATUS</th>"
        f"<th>INDICE EROSAO</th><th>NIVEL</th>"
        f"<th>MEDIA LP</th><th>MEDIA CP</th><th>RISCO</th>"
        f"</tr></thead><tbody>{rows_html}</tbody></table></div>",
        unsafe_allow_html=True
    )
else:
    st.info("Nenhum cliente encontrado para os filtros selecionados.")

# ════════════════════════════════════════════════════════════════════════
# RAIO-X
# ════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>RAIO-X DO CLIENTE</div>", unsafe_allow_html=True)

if df_fila.empty:
    st.info("Aplique os filtros acima para visualizar clientes disponiveis para o Raio-X.")
    st.stop()

nomes_lista = ['Selecione um cliente...'] + df_fila[col_cli].astype(str).tolist()
sel_cliente = st.selectbox("SELECIONAR CLIENTE", nomes_lista)

if sel_cliente == 'Selecione um cliente...':
    st.stop()

row    = df_fila[df_fila[col_cli].astype(str) == sel_cliente].iloc[0]
r_nome = str(row.get(col_cli, ''))
r_vend = str(row.get(col_vend, '')) if col_vend else '—'
r_curv = str(row.get(col_curv, '')) if col_curv else '—'
r_sta  = str(row.get(col_sta, '')).strip().upper()
r_mlp  = float(row.get(col_mlp, 0) or 0)
r_mcp  = float(row.get(col_mcp, 0) or 0)
r_eros = int(row['_EROSAO'])
r_risco= float(row['_RISCO'])
r_diff = round(((r_mlp - r_mcp) / r_mlp * 100), 1) if r_mlp > 0 else 0.0

ebg, efg, elbl    = erosao_display(r_eros)
p_lbl, p_bg, p_fg = sinal_prioridade(r_curv, r_sta)
sta_css            = STATUS_CSS.get(r_sta, '')

# Cabeçalho
st.markdown(f"""
<div class='raio-header'>
  <div class='raio-nome'>{r_nome}</div>
  <div class='raio-meta'>
    <div class='raio-tag'>Vendedor: <strong>{r_vend}</strong></div>
    <div class='raio-tag'>Curva: <strong>{r_curv}</strong></div>
    <div class='raio-tag'><span style='{sta_css}'>{r_sta}</span></div>
    <div class='raio-tag'><span style='background:{ebg};color:{efg};font-weight:800;border-radius:8px;padding:3px 12px;font-size:0.85rem;'>EROSAO STAR {r_eros}</span></div>
    <div class='raio-tag'><span style='background:{p_bg};color:{p_fg};font-weight:700;border-radius:6px;padding:3px 12px;font-size:0.80rem;'>{p_lbl}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPIs
rk1, rk2, rk3, rk4 = st.columns(4)
with rk1:
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>INDICE DE EROSAO STAR</div><div class='raio-kpi-val'><span style='background:{ebg};color:{efg};border-radius:8px;padding:2px 14px;'>STAR {r_eros}</span></div><div class='raio-kpi-sub'>{elbl}</div></div>", unsafe_allow_html=True)
with rk2:
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>MEDIA LP</div><div class='raio-kpi-val'>{fmt_num(r_mlp)}</div><div class='raio-kpi-sub'>referencia historica</div></div>", unsafe_allow_html=True)
with rk3:
    cor_cp = '#C00000' if r_mcp < r_mlp * 0.98 else '#1A6B3A'
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>MEDIA CP</div><div class='raio-kpi-val' style='color:{cor_cp};'>{fmt_num(r_mcp)}</div><div class='raio-kpi-sub'>comportamento recente</div></div>", unsafe_allow_html=True)
with rk4:
    sinal = f"▼ {r_diff}% abaixo da media" if r_diff > 0 else f"▲ {abs(r_diff)}% acima da media"
    cor_r = '#C00000' if r_diff > 0 else '#1A6B3A'
    st.markdown(f"<div class='raio-kpi-wrap'><div class='raio-kpi-lbl'>RECEITA EM RISCO</div><div class='raio-kpi-val' style='color:{cor_r};'>{fmt_num(r_risco)}</div><div class='raio-kpi-sub'>{sinal}</div></div>", unsafe_allow_html=True)

# Histórico
if meses_cols:
    valores_meses = [float(row.get(m, 0) or 0) for m in meses_cols]
    cores_barras  = ['#C00000' if v < r_mlp * 0.98 else '#1A6B3A' for v in valores_meses]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=meses_cols, y=valores_meses, marker_color=cores_barras,
        text=[fmt_num(v) for v in valores_meses], textposition='outside',
        textfont=dict(size=10, color='#1A2540')))
    if r_mlp > 0:
        fig.add_hline(y=r_mlp, line_dash='dash', line_color='#145A32', line_width=2,
            annotation_text=f'Media LP: {fmt_num(r_mlp)}',
            annotation_font_color='#145A32', annotation_font_size=11)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=250,
        margin=dict(t=30, b=10, l=10, r=10), showlegend=False,
        yaxis=dict(showgrid=True, gridcolor='#E5EAF2', tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=11, color='#1A2540', family='Arial')))
    st.markdown("<div style='margin-top:16px;'><div class='chart-wrap'><div class='chart-lbl'>HISTORICO MENSAL DE COMPRAS</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div></div>", unsafe_allow_html=True)

# ── HIPOTESES — BULLETS VERMELHOS ────────────────────────────────────────
hips = HIPOTESES.get(r_sta, HIPOTESES.get('ESTAVEL', []))
miss = MISSAO.get(r_sta, MISSAO.get('ESTAVEL', {}))

st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
items_hip = "".join([
    f"<li><div class='hip-bullet'></div>{h}</li>"
    for h in hips
])
st.markdown(
    f"<div class='hip-section'>"
    f"<div class='hip-section-titulo'>HIPOTESES INICIAIS</div>"
    f"<ul class='hip-list'>{items_hip}</ul>"
    f"</div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ── MISSAO — BRIEFING CARD ────────────────────────────────────────────────
st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
st.markdown(f"""
<div class='missao-card'>
  <div class='missao-card-header'>
    <div class='missao-card-header-txt'>MISSAO DO CONTATO</div>
  </div>
  <div class='missao-objetivo'>
    <div class='missao-obj-lbl'>OBJETIVO DO CONTATO</div>
    <div class='missao-obj-txt'>{miss.get('objetivo','—')}</div>
  </div>
  <div class='missao-callout'>
    <div class='missao-call-lbl'>SUA MISSAO</div>
    <div class='missao-call-txt'>{miss.get('missao','—')}</div>
  </div>
  <div class='missao-metrics'>
    <div class='missao-metric'>
      <div class='missao-metric-lbl'>PRAZO</div>
      <div class='missao-metric-val'>{miss.get('prazo','—')}</div>
    </div>
    <div class='missao-metric'>
      <div class='missao-metric-lbl'>REAVALIACAO</div>
      <div class='missao-metric-val'>{miss.get('reavaliacao','—')}</div>
    </div>
  </div>
  <div class='missao-sucesso'>
    <div class='missao-suc-ico'>&#10003;</div>
    <div>
      <div class='missao-suc-lbl'>CRITERIO DE SUCESSO</div>
      <div class='missao-suc-txt'>{miss.get('sucesso','—')}</div>
    </div>
  </div>
  <div class='missao-escala'>
    <div class='missao-esc-ico'>!</div>
    <div>
      <div class='missao-esc-lbl'>QUANDO ESCALAR</div>
      <div class='missao-esc-txt'>{miss.get('escala','—')}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── PERGUNTAS ─────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
pergs  = PERGUNTAS.get(r_sta, PERGUNTAS.get('ESTAVEL', []))
p_html = ""
for i, pq in enumerate(pergs, 1):
    opcoes_html = "".join([f"<span class='opcao-pill'>{o}</span>" for o in pq['o']])
    p_html += f"<div class='perg-bloco'><div class='perg-num'>Pergunta {i}</div><div class='perg-txt'>{pq['p']}</div><div>{opcoes_html}</div></div>"
st.markdown(
    f"<div class='perg-section'>"
    f"<div class='perg-section-titulo'>PERGUNTAS DE DIAGNOSTICO — {r_sta}</div>"
    f"{p_html}</div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ── ABORDAGEM ─────────────────────────────────────────────────────────────
abord = miss.get('abordagem', '')
if abord:
    st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='abordagem-bloco'>"
        f"<div class='abordagem-lbl'>LINHA DE ABORDAGEM SUGERIDA</div>"
        f"<div class='abordagem-txt'>{abord}</div>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
