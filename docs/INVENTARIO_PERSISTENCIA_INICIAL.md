# INVENTÁRIO DA PERSISTÊNCIA INICIAL — STAR OS

## 1. Módulos criados

### `star_persistence/__init__.py`

- **Responsabilidade:** documentar o propósito do pacote `star_persistence`.
- **Entrada esperada:** nenhuma (arquivo de inicialização de pacote).
- **Saída esperada:** nenhuma (apenas docstring do pacote).
- **O que não deve fazer:** não deve executar código automaticamente no
  import, não deve abrir conexão, não deve criar banco.

### `star_persistence/contrato_historico.py`

- **Responsabilidade:** transformar dados já calculados (cliente, sessão,
  snapshot STAR, itens investigativos, pacote investigativo, conclusão
  investigativa, metadados de execução) em um payload canônico
  serializável e determinístico.
- **Entrada esperada:** dicionários ou `pd.Series` já produzidos pelo
  Motor de Investigação e pela Inteligência de Carteira.
- **Saída esperada:** um dicionário Python puro, seguro para
  `json.dumps`, com IDs determinísticos (`hashlib.sha256`) e timestamps
  ISO-8601.
- **O que não deve fazer:** não deve salvar em disco, não deve abrir
  banco, não deve recalcular regras STAR, não deve chamar IA.

### `star_persistence/repositorio_local.py`

- **Responsabilidade:** persistir e consultar o payload canônico em um
  banco SQLite local, usando apenas o módulo padrão `sqlite3`.
- **Entrada esperada:** um `db_path` explícito e um payload já validado
  pelo contrato de dados.
- **Saída esperada:** dicionários de resultado (`ok`, `sessao_id`,
  `cliente_id`, `itens_salvos`, `erro`) e listas de registros consultados.
- **O que não deve fazer:** não deve criar banco automaticamente no
  import, não deve sobrescrever sessão existente silenciosamente, não
  deve recalcular a Matriz STAR.

### `star_persistence/configuracao.py`

- **Responsabilidade:** determinar e validar o caminho do banco SQLite
  local, sem depender de Streamlit ou pandas.
- **Entrada esperada:** variável de ambiente opcional
  `STAR_OS_HISTORICO_DB` e/ou um `db_path` explícito.
- **Saída esperada:** string de caminho e dicionário de validação
  (`valido`, `db_path`, `avisos`, `erros`).
- **O que não deve fazer:** não deve criar arquivo, não deve criar
  diretório automaticamente, não deve abrir conexão.

## 2. Testes manuais criados

- **`tests/manual/testar_contrato_historico_investigativo.py`** — valida
  a limpeza de valores serializáveis, geração de IDs determinísticos,
  timestamps, normalização de status de sessão, construção de cada
  entidade do payload e validação estrutural do payload completo.
- **`tests/manual/testar_repositorio_local_historico.py`** — valida
  conexão, inicialização e verificação de schema, salvamento, contagem de
  registros, bloqueio e atualização explícita de sobrescrita, consulta
  por cliente e por sessão, remoção de sessão de teste e ausência de
  artefatos permanentes.
- **`tests/manual/testar_configuracao_persistencia.py`** — valida
  obtenção do caminho padrão e customizado via variável de ambiente,
  preparação de diretório sem criar o banco, verificação de caminho
  dentro/fora do repositório e formatação da validação.

## 3. Documentos criados

- `docs/ARQUITETURA_PERSISTENCIA_HISTORICO_INVESTIGATIVO.md`
- `docs/MODELO_DADOS_HISTORICO_INVESTIGATIVO.md`
- `docs/DECISOES_ARQUITETURAIS_PERSISTENCIA_INVESTIGATIVA.md`
- `docs/ROADMAP_SPRINT_5_PERSISTENCIA_HISTORICO.md`
- `docs/CONTRATO_DADOS_HISTORICO_INVESTIGATIVO.md`
- `docs/REPOSITORIO_LOCAL_HISTORICO_INVESTIGATIVO.md`
- `docs/HISTORICO_INVESTIGATIVO_STREAMLIT.md`
- `docs/FECHAMENTO_PERSISTENCIA_INICIAL.md`
- `docs/INVENTARIO_PERSISTENCIA_INICIAL.md`
- `docs/REGRESSAO_PERSISTENCIA_INICIAL.md`
- `docs/ROADMAP_POS_PERSISTENCIA_INICIAL.md`

## 4. Tabelas SQLite previstas

- **`clientes_investigados`** — identidade do cliente investigado (nome,
  vendedor, cidade, colunas de origem do mapeamento).
- **`sessoes_investigativas`** — cada sessão de investigação vinculada a
  um cliente.
- **`snapshots_star`** — fotografia dos dados STAR no momento da sessão,
  nunca recalculada.
- **`itens_investigativos`** — cada pergunta/hipótese investigada, com
  resposta e evidência.
- **`pacotes_investigativos`** — pacote consolidado da investigação
  (prioridade, hipótese-resumo, maturidade).
- **`conclusoes_investigativas`** — classificação conclusiva da sessão,
  com contagens de hipóteses por status.
- **`metadados_execucao`** — dados técnicos da execução (arquivo de
  origem, versão do modelo, ambiente).
- **`payloads_historico`** — payload JSON bruto completo, preservado como
  registro original imutável.

## 5. Dados persistidos

- Cliente investigado.
- Sessão investigativa.
- Snapshot STAR.
- Itens investigativos.
- Pacote investigativo.
- Conclusão investigativa.
- Metadados da execução.
- Payload bruto serializado.

## 6. Dados não persistidos ainda

- Plano de ação.
- Tarefas.
- Responsáveis.
- Prazos.
- Agenda.
- Acompanhamento de execução.
- Anexos reais.
- Dados de CRM.
- Dados de ERP.
- Mensagens WhatsApp.
- Usuário autenticado.
- Permissões.
- Logs de auditoria avançados.
- Inferências de IA.

## 7. Como usar na regressão

- Os testes Python (`tests/manual/testar_*.py`) validam contrato,
  repositório e configuração de forma isolada, sem depender do
  Streamlit.
- O Streamlit valida o comportamento real da integração (botão de
  salvar, consulta, mensagens).
- A regressão deve confirmar que o Histórico Investigativo aparece,
  salva por clique, bloqueia duplicidade, permite consultar sessão e não
  altera a investigação atual em tela.
- O GitHub Desktop deve ser usado para push após o commit local ser
  validado (nenhum push é feito automaticamente pelas sprints).
