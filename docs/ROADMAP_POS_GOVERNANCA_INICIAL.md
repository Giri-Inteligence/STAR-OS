# ROADMAP PÓS-GOVERNANÇA INICIAL — STAR OS

## 1. Estado atual

A Governança Inicial permite estruturar acompanhamento, status e loop
semanal em memória, consumindo o histórico investigativo já persistido
(Sprint 5) e preservando separação entre análise, acompanhamento e
execução. Nada da governança é salvo, exposto no Streamlit ou
automatizado nesta fase.

## 2. Próxima fase recomendada

**Sprint 7 — Integração Controlada da Governança.**

A próxima fase deve estudar como expor e/ou persistir governança de
forma controlada, sem transformar o STAR OS em dashboard, CRM paralelo
ou gestor de tarefas.

## 3. Possíveis sub-sprints da Sprint 7

Propostas apenas como roadmap, sujeitas a detalhamento e aprovação em
sprints próprias:

- Sprint 7.1 — Arquitetura da Integração Controlada da Governança.
- Sprint 7.2 — Contrato de Persistência da Governança.
- Sprint 7.3 — Repositório Local de Governança.
- Sprint 7.4 — Governança no Streamlit.
- Sprint 7.5 — Fechamento da Governança Integrada.

## 4. O que a Sprint 7 não deve fazer no início

- Não criar IA.
- Não criar agente.
- Não criar automação externa.
- Não enviar mensagem.
- Não criar tarefa automática.
- Não criar agenda automática.
- Não transformar loop em execução.
- Não alterar Motor STAR.
- Não misturar governança com cálculo.
- Não substituir julgamento humano.
- Não criar CRM paralelo.
- Não criar dashboard paralelo.

## 5. Critério para avanço

- Governança inicial validada em memória.
- Testes de acompanhamento, status e loop passando.
- Nenhuma regra STAR alterada.
- Nenhum banco commitado.
- Nenhum JSON funcional criado.
- Regressão manual aprovada.
- Decisão arquitetural explícita antes de persistir ou expor governança
  no Streamlit.

**Atualização:** a Sprint 7.1 iniciou a Arquitetura da Integração
Controlada da Governança (ver
`docs/ARQUITETURA_INTEGRACAO_CONTROLADA_GOVERNANCA.md`).

**Atualização:** a Sprint 7.2 avançou para o contrato de persistência da
governança, ainda sem salvar dados (ver
`docs/CONTRATO_PERSISTENCIA_GOVERNANCA.md`).

**Atualização:** a Sprint 7.3 avançou para o Repositório Local de
Governança, ainda sem Streamlit (ver
`docs/REPOSITORIO_LOCAL_GOVERNANCA.md`).

**Atualização:** a Sprint 7.4 avançou para exposição controlada da
governança no Streamlit (ver `docs/GOVERNANCA_STREAMLIT.md`).

**Atualização:** a Integração Controlada da Governança foi formalmente
fechada na Sprint 7.5 (ver `docs/FECHAMENTO_GOVERNANCA_INTEGRADA.md`).
