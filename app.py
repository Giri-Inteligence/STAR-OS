def engine_star(row, lp, cp):
    # LÓGICA DE STATUS: ORIENTAÇÃO METODOLÓGICA (MÉTODO STAR)
    if cp == 0: 
        return "⚫ INATIVO", 0, (
            "OBJETIVO: Diagnóstico de Churn e Reconexão. "
            "AÇÃO: Reestabelecer o canal de comunicação sem viés de venda imediata. "
            "ORIENTAÇÃO: Identifique o motivo real da interrupção (atendimento, preço ou mudança no processo dele). "
            "Sua meta é validar se a dor que resolvíamos no passado ainda existe ou se ele tem uma nova prioridade hoje."
        )
    
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, (
            "OBJETIVO: Contenção de Perda e Defesa de Share. "
            "AÇÃO: Investigar a entrada de concorrência ou falha crítica no nosso serviço. "
            "ORIENTAÇÃO: Não foque em produto. Foque no negócio dele. Entenda onde a operação do cliente está perdendo fôlego "
            "ou margem. Apresente-se como um consultor preocupado em recuperar a saúde do estoque/giro dele."
        )
    
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, (
            "OBJETIVO: Estabilização de Giro. "
            "AÇÃO: Realizar análise de contexto para identificar redução de demanda. "
            "ORIENTAÇÃO: Entenda se a queda é sazonal ou se ele está substituindo itens por opções de menor margem. "
            "Sugira ajustes de mix que ajudem o cliente a reduzir perdas e manter o custo operacional controlado."
        )
    
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), (
            "OBJETIVO: Expansão de Share e Upsell Estratégico. "
            "AÇÃO: Analisar o mix de clientes parecidos e elevar o Ticket Médio. "
            "ORIENTAÇÃO: Identifique lacunas no mix atual. Recomende itens que complementam o que ele já compra bem, "
            "explicando como isso ajuda o cliente a atrair novos consumidores ou melhorar a margem final dele."
        )
    
    return "🔵 ESTÁVEL", int(lp * 1.05), (
        "OBJETIVO: Manutenção e Identificação de Oportunidades. "
        "AÇÃO: Garantir a blindagem do relacionamento e prevenir inércia. "
        "ORIENTAÇÃO: Confirme se os objetivos de curto prazo do cliente estão sendo atingidos com o nosso mix. "
        "Aproveite a estabilidade para prospectar necessidades futuras e validar se há espaço para novos projetos."
    )
