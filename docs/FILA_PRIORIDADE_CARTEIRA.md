# FILA DE PRIORIDADE DA CARTEIRA — STAR OS

## 1. Finalidade

A fila de prioridade ordena a atenção operacional sobre a carteira a partir
da Matriz STAR já gerada. Ela ajuda a responder quais clientes devem ser
olhados primeiro, sem recalcular ou substituir nada do Motor STAR.

## 2. O que ela usa

Somente campos já existentes na Matriz STAR:

- `CURVA`
- `STATUS`
- `MESES_SEM_COMPRA`
- `EROSAO STAR`
- `MEDIA LP`
- `MEDIA CP`

## 3. O que ela não altera

- Não altera o Motor STAR.
- Não altera curva ABC.
- Não altera status STAR.
- Não altera recência.
- Não altera erosão.
- Não altera cálculo.
- Não altera PDF.
- Não altera Excel de saída.

## 4. Níveis de prioridade

- **P1 CRITICA** — pontuação ≥ 90.
- **P2 ALTA** — pontuação entre 70 e 89.
- **P3 MEDIA** — pontuação entre 45 e 69.
- **P4 MONITORAMENTO** — pontuação abaixo de 45.

## 5. Tipos de prioridade

- **REATIVACAO** — cliente inativo.
- **PRESERVACAO** — cliente em queda ou queda acentuada.
- **INVESTIGACAO** — cliente estável com erosão relevante.
- **EXPANSAO CONTROLADA** — cliente em crescimento.
- **MONITORAMENTO** — demais casos.

## 6. Limites

- A fila não é recomendação completa.
- A fila não substitui gestor.
- A fila não explica causa raiz.
- A fila não cria plano de ação.
- Hipóteses e recomendações serão tratadas em sprints futuras (3.4 e 3.5).
