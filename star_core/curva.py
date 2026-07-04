import pandas as pd


def curva_label_fmt(sel):
    if not sel:
        return "NENHUMA"

    if set(sel) == {"A", "B", "C"}:
        return "TODA A CARTEIRA"

    if len(sel) == 1:
        return f"CURVA {sel[0]}"

    return "CURVAS " + " + ".join(sorted(sel))


def curva_short(sel):
    if not sel:
        return ""

    if set(sel) == {"A", "B", "C"}:
        return "TOTAL"

    return "+".join(sorted(sel))


def calcular_curva_abc_por_receita(df, coluna_total="TOTAL LP"):
    df = df.copy()

    if coluna_total not in df.columns:
        df["CURVA"] = "C"
        return df

    receita_total = df[coluna_total].sum()

    if receita_total <= 0:
        df["CURVA"] = "C"
        return df

    df = df.sort_values(coluna_total, ascending=False).reset_index(drop=True)

    participacao_acumulada = df[coluna_total].cumsum() / receita_total

    df["CURVA"] = participacao_acumulada.apply(
        lambda x: "A" if x <= 0.80 else ("B" if x <= 0.95 else "C")
    )

    return df


def normalizar_curva_existente(serie):
    valores = serie.astype(str).str.upper().str.strip()
    valores = valores.where(valores.isin(["A", "B", "C"]), other=pd.NA)
    return valores.ffill().fillna("C")