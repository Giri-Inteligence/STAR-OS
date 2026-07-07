# INVENTÁRIO DA VALIDAÇÃO OPERACIONAL LOCAL — STAR OS

## 1. Módulos funcionais envolvidos

**`app.py`**
- Responsabilidade: orquestrar a interface Streamlit — upload, Matriz
  STAR, Raio-X, investigação, Histórico Investigativo e Governança
  Investigativa.
- Entrada esperada: planilha enviada pelo usuário, interações de
  formulário (seleção de cliente, tipo/status/observação, cliques em
  botão).
- Saída esperada: telas renderizadas, payloads criados e passados aos
  módulos especializados, mensagens de confirmação.
- O que não deve fazer: calcular regra STAR, decidir persistência,
  validar payload — isso é delegado aos módulos especializados.

**`star_governance/leitura_operacional.py`**
- Responsabilidade: gerar uma leitura textual, determinística e não
  prescritiva sobre payloads de governança consultados.
- Entrada esperada: lista de payloads de governança (do repositório).
- Saída esperada: dicionário de síntese e texto formatado, sem
  recomendação de ação.
- O que não deve fazer: recomendar tarefa, plano de ação, prazo ou
  responsável; chamar IA ou agente.

**`star_persistence/contrato_governanca.py`**
- Responsabilidade: definir e validar os payloads persistíveis de
  governança (registro, snapshot, item de loop, ciclo de loop,
  governança integrada).
- Entrada esperada: dados de acompanhamento, status, loop.
- Saída esperada: payloads com metadados de persistência
  (`persistido=False`, `persistencia_habilitada=False`) e identificadores
  determinísticos.
- O que não deve fazer: salvar em banco, executar ação, gerar tarefa.

**`star_persistence/repositorio_governanca.py`**
- Responsabilidade: persistir e consultar payloads de governança em
  SQLite local.
- Entrada esperada: payloads validados, filtros de consulta
  (cliente_id, sessao_id, tipo).
- Saída esperada: registros salvos/consultados, contagens do
  repositório.
- O que não deve fazer: validar regra de negócio, decidir ação,
  alterar schema fora de migração explícita.

**`star_persistence/configuracao_governanca.py`**
- Responsabilidade: resolver o caminho do banco de governança
  (variável de ambiente ou padrão) e relatar se diretório/arquivo já
  existem.
- Entrada esperada: variável de ambiente `STAR_OS_GOVERNANCA_DB`
  (opcional).
- Saída esperada: caminho resolvido, booleanos de existência.
- O que não deve fazer: criar banco ou diretório por conta própria.

**`star_governance/acompanhamento.py`**
- Responsabilidade: criar o registro de acompanhamento operacional
  (tipo, status, observação, usuário) a partir do payload histórico.
- Entrada esperada: payload histórico, tipo/status/observação/usuário.
- Saída esperada: registro de acompanhamento serializável.
- O que não deve fazer: persistir, validar contrato de persistência,
  criar tarefa.

**`star_governance/status_acompanhamento.py`**
- Responsabilidade: normalizar e validar transições de status de
  acompanhamento, gerar snapshot de status.
- Entrada esperada: registros de acompanhamento ordenados.
- Saída esperada: snapshot de status, validação de transições.
- O que não deve fazer: decidir ação, criar prazo ou responsável.

**`star_governance/loop_semanal.py`**
- Responsabilidade: classificar itens no loop semanal e consolidar
  ciclo de loop.
- Entrada esperada: registros de acompanhamento, snapshot de status.
- Saída esperada: item de loop, ciclo de loop, resumo do loop.
- O que não deve fazer: agendar execução, criar tarefa, decidir
  prioridade comercial.

## 2. Testes manuais envolvidos

- `tests/manual/testar_estabilizacao_experiencia_governanca_streamlit.py`
  — valida estaticamente a estabilização da experiência (Sprint 9.4):
  campo Observação com key estável, ausência de elementos proibidos,
  identidade de sessão e leitura operacional presentes.
- `tests/manual/testar_identidade_sessao_governanca_streamlit.py` —
  valida estaticamente que a identidade de sessão investigativa é
  estabilizada antes da seção de Governança e usada tanto no
  salvamento quanto na consulta (Sprint 9.3).
- `tests/manual/testar_validacao_estatica_governanca_streamlit.py` —
  valida estaticamente a estrutura completa do bloco de Governança
  investigativa em `app.py` (aviso metodológico, campos permitidos,
  botões, ausência de elementos proibidos, legenda pós-salvamento).
- `tests/manual/testar_leitura_operacional_governanca.py` — valida a
  lógica de `leitura_operacional.py` isoladamente.
- `tests/manual/testar_contrato_persistencia_governanca.py` — valida
  `contrato_governanca.py` isoladamente.
- `tests/manual/testar_repositorio_local_governanca.py` — valida
  `repositorio_governanca.py` isoladamente.
- `tests/manual/testar_configuracao_governanca.py` — valida
  `configuracao_governanca.py` isoladamente.
- `tests/manual/testar_loop_semanal_governanca.py` — valida
  `loop_semanal.py` isoladamente.
- `tests/manual/testar_status_acompanhamento.py` — valida
  `status_acompanhamento.py` isoladamente.
- `tests/manual/testar_acompanhamento_operacional.py` — valida
  `acompanhamento.py` isoladamente.

## 3. Documentos da Sprint 9

- `docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/PROTOCOLO_VALIDACAO_LOCAL_STREAMLIT.md`
- `docs/MODELO_REGISTRO_ACHADOS_VALIDACAO_LOCAL.md`
- `docs/DECISOES_ARQUITETURAIS_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/ROADMAP_SPRINT_9_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`
- `docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md`
- `docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`
- `docs/CORRECAO_IDENTIDADE_SESSAO_GOVERNANCA.md`
- `docs/RESULTADO_REVALIDACAO_SESSAO_GOVERNANCA_STREAMLIT.md`
- `docs/ESTABILIZACAO_EXPERIENCIA_GOVERNANCA.md`
- `docs/RESULTADO_ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_STREAMLIT.md`
- `docs/FECHAMENTO_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/INVENTARIO_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/REGRESSAO_VALIDACAO_OPERACIONAL_LOCAL.md`
- `docs/GATE_GOVERNANCA_OPERACIONAL_LOCAL_VALIDADA.md`
- `docs/ROADMAP_POS_VALIDACAO_OPERACIONAL_LOCAL.md`

## 4. Capacidades validadas

- Upload e geração da Matriz STAR.
- Acesso ao Raio-X.
- Seção Governança Investigativa.
- Salvamento explícito.
- Consulta read-only.
- Identidade estável de sessão.
- `CICLO_LOOP` por cliente/sessão.
- Leitura operacional não prescritiva.
- Campo Observação validado.
- Legenda pós-salvamento estabilizada.
- Ausência de elementos proibidos.

## 5. Dados tratados

A validação pode ler:

- `cliente_id`;
- `nome_cliente`;
- `vendedor`;
- arquivo/contexto;
- `sessao_id`;
- `tipo_payload_governanca`;
- `registro_id`;
- `snapshot_id`;
- `item_loop_id`;
- `ciclo_id`;
- `governanca_id`;
- `status_acompanhamento`;
- `classificacao_loop`;
- observação;
- payload JSON.

Esses dados **não são**:

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
