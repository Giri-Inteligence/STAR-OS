# INVENTÁRIO DA CONSOLIDAÇÃO OPERACIONAL DA GOVERNANÇA — STAR OS

## 1. Módulos funcionais envolvidos

### `star_persistence/contrato_governanca.py`

- **Responsabilidade:** transformar estruturas de governança em
  payloads canônicos persistíveis; extrair identificadores (incluindo,
  desde a Sprint 8.2, a partir do `CICLO_LOOP`).
- **Entrada esperada:** registro, snapshot, item e/ou ciclo já criados
  por `star_governance`.
- **Saída esperada:** payloads serializáveis com metadados de
  persistência.
- **O que não deve fazer:** não salvar em disco, não criar banco, não
  habilitar persistência.

### `star_persistence/repositorio_governanca.py`

- **Responsabilidade:** persistir localmente em SQLite os payloads já
  validados pelo contrato, incluindo listagem por cliente/sessão.
- **Entrada esperada:** caminho de banco explícito e payload validado.
- **Saída esperada:** resultado de salvar/carregar/listar/contar/validar
  integridade.
- **O que não deve fazer:** não criar banco automaticamente no import,
  não sobrescrever silenciosamente.

### `star_persistence/configuracao_governanca.py`

- **Responsabilidade:** determinar e validar o caminho do banco SQLite
  de governança.
- **Entrada esperada:** variável de ambiente opcional
  `STAR_OS_GOVERNANCA_DB`.
- **Saída esperada:** caminho e resumo de configuração.
- **O que não deve fazer:** não criar arquivo, não criar diretório, não
  abrir conexão.

### `star_governance/acompanhamento.py`

- **Responsabilidade:** criar e validar o Registro de Acompanhamento
  Operacional em memória.
- **Entrada esperada:** payload histórico e parâmetros de acompanhamento.
- **Saída esperada:** registro serializável.
- **O que não deve fazer:** não salvar dados, não criar tarefa.

### `star_governance/status_acompanhamento.py`

- **Responsabilidade:** avaliar, validar e interpretar estados e
  transições do acompanhamento.
- **Entrada esperada:** payload histórico e registros de acompanhamento.
- **Saída esperada:** snapshot de status e leitura textual.
- **O que não deve fazer:** não persistir status, não recomendar ação.

### `star_governance/loop_semanal.py`

- **Responsabilidade:** consolidar registros e status em um ciclo
  semanal técnico, em memória.
- **Entrada esperada:** payload histórico, registros e contexto opcional.
- **Saída esperada:** item de loop e ciclo semanal.
- **O que não deve fazer:** não persistir o ciclo, não criar agenda.

### `star_governance/leitura_operacional.py`

- **Responsabilidade:** interpretar payloads de governança consultados
  em uma leitura curta, determinística e não prescritiva.
- **Entrada esperada:** lista de payloads puros ou linhas retornadas por
  `listar_payloads_governanca`.
- **Saída esperada:** itens normalizados, resumo quantitativo e síntese
  operacional.
- **O que não deve fazer:** não recomendar ação, não criar tarefa, não
  depender de Streamlit ou SQLite.

### `app.py`

- **Responsabilidade:** orquestrar a exibição da seção "Governança
  investigativa" (formulário, salvamento explícito, consulta read-only
  e leitura operacional), chamando os módulos especializados acima.
- **Entrada esperada:** payload histórico do fluxo atual e interação do
  usuário.
- **Saída esperada:** payloads criados/salvos/consultados sob demanda.
- **O que não deve fazer:** não concentrar regras de governança, não
  criar dashboard paralelo.

## 2. Testes manuais envolvidos

- **`tests/manual/testar_contrato_persistencia_governanca.py`** — valida
  os 5 tipos de payload, incluindo identificadores do `CICLO_LOOP`
  (Sprint 8.2).
- **`tests/manual/testar_repositorio_local_governanca.py`** — valida
  schema, salvamento, listagem por cliente/sessão (incluindo
  `CICLO_LOOP`), contagem e integridade.
- **`tests/manual/testar_configuracao_governanca.py`** — valida caminho
  do banco sem criar arquivo.
