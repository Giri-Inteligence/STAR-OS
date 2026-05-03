# --- ABA DE DESEMPENHO INDIVIDUAL (V30) ---
elif menu == "Desempenho (Vendedores)":
    st.title("Governança de Performance | STAR-OS")
    st.markdown("### 1. CONFIGURAÇÃO DA RÉGUA COMERCIAL")
    
    # Bloco de Tempo Automático
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1)
    if hoje.month == 12: ultimo_dia = hoje.replace(day=31)
    else: ultimo_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    
    d_uteis_totais = get_working_days(primeiro_dia, ultimo_dia)
    d_uteis_hoje = get_working_days(primeiro_dia, hoje)

    with st.expander("⚙️ DEFINIR INDICADORES E METAS DO MÊS", expanded=True):
        col_ind1, col_ind2 = st.columns([2, 1])
        vendedor_nome = col_ind1.text_input("Nome do Vendedor", placeholder="Digite o nome do consultor...")
        
        # Definição dos 5 Indicadores
        st.write("Defina os 5 indicadores estratégicos:")
        ind_list = []
        c1, c2, c3, c4, c5 = st.columns(5)
        cols_ind = [c1, c2, c3, c4, c5]
        
        for i, col in enumerate(cols_ind):
            nome_i = col.text_input(f"Indicador {i+1}", value=f"IND {i+1}", key=f"nome_ind_{i}")
            meta_i = col.number_input(f"Meta {i+1}", min_value=0.01, key=f"meta_ind_{i}")
            real_i = col.number_input(f"Realizado {i+1}", min_value=0.0, key=f"real_ind_{i}")
            ind_list.append({"NOME": nome_i, "META": meta_i, "REALIZADO": real_i})

    # --- PROCESSAMENTO DOS DADOS ---
    if vendedor_nome:
        st.markdown(f"### 2. ANÁLISE DE ROTA: {vendedor_nome.upper()}")
        
        resultados = []
        for item in ind_list:
            # Cálculo de Rota e Tendência
            v_esperado = (item["META"] / d_uteis_totais) * d_uteis_hoje
            percentual_rota = (item["REALIZADO"] / v_esperado) if v_esperado > 0 else 0
            tendencia_final = (item["REALIZADO"] / d_uteis_hoje) * d_uteis_totais if d_uteis_hoje > 0 else 0
            
            # Definição de Status Visual
            if percentual_rota >= 1.0: status = "🟢 NO RITMO"
            elif percentual_rota >= 0.85: status = "🟡 ATENÇÃO"
            else: status = "🚨 CRÍTICO"
            
            resultados.append({
                "INDICADOR": item["NOME"],
                "META MENSAL": item["META"],
                "ESPERADO (D+" + str(d_uteis_hoje) + ")": round(v_esperado, 2),
                "REALIZADO": item["REALIZADO"],
                "EFICIÊNCIA (ROTA)": f"{round(percentual_rota * 100, 1)}%",
                "PROJEÇÃO FINAL": round(tendencia_final, 2),
                "STATUS": status
            })

        df_performance = pd.DataFrame(resultados)
        
        # Exibição Estilizada
        st.table(df_performance)
        
        # Insight de Governança
        st.markdown("---")
        st.subheader("💡 ORIENTAÇÃO PARA O GESTOR")
        for res in resultados:
            if "🚨" in res["STATUS"]:
                st.error(f"**{res['INDICADOR']}**: O vendedor está muito abaixo do esperado. "
                         f"Risco de entregar apenas {format_br(res['PROJEÇÃO FINAL'])} contra uma meta de {format_br(res['META MENSAL'])}. "
                         "Exigir plano de ação imediato.")
