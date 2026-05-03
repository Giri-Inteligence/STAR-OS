def engine_star(row, lp, cp):
    # LÓGICA DE STATUS COM INSTRUÇÕES DE POSICIONAMENTO CONSULTIVO
    if cp == 0: 
        return "⚫ INATIVO", 0, (
            "RECUPERAÇÃO: 90 dias sem compra. FOCO: Interesse Genuíno. "
            "Ação: Ligue para reaproximar e entender a realidade dele. "
            "Diga: 'Sumimos um do outro e meu papel aqui é garantir que sua operação não pare. "
            "O que mudou no seu cenário que nos afastou? Quero te ouvir antes de falarmos de produtos.'"
        )
    
    if cp < (lp * 0.80):
        return "🚨 QUEDA ACENTUADA", lp, (
            "ALERTA CRÍTICO: Perda de Share. FOCO: Diagnóstico de Perda. "
            "Ação: PARE TUDO. Não ofereça produtos. Sua missão é descobrir onde o cliente está perdendo margem. "
            "Diga: 'Notei uma queda forte no seu volume e me preocupei. Meu objetivo é te ajudar a bater suas metas. "
            "Houve alguma mudança no seu processo ou mercado que eu precise saber para te ajudar a recuperar esse fôlego?'"
        )
    
    if cp < (lp * 0.95): 
        return "🔴 QUEDA", lp, (
            "ATENÇÃO: Desvio de Consumo. FOCO: Consultoria de Contexto. "
            "Ação: Investigue se a concorrência entrou ou se ele reduziu a produção. "
            "Diga: 'Percebi que seu giro diminuiu. Como está sua meta de redução de custos e perdas este mês? "
            "Quero entender se nosso mix atual ainda faz sentido para o seu objetivo de margem.'"
        )
    
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), (
            "ACELERAÇÃO: Expansão de Mix. FOCO: Modelo Multiplicativo. "
            "Ação: O cliente está performando bem. Ajude-o a ganhar mais mercado. "
            "Diga: 'Sua operação está ganhando tração! Para te ajudar a lucrar mais e atrair novos clientes, "
            "precisamos ajustar seu mix com estes novos itens que trazem mais eficiência. Vamos planejar o próximo mês?'"
        )
    
    return "🔵 ESTÁVEL", int(lp * 1.05), (
        "ROTINA: Blindagem e Relacionamento. FOCO: Garantia de Objetivo. "
        "Ação: Confirme a reposição e valide o sucesso do cliente. "
        "Diga: 'Tudo rodando conforme o planejado! Para garantir que você continue com esse custo controlado, "
        "podemos confirmar a reposição? Há algum novo desafio de margem que você queira que eu te ajude a resolver?'"
    )
