# INVENTÁRIO DA GOVERNANÇA INTEGRADA — STAR OS

## 1. Módulos envolvidos

### `star_governance/acompanhamento.py`

- **Responsabilidade:** criar e validar o Registro de Acompanhamento
  Operacional em memória, extraindo contexto do payload histórico da
  Sprint 5.
- **Entrada esperada:** payload canônico do Histórico Investigativo e
  parâmetros de tipo/status/observação/evidência/decisão.
- **Saída esperada:** dicionário serializável com `json.dumps`,
  identificado por hash determinístico.
- **O que não deve fazer:** não salvar dados, não criar tarefa, não
  chamar IA.

### `star_governance/status_acompanhamento.py`

- **Responsabilidade:** avaliar, validar e interpretar estados e
  transições do acompanhamento.
- **Entrada esperada:** payload histórico e lista de registros de
  acompanhamento.
- **Saída esperada:** snapshot de status (dict serializável) e leitura
  textual não prescritiva.
- **O que não deve fazer:** não persistir status, não recomendar ação.

### `star_governance/loop_semanal.py`

- **Responsabilidade:** consolidar registros e status de acompanhamento
  em um ciclo semanal técnico, em memória.
- **Entrada esperada:** payload histórico, registros de acompanhamento e
  contexto opcional.
- **Saída esperada:** item de loop e ciclo semanal (dicts serializáveis),
  ordenados por peso técnico de leitura.
- **O que não deve fazer:** não persistir o ciclo, não criar agenda.

### `star_persistence/contrato_governanca.py`

- **Responsabilidade:** transformar estruturas da governança em
  payloads canônicos persistíveis (`REGISTRO_ACOMPANHAMENTO`,
  `SNAPSHOT_STATUS`, `ITEM_LOOP`, `CICLO_LOOP`, `GOVERNANCA_INTEGRADA`).
- **Entrada esperada:** registro, snapshot, item e/ou ciclo já criados
  pelos módulos de `star_governance`.
- **Saída esperada:** payloads serializáveis, com metadados de
  persistência sempre `persistido=False`/`persistencia_habilitada=False`.
- **O que não deve fazer:** não salvar em disco, não criar banco.

### `star_persistence/repositorio_governanca.py`

- **Responsabilidade:** persistir localmente em SQLite os payloads já
  validados pelo contrato.
- **Entrada esperada:** caminho de banco explícito e payload validado.
- **Saída esperada:** resultado de salvar/carregar/listar/contar/validar
  integridade.
- **O que não deve fazer:** não criar banco automaticamente no import,
  não sobrescrever silenciosamente.

### `star_persistence/configuracao_governanca.py`

- **Responsabilidade:** determinar e validar o caminho do banco SQLite
  de governança, sem depender de Streamlit.
- **Entrada esperada:** variável de ambiente opcional
  `STAR_OS_GOVERNANCA_DB`.
- **Saída esperada:** string/`Path` de caminho e resumo de configuração.
- **O que não deve fazer:** não criar arquivo, não criar diretório, não
  abrir conexão.

### `app.py`

- **Responsabilidade:** orquestrar a exibição da seção "Governança
  investigativa" dentro do fluxo do Raio-X/Histórico Investigativo,
  chamando os módulos especializados acima.
- **Entrada esperada:** payload histórico já construído no fluxo
  (Sprint 5.4) e interação do usuário (formulário e botões).
- **Saída esperada:** registro/snapshot/item/ciclo criados sob demanda,
  payloads salvos ou consultados por ação explícita.
- **O que não deve fazer:** não concentrar regras de governança, não
  salvar automaticamente, não criar dashboard paralelo.

## 2. Testes manuais envolvidos

- **`tests/manual/testar_acompanhamento_operacional.py`** — valida o
  contrato de acompanhamento (normalização, criação, validação, leitura,
  formatação).
- **`tests/manual/testar_status_acompanhamento.py`** — valida status
  permitidos, transições, snapshot e consistência de sequência.
- **`tests/manual/testar_loop_semanal_governanca.py`** — valida
  classificação, item, ciclo, ordenação, resumo e validação do loop.
- **`tests/manual/testar_contrato_persistencia_governanca.py`** —
  valida os 5 tipos de payload, identificadores, metadados de
  persistência e bloqueio de `persistido=True`/`persistencia_habilitada=True`.
