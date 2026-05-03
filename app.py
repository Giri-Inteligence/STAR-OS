# 2. MOTOR DE STATUS STAR - SENSIBILIDADE REFINADA (5%)
        def engine_star(row):
            lp, cp = row['MEDIA_LP'], row['MEDIA_CP']
            
            # Regra de Inatividade (90 dias)
            if cp == 0: 
                return "⚫ INATIVO", lp, "RECUPERAÇÃO: Cliente sem compra há 90 dias. Visita imediata."
            
            # Regra de Queda: CP < 95% do LP
            if cp < (lp * 0.95): 
                return "🔴 QUEDA", lp, "DEFESA: Desvio negativo detectado. Investigar perda de share."
            
            # Regra de Crescimento: CP > 105% do LP
            if cp > (lp * 1.05): 
                return "🟢 CRESCIMENTO", int(cp * 1.10), "EXPANSÃO: Tração positiva detectada. Aplicar Upsell."
            
            # Regra de Estabilidade (Margem de +/- 5%)
            return "🔵 ESTÁVEL", int(lp * 1.05), "MANUTENÇÃO: Ritual de atendimento e blindagem de conta."

        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*df_agrupado.apply(engine_star, axis=1))
