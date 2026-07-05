# FECHAMENTO DA PERSISTÊNCIA INICIAL — STAR OS

## 1. Finalidade

A Persistência Inicial existe para transformar o estado investigativo
temporário (antes vivo apenas em `st.session_state`) em histórico local
rastreável por cliente, sem alterar o Motor STAR e sem transformar
recomendação em execução automática.

- Persistência não é dashboard.
- Persistência não é Motor STAR.
- Persistência não recalcula Matriz STAR.
- Persistência não cria recomendação.
- Persistência não cria plano de ação.
- Persistência não cria tarefa.
- Persistência não conclui causa raiz.
- Persistência não usa IA nesta fase.
- Persistência não consome token.
- Persistência não chama API externa.
- Persistência não cria integração externa.
- Persistência atua como camada de rastreabilidade.

## 2. Escopo consolidado da Sprint 5

- Arquitetura da Persistência e Histórico Investigativo (5.1).
- Modelo de Dados do Histórico Investigativo (5.1).
- Contrato de Dados e Serialização (5.2).
- Repositório Local Controlado com SQLite (5.3).
- Configuração de caminho do banco (5.4).
- Integração do Histórico Investigativo no Streamlit (5.4).
- Salvamento explícito por botão (5.4).
- Consulta somente leitura de sessões históricas (5.4).
- Bloqueio de sobrescrita silenciosa (5.3/5.4).
- Proteção contra commit acidental de bancos locais via `.gitignore` (5.4).

## 3. Fluxo conceitual consolidado

1. Upload Excel.
2. Motor de Ingestão.
3. Matriz STAR.
4. Inteligência de Carteira.
5. Motor de Investigação.
6. Pacote Investigativo.
7. Conclusão Investigativa.
8. Contrato de Dados.
9. Payload Canônico.
10. Repositório Local.
11. Histórico Investigativo no Streamlit.
12. Governança futura.

## 4. Como a persistência funciona hoje

- O banco padrão fica fora do repositório.
- O caminho padrão é `Path.home() / ".star_os" / "historico_investigativo.sqlite"`.
- O caminho pode ser sobrescrito por `STAR_OS_HISTORICO_DB`.
- O banco não é criado apenas por abrir a tela.
- O diretório e o schema só são preparados ao clicar em
  "Salvar histórico investigativo".
- A sessão duplicada não é sobrescrita automaticamente.
- A consulta histórica é somente leitura.
- Carregar histórico não altera a investigação atual.

## 5. Critérios de sucesso consolidados

- Payload canônico é gerado.
- Payload é serializável com `json.dumps`.
- Schema SQLite é inicializado por chamada explícita.
- Payload é salvo no repositório local.
- Payload pode ser carregado por sessão.
- Sessões podem ser listadas por cliente.
- Clientes investigados podem ser listados.
- Sobrescrita silenciosa é bloqueada.
- Banco local não é commitado no repositório.
- `.gitignore` protege extensões `.db`, `.sqlite` e `.sqlite3`.
- Histórico aparece no Streamlit.
- Salvamento só ocorre por ação explícita.
- Consulta histórica não altera investigação atual.
- Nenhum arquivo `star_core` foi alterado.
- Nenhuma regra STAR foi alterada.
- Excel e PDF continuam preservados.

## 6. Limites atuais

- Persistência é local.
- Não há login.
- Não há multiusuário.
- Não há controle de permissão.
- Não há sincronização em nuvem.
- Não há versionamento avançado.
- Não há trilha de auditoria completa.
- Não há governança operacional persistente completa.
- Não há plano de ação persistente.
- Não há tarefa persistente.
- Não há responsáveis.
- Não há prazos.
- Não há integração com CRM.
- Não há integração com ERP.
- Não há WhatsApp.
- Não há MCP.
- Não há IA assistiva sobre histórico.
- Ambientes hospedados exigirão configuração específica do caminho do
  banco.

## 7. Condição de avanço

O STAR OS só deve avançar para a próxima fase se:

- A regressão manual continuar passando.
- O Motor STAR permanecer protegido.
- A persistência permanecer separada do cálculo.
- O histórico não virar dashboard paralelo.
- O histórico não virar execução automática.
- A consulta histórica continuar somente leitura.
- A governança futura preservar separação entre hipótese, evidência,
  recomendação, ação e acompanhamento.
- A validação visual no Streamlit real for realizada.