- **`tests/manual/testar_loop_semanal_governanca.py`** — valida
  classificação, item, ciclo e ordenação do loop.
- **`tests/manual/testar_status_acompanhamento.py`** — valida status e
  transições de acompanhamento.
- **`tests/manual/testar_acompanhamento_operacional.py`** — valida o
  contrato de acompanhamento.
- **`tests/manual/testar_validacao_estatica_governanca_streamlit.py`** —
  valida estaticamente (sem executar Streamlit) a seção "Governança
  investigativa" em `app.py`: presença, avisos, campos, botões, uso dos
  módulos corretos, ausência de campos/gráficos/downloads proibidos.
- **`tests/manual/testar_leitura_operacional_governanca.py`** — valida a
  leitura operacional: payloads vazios, os 5 tipos de payload, linhas do
  repositório, resumo quantitativo, formatação e imutabilidade.

## 3. Documentos da Sprint 8

- `docs/ARQUITETURA_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
- `docs/MODELO_VALIDACAO_VISUAL_GOVERNANCA.md`
- `docs/DECISOES_ARQUITETURAIS_CONSOLIDACAO_OPERACIONAL.md`
- `docs/ROADMAP_SPRINT_8_CONSOLIDACAO_OPERACIONAL.md`
- `docs/CORRECAO_IDENTIFICADORES_CICLO_LOOP.md`
- `docs/VALIDACAO_VISUAL_GUIADA_GOVERNANCA_STREAMLIT.md`
- `docs/ROTEIRO_VALIDACAO_VISUAL_GOVERNANCA_STREAMLIT.md`
- `docs/RESULTADO_VALIDACAO_VISUAL_GOVERNANCA_STREAMLIT.md`
- `docs/LEITURA_OPERACIONAL_GOVERNANCA_SEM_TAREFAS.md`
- `docs/FECHAMENTO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
- `docs/INVENTARIO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
- `docs/REGRESSAO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`
- `docs/ROADMAP_POS_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`

## 4. Capacidades consolidadas

- **Identidade corrigida do CICLO_LOOP** — payload agora carrega
  `cliente_id`/`sessao_id`/`nome_cliente` quando extraíveis dos itens do
  ciclo.
- **Listagem de CICLO_LOOP por cliente/sessão** — repositório passa a
  retornar o `CICLO_LOOP` em consultas filtradas, sem alteração de
  schema.
- **Validação estática da seção Governança Investigativa** — 27
  critérios confirmados por inspeção e teste automatizado do
  código-fonte de `app.py`.
- **Roteiro de validação visual humana** — checklist operacional para
  quando o Streamlit estiver disponível localmente.
- **Leitura operacional não prescritiva** — interpretação curta de
  payloads consultados, sem recomendar ação.
- **Síntese operacional da governança** — resumo booleano de presença
  de cada tipo de payload e completude de identidade.
- **Resumo quantitativo de payloads** — contagem por tipo, status,
  classificação de loop e completude de cliente/sessão.
- **Detalhamento simples por payload** — formatação individual de cada
  item consultado, em expander discreto.
- **Regressão ampliada** — checklist manual cobrindo as quatro
  sub-sprints da Sprint 8.

## 5. Dados tratados

A consolidação pode ler:

- `tipo_payload_governanca`;
- `registro_id`;
- `snapshot_id`;
- `item_loop_id`;
- `ciclo_id`;
- `governanca_id`;
- `cliente_id`;
- `sessao_id`;
- `nome_cliente`;
- `origem`;
- `criado_em`;
- `status_acompanhamento`;
- `classificacao_loop`;
- payload JSON.

Esses dados não são:

- tarefa;
- agenda;
- plano de ação;
- prazo;
- responsável automático;
- mensagem;
- ação externa;
- decisão automatizada.

## 6. O que permanece fora do escopo

- CRM.
- ERP.
- WhatsApp.
- MCP.
- IA.
- Agente.
- Automação externa.
- Tarefa.
- Agenda.
- Calendário.
- Plano de ação automático.
- Recomendação prescritiva.
- Dashboard paralelo.
- Ranking.
- Gráfico.
