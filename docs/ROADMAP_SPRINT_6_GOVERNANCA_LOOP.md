# ROADMAP DA SPRINT 6 — GOVERNANÇA INVESTIGATIVA E LOOP OPERACIONAL

## 1. Objetivo da Sprint 6

A Sprint 6 deve transformar histórico investigativo em governança
operacional, sem criar execução automática.

## 2. Sub-sprints planejadas

- Sprint 6.1 — Arquitetura da Governança Investigativa e Loop Operacional — **CONCLUÍDA**.
- Sprint 6.2 — Registro de Acompanhamento Operacional — **CONCLUÍDA** (contrato determinístico em memória, sem persistência e sem execução automática — ver `docs/REGISTRO_ACOMPANHAMENTO_OPERACIONAL.md`).
- Sprint 6.3 — Status de Acompanhamento da Investigação — **CONCLUÍDA** (regras determinísticas de status e transição de acompanhamento em memória, sem persistência e sem execução automática — ver `docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`).
- Sprint 6.4 — Loop Semanal de Governança — próxima etapa recomendada.
- Sprint 6.5 — Fechamento da Governança Inicial.

## 3. Objetivo de cada sub-sprint

- **Sprint 6.1** — documentar arquitetura, modelo conceitual e decisões.
- **Sprint 6.2** — criar contrato de registro de acompanhamento, ainda
  sem execução automática.
- **Sprint 6.3** — criar estados determinísticos de acompanhamento.
- **Sprint 6.4** — criar lógica de loop semanal de governança, ainda sem
  agentes.
- **Sprint 6.5** — documentar fechamento, inventário, decisões e
  regressão.

## 4. O que a Sprint 6 não deve fazer inicialmente

- Não criar IA.
- Não criar agente.
- Não criar integração externa.
- Não criar automação.
- Não criar tarefa automática.
- Não enviar mensagem.
- Não alterar Motor STAR.
- Não misturar governança com cálculo.
- Não substituir julgamento humano.

## 5. Critérios de sucesso da Sprint 6

- Governança separada do Motor STAR.
- Acompanhamento separado de execução.
- Histórico usado como base.
- Nenhuma regra STAR alterada.
- Nenhuma tarefa automática criada.
- Nenhum agente acionado.
- Regressão manual passando.
