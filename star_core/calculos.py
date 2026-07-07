def calcular_erosao_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        return 1

    if lp_v <= 0:
        return 1

    if cp_v <= 0:
        return 10

    diff = ((lp_v - cp_v) / lp_v) * 100

    if diff <= 0:
        return 1
    if diff <= 5:
        return 1
    if diff <= 10:
        return 2
    if diff <= 15:
        return 3
    if diff <= 20:
        return 4
    if diff <= 30:
        return 5
    if diff <= 40:
        return 6
    if diff <= 50:
        return 7
    if diff <= 60:
        return 8
    if diff <= 70:
        return 9

    return 10


def engine_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        lp_v, cp_v = 0.0, 0.0

    txt_ina = "OBJETIVO: Diagnóstico de causa\nPRÉ-CONTATO: Revisar último pedido.\nCONTATO: Contato de diagnóstico sem pressão.\nORIENTAÇÃO: Não ofertar produto na primeira interação."

    txt_q_ac = "OBJETIVO: Recuperação emergencial\nPRÉ-CONTATO: Revisar histórico completo.\nCONTATO: Priorizar visita ou ligação direta.\nORIENTAÇÃO: O objetivo é entender, não vender."

    txt_q = "OBJETIVO: Estabilização\nPRÉ-CONTATO: Revisar histórico de mix.\nCONTATO: Diagnosticar contexto atual.\nORIENTAÇÃO: Registrar causa e propor recomposição de mix apenas se fizer sentido."

    txt_est = "OBJETIVO: Blindagem e crescimento incremental\nPRÉ-CONTATO: Revisar mix. Mapear categorias não compradas.\nCONTATO: Manter frequência. Explorar expansão.\nORIENTAÇÃO: Cliente estável não é cliente seguro."

    txt_cre = "OBJETIVO: Consolidação\nPRÉ-CONTATO: Identificar driver do crescimento.\nCONTATO: Reforçar relacionamento.\nORIENTAÇÃO: Proteger o cliente."

    txt_ca = "OBJETIVO: Consolidação e proteção\nPRÉ-CONTATO: Identificar produtos que puxaram crescimento.\nCONTATO: Reforçar presença.\nORIENTAÇÃO: Crescimento acentuado atrai concorrência."

    if cp_v <= 0:
        return "INATIVO", 0, txt_ina

    if lp_v <= 0:
        return "ESTAVEL", int(cp_v * 1.05), txt_est

    if cp_v < lp_v * 0.90:
        return "QUEDA ACENTUADA", int(lp_v), txt_q_ac

    if cp_v < lp_v * 0.98:
        return "QUEDA", int(lp_v), txt_q

    if cp_v > lp_v * 1.10:
        return "CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_ca

    if cp_v > lp_v * 1.02:
        return "CRESCIMENTO", int(cp_v * 1.05), txt_cre

    return "ESTAVEL", int(lp_v * 1.05), txt_est