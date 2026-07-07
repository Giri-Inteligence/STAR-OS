# ROADMAP PÓS-PERSISTÊNCIA INICIAL — STAR OS

## 1. Estado atual

A Persistência Inicial permite salvar e consultar histórico investigativo
local, com payload canônico, SQLite controlado e integração discreta no
Streamlit. O salvamento é sempre explícito, a consulta é somente leitura,
e o Motor STAR permanece intocado e separado da camada de persistência.

## 2. Próxima fase recomendada

**Sprint 6 — Governança Investigativa e Loop Operacional.**

A próxima fase deve estudar como transformar o histórico investigativo em
governança operacional recorrente, sem transformar recomendação em
execução automática e sem substituir o julgamento humano por automação.

## 3. Possíveis sub-sprints da Sprint 6

Propostas apenas como roadmap, sujeitas a detalhamento e aprovação em
sprints próprias:

- Sprint 6.1 — Arquitetura da Governança Investigativa.
- Sprint 6.2 — Registro de Acompanhamento Operacional.
- Sprint 6.3 — Status de Acompanhamento da Investigação.
- Sprint 6.4 — Loop Semanal de Governança.
- Sprint 6.5 — Fechamento da Governança Inicial.

## 4. O que a Sprint 6 não deve fazer no início

- Não criar IA.
- Não criar agente.
- Não criar automação externa.
- Não enviar mensagem.
- Não criar tarefa automática.
- Não transformar recomendação em execução.
- Não alterar Motor STAR.
- Não misturar governança com cálculo.
- Não substituir julgamento humano.

## 5. Critério para avanço

- Persistência inicial validada no Streamlit real.
- Histórico salvo e carregado com sucesso.
- Nenhuma regra STAR alterada.
- Nenhum banco commitado.
- Regressão manual aprovada.

**Atualização:** a Sprint 6.1 iniciou a Arquitetura da Governança
Investigativa e Loop Operacional (ver
`docs/ARQUITETURA_GOVERNANCA_INVESTIGATIVA.md`).
