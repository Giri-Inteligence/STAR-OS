# ROADMAP DA SPRINT 5 — PERSISTÊNCIA E HISTÓRICO INVESTIGATIVO

## 1. Objetivo da Sprint 5

A Sprint 5 deve transformar o estado investigativo temporário em histórico
rastreável, sem quebrar o Motor STAR e sem transformar recomendação em
execução automática.

## 2. Sub-sprints planejadas

- Sprint 5.1 — Arquitetura da Persistência e Histórico Investigativo — **CONCLUÍDA**.
- Sprint 5.2 — Contrato de Dados e Serialização do Histórico Investigativo — **CONCLUÍDA**.
- Sprint 5.3 — Repositório Local Controlado — **CONCLUÍDA** (decisão: SQLite via `sqlite3` da biblioteca padrão).
- Sprint 5.4 — Histórico Investigativo no Streamlit — próxima etapa recomendada.
- Sprint 5.5 — Fechamento da Persistência Inicial.

## 3. Objetivo de cada sub-sprint

- **Sprint 5.1** — documentar arquitetura, modelo de dados e decisões.
- **Sprint 5.2** — criar funções determinísticas para transformar
  investigação, pacote e conclusão em payload canônico serializável, ainda
  sem salvar.
- **Sprint 5.3** — implementar repositório local controlado, após decisão
  entre JSON ou SQLite.
- **Sprint 5.4** — integrar consulta de histórico no Streamlit de forma
  discreta.
- **Sprint 5.5** — documentar fechamento, inventário, decisões e
  regressão.

## 4. O que a Sprint 5 não deve fazer inicialmente

- Não criar agente.
- Não criar IA.
- Não criar integração externa.
- Não criar automação.
- Não criar plano de ação automático.
- Não criar tarefa automática.
- Não alterar Motor STAR.
- Não misturar persistência com cálculo.
- Não substituir julgamento humano.

## 5. Critérios de sucesso da Sprint 5

- Persistência rastreável.
- Histórico por cliente.
- Separação entre sessões.
- Preservação de snapshots.
- Nenhuma regra STAR alterada.
- Nenhuma conclusão de causa raiz automática.
- Exportações Excel/PDF preservadas.
- Regressão manual passando.
