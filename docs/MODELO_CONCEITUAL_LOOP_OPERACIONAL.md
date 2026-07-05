# MODELO CONCEITUAL DO LOOP OPERACIONAL — STAR OS

## 1. Finalidade

O Loop Operacional define como uma investigação deve evoluir ao longo do
tempo, preservando rastreabilidade e disciplina de acompanhamento, sem
transformar recomendação em execução automática.

## 2. Fluxo conceitual do loop

1. Matriz STAR.
2. Inteligência de Carteira.
3. Hipótese Operacional.
4. Pergunta de Validação.
5. Investigação Operacional.
6. Evidência.
7. Conclusão Investigativa.
8. Histórico Investigativo.
9. Acompanhamento de Governança.
10. Revisão.
11. Nova evidência.
12. Nova conclusão ou manutenção da pendência.

## 3. Separação entre conceitos

- **Diagnóstico** — leitura estruturada da situação.
- **Hipótese** — possibilidade a ser validada.
- **Evidência** — dado ou informação que sustenta validação.
- **Conclusão investigativa** — classificação do estado da hipótese.
- **Recomendação** — orientação sugerida por papel.
- **Acompanhamento** — registro de retorno, evolução ou pendência.
- **Decisão operacional** — escolha humana sobre o que será feito.
- **Execução** — ação realizada fora ou dentro de sistema futuro.

A Sprint 6.1 não implementa execução.

## 4. Estados conceituais de acompanhamento

Propostos apenas conceitualmente, ainda não implementados em código
nesta sprint:

- `NAO_INICIADO`
- `EM_ACOMPANHAMENTO`
- `AGUARDANDO_EVIDENCIA`
- `AGUARDANDO_DECISAO`
- `DECISAO_REGISTRADA`
- `ENCERRADO`
- `SUSPENSO`

## 5. Entidades conceituais futuras

### Ciclo de Governança
- **Finalidade:** agrupar conceitualmente o acompanhamento recorrente de
  um cliente ao longo de múltiplas sessões investigativas.
- **Entrada esperada:** histórico investigativo do cliente.
- **Saída esperada:** leitura consolidada da evolução do cliente.
- **O que não deve fazer:** não deve decidir ou executar nada sozinho.

### Registro de Acompanhamento
- **Finalidade:** registrar que uma sessão ou pendência foi revisitada.
- **Entrada esperada:** sessão ou pendência investigativa existente.
- **Saída esperada:** anotação de acompanhamento vinculada à sessão.
- **O que não deve fazer:** não deve criar tarefa nem enviar mensagem.

### Pendência Investigativa
- **Finalidade:** identificar hipóteses ou itens ainda sem resposta
  conclusiva.
- **Entrada esperada:** itens investigativos com status pendente ou
  inconclusivo.
- **Saída esperada:** lista de pendências a revisitar.
- **O que não deve fazer:** não deve concluir causa raiz automaticamente.

### Decisão Operacional
- **Finalidade:** registrar a escolha humana sobre o que será feito a
  partir de uma conclusão.
- **Entrada esperada:** conclusão investigativa e contexto de
  acompanhamento.
- **Saída esperada:** registro textual da decisão tomada por uma pessoa.
- **O que não deve fazer:** não deve ser gerada automaticamente por
  regra ou por IA.

### Marco de Revisão
- **Finalidade:** sinalizar um ponto no tempo em que uma investigação
  deve ser revisitada.
- **Entrada esperada:** sessão investigativa e cadência de revisão.
- **Saída esperada:** data ou evento conceitual de revisão.
- **O que não deve fazer:** não deve disparar notificação automática
  nesta fase.

### Evidência Complementar
- **Finalidade:** permitir adicionar nova evidência a uma investigação já
  concluída ou pendente, sem apagar a evidência anterior.
- **Entrada esperada:** sessão investigativa existente.
- **Saída esperada:** evidência adicional vinculada à sessão original.
- **O que não deve fazer:** não deve sobrescrever a evidência anterior.

### Histórico de Evolução
- **Finalidade:** permitir comparar o estado de um cliente entre sessões
  diferentes ao longo do tempo.
- **Entrada esperada:** múltiplas sessões investigativas do mesmo
  cliente.
- **Saída esperada:** leitura comparativa entre sessões.
- **O que não deve fazer:** não deve recalcular a Matriz STAR.

## 6. Cadência conceitual

O loop poderá apoiar no futuro:

- revisão semanal;
- revisão mensal;
- acompanhamento de clientes críticos;
- acompanhamento de hipóteses pendentes;
- acompanhamento de conclusões inconclusivas;
- acompanhamento de recomendações não executadas;
- retorno ao histórico investigativo.

Cadência não é implementada nesta sprint.

## 7. Limites do loop

- Loop não envia mensagem.
- Loop não cria tarefa automática.
- Loop não executa ação.
- Loop não substitui CRM.
- Loop não substitui gestor.
- Loop não substitui consultor.
- Loop não substitui julgamento humano.
- Loop não altera Motor STAR.

## 8. Relação com persistência

A Persistência Inicial da Sprint 5 é pré-requisito para o loop porque
permite recuperar histórico, comparar evolução e registrar continuidade
— sem histórico salvo, não há base para acompanhamento.

## 9. Relação com agentes futuros

Agentes futuros poderão auxiliar na execução, mas apenas depois que o
modelo de governança estiver maduro.

- Agente não deve decidir sozinho.
- Agente não deve alterar histórico sem rastreabilidade.
- Agente não deve transformar recomendação em execução sem validação.
- Agente futuro deve operar sobre regras e trilhas já definidas.

## 10. Continuidade — Sprint 6.2

O Registro de Acompanhamento Operacional (`star_governance/acompanhamento.py`)
é a primeira entidade funcional do loop, ainda sem persistência (ver
`docs/REGISTRO_ACOMPANHAMENTO_OPERACIONAL.md`).

## 11. Continuidade — Sprint 6.3

O status de acompanhamento (`star_governance/status_acompanhamento.py`)
é pré-condição para o futuro loop semanal (ver
`docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`).

## 12. Continuidade — Sprint 6.4

O Loop Semanal de Governança (`star_governance/loop_semanal.py`)
materializa o ciclo conceitual em memória, ainda sem persistência (ver
`docs/LOOP_SEMANAL_GOVERNANCA.md`).
