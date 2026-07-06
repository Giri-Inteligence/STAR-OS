# ROADMAP DA SPRINT 9 — VALIDAÇÃO OPERACIONAL LOCAL E ESTABILIZAÇÃO DA EXPERIÊNCIA

## 1. Objetivo da Sprint 9

A Sprint 9 deve validar a experiência real da Governança Investigativa
em ambiente local, registrar achados, corrigir UX sem nova capacidade e
estabilizar a experiência antes de IA/agentes.

## 2. Sub-sprints planejadas

- Sprint 9.1 — Arquitetura da Validação Operacional Local — **CONCLUÍDA**.
- Sprint 9.2 — Execução Guiada da Validação Visual Local — **CONCLUÍDA
  COM BUG FUNCIONAL** (ver
  `docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`).
- Sprint 9.3 — Correção Controlada da Identidade de Sessão da
  Investigação para Consulta de Governança — **CONCLUÍDA** (correção
  aplicada e revalidada em navegador real, resultado CORREÇÃO APROVADA
  — ver `docs/RESULTADO_REVALIDACAO_SESSAO_GOVERNANCA_STREAMLIT.md`).
- Sprint 9.4 — Estabilização da Experiência de Governança — **CONCLUÍDA**
  (ACHADO-9-2-002 não reproduzido/limitação de automação; ACHADO-9-2-003
  corrigido; resultado ESTABILIZAÇÃO APROVADA — ver
  `docs/RESULTADO_ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_STREAMLIT.md`).
- Sprint 9.5 — Fechamento da Validação Operacional Local.

## 3. Objetivo de cada sub-sprint

- **Sprint 9.1** — documentar arquitetura, protocolo, modelo de
  achados, decisões e roadmap.
- **Sprint 9.2** — executar validação visual local real, registrar
  evidências e classificar achados.
- **Sprint 9.3** — corrigir apenas ajustes aprovados de UX, sem criar
  nova capacidade.
- **Sprint 9.4** — estabilizar experiência, textos, ordem e clareza.
- **Sprint 9.5** — fechar validação local, inventário, regressão e
  critérios de avanço.

## 4. O que a Sprint 9 não deve fazer inicialmente

- Não criar IA.
- Não criar agente.
- Não criar automação externa.
- Não enviar mensagem.
- Não criar tarefa automática.
- Não criar agenda automática.
- Não criar CRM paralelo.
- Não criar dashboard paralelo.
- Não criar plano de ação automático.
- Não alterar Motor STAR.
- Não misturar governança com cálculo.
- Não substituir julgamento humano.

## 5. Critérios de sucesso da Sprint 9

- Validação local registrada.
- Achados classificados.
- UX estabilizada.
- Leitura operacional confirmada como não prescritiva.
- Ausência de tarefa/agenda/plano preservada.
- Motor STAR protegido.
- Regressão passando.
- Decisão clara sobre possibilidade ou bloqueio de IA/agentes.

## 6. Atualização — Sprint 9.2

A validação visual local real foi executada (não estática, não
simulada). O resultado, os achados e a decisão de avanço estão
registrados em `docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`,
`docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md` e
`docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`. Um achado de bug
funcional (identidade de sessão da investigação) foi confirmado e
redefine o escopo da Sprint 9.3.

## 7. Atualização — Sprint 9.3

O ACHADO-9-2-001 foi corrigido (estabilização do `sessao_id` via
`st.session_state` em `app.py`) e revalidado em navegador real, com
resultado CORREÇÃO APROVADA (ver
`docs/CORRECAO_IDENTIDADE_SESSAO_GOVERNANCA.md` e
`docs/RESULTADO_REVALIDACAO_SESSAO_GOVERNANCA_STREAMLIT.md`). Próxima
sprint recomendada: **Sprint 9.4 — Estabilização da Experiência de
Governança.**

## 8. Atualização — Sprint 9.4

O ACHADO-9-2-002 foi reavaliado e classificado como não reproduzido em
revalidação local (limitação da automação sintética anterior); o
ACHADO-9-2-003 foi corrigido com ajuste visual mínimo. Resultado:
ESTABILIZAÇÃO APROVADA (ver
`docs/ESTABILIZACAO_EXPERIENCIA_GOVERNANCA.md` e
`docs/RESULTADO_ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_STREAMLIT.md`).
Próxima sprint recomendada: **Sprint 9.5 — Fechamento da Validação
Operacional Local.**
