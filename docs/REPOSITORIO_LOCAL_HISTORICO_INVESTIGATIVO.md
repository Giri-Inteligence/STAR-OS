# REPOSITÓRIO LOCAL DO HISTÓRICO INVESTIGATIVO — STAR OS

## 1. Finalidade

O repositório local transforma o payload canônico do histórico investigativo
(`star_persistence/contrato_historico.py`) em registros persistidos em um
banco SQLite local, permitindo salvar, consultar e remover sessões
investigativas sem depender de `st.session_state`.

Esta sprint cria apenas a camada de repositório. Não há integração com
`app.py`, não há tela de histórico e não há botão de salvamento no
Streamlit.

## 2. Decisão técnica: SQLite via `sqlite3` (stdlib)

A persistência local usa exclusivamente o módulo padrão `sqlite3` do
Python, sem pacotes externos. Motivos:

- não exige instalação de pacote novo;
- é local e controlado, sem serviço externo;
- é transacional (commit/rollback), reduzindo risco de corrupção parcial;
- reduz o risco de sobrescrita silenciosa presente em arquivos JSON soltos
  (não há como duas escritas concorrentes corromperem o arquivo inteiro);
- permite consultas futuras por cliente, sessão e data sem precisar
  carregar todo o histórico em memória;
- aproxima o STAR OS de um eventual banco relacional gerenciado, caso o
  produto evolua nessa direção;
- preserva a separação já estabelecida na Sprint 5.2 entre o contrato de
  dados (payload canônico) e a camada de persistência (este repositório).

Esta decisão não cria um SaaS, não cria autenticação, não cria
multiusuário e não cria integração externa.

## 3. O que o repositório faz

- Abre conexões SQLite sob demanda (`obter_conexao`), nunca automaticamente.
- Cria o schema de 8 tabelas apenas quando `inicializar_schema` é chamada
  explicitamente com um caminho de banco.
- Verifica a integridade do schema (`verificar_schema`).
- Salva um payload histórico completo (`salvar_payload_historico`),
  incluindo cliente, sessão, snapshot STAR, itens investigativos, pacote
  investigativo, conclusão investigativa e metadados de execução.
- Bloqueia sobrescrita silenciosa de uma sessão já existente, exigindo
  `permitir_atualizacao=True` para atualizar explicitamente.
- Sempre armazena o payload bruto (JSON) na tabela `payloads_historico`,
  preservando o registro original.
- Permite consultar sessões por cliente, listar clientes investigados,
  contar registros e carregar um payload completo por sessão.
- Permite remover uma sessão de teste (`remover_sessao_teste`), preservando
  o cliente.

## 4. O que não faz

- Não integra com `app.py` ou com qualquer tela do Streamlit.
- Não cria botão, download ou histórico visível ao usuário.
- Não cria login, autenticação ou multiusuário.
- Não cria plano de ação, tarefa ou automação.
- Não usa IA, agente, token ou API externa.
- Não instala pacotes novos.
- Não recalcula a Matriz STAR — apenas armazena o snapshot já calculado.
- Não altera `star_core`, `star_ingestion` ou `star_intelligence`.
- Não cria diretório de dados persistidos dentro do repositório de código.
- Não cria arquivo `.db`, `.sqlite` ou `.sqlite3` permanente no projeto.

## 5. Tabelas criadas

- **`clientes_investigados`** — identidade do cliente investigado (nome,
  vendedor, cidade e colunas de origem do mapeamento).
- **`sessoes_investigativas`** — cada sessão de investigação vinculada a um
  cliente, com status, origem e responsável.
- **`snapshots_star`** — a fotografia dos dados STAR (status, curva,
  médias, erosão, meta, ação) no momento da sessão, nunca recalculada.
- **`itens_investigativos`** — cada pergunta/hipótese investigada, com
  resposta e evidência textual.
- **`pacotes_investigativos`** — o pacote consolidado da investigação
  (prioridade, hipótese-resumo, maturidade da investigação).
- **`conclusoes_investigativas`** — a classificação conclusiva da sessão,
  com contagens de hipóteses confirmadas, descartadas e inconclusivas.
- **`metadados_execucao`** — dados técnicos da execução (arquivo de
  origem, versão do modelo, ambiente).
- **`payloads_historico`** — o payload JSON bruto completo da sessão,
  preservado como registro original imutável.

## 6. Regra de sobrescrita

- Salvar uma sessão já existente sem `permitir_atualizacao=True` retorna
  `{"ok": False, "erro": "SESSAO_JA_EXISTE"}` e não altera nenhum dado.
- Salvar com `permitir_atualizacao=True` atualiza os dados da mesma sessão
  (mesmo `sessao_id`), sem duplicar linhas e sem criar uma segunda sessão.
- O cliente (`clientes_investigados`) é atualizado por `UPDATE`, nunca
  recriado, preservando `criado_em` original e evitando qualquer conflito
  de chave estrangeira com outras sessões do mesmo cliente.

## 7. Limites atuais

- Não há versionamento histórico de alterações dentro da mesma sessão
  (a atualização substitui os dados da sessão, não cria uma nova versão).
- Não há identificador externo de cliente (CRM/ERP); a identificação
  continua sendo determinística a partir de nome, vendedor e cidade,
  como definido na Sprint 5.2.
- Não há controle de acesso, login ou permissões.
- Não há integração com o Streamlit — o repositório existe apenas como
  camada testável de forma isolada.

## 8. Próxima etapa (Sprint 5.4)

A Sprint 5.4 deve integrar a consulta de histórico investigativo ao
Streamlit de forma discreta, permitindo visualizar sessões salvas por
cliente sem alterar o Motor STAR nem os fluxos de ingestão e investigação
já existentes.

**Atualização:** a Sprint 5.4 integrou este repositório ao Streamlit, com
salvamento explícito por botão e consulta somente leitura ao histórico do
cliente selecionado (ver `docs/HISTORICO_INVESTIGATIVO_STREAMLIT.md`).
