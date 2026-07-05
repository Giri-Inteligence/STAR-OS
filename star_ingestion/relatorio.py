def criar_relatorio_ingestao():
    return {
        "status": "INICIADO",
        "linhas_iniciais": 0,
        "colunas_iniciais": 0,
        "linhas_finais": 0,
        "colunas_finais": 0,
        "cliente_col": None,
        "vendedor_col": None,
        "cidade_col": None,
        "meses_col": [],
        "acoes_saneamento": [],
        "avisos": [],
        "erros": [],
        "bloqueado": False,
    }


def registrar_estado_inicial(relatorio, df):
    relatorio["linhas_iniciais"] = len(df)
    relatorio["colunas_iniciais"] = df.shape[1]

    return relatorio


def registrar_estado_final(relatorio, df):
    relatorio["linhas_finais"] = len(df)
    relatorio["colunas_finais"] = df.shape[1]

    return relatorio


def registrar_mapeamento(relatorio, cliente_col=None, vendedor_col=None, cidade_col=None, meses_col=None):
    relatorio["cliente_col"] = cliente_col
    relatorio["vendedor_col"] = vendedor_col
    relatorio["cidade_col"] = cidade_col
    relatorio["meses_col"] = list(meses_col) if meses_col else []

    return relatorio


def adicionar_saneamento(relatorio, mensagens):
    for mensagem in mensagens or []:
        if mensagem:
            relatorio["acoes_saneamento"].append(mensagem)

    return relatorio


def adicionar_avisos(relatorio, avisos):
    for aviso in avisos or []:
        if aviso:
            relatorio["avisos"].append(aviso)

    return relatorio


def adicionar_erros(relatorio, erros):
    for erro in erros or []:
        if erro:
            relatorio["erros"].append(erro)

    if relatorio["erros"]:
        relatorio["bloqueado"] = True
        relatorio["status"] = "BLOQUEADO"

    return relatorio


def marcar_processado(relatorio):
    if not relatorio["erros"]:
        relatorio["status"] = "PROCESSADO"
        relatorio["bloqueado"] = False
    else:
        relatorio["status"] = "BLOQUEADO"
        relatorio["bloqueado"] = True

    return relatorio


def formatar_relatorio_texto(relatorio):
    linhas = []

    linhas.append(f"Status da ingestao: {relatorio['status']}")
    linhas.append(f"Base inicial: {relatorio['linhas_iniciais']} linhas x {relatorio['colunas_iniciais']} colunas")
    linhas.append(f"Base final: {relatorio['linhas_finais']} linhas x {relatorio['colunas_finais']} colunas")
    linhas.append(f"Cliente: {relatorio['cliente_col']}")
    linhas.append(f"Vendedor: {relatorio['vendedor_col']}")
    linhas.append(f"Cidade: {relatorio['cidade_col']}")
    linhas.append(f"Meses detectados: {len(relatorio['meses_col'])}")

    for mensagem in relatorio["acoes_saneamento"]:
        linhas.append(f"Saneamento: {mensagem}")

    for aviso in relatorio["avisos"]:
        linhas.append(f"Aviso: {aviso}")

    for erro in relatorio["erros"]:
        linhas.append(f"Erro: {erro}")

    return linhas