- **`tests/manual/testar_repositorio_local_governanca.py`** — valida
  schema, salvamento, duplicidade, sobrescrita, carregamento, listagem,
  lote, contagem e integridade, em banco temporário.
- **`tests/manual/testar_configuracao_governanca.py`** — valida caminho
  padrão/customizado do banco e resumo de configuração, sem criar
  arquivo.

## 3. Documentos criados na Sprint 7

- `docs/ARQUITETURA_INTEGRACAO_CONTROLADA_GOVERNANCA.md`
- `docs/MODELO_CONCEITUAL_GOVERNANCA_INTEGRADA.md`
- `docs/DECISOES_ARQUITETURAIS_INTEGRACAO_GOVERNANCA.md`
- `docs/ROADMAP_SPRINT_7_INTEGRACAO_GOVERNANCA.md`
- `docs/CONTRATO_PERSISTENCIA_GOVERNANCA.md`
- `docs/REPOSITORIO_LOCAL_GOVERNANCA.md`
- `docs/GOVERNANCA_STREAMLIT.md`
- `docs/FECHAMENTO_GOVERNANCA_INTEGRADA.md`
- `docs/INVENTARIO_GOVERNANCA_INTEGRADA.md`
- `docs/REGRESSAO_GOVERNANCA_INTEGRADA.md`
- `docs/ROADMAP_POS_GOVERNANCA_INTEGRADA.md`

## 4. Entidades conceituais consolidadas

- **Registro de Acompanhamento Operacional** — documenta observação,
  retorno, evidência ou decisão sobre uma sessão investigativa.
- **Status de Acompanhamento da Investigação** — estado conceitual da
  continuidade de uma sessão.
- **Snapshot de Status** — fotografia em memória do estado atual de
  acompanhamento.
- **Item de Loop Semanal** — unidade do ciclo semanal, classificando uma
  sessão conforme seu status.
- **Ciclo de Loop Semanal** — pacote que agrupa itens de loop em um
  período de referência.
- **Payload de Registro de Acompanhamento** — versão persistível do
  registro.
- **Payload de Snapshot de Status** — versão persistível do snapshot.
- **Payload de Item de Loop** — versão persistível do item.
- **Payload de Ciclo de Loop** — versão persistível do ciclo.
- **Payload de Governança Integrada** — payload que consolida registro,
  snapshot, item e ciclo em um único ponto de referência.
- **Repositório Local de Governança** — banco SQLite local, separado do
  schema do Histórico Investigativo.
- **Configuração Local de Governança** — determinação do caminho do
  banco, sem criar arquivo automaticamente.
- **Seção Governança Investigativa no Streamlit** — interface controlada
  para registrar, salvar e consultar governança.

## 5. Dados persistíveis

- Payload de registro de acompanhamento.
- Payload de snapshot de status.
- Payload de item de loop.
- Payload de ciclo de loop.
- Payload de governança integrada.
- Identificadores de cliente.
- Identificadores de sessão.
- Tipo de payload.
- Origem.
- Timestamps.
- Payload JSON serializado.

## 6. Dados que não são execução

Não devem ser tratados como execução:

- status de acompanhamento;
- observação de acompanhamento;
- classificação do loop;
- leitura do loop;
- aviso de evidência;
- aviso de decisão;
- ciclo semanal;
- consulta de governança.

Esses dados não são:

- tarefa;
- agenda;
- plano de ação;
- prazo;
- responsável automático;
- mensagem;
- ação externa;
- decisão automatizada.

## 7. Como usar na regressão

- Os testes Python validam acompanhamento, status, loop, contrato,
  repositório e configuração.
- A regressão visual deve confirmar que a seção aparece no fluxo do
  cliente.
- A regressão visual deve confirmar que não há campo de responsável,
  prazo, tarefa, plano de ação, agenda ou calendário.
- A regressão deve confirmar que a governança não altera o Motor STAR.
- A regressão deve confirmar que PDF e Excel não mudaram.
- A regressão deve confirmar que nenhum banco permanente é criado dentro
  do repositório.
- O GitHub Desktop deve ser usado para push após o commit local ser
  validado.
