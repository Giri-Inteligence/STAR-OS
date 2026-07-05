# CONTRATO DE PERSISTÊNCIA DA GOVERNANÇA — STAR OS

## 1. Finalidade

O contrato de persistência da governança define estruturas canônicas,
serializáveis e validáveis para futura persistência de governança.

- Contrato não salva dados.
- Contrato não cria banco.
- Contrato não cria tabela.
- Contrato não altera schema SQLite.
- Contrato não cria repositório.
- Contrato não integra com Streamlit.
- Contrato não cria tarefa.
- Contrato não cria plano de ação.
- Contrato não cria agenda.
- Contrato não usa IA.
- Contrato não consome token.
- Contrato não chama API externa.

## 2. Problema estrutural resolvido

A Governança Inicial (Sprint 6) já existe em memória, mas ainda não
possui formato persistível padronizado. O contrato resolve:

- padronização de payloads de governança;
- serialização segura;
- validação estrutural;
- separação entre dado persistível e execução;
- preparação para repositório local futuro;
- redução do risco de schema prematuro;
- prevenção de acoplamento direto entre Streamlit e objetos em memória.

## 3. Tipos de payload

- `REGISTRO_ACOMPANHAMENTO`
- `SNAPSHOT_STATUS`
- `ITEM_LOOP`
- `CICLO_LOOP`
- `GOVERNANCA_INTEGRADA`

## 4. Payload de Registro de Acompanhamento

Campos principais:

- `tipo_payload_governanca`
- `versao_payload_governanca`
- `registro_id`
- `cliente_id`
- `sessao_id`
- `nome_cliente`
- `dados_registro`
- `metadados_persistencia`

`dados_registro` preserva integralmente a estrutura criada pela Sprint
6.2 (`star_governance/acompanhamento.py`).

## 5. Payload de Snapshot de Status

Campos principais:

- `tipo_payload_governanca`
- `versao_payload_governanca`
- `snapshot_id`
- `cliente_id`
- `sessao_id`
- `nome_cliente`
- `status_atual_acompanhamento`
- `dados_snapshot`
- `metadados_persistencia`

`dados_snapshot` preserva integralmente a estrutura criada pela Sprint
6.3 (`star_governance/status_acompanhamento.py`). Como o snapshot não
possui ID próprio, o `snapshot_id` é gerado deterministicamente a partir
de `cliente_id`, `sessao_id`, `status_atual_acompanhamento`,
`registro_id_atual` e `total_registros`.

## 6. Payload de Item de Loop

Campos principais:

- `tipo_payload_governanca`
- `versao_payload_governanca`
- `item_loop_id`
- `cliente_id`
- `sessao_id`
- `nome_cliente`
- `classificacao_loop`
- `entra_no_loop_ativo`
- `dados_item_loop`
- `metadados_persistencia`

`dados_item_loop` preserva integralmente a estrutura criada pela Sprint
6.4 (`star_governance/loop_semanal.py`).

## 7. Payload de Ciclo de Loop

Campos principais:

- `tipo_payload_governanca`
- `versao_payload_governanca`
- `ciclo_id`
- `tipo_ciclo`
- `periodo_referencia`
- `origem`
- `total_itens`
- `dados_ciclo_loop`
- `metadados_persistencia`

`dados_ciclo_loop` preserva integralmente a estrutura criada pela Sprint
6.4 (`star_governance/loop_semanal.py`).

## 8. Payload de Governança Integrada

Campos principais:

- `tipo_payload_governanca`
- `versao_payload_governanca`
- `governanca_id`
- `cliente_id`
- `sessao_id`
- `nome_cliente`
- `registro_acompanhamento`
- `snapshot_status`
- `item_loop`
- `ciclo_loop`
- `referencias`
- `metadados_persistencia`

Este payload consolida as estruturas da governança (registro, snapshot,
item e ciclo) em um único ponto de referência, sem criar execução — pode
receber qualquer combinação das estruturas, não exigindo que todas
existam simultaneamente.

## 9. Metadados de persistência

Campos:

- `versao_contrato_persistencia_governanca`
- `origem`
- `usuario_registro`
- `criado_em`
- `atualizado_em`
- `persistido`
- `persistencia_habilitada`
- `observacao_contrato`

- `persistido` deve permanecer `False` na Sprint 7.2.
- `persistencia_habilitada` deve permanecer `False` na Sprint 7.2.
- Qualquer payload com `persistido=True` é inválido nesta sprint.
- Qualquer payload com `persistencia_habilitada=True` é inválido nesta
  sprint.

## 10. Validação

O contrato valida:

- tipo de payload;
- versão;
- metadados;
- identificadores mínimos (conforme o tipo);
- serialização com `json.dumps`;
- bloqueio de persistência indevida (`persistido`/`persistencia_habilitada`);
- avisos (não erros) para ausência de `cliente_id` ou `sessao_id`.

## 11. Relação com Sprint 7.3

A Sprint 7.3 poderá usar este contrato para criar o Repositório Local de
Governança.

- A Sprint 7.3 não deve criar contrato novo paralelo.
- A Sprint 7.3 deve reutilizar os payloads desta sprint.
- A Sprint 7.3 deve persistir apenas depois de validar payloads.
- A Sprint 7.3 deve preservar separação entre governança, histórico e
  execução.

## 12. Limites atuais

- Não há banco.
- Não há tabela.
- Não há schema.
- Não há repositório.
- Não há Streamlit.
- Não há tela.
- Não há botão.
- Não há edição.
- Não há exclusão.
- Não há tarefa.
- Não há agenda.
- Não há automação.
- Não há agente.
- Não há IA.

## 13. Continuidade — Sprint 7.3

A Sprint 7.3 passou a usar este contrato como base do Repositório Local
de Governança (ver `docs/REPOSITORIO_LOCAL_GOVERNANCA.md`).

## 14. Continuidade — Sprint 7.4

A Sprint 7.4 passou a gerar payloads pelo contrato a partir da interface
Streamlit (ver `docs/GOVERNANCA_STREAMLIT.md`).

## 15. Fechamento — Sprint 7.5

Este contrato compõe a Governança Integrada fechada na Sprint 7.5 (ver
`docs/FECHAMENTO_GOVERNANCA_INTEGRADA.md`).
