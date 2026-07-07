# LOOP SEMANAL DE GOVERNANÇA — STAR OS

## 1. Finalidade

O Loop Semanal de Governança cria uma camada determinística para
consolidar a leitura semanal da continuidade investigativa, a partir dos
registros de acompanhamento (Sprint 6.2) e do status de acompanhamento
(Sprint 6.3), sem criar execução automática.

## 2. O que o loop faz

- Consome payload histórico.
- Consome registros de acompanhamento.
- Consome status de acompanhamento (snapshot da Sprint 6.3).
- Cria item de loop (`criar_item_loop_governanca`).
- Classifica item no ciclo (`classificar_item_loop`).
- Identifica itens sem registro operacional.
- Identifica itens em acompanhamento.
- Identifica itens aguardando evidência.
- Identifica itens aguardando decisão humana.
- Identifica itens com decisão registrada.
- Identifica itens encerrados.
- Identifica itens suspensos.
- Identifica inconsistências.
- Ordena itens para leitura técnica (`ordenar_itens_loop`).
- Gera resumo do ciclo (`gerar_resumo_loop_semanal`).
- Cria pacote semanal em memória (`criar_ciclo_loop_semanal`).
- Valida ciclo (`validar_ciclo_loop_semanal`).
- Formata leitura textual simples.

## 3. O que o loop não faz

- Não salva dados.
- Não cria banco.
- Não cria tabela.
- Não altera schema SQLite.
- Não altera `app.py`.
- Não integra com Streamlit.
- Não cria tela.
- Não cria botão.
- Não cria calendário.
- Não cria agenda.
- Não cria tarefa.
- Não cria plano de ação.
- Não cria prazo.
- Não cria responsável automático.
- Não envia mensagem.
- Não aciona agente.
- Não usa IA.
- Não consome token.
- Não chama API externa.
- Não altera o Motor STAR.
- Não recalcula a Matriz STAR.
- Não altera o Excel de saída.
- Não altera o PDF.

## 4. Classificações do loop

- `SEM_REGISTRO_OPERACIONAL`
- `REVISAO_DO_CICLO`
- `AGUARDANDO_EVIDENCIA`
- `AGUARDANDO_DECISAO`
- `DECISAO_REGISTRADA`
- `ENCERRADO`
- `SUSPENSO`
- `INCONSISTENTE`

## 5. Ordem técnica de leitura

A ordenação por peso (`obter_pesos_classificacao_loop`) é apenas
organização técnica da leitura semanal — itens inconsistentes e que
dependem de decisão humana aparecem primeiro, para facilitar a revisão.

- Não é prioridade comercial.
- Não é recomendação de ação.
- Não é plano de ação.
- Não é agenda de execução.
- Não é lista de tarefas.

## 6. Relação com Registro de Acompanhamento

O loop consome os registros criados pela Sprint 6.2
(`star_governance/acompanhamento.py`), sem alterá-los.

## 7. Relação com Status de Acompanhamento

O loop usa o snapshot e a validação de consistência de status criados
pela Sprint 6.3 (`star_governance/status_acompanhamento.py`), sem
alterar aquele módulo.

## 8. Relação com Persistência

Esta sprint não persiste o loop. A Persistência Inicial (Sprint 5)
permanece separada. Persistência futura do loop deve ser tratada em
sprint própria, se houver justificativa metodológica e arquitetural.

## 9. Relação com agentes futuros

Agentes futuros poderão operar sobre ciclos de governança apenas depois
que a governança determinística estiver consolidada.

- Agente futuro não deve decidir sozinho.
- Agente futuro não deve executar sem validação.
- Agente futuro não deve alterar histórico sem rastreabilidade.
- Agente futuro não deve transformar loop em automação invisível.

## 10. Limites atuais

- Loop existe apenas em memória.
- Não há persistência de loop.
- Não há tela no Streamlit.
- Não há edição.
- Não há exclusão.
- Não há envio de mensagem.
- Não há tarefa.
- Não há agenda.
- Não há automação.
- Não há agente.

## 11. Fechamento — Sprint 6.5

O Loop Semanal compõe a Governança Inicial fechada na Sprint 6.5 (ver
`docs/FECHAMENTO_GOVERNANCA_INICIAL.md`).
