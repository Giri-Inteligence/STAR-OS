def calcular_meses_sem_compra(row, meses_col):
    for i in range(len(meses_col) - 1, -1, -1):
        if row[meses_col[i]] > 0:
            return len(meses_col) - 1 - i

    return len(meses_col)