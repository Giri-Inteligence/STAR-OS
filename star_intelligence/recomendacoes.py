from star_intelligence.priorizacao import obter_valor_numerico, obter_texto
from star_intelligence.hipoteses import normalizar_status


MAPA_PAPEIS = {
    "VENDEDOR": "VENDEDOR",
    "GESTOR": "GESTOR",
    "GERENTE": "GESTOR",
    "SOCIO": "SOCIO",
    "CEO": "SOCIO",
    "DIRETOR": "SOCIO",
    "CONSULTOR": "CONSULTOR",
}

RECOMENDACOES_VENDEDOR = {
    "REATIVACAO": [
        "Validar se o cliente ainda compra a categoria.",
        "Levantar o motivo da interrupção de compra.",
        "Registrar evidência objetiva sobre situação atual do cliente.",
    ],
    "PRESERVACAO DE RECEITA": [
        "Verificar se a queda ocorreu por volume, frequência ou mix.",
        "Identificar se houve mudança de demanda, preço, entrega ou concorrência.",
        "Registrar o principal sinal observado na conta.",
    ],
    "INVESTIGACAO DE EROSAO": [
        "Verificar se a estabilidade aparente esconde perda de mix ou frequência.",
        "Comparar o padrão recente com o comportamento histórico do cliente.",
    ],
    "MONITORAMENTO": [
        "Manter acompanhamento do comportamento de compra.",
        "Observar sinais de mudança de frequência, volume ou mix.",
    ],
    "EXPANSAO CONTROLADA": [
        "Verificar se o crescimento é recorrente ou pontual.",
        "Identificar se existe expansão real de mix, volume ou frequência.",
    ],
}

RECOMENDACOES_GESTOR = {
    "REATIVACAO": [
        "Verificar se o vendedor possui evidência atual sobre a situação do cliente.",
        "Cobrar clareza sobre motivo de inatividade antes de definir intervenção.",
        "Avaliar se o cliente deve entrar em pauta de reativação no ritual comercial.",
    ],
    "PRESERVACAO DE RECEITA": [
        "Priorizar a conta na revisão de carteira.",
        "Validar com o vendedor se a queda é por volume, frequência, mix ou concorrência.",
        "Acompanhar se existe risco relevante de perda de receita.",
    ],
    "INVESTIGACAO DE EROSAO": [
        "Checar se a estabilidade aparente está mascarando deterioração.",
        "Solicitar evidências sobre mix, frequência e ticket recente.",
    ],
    "MONITORAMENTO": [
        "Manter o cliente sob observação nos indicadores da carteira.",
        "Evitar intervenção excessiva sem sinal concreto de risco.",
    ],
    "EXPANSAO CONTROLADA": [
        "Verificar se o crescimento é sustentável ou pontual.",
        "Avaliar se há oportunidade de consolidar o novo patamar de compra.",
    ],
}

RECOMENDACOES_SOCIO = {
    "REATIVACAO": [
        "Avaliar se a carteira possui perda relevante de clientes anteriormente ativos.",
        "Observar se a inatividade indica falha de retenção, posicionamento ou governança.",
    ],
    "PRESERVACAO DE RECEITA": [
        "Observar impacto potencial da queda sobre receita recorrente da carteira.",
        "Verificar se a operação possui governança suficiente para preservar clientes relevantes.",
    ],
    "INVESTIGACAO DE EROSAO": [
        "Avaliar se há deterioração silenciosa em clientes aparentemente estáveis.",
        "Observar se a liderança comercial identifica erosão antes da perda consolidada.",
    ],
    "MONITORAMENTO": [
        "Acompanhar se a carteira mantém previsibilidade sem depender apenas de esforço individual.",
    ],
    "EXPANSAO CONTROLADA": [
        "Avaliar se o crescimento representa ganho estrutural ou evento pontual.",
        "Observar se a operação possui processo para sustentar o novo patamar.",
    ],
}

RECOMENDACOES_CONSULTOR = {
    "REATIVACAO": [
        "Investigar se a inatividade é caso isolado ou padrão recorrente da carteira.",
        "Separar hipótese de perda comercial, perda de demanda, falha de atendimento ou ausência de cadência.",
    ],
    "PRESERVACAO DE RECEITA": [
        "Investigar se a queda está concentrada em curva A, vendedor, cidade, segmento ou período.",
        "Validar se a causa provável está em demanda, funil, gestão, governança ou execução.",
    ],
    "INVESTIGACAO DE EROSAO": [
        "Avaliar se a erosão é sinal precoce de deterioração silenciosa.",
        "Cruzar erosão com curva, recência, status e comportamento por vendedor.",
    ],
    "MONITORAMENTO": [
        "Verificar se o cliente é caso estável real ou se há limitação de dados.",
    ],
    "EXPANSAO CONTROLADA": [
        "Investigar se o crescimento é estrutural, sazonal, pontual ou efeito de recomposição.",
    ],
}

