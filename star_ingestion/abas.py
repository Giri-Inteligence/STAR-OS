import pandas as pd


NOMES_ABA_CONSOLIDADA = ("CONSOLIDADO", "CONSOLIDADA", "GERAL", "BASE", "CARTEIRA")


def listar_abas_excel(uploaded_file):
    uploaded_file.seek(0)
    excel_file = pd.ExcelFile(uploaded_file)
    return excel_file.sheet_names


def eh_aba_consolidada(nome_aba):
    return str(nome_aba).strip().upper() in NOMES_ABA_CONSOLIDADA


def escolher_aba_padrao(abas):
    for aba in abas:
        if eh_aba_consolidada(aba):
            return aba

    return abas[0] if abas else None


def ler_aba_excel(uploaded_file, aba, detectar_header_func):
    uploaded_file.seek(0)
    header = detectar_header_func(uploaded_file, sheet_name=aba)
    uploaded_file.seek(0)
    return pd.read_excel(uploaded_file, sheet_name=aba, header=header)


def consolidar_abas_excel(uploaded_file, abas_selecionadas, tipo_organizacao, detectar_header_func):
    bases = []

    for aba in abas_selecionadas:
        df = ler_aba_excel(uploaded_file, aba, detectar_header_func)

        nome_aba = str(aba).strip()

        if tipo_organizacao == "Abas por vendedor":
            df["VENDEDOR_STAR_ABA"] = nome_aba

        elif tipo_organizacao == "Abas por segmento":
            df["SEGMENTO_STAR"] = nome_aba

        elif tipo_organizacao == "Abas por região":
            df["REGIAO_STAR"] = nome_aba

        elif tipo_organizacao == "Abas por cidade":
            df["CIDADE_STAR_ABA"] = nome_aba

        elif tipo_organizacao == "Abas por filial":
            df["FILIAL_STAR"] = nome_aba

        bases.append(df)

    if not bases:
        return pd.DataFrame()

    return pd.concat(bases, ignore_index=True)