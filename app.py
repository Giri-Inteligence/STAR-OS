if sel_vend == "Todos":
        st.markdown('<div class="section-title">PERFORMANCE POR VENDEDOR</div>', unsafe_allow_html=True)
        rows = []
        for v in sorted(df[vend_col].dropna().astype(str).unique()):
            dv = df[df[vend_col].astype(str) == v]
            rows.append({
                'VENDEDOR':      v,
                'CLIENTES':      str(len(dv)),
                'CURVA A':       str(len(dv[dv['CURVA'] == 'A'])),
                'RECEITA TOTAL': f"R$ {fmt_br(dv['TOTAL LP'].sum())}",
                'EM RISCO':      str(len(dv[dv['STATUS'].isin(['QUEDA', 'QUEDA ACENTUADA', 'INATIVO'])])),
                'CRESCIMENTO':   str(len(dv[dv['STATUS'].isin(['CRESCIMENTO', 'CRESCIMENTO ACENTUADO'])])),
                'INATIVOS':      str(len(dv[dv['STATUS'] == 'INATIVO'])),
            })

        cols_vend = ['VENDEDOR', 'CLIENTES', 'CURVA A', 'RECEITA TOTAL', 'EM RISCO', 'CRESCIMENTO', 'INATIVOS']
        header_html = "".join([f"<th>{c}</th>" for c in cols_vend])
        rows_html = ""
        for r in rows:
            cells = "".join([f"<td>{r[c]}</td>" for c in cols_vend])
            rows_html += f"<tr>{cells}</tr>"

        st.markdown(f"""
        <style>
        .vend-table {{ width:100%; border-collapse:collapse; font-family:Arial; font-size:0.88rem; }}
        .vend-table th {{
            background:#1A2540; color:#FFFFFF; font-weight:700;
            padding:12px 16px; text-align:center; letter-spacing:0.8px;
            font-size:0.75rem; text-transform:uppercase;
        }}
        .vend-table td {{
            padding:12px 16px; text-align:center; color:#1A2540;
            border-bottom:1px solid #E5EAF2; font-weight:500;
        }}
        .vend-table tr:last-child td {{ border-bottom:none; }}
        .vend-table tr:hover td {{ background:#F5F7FB; }}
        .vend-wrap {{
            background:#FFFFFF; border-radius:14px;
            box-shadow:0 2px 18px rgba(0,0,0,0.07); overflow:hidden;
        }}
        </style>
        <div class="vend-wrap">
            <table class="vend-table">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
