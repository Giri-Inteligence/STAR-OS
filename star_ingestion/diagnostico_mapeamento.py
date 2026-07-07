import re
import unicodedata


MESES_TEXTO = (
    "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
    "JUL", "AGO", "SET", "OUT", "NOV", "DEZ",
    "JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO",
)

TERMOS_CLIENTE = ("CLIENTE", "RAZAO", "EMPRESA", "CONTA")
TERMOS_VENDEDOR = ("VENDEDOR", "REPRESENTANTE", "CONSULTOR", "RESPONSAVEL")
TERMOS_CIDADE = ("CIDADE", "MUNICIPIO", "LOCALIDADE", "REGIAO")


def normalizar_nome_coluna(nome):
    texto = " ".join(str(nome).strip().upper().split())
    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(c for c in texto_decomposto if not unicodedata.combining(c))


def classificar_colunas_disponiveis(df):
    colunas_originais = list(df.columns)
    colunas_normalizadas = [normalizar_nome_coluna(c) for c in colunas_originais]

    return {
        "total_colunas": len(colunas_originais),
        "colunas_originais": colunas_originais,
        "colunas_normalizadas": colunas_normalizadas,
    }


def _tem_termo(nome_normalizado, termos):
    return any(termo in nome_normalizado for termo in termos)


def _parece_coluna_mes(nome_normalizado):
    tem_mes_texto = any(mes in nome_normalizado for mes in MESES_TEXTO)
    tem_formato_numerico = bool(re.search(r"\b(0?[1-9]|1[0-2])[/\-]\d{2,4}\b", nome_normalizado))

    return tem_mes_texto or tem_formato_numerico


def diagnosticar_mapeamento(df, cliente_col=None, vendedor_col=None, cidade_col=None, meses_col=None):
    meses_col = meses_col or []
    colunas = list(df.columns)

    erros = []
    avisos = []
    sugestoes = []

    if not cliente_col or cliente_col not in colunas:
        erros.append("Coluna de cliente não foi reconhecida.")
        sugestoes.append(
            "Verifique se a planilha possui uma coluna como CLIENTE, NOME DO CLIENTE, "
            "RAZÃO SOCIAL, EMPRESA ou CONTA."
        )

    if not vendedor_col or vendedor_col not in colunas:
        erros.append("Coluna de vendedor não foi reconhecida.")
        sugestoes.append(
            "Verifique se a planilha possui uma coluna como VENDEDOR, REPRESENTANTE, "
            "CONSULTOR ou RESPONSÁVEL."
        )

    if not cidade_col or cidade_col not in colunas:
        avisos.append("Coluna de cidade não foi reconhecida. A análise pode seguir sem cidade.")

    if not meses_col:
        erros.append("Nenhuma coluna mensal foi reconhecida.")
        sugestoes.append(
            "Verifique se os meses estão em formato como JAN/25, JANEIRO/25, 01/25 ou JANEIRO 2025."
        )
    elif len(meses_col) < 2:
        avisos.append("Poucas colunas mensais foram reconhecidas. A leitura de tendência pode ficar limitada.")

    return {
        "ok": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
        "sugestoes": sugestoes,
    }


def detectar_colunas_candidatas(df):
    colunas = list(df.columns)

    possiveis_clientes = []
    possiveis_vendedores = []
    possiveis_cidades = []
    possiveis_meses = []

    for coluna in colunas:
        nome_normalizado = normalizar_nome_coluna(coluna)

        if _tem_termo(nome_normalizado, TERMOS_CLIENTE):
            possiveis_clientes.append(coluna)

        if _tem_termo(nome_normalizado, TERMOS_VENDEDOR):
            possiveis_vendedores.append(coluna)

        if _tem_termo(nome_normalizado, TERMOS_CIDADE):
            possiveis_cidades.append(coluna)

        if _parece_coluna_mes(nome_normalizado):
            possiveis_meses.append(coluna)

    return {
        "possiveis_clientes": possiveis_clientes,
        "possiveis_vendedores": possiveis_vendedores,
        "possiveis_cidades": possiveis_cidades,
        "possiveis_meses": possiveis_meses,
    }


def formatar_diagnostico_mapeamento_texto(diagnostico, candidatos=None):
    linhas = []

    for erro in diagnostico.get("erros", []):
        linhas.append(f"Erro: {erro}")

    for sugestao in diagnostico.get("sugestoes", []):
        linhas.append(f"Sugestão: {sugestao}")

    for aviso in diagnostico.get("avisos", []):
        linhas.append(f"Aviso: {aviso}")

    if candidatos:
        rotulos = (
            ("possiveis_clientes", "Possíveis colunas de cliente"),
            ("possiveis_vendedores", "Possíveis colunas de vendedor"),
            ("possiveis_cidades", "Possíveis colunas de cidade"),
            ("possiveis_meses", "Possíveis colunas de mês"),
        )

        for chave, rotulo in rotulos:
            valores = candidatos.get(chave) or []

            if valores:
                linhas.append(f"{rotulo}: {', '.join(str(v) for v in valores)}")

    return linhas