FUNCOES_POR_PAPEL = {}


def normalizar_papel(papel):
    texto = normalizar_status(papel)

    return MAPA_PAPEIS.get(texto, "CONSULTOR")


def definir_foco_por_status(row):
    status = normalizar_status(obter_texto(row, "STATUS"))
    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if status == "INATIVO":
        return "REATIVACAO"

    if status in ("QUEDA", "QUEDA ACENTUADA"):
        return "PRESERVACAO DE RECEITA"

    if status == "ESTAVEL" and erosao >= 5:
        return "INVESTIGACAO DE EROSAO"

    if status == "ESTAVEL":
        return "MONITORAMENTO"

    if status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        return "EXPANSAO CONTROLADA"

    return "MONITORAMENTO"


def gerar_recomendacao_vendedor(row, pacote_hipoteses=None):
    foco = definir_foco_por_status(row)

    return list(RECOMENDACOES_VENDEDOR.get(foco, RECOMENDACOES_VENDEDOR["MONITORAMENTO"]))


def gerar_recomendacao_gestor(row, pacote_hipoteses=None):
    foco = definir_foco_por_status(row)

    return list(RECOMENDACOES_GESTOR.get(foco, RECOMENDACOES_GESTOR["MONITORAMENTO"]))


def gerar_recomendacao_socio(row, pacote_hipoteses=None):
    foco = definir_foco_por_status(row)

    return list(RECOMENDACOES_SOCIO.get(foco, RECOMENDACOES_SOCIO["MONITORAMENTO"]))


def gerar_recomendacao_consultor(row, pacote_hipoteses=None):
    foco = definir_foco_por_status(row)

    return list(RECOMENDACOES_CONSULTOR.get(foco, RECOMENDACOES_CONSULTOR["MONITORAMENTO"]))


FUNCOES_POR_PAPEL.update({
    "VENDEDOR": gerar_recomendacao_vendedor,
    "GESTOR": gerar_recomendacao_gestor,
    "SOCIO": gerar_recomendacao_socio,
    "CONSULTOR": gerar_recomendacao_consultor,
})


def gerar_recomendacoes_por_papel(row, papel, pacote_hipoteses=None):
    papel_normalizado = normalizar_papel(papel)
    foco = definir_foco_por_status(row)

    recomendacoes = FUNCOES_POR_PAPEL[papel_normalizado](row, pacote_hipoteses)

    observacoes = []

    nivel_prioridade = normalizar_status(obter_texto(row, "NIVEL_PRIORIDADE"))
    curva = normalizar_status(obter_texto(row, "CURVA"))
    status = normalizar_status(obter_texto(row, "STATUS"))

    if nivel_prioridade == "P1 CRITICA":
        observacoes.append("Cliente em prioridade crítica exige validação cuidadosa antes de intervenção.")

    if curva == "A" and status in ("QUEDA", "QUEDA ACENTUADA", "INATIVO"):
        observacoes.append("Cliente relevante para a carteira; evitar decisão sem evidência.")

    if status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        observacoes.append("Crescimento deve ser validado quanto à recorrência antes de virar premissa.")

    return {
        "papel": papel_normalizado,
        "foco_operacional": foco,
        "recomendacoes": recomendacoes,
        "observacoes": observacoes,
    }


def gerar_recomendacoes_multiplos_papeis(row, pacote_hipoteses=None):
    return {
        papel: gerar_recomendacoes_por_papel(row, papel, pacote_hipoteses)
        for papel in ("VENDEDOR", "GESTOR", "SOCIO", "CONSULTOR")
    }


def formatar_recomendacoes_texto(resultado):
    linhas = []

    if "papel" in resultado:
        pacotes = [resultado]
    else:
        pacotes = list(resultado.values())

    for pacote in pacotes:
        linhas.append(f"Papel: {pacote.get('papel', '')}")
        linhas.append(f"Foco operacional: {pacote.get('foco_operacional', '')}")

        for recomendacao in pacote.get("recomendacoes", []):
            linhas.append(f"Recomendação: {recomendacao}")

        for observacao in pacote.get("observacoes", []):
            linhas.append(f"Observação: {observacao}")

    return linhas
