# ROADMAP DA SPRINT 4 — MOTOR DE INVESTIGAÇÃO

## 1. Objetivo da Sprint 4

A Sprint 4 criou a primeira camada investigativa do STAR OS, ainda
temporária e determinística, permitindo transformar hipóteses e perguntas
de validação em itens investigativos registráveis, consolidá-los por
cliente e classificar seu estado conclusivo — sem IA, sem execução
automática e sem persistência.

## 2. Sprints concluídas

- Sprint 4.1 — Motor de Investigação Operacional — **CONCLUÍDA**.
- Sprint 4.2 — Pacote Investigativo do Cliente — **CONCLUÍDA**.
- Sprint 4.3 — Conclusão Investigativa — **CONCLUÍDA**.
- Sprint 4.4 — Fechamento do Motor de Investigação — **CONCLUÍDA**.

## 3. Entregas por sprint

- **Sprint 4.1** — `star_intelligence/investigacao.py`: transforma
  perguntas de validação em itens investigativos com id determinístico,
  permite registrar resposta/evidência/status (PENDENTE, CONFIRMADA,
  DESCARTADA, INCONCLUSIVA) e gera resumo quantitativo. Integrado ao
  `app.py` via `st.session_state`, dentro do expander do Raio-X.
- **Sprint 4.2** — `star_intelligence/pacote_investigativo.py`: consolida
  Raio-X, hipóteses, recomendações e itens investigativos em um único
  pacote legível por cliente, com maturidade investigativa e leitura
  consolidada. Integrado logo após a Investigação Operacional.
- **Sprint 4.3** — `star_intelligence/conclusao_investigativa.py`:
  classifica cada item investigativo do Pacote em HIPOTESE CONFIRMADA,
  HIPOTESE DESCARTADA, HIPOTESE INCONCLUSIVA, PENDENTE DE VALIDACAO ou
  RESPOSTA SEM CLASSIFICACAO, com resumo e leitura conclusiva. Integrado
  logo após o Pacote Investigativo.
- **Sprint 4.4** — Documentação de fechamento consolidando o Motor de
  Investigação antes de avançar para a próxima fase.

## 4. O que a Sprint 4 não fez

- Não criou IA.
- Não consumiu token.
- Não criou agente.
- Não criou integração.
- Não criou banco de dados.
- Não criou login.
- Não criou histórico persistente.
- Não criou plano de ação.
- Não criou tarefa automática.
- Não alterou o Motor STAR.

## 5. Próxima fase recomendada

**Sprint 5 — Persistência e Histórico Investigativo.**

A próxima fase deve estudar como salvar investigação, pacote e conclusão de
forma rastreável, sem quebrar a arquitetura existente e sem transformar
recomendação em execução automática — preservando a separação entre
diagnóstico, hipótese, evidência, recomendação, ação e acompanhamento.
