# HISTÓRICO INVESTIGATIVO NO STREAMLIT — STAR OS

## 1. Finalidade

A Sprint 5.4 integra o repositório local controlado (Sprint 5.3) ao
Streamlit, permitindo salvar e consultar o histórico investigativo de
forma controlada, dentro do expander do Raio-X Operacional do Cliente,
logo após a Conclusão Investigativa.

## 2. O que a integração faz

- Exibe a seção "Histórico Investigativo".
- Valida o caminho local do banco (`validar_caminho_db_historico`).
- Permite salvar histórico por ação explícita do usuário (botão).
- Gera o payload canônico a partir dos dados já existentes na tela.
- Inicializa o schema SQLite quando necessário, apenas ao salvar.
- Salva o payload no repositório local (`salvar_payload_historico`).
- Bloqueia sobrescrita silenciosa de uma sessão já existente.
- Lista sessões históricas do cliente selecionado.
- Permite carregar um payload histórico para leitura.
- Exibe um resumo simples da sessão histórica carregada.

## 3. O que a integração não faz

- Não salva automaticamente.
- Não altera a investigação atual ao carregar histórico.
- Não preenche campos automaticamente.
- Não cria plano de ação.
- Não cria tarefa.
- Não cria automação.
- Não usa IA.
- Não consome token.
- Não chama API externa.
- Não cria login.
- Não cria multiusuário.
- Não cria dashboard paralelo.
- Não altera o Motor STAR.
- Não recalcula a Matriz STAR.
- Não altera o Excel de saída.
- Não altera o PDF.

## 4. Caminho do banco

- O caminho padrão é definido por `star_persistence/configuracao.py`
  (`obter_caminho_db_historico`).
- A variável de ambiente `STAR_OS_HISTORICO_DB` pode sobrescrever o
  caminho padrão.
- O padrão recomendado é fora do repositório
  (`Path.home() / ".star_os" / "historico_investigativo.sqlite"`).
- Arquivos `.db`, `.sqlite` e `.sqlite3` foram adicionados ao
  `.gitignore` para reduzir o risco de commit acidental.

## 5. Regra de salvamento

- O salvamento só ocorre quando o usuário clica em
  "Salvar histórico investigativo".
- Uma sessão já existente não é sobrescrita automaticamente.
- `permitir_atualizacao=True` não é exposto na interface nesta sprint.
- Isso preserva o histórico contra perda silenciosa.

## 6. Regra de consulta

- A consulta histórica é somente leitura.
- Carregar uma sessão histórica não altera os campos da investigação
  atual em tela.
- O histórico carregado é exibido apenas como resumo.
- Não há edição de histórico nesta sprint.
- Não há exclusão de histórico nesta sprint.

## 7. Limites atuais

- Persistência é local.
- Sem login.
- Sem multiusuário.
- Sem controle de permissão.
- Sem sincronização em nuvem.
- Sem governança operacional completa.
- Sem versionamento avançado (atualização substitui a mesma sessão, não
  cria uma nova versão).
- O caminho do banco em ambiente hospedado pode exigir configuração
  futura via `STAR_OS_HISTORICO_DB`.

## 8. Próxima etapa

A Sprint 5.5 — Fechamento da Persistência Inicial — deve documentar o
fechamento, o inventário, as decisões e os limites da persistência
inicial, além de consolidar a regressão manual de toda a Sprint 5.

**Atualização:** a Sprint 5.5 consolidou esta integração como parte do
fechamento formal da Persistência Inicial (ver
`docs/FECHAMENTO_PERSISTENCIA_INICIAL.md`).
