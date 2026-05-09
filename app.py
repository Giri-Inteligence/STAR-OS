import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter

st.set_page_config(page_title="Giri | Sistema STAR", layout="wide")

# ─── ENGINE STAR ────────────────────────────────────────────────────────────
def engine_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        lp_v, cp_v = 0.0, 0.0

    txt_ina = (
        "OBJETIVO: Diagnóstico de causa\n"
        "PRÉ-CONTATO: Revisar último pedido. Identificar o que parou de ser comprado e em que momento.\n"
        "CONTATO: Contato de diagnóstico. Entender o motivo da inatividade sem pressão de venda.\n"
        "ORIENTAÇÃO: Não ofertar produto na primeira interação. Primeiro entender o que aconteceu. "
        "Registrar motivo antes de qualquer ação de reconquista."
    )
    txt_q_ac = (
        "OBJETIVO: Recuperação emergencial\n"
        "PRÉ-CONTATO: Revisar histórico completo do cliente. Identificar exatamente quais produtos caíram, "
        "em que momento e qual era o volume anterior. Calcular o gap entre a média histórica e o momento atual.\n"
        "CONTATO: Priorizar visita presencial ou ligação direta — não mensagem. Abrir diagnóstico sem pressão. "
        "Entender se houve mudança interna no cliente, problema de relacionamento ou entrada de concorrente.\n"
        "ORIENTAÇÃO: Este cliente está em risco de perda. O objetivo da primeira interação não é vender — é entender. "
        "Registrar causa com precisão. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    )
    txt_q = (
        "OBJETIVO: Estabilização\n"
        "PRÉ-CONTATO: Revisar histórico de mix. Identificar quais produtos reduziram ou desapareceram nos últimos 3 meses.\n"
        "CONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudança operacional, financeira ou troca de fornecedor.\n"
        "ORIENTAÇÃO: Registrar causa identificada. Se houver abertura, propor recomposição de mix com base no histórico anterior."
    )
    txt_est = (
        "OBJETIVO: Blindagem e crescimento incremental\n"
        "PRÉ-CONTATO: Revisar mix atual. Mapear categorias que o cliente não compra mas que são compatíveis com seu perfil.\n"
        "CONTATO: Manter frequência de relacionamento. Explorar oportunidade de expansão de mix.\n"
        "ORIENTAÇÃO: Cliente estável não é cliente seguro. Monitorar frequência de pedidos e introduzir novos itens gradualmente."
    )
    txt_cre = (
        "OBJETIVO: Consolidação\n"
        "PRÉ-CONTATO: Identificar o driver do crescimento. Avaliar se é sazonalidade ou mudança estrutural no cliente.\n"
        "CONTATO: Reforçar relacionamento. Garantir abastecimento e antecipar demanda dos próximos períodos.\n"
        "ORIENTAÇÃO: Proteger o cliente. Momento de crescimento é o de maior risco de abordagem pelo concorrente."
    )
    txt_cre_ac = (
        "OBJETIVO: Consolidação e proteção\n"
        "PRÉ-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar "
        "esse volume ou se é pontual. Verificar se há mix ainda não explorado.\n"
        "CONTATO: Reforçar presença. Garantir que o abastecimento está adequado ao novo patamar de compra. Antecipar pedidos futuros.\n"
        "ORIENTAÇÃO: Crescimento acentuado atrai concorrência. Este é o momento de maior risco de abordagem externa. "
        "Aumentar frequência de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."
    )

    if cp_v <= 0:
        return "INATIVO", 0, txt_ina
    if lp_v <= 0:
        return "ESTÁVEL", int(cp_v * 1.05), txt_est
    if cp_v < (lp_v * 0.85):
        return "QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < (lp_v * 0.98):
        return "QUEDA", int(lp_v), txt_q
    if cp_v > (lp_v * 1.20):
        return "CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_cre_ac
    if cp_v > (lp_v * 1.05):
        return "CRESCIMENTO", int(cp_v * 1.05), txt_cre
    return "ESTÁVEL", int(lp_v * 1.05), txt_est


# ─── GERAÇÃO DO EXCEL ────────────────────────────────────────────────────────
def gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='STAR')
        wb  = writer.book
        ws  = writer.sheets['STAR']

        # ── FORMATOS BASE ──────────────────────────────────────────────────
        hdr = wb.add_format({
            'bold': True, 'bg_color': '#002060', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'text_wrap': True, 'font_name': 'Arial'
        })
        txt = wb.add_format({
            'valign': 'top', 'align': 'left', 'border': 1,
            'text_wrap': True, 'font_name': 'Arial'
        })
        num = wb.add_format({
            'num_format': '#,##0', 'valign': 'top', 'align': 'center',
            'border': 1, 'font_name': 'Arial'
        })
        total_f = wb.add_format({
            'num_format': '#,##0', 'bg_color': '#D9D9D9', 'bold': True,
            'font_color': '#000000', 'valign': 'top', 'align': 'center',
            'border': 1, 'font_name': 'Arial'
        })

        # ── STATUS COLORIZADOS ─────────────────────────────────────────────
        # QUEDA ACENTUADA: fundo vermelho claro + letra vermelha negrito
        fmt_qa = wb.add_format({
            'bg_color': '#FFC7CE', 'font_color': '#C00000', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        # QUEDA: letra vermelha negrito (sem fundo)
        fmt_q = wb.add_format({
            'font_color': '#C00000', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        # CRESCIMENTO ACENTUADO: fundo verde claro + letra verde escuro negrito
        fmt_ca = wb.add_format({
            'bg_color': '#C6EFCE', 'font_color': '#375623', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        # CRESCIMENTO: letra verde escuro negrito (sem fundo)
        fmt_c = wb.add_format({
            'font_color': '#375623', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        # ESTÁVEL: letra azul negrito (sem fundo)
        fmt_e = wb.add_format({
            'font_color': '#0070C0', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })
        # INATIVO: letra preta negrito (sem fundo)
        fmt_i = wb.add_format({
            'font_color': '#000000', 'bold': True,
            'valign': 'top', 'align': 'center', 'border': 1, 'font_name': 'Arial'
        })

        # ── ALTURAS DE LINHA ───────────────────────────────────────────────
        ws.set_default_row(150)
        ws.set_row(0, 40)

        # ── LARGURAS DE COLUNA E CABEÇALHOS ───────────────────────────────
        larguras = {
            'CURVA': 7,
            clie_col: 30,
            vend_col: 22,
            'TOTAL LP': 13,
            'MÉDIA LP': 13,
            'MÉDIA CP': 13,
            'STATUS': 24,
            'META': 12,
            'AÇÃO': 88,
        }

        for i, col in enumerate(final_ordem):
            ws.write(0, i, col, hdr)
            if col in larguras:
                ws.set_column(i, i, larguras[col])
            elif col in meses_col:
                ws.set_column(i, i, 11)
            else:
                ws.set_column(i, i, 13)

        # ── DADOS ──────────────────────────────────────────────────────────
        for r_idx, row in df_raw.iterrows():
            xl_r = r_idx + 1
            for c_idx, col_n in enumerate(final_ordem):
                val = row[col_n]
                if col_n == 'STATUS':
                    s = str(val)
                    if s == 'QUEDA ACENTUADA':    f = fmt_qa
                    elif s == 'QUEDA':            f = fmt_q
                    elif s == 'CRESCIMENTO ACENTUADO': f = fmt_ca
                    elif s == 'CRESCIMENTO':      f = fmt_c
                    elif s == 'ESTÁVEL':          f = fmt_e
                    else:                         f = fmt_i   # INATIVO
                    ws.write_string(xl_r, c_idx, s, f)
                elif col_n == 'TOTAL LP':
                    ws.write_number(xl_r, c_idx, int(val), total_f)
                elif col_n in ('MÉDIA LP', 'MÉDIA CP', 'META') or col_n in meses_col:
                    ws.write_number(xl_r, c_idx, int(val), num)
                elif col_n == 'AÇÃO':
                    ws.write_string(xl_r, c_idx, str(val), txt)
                else:
                    ws.write_string(xl_r, c_idx, str(val), txt)

    return buffer.getvalue()


# ─── INTERFACE ───────────────────────────────────────────────────────────────
st.markdown("## GIRI | SISTEMA DE GOVERNANÇA STAR")
st.markdown("---")

uploaded_file = st.file_uploader("Faça upload da base (XLSX ou CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    df_raw = (
        pd.read_excel(uploaded_file)
        if uploaded_file.name.endswith('xlsx')
        else pd.read_csv(uploaded_file)
    )
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    cols = df_raw.columns.tolist()

    meses_col = [
        c for c in cols
        if any(m in c for m in ("JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"))
    ]
    clie_col = next((c for c in cols if "CLIENTE" in c or "NOME" in c or "RAZAO" in c), cols[0])
    vend_col = next((c for c in cols if "VENDEDOR" in c or "REP" in c), cols[1] if len(cols) > 1 else cols[0])

    for c in meses_col:
        df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)

    df_raw['TOTAL LP']  = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MÉDIA LP']  = df_raw[meses_col].mean(axis=1).astype(int)
    df_raw['MÉDIA CP']  = df_raw[meses_col[-3:]].mean(axis=1).astype(int)
    df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)

    cumsum_pct = df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()
    df_raw['CURVA'] = cumsum_pct.apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))

    res = df_raw.apply(lambda r: engine_star(r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
    df_raw['STATUS'], df_raw['META'], df_raw['AÇÃO'] = zip(*res)

    final_ordem = (
        ['CURVA', clie_col, vend_col]
        + meses_col
        + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']
    )

    # ── VISUALIZAÇÃO NA TELA ───────────────────────────────────────────────
    st.markdown("### MATRIZ STAR — VISUALIZAÇÃO")

    # Colunas visíveis na tela (sem texto longo da AÇÃO para legibilidade)
    cols_display = ['CURVA', clie_col, vend_col, 'TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META']
    df_display = df_raw[cols_display].copy()

    # Mapa de cores por status
    def colorir_status(val):
        cores = {
            'QUEDA ACENTUADA':     'background-color:#FFC7CE; color:#C00000; font-weight:bold',
            'QUEDA':               'color:#C00000; font-weight:bold',
            'CRESCIMENTO ACENTUADO': 'background-color:#C6EFCE; color:#375623; font-weight:bold',
            'CRESCIMENTO':         'color:#375623; font-weight:bold',
            'ESTÁVEL':             'color:#0070C0; font-weight:bold',
            'INATIVO':             'color:#000000; font-weight:bold',
        }
        return cores.get(val, '')

    styled = (
        df_display.style
        .applymap(colorir_status, subset=['STATUS'])
        .format({
            'TOTAL LP': '{:,.0f}',
            'MÉDIA LP': '{:,.0f}',
            'MÉDIA CP': '{:,.0f}',
            'META':     '{:,.0f}',
        })
    )

    st.dataframe(styled, use_container_width=True, height=520)

    # Resumo por status
    st.markdown("### DISTRIBUIÇÃO POR STATUS")
    dist = df_raw['STATUS'].value_counts().reset_index()
    dist.columns = ['STATUS', 'CLIENTES']
    st.dataframe(dist, use_container_width=False, hide_index=True)

    # ── DOWNLOAD ──────────────────────────────────────────────────────────
    st.markdown("---")
    excel_bytes = gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col)

    st.download_button(
        label="BAIXAR PLANILHA STAR",
        data=excel_bytes,
        file_name="Matriz_STAR_Giri.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
