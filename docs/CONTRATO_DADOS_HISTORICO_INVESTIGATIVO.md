# CONTRATO DE DADOS DO HISTÓRICO INVESTIGATIVO — STAR OS

## 1. Finalidade

O contrato de dados transforma o estado investigativo atual (Raio-X,
hipóteses, recomendações, itens investigativos, pacote e conclusão) em um
payload canônico serializável, pronto para uma futura camada de
persistência — sem salvar nada nesta sprint.

## 2. O que o contrato faz

- Cria cliente investigado.
- Cria sessão investigativa.
- Cria snapshot STAR.
- Cria itens investigativos.
- Cria pacote investigativo serializável.
- Cria conclusão investigativa serializável.
- Cria metadados de execução.
- Valida a estrutura final.
- Garante compatibilidade com `json.dumps`.

## 3. O que o contrato não faz

- Não salva dados.
- Não cria banco.
- Não cria JSON funcional.
- Não cria SQLite.
- Não altera `app.py`.
- Não integra com Streamlit.
- Não cria histórico funcional.
- Não cria plano de ação.
- Não cria tarefa.
- Não chama IA.
- Não consome token.
- Não chama API externa.

## 4. Entidades serializadas

- Cliente.
- Sessão.
- Snapshot STAR.
- Itens Investigativos.
- Pacote Investigativo.
- Conclusão Investigativa.
- Metadados da Execução.

## 5. Decisões de contrato

- Payload deve ser dicionário Python puro.
- Payload deve ser serializável em JSON.
- Payload não deve conter DataFrame.
- Payload não deve conter Series.
- Payload não deve conter NaN.
- Payload não deve conter infinito.
- Payload não deve conter objetos complexos.
- IDs devem ser determinísticos.
- Timestamp deve ser string ISO.
- Snapshot STAR copia o estado, não recalcula.

## 6. Relação com a Sprint 5.3

A Sprint 5.3 poderá decidir entre JSON local ou SQLite, usando este
contrato como entrada.

- Se a Sprint 5.3 usar JSON, este payload será a base do arquivo.
- Se a Sprint 5.3 usar SQLite, este payload será a base para mapeamento em
  tabelas.
- A decisão técnica ainda não deve ser implementada nesta sprint.

**Atualização:** a Sprint 5.3 decidiu por SQLite e implementou o
mapeamento deste payload em 8 tabelas relacionais (ver
`docs/REPOSITORIO_LOCAL_HISTORICO_INVESTIGATIVO.md`). Este contrato
continua sendo a fronteira de entrada do repositório, e o payload bruto
também é preservado integralmente na tabela `payloads_historico`.

**Atualização (Sprint 5.4):** o payload canônico passou a ser usado
diretamente pela interface do Streamlit para salvar o histórico
investigativo do cliente selecionado, por ação explícita do usuário (ver
`docs/HISTORICO_INVESTIGATIVO_STREAMLIT.md`).

**Atualização (Sprint 5.5):** este contrato de dados compõe a
Persistência Inicial fechada formalmente na Sprint 5.5 (ver
`docs/FECHAMENTO_PERSISTENCIA_INICIAL.md`).
