# DECISÃO PÓS-VALIDAÇÃO LOCAL NO STREAMLIT — STAR OS

## 1. Finalidade

Este documento consolida a decisão sobre avanço do STAR OS após a
execução real da Sprint 9.2, com base em
`docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md` e
`docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md`.

## 2. Resultado consolidado

- Validação visual real foi executada de fato em navegador, contra um
  servidor Streamlit local real, com planilha válida e cliente real.
- A maior parte do fluxo da Governança Investigativa funcionou
  corretamente: seção localizada, aviso metodológico íntegro, campos
  permitidos corretos, ausência de campos proibidos, ausência de
  gráfico/ranking/dashboard/CRM, salvamento explícito funcional,
  preservação de PDF/Excel, preservação do Motor STAR.
- Um achado foi classificado como **BUG FUNCIONAL — ALTA**
  (ACHADO-9-2-001): o identificador de sessão da investigação é
  recalculado a cada rerun do Streamlit, o que faz a consulta de
  governança salva não localizar dados que foram de fato persistidos
  minutos antes para o mesmo cliente.
- Um achado foi registrado como **RISCO METODOLÓGICO — MÉDIA**
  (ACHADO-9-2-002), sem confirmação de defeito real do produto —
  necessita reconfirmação com interação humana real.
- Um achado foi registrado como **AJUSTE VISUAL — BAIXA**
  (ACHADO-9-2-003), sem impacto funcional.

## 3. Decisão sobre avanço

**O STAR OS não avança para IA, agentes ou qualquer integração
externa até que o ACHADO-9-2-001 seja corrigido e reconfirmado por
nova validação local real.**

Isso não é uma mudança de política — é a aplicação direta da condição
já prevista em `docs/FECHAMENTO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
(Seção 7) e em `docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md`
(Seção 7), que já bloqueavam avanço a IA/agentes até validação visual
real ser executada e aprovada. O achado confirmado nesta sprint torna
esse bloqueio explícito e fundamentado, em vez de apenas pendente por
ausência de execução.

## 4. Justificativa

- O achado ACHADO-9-2-001 compromete diretamente um dos critérios de
  aprovação do protocolo de validação
  (`docs/PROTOCOLO_VALIDACAO_LOCAL_STREAMLIT.md`, Seção 7 — "Consulta
  read-only funciona") e aciona um critério de bloqueio já previsto na
  arquitetura da validação (`docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md`,
  Seção 7 — "`CICLO_LOOP` não aparecendo por cliente/sessão após
  salvamento").
- A causa raiz está isolada em `app.py` (camada de orquestração), não
  em `contrato_governanca.py`, `repositorio_governanca.py` ou no
  schema SQLite — confirmado por chamada direta ao repositório com o
  `sessao_id` correto, que retornou os 5 payloads esperados,
  incluindo o `CICLO_LOOP`.
- Corrigir esse problema antes de qualquer evolução futura é coerente
  com o princípio já registrado no roadmap: "validar antes de
  expandir", "observar antes de corrigir", "registrar achado antes de
  alterar" (`docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md`, Seção 5).

## 5. Restrições preservadas

- `star_core` permanece protegido e inalterado.
- `star_ingestion` permanece protegido e inalterado.
- `star_intelligence` permanece protegido e inalterado.
- `star_persistence` permanece protegido e inalterado nesta sprint.
- `star_governance` permanece protegido e inalterado nesta sprint.
- `app.py` não foi alterado nesta sprint (a correção do
  ACHADO-9-2-001 fica para sprint própria, controlada).
- `tests/manual` permanece protegido e inalterado nesta sprint.
- Nenhum banco foi criado dentro do repositório.
- Nenhum PDF ou Excel foi alterado.
- Nenhuma tarefa, agenda, plano de ação, CRM, dashboard, IA ou agente
  foi criado.
- Nenhum bug foi corrigido nesta sprint — apenas observado, registrado
  e classificado, conforme exigido pela Sprint 9.2.

## 6. Condição para IA/agentes

IA e agentes continuam bloqueados até:

- o fechamento completo da Sprint 9 (validação, correção controlada do
  ACHADO-9-2-001, reconfirmação real em navegador, estabilização de
  UX);
- decisão arquitetural específica e explícita para permitir IA ou
  agentes, tomada em sprint própria;
- confirmação de que a consulta de governança salva localiza
  corretamente os dados persistidos para o cliente/sessão testado, em
  nova execução real no navegador.

Esta condição é consistente com — e não substitui — a condição já
registrada em `docs/ROADMAP_POS_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
(Seção 5) e em `docs/FECHAMENTO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
(Seção 7).

## 7. Próxima sprint recomendada

**Sprint 9.3 — Correção Controlada da Identidade de Sessão da
Investigação para Consulta de Governança**, com escopo estrito
definido em `docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`, Seção 7.
