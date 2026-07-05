# INVENTÁRIO DA GOVERNANÇA INICIAL — STAR OS

## 1. Módulos criados

### `star_governance/__init__.py`

- **Responsabilidade:** documentar o propósito do pacote `star_governance`.
- **Entrada esperada:** nenhuma (arquivo de inicialização de pacote).
- **Saída esperada:** nenhuma (apenas docstring do pacote).
- **O que não deve fazer:** não deve executar código automaticamente no
  import, não deve abrir conexão, não deve criar banco.

### `star_governance/acompanhamento.py`

- **Responsabilidade:** criar e validar o Registro de Acompanhamento
  Operacional em memória, extraindo contexto do payload histórico da
  Sprint 5.
- **Entrada esperada:** payload canônico do Histórico Investigativo e
  parâmetros de tipo/status/observação/evidência/decisão.
- **Saída esperada:** dicionário serializável com `json.dumps`,
  identificado por hash determinístico, sem alterar o payload original.
- **O que não deve fazer:** não deve salvar dados, não deve criar tarefa,
  não deve chamar IA, não deve enviar mensagem.

### `star_governance/status_acompanhamento.py`

- **Responsabilidade:** avaliar, validar e interpretar estados e
  transições do acompanhamento, a partir dos registros da Sprint 6.2.
- **Entrada esperada:** payload histórico e lista de registros de
  acompanhamento.
- **Saída esperada:** snapshot de status (dict serializável), avaliação
  de transições e leitura textual não prescritiva.
- **O que não deve fazer:** não deve persistir status, não deve criar
  tarefa, não deve recomendar ação.

### `star_governance/loop_semanal.py`

- **Responsabilidade:** consolidar registros e status de acompanhamento
  em um ciclo semanal técnico de governança, em memória.
- **Entrada esperada:** payload histórico, registros de acompanhamento e
  contexto opcional (uma ou mais sessões/clientes).
- **Saída esperada:** item de loop e ciclo semanal (dicts serializáveis
  com `json.dumps`), ordenados por peso técnico de leitura.
- **O que não deve fazer:** não deve persistir o ciclo, não deve criar
  agenda ou calendário, não deve recomendar ação.

## 2. Testes manuais criados

- **`tests/manual/testar_acompanhamento_operacional.py`** — valida
  utilitários seguros de dict/lista, normalização de tipo e status,
  extração de contexto do payload histórico, criação e validação do
  registro de acompanhamento, geração de leitura e formatação textual.
- **`tests/manual/testar_status_acompanhamento.py`** — valida listagem
  de status e transições permitidas, identificação de status final,
  dependência de evidência/decisão, avaliação de transições (incluindo
  bloqueio e reabertura controlada de `ENCERRADO`), ordenação de
  registros, identificação de status atual, validação de consistência de
  sequência e criação de snapshot.
- **`tests/manual/testar_loop_semanal_governanca.py`** — valida
  classificações e pesos técnicos do loop, geração de ID determinístico,
  classificação de itens a partir de um snapshot de status, criação de
  item e ciclo semanal, ordenação técnica, resumo quantitativo e
  validação estrutural de item/ciclo.

## 3. Documentos criados

- `docs/ARQUITETURA_GOVERNANCA_INVESTIGATIVA.md`
- `docs/MODELO_CONCEITUAL_LOOP_OPERACIONAL.md`
- `docs/DECISOES_ARQUITETURAIS_GOVERNANCA_INVESTIGATIVA.md`
- `docs/ROADMAP_SPRINT_6_GOVERNANCA_LOOP.md`
- `docs/REGISTRO_ACOMPANHAMENTO_OPERACIONAL.md`
- `docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`
- `docs/LOOP_SEMANAL_GOVERNANCA.md`
- `docs/FECHAMENTO_GOVERNANCA_INICIAL.md`
- `docs/INVENTARIO_GOVERNANCA_INICIAL.md`
- `docs/REGRESSAO_GOVERNANCA_INICIAL.md`
- `docs/ROADMAP_POS_GOVERNANCA_INICIAL.md`

## 4. Entidades conceituais consolidadas

- **Registro de Acompanhamento Operacional** — documenta uma observação,
  retorno, evidência complementar ou decisão sobre uma sessão
  investigativa já salva.
- **Status de Acompanhamento da Investigação** — estado conceitual
  (`NAO_INICIADO` a `ENCERRADO`/`SUSPENSO`) que organiza a continuidade
  de uma sessão.
- **Snapshot de Status** — fotografia em memória do estado atual de
  acompanhamento de uma sessão, com validação de consistência.
- **Item de Loop Semanal** — unidade do ciclo semanal, classificando uma
  sessão conforme seu status atual de acompanhamento.
- **Ciclo de Loop Semanal** — pacote que agrupa múltiplos itens de loop
  em um período de referência.
- **Resumo do Loop** — contagem quantitativa dos itens do ciclo por
  classificação.
- **Classificação do Loop** — categoria técnica de leitura
  (`SEM_REGISTRO_OPERACIONAL` a `INCONSISTENTE`) usada para ordenar itens
  do ciclo, sem qualquer juízo de prioridade comercial.

## 5. Dados organizados em memória

- Cliente investigado.
- Sessão histórica.
- Status STAR do snapshot.
- Status conclusivo da investigação.
- Registros de acompanhamento.
- Status atual do acompanhamento.
- Transições avaliadas.
- Item de loop.
- Classificação do loop.
- Ciclo semanal.
- Resumo quantitativo do ciclo.

## 6. Dados não persistidos ainda

- Registros de acompanhamento.
- Status de acompanhamento.
- Snapshots de status.
- Itens de loop.
- Ciclos semanais.
- Decisões operacionais persistidas.
- Responsáveis.
- Prazos.
- Tarefas.
- Agenda.
- Calendário.
- Logs de auditoria.
- Integrações externas.
- Inferências de IA.

## 7. Como usar na regressão

- Os testes Python (`tests/manual/testar_*.py`) validam acompanhamento,
  status e loop semanal de forma isolada, sem depender do Streamlit.
- A regressão deve confirmar que a governança não altera o Motor STAR.
- A regressão deve confirmar que nenhum banco, JSON funcional ou
  diretório de dados é criado.
- A regressão deve confirmar que `app.py`, `star_core`, `star_ingestion`,
  `star_intelligence` e `star_persistence` permanecem intocados.
- O GitHub Desktop deve ser usado para push após o commit local ser
  validado (nenhum push é feito automaticamente pelas sprints).
