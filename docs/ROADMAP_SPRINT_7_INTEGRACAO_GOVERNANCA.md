# ROADMAP DA SPRINT 7 — INTEGRAÇÃO CONTROLADA DA GOVERNANÇA

## 1. Objetivo da Sprint 7

A Sprint 7 deve transformar a governança em memória em governança
integrada, com contrato, persistência e exposição controlada, sem criar
execução automática.

## 2. Sub-sprints planejadas

- Sprint 7.1 — Arquitetura da Integração Controlada da Governança — **CONCLUÍDA**.
- Sprint 7.2 — Contrato de Persistência da Governança — **CONCLUÍDA** (payloads canônicos de governança em memória, sem banco, sem tabela e sem repositório — ver `docs/CONTRATO_PERSISTENCIA_GOVERNANCA.md`).
- Sprint 7.3 — Repositório Local de Governança — **CONCLUÍDA** (persistência SQLite local controlada, usando o contrato da Sprint 7.2, sem Streamlit e sem execução automática — ver `docs/REPOSITORIO_LOCAL_GOVERNANCA.md`).
- Sprint 7.4 — Governança no Streamlit — próxima etapa recomendada.
- Sprint 7.5 — Fechamento da Governança Integrada.

## 3. Objetivo de cada sub-sprint

- **Sprint 7.1** — documentar arquitetura, modelo conceitual e decisões.
- **Sprint 7.2** — criar contrato de persistência da governança, sem
  salvar dados.
- **Sprint 7.3** — criar repositório local de governança, sem
  interface.
- **Sprint 7.4** — expor governança no Streamlit de forma discreta e
  controlada.
- **Sprint 7.5** — documentar fechamento, inventário, decisões e
  regressão.

## 4. O que a Sprint 7 não deve fazer inicialmente

- Não criar IA.
- Não criar agente.
- Não criar integração externa.
- Não criar automação.
- Não criar tarefa automática.
- Não criar agenda automática.
- Não enviar mensagem.
- Não alterar Motor STAR.
- Não misturar governança com cálculo.
- Não substituir julgamento humano.
- Não criar CRM paralelo.
- Não criar dashboard paralelo.

## 5. Critérios de sucesso da Sprint 7

- Governança integrada separada do Motor STAR.
- Contrato antes de persistência.
- Persistência antes de interface longitudinal.
- Interface sem execução automática.
- Nenhuma regra STAR alterada.
- Nenhuma tarefa automática criada.
- Nenhum agente acionado.
- Regressão manual passando.
