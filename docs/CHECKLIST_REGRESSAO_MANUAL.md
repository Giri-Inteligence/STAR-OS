# Checklist de Regressão Manual — STAR OS

Use este checklist antes de qualquer evolução futura sobre o MVP Excel-first.

## 1. Validação inicial

- [ ] Confirmar branch.
- [ ] Confirmar git status limpo.
- [ ] Confirmar que não está na main.

## 2. Teste da planilha base funcional

- [ ] Upload da planilha base.
- [ ] Consolidado retorna 600 clientes.
- [ ] Abas por vendedor retornam João 300, Maria 200, Pedro 100.
- [ ] Bloqueio de duplicidade funciona.
- [ ] Matriz STAR gera.
- [ ] Excel baixa.
- [ ] PDF baixa.

## 3. Teste da planilha suja controlada

- [ ] Linhas vazias removidas.
- [ ] Colunas vazias removidas.
- [ ] Cabeçalho repetido removido.
- [ ] TOTAL removido.
- [ ] SUBTOTAL removido.
- [ ] Cliente real com Total no nome mantido.
- [ ] Carteira final com 11 clientes.
- [ ] Matriz STAR gera.
- [ ] Excel baixa.
- [ ] PDF baixa.

## 4. Teste das planilhas inválidas

- [ ] `sem_cliente.xlsx` bloqueia.
- [ ] `sem_vendedor.xlsx` bloqueia ou exige vendedor manual.
- [ ] `sem_meses.xlsx` bloqueia.
- [ ] `cliente_vazio.xlsx` bloqueia.
- [ ] `base_vazia.xlsx` bloqueia.
- [ ] `meses_invalidos.xlsx` bloqueia.
- [ ] Em planilhas inválidas ou mal mapeadas, verificar se o diagnóstico informa qual campo não foi reconhecido.

## 5. Teste de formatos reais

- [ ] `razao_representante_municipio.xlsx` processa.
- [ ] `empresa_consultor_regiao.xlsx` processa.
- [ ] `conta_responsavel_localidade.xlsx` processa.
- [ ] `meses_numericos.xlsx` processa.
- [ ] `valores_monetarios.xlsx` processa.

## 5.1 Relatório de ingestão

- [ ] O expander "Relatório de ingestão" aparece após o processamento da base.
- [ ] O relatório mostra status PROCESSADO quando a base é aceita.
- [ ] O relatório mostra status BLOQUEADO e os erros quando a base é rejeitada.

## 5.2 Teste de meses avançados

- [ ] `meses_texto_variado.xlsx` processa.
- [ ] `meses_numericos_variados.xlsx` processa.
- [ ] `meses_com_prefixo.xlsx` processa.
- [ ] `meses_fora_ordem.xlsx` processa com meses ordenados corretamente.
- [ ] `meses_invalidos_parciais.xlsx` ignora meses inválidos e processa meses válidos.

## 5.3 Teste de valores monetários avançados

- [ ] `valores_brasileiros.xlsx` processa.
- [ ] `valores_americanos.xlsx` processa.
- [ ] `valores_mistos.xlsx` processa.
- [ ] `valores_vazios_hifen.xlsx` processa.
- [ ] `valores_invalidos_parciais.xlsx` processa com aviso de valores inválidos.

## 5.4 Teste de qualidade de linhas

- [ ] `clientes_zerados_validos.xlsx` processa e preserva clientes zerados reais.
- [ ] `linhas_residuais_obvias.xlsx` remove resíduos evidentes.
- [ ] `misto_zero_residuo.xlsx` preserva cliente real com zero e remove resíduo.
- [ ] `base_parcial_vendedor_ausente.xlsx` gera aviso ou bloqueia conforme validação atual, sem alteração de regra STAR.
- [ ] `cliente_compra_parcial.xlsx` preserva clientes reais com compra parcial, baixa frequência ou meses zerados.

## 6. Critério de aprovação

- Nenhuma planilha válida pode quebrar.
- Nenhuma planilha inválida pode passar silenciosamente.
- Nenhuma regra STAR pode ser alterada para corrigir problema de ingestão.
- Nenhum arquivo `star_core` pode ser alterado em sprint de ingestão sem autorização explícita.

## 7. Fechamento da robustez de ingestão

- [ ] Relatório de ingestão aparece.
- [ ] Diagnóstico de mapeamento explica falhas.
- [ ] Meses avançados processam.
- [ ] Valores avançados processam.
- [ ] Clientes zerados reais permanecem.
- [ ] Linhas residuais evidentes são removidas.
- [ ] Planilhas inválidas continuam bloqueando.
- [ ] Planilhas válidas continuam processando.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 8. Preparação para Inteligência de Carteira

- [ ] Matriz STAR gera corretamente.
- [ ] Campos calculados continuam presentes.
- [ ] Relatório de ingestão continua funcionando.
- [ ] Downloads continuam funcionando.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Nenhum arquivo `star_core` foi alterado.

## 9. Fila de Prioridade da Carteira

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade aparece após a Matriz STAR.
- [ ] Clientes não são removidos da fila.
- [ ] PONTUACAO_PRIORIDADE é exibida.
- [ ] NIVEL_PRIORIDADE é exibido.
- [ ] TIPO_PRIORIDADE é exibido.
- [ ] PDF continua baixando.
- [ ] Excel continua baixando.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Nenhum arquivo `star_core` foi alterado.

## 10. Raio-X Operacional do Cliente

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade continua aparecendo.
- [ ] Raio-X Operacional aparece após a Fila de Prioridade.
- [ ] É possível selecionar um cliente.
- [ ] O cliente selecionado exibe sinais operacionais.
- [ ] A leitura operacional aparece.
- [ ] Nenhuma recomendação nova é criada.
- [ ] PDF continua baixando.
- [ ] Excel continua baixando.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Nenhum arquivo `star_core` foi alterado.

## 11. Hipóteses Operacionais

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade continua aparecendo.
- [ ] Raio-X Operacional continua aparecendo.
- [ ] Hipóteses Operacionais aparecem para o cliente selecionado.
- [ ] Hipóteses por status são exibidas.
- [ ] Hipóteses por sinais são exibidas.
- [ ] Perguntas de validação são exibidas.
- [ ] Alertas de investigação são exibidos.
- [ ] Nenhuma recomendação completa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Nenhum arquivo `star_core` foi alterado.

## 12. Recomendações por Papel

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade continua aparecendo.
- [ ] Raio-X Operacional continua aparecendo.
- [ ] Hipóteses Operacionais continuam aparecendo.
- [ ] Recomendações por Papel aparecem para o cliente selecionado.
- [ ] É possível selecionar VENDEDOR.
- [ ] É possível selecionar GESTOR.
- [ ] É possível selecionar SOCIO.
- [ ] É possível selecionar CONSULTOR.
- [ ] É possível selecionar TODOS.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Nenhum arquivo `star_core` foi alterado.

## 13. Fechamento da Inteligência de Carteira

- [ ] Matriz STAR gera corretamente.
- [ ] Relatório de ingestão continua funcionando.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Opção TODOS funciona nas recomendações.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Nenhuma tarefa automática é criada.
- [ ] Nenhum plano de ação formal é criado.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 14. Motor de Investigação Operacional

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Perguntas de validação viram itens investigativos.
- [ ] É possível preencher resposta textual.
- [ ] É possível selecionar status PENDENTE.
- [ ] É possível selecionar status CONFIRMADA.
- [ ] É possível selecionar status DESCARTADA.
- [ ] É possível selecionar status INCONCLUSIVA.
- [ ] Resumo da investigação aparece.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 15. Pacote Investigativo do Cliente

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Pacote Investigativo aparece.
- [ ] Pacote mostra cliente selecionado.
- [ ] Pacote mostra status STAR.
- [ ] Pacote mostra resumo da hipótese.
- [ ] Pacote mostra resumo da investigação.
- [ ] Pacote mostra maturidade investigativa.
- [ ] Pacote mostra leitura consolidada.
- [ ] Evidências aparecem quando resposta/evidência for preenchida.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 16. Conclusão Investigativa

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Pacote Investigativo aparece.
- [ ] Conclusão Investigativa aparece.
- [ ] Itens confirmados aparecem como HIPOTESE CONFIRMADA.
- [ ] Itens descartados aparecem como HIPOTESE DESCARTADA.
- [ ] Itens inconclusivos aparecem como HIPOTESE INCONCLUSIVA.
- [ ] Itens pendentes aparecem como PENDENTE DE VALIDACAO.
- [ ] Respostas sem status conclusivo aparecem como RESPOSTA SEM CLASSIFICACAO.
- [ ] Status conclusivo geral aparece.
- [ ] Nenhuma causa raiz é concluída automaticamente.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 17. Fechamento do Motor de Investigação

- [ ] Matriz STAR gera corretamente.
- [ ] Relatório de ingestão continua funcionando.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Pacote Investigativo aparece.
- [ ] Conclusão Investigativa aparece.
- [ ] Status investigativo funciona.
- [ ] Classificação conclusiva funciona.
- [ ] Nenhuma causa raiz é concluída automaticamente.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Nenhum banco de dados é criado.
- [ ] Nenhum histórico persistente é criado.
- [ ] Nenhuma tarefa automática é criada.
- [ ] Nenhum plano de ação formal é criado.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 18. Arquitetura da Persistência e Histórico Investigativo

- [ ] Documentação da arquitetura de persistência criada.
- [ ] Modelo de dados do histórico investigativo criado.
- [ ] Decisões arquiteturais da persistência registradas.
- [ ] Roadmap da Sprint 5 criado.
- [ ] Nenhum banco de dados criado.
- [ ] Nenhum arquivo de persistência funcional criado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Excel continua baixando.
- [ ] PDF continua baixando.
- [ ] Testes manuais continuam passando.

## 19. Contrato de Dados e Serialização do Histórico Investigativo

- [ ] Pacote `star_persistence` criado.
- [ ] Contrato de histórico investigativo criado.
- [ ] Payload canônico é gerado em memória.
- [ ] Payload é serializável com `json.dumps`.
- [ ] Payload contém cliente.
- [ ] Payload contém sessão.
- [ ] Payload contém snapshot STAR.
- [ ] Payload contém itens investigativos.
- [ ] Payload contém pacote investigativo.
- [ ] Payload contém conclusão investigativa.
- [ ] Payload contém metadados da execução.
- [ ] Validação estrutural do payload funciona.
- [ ] Nenhum banco de dados é criado.
- [ ] Nenhum JSON funcional de persistência é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 20. Histórico Investigativo no Streamlit

- [ ] Matriz STAR gera corretamente.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Pacote Investigativo aparece.
- [ ] Conclusão Investigativa aparece.
- [ ] Histórico Investigativo aparece.
- [ ] Caminho do banco é exibido discretamente.
- [ ] Banco não é criado apenas por abrir a tela.
- [ ] Histórico só é salvo ao clicar no botão.
- [ ] Payload canônico é gerado.
- [ ] Schema SQLite é inicializado ao salvar.
- [ ] Histórico é salvo com sucesso.
- [ ] Sessão duplicada não é sobrescrita silenciosamente.
- [ ] Sessões históricas do cliente aparecem para consulta.
- [ ] Carregar histórico não altera investigação atual.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.

## 21. Repositório Local Controlado do Histórico Investigativo

- [ ] Pacote `star_persistence.repositorio_local` criado.
- [ ] Decisão técnica por SQLite (stdlib `sqlite3`) registrada.
- [ ] Schema de 8 tabelas criado apenas mediante chamada explícita.
- [ ] Nenhum banco criado automaticamente no import.
- [ ] Salvar payload histórico funciona.
- [ ] Sobrescrita silenciosa de sessão é bloqueada.
- [ ] Atualização explícita (`permitir_atualizacao=True`) não duplica sessão.
- [ ] Consulta de sessões por cliente funciona.
- [ ] Consulta de clientes investigados funciona.
- [ ] Remoção de sessão de teste preserva o cliente.
- [ ] Nenhum arquivo `.db`/`.sqlite`/`.sqlite3` permanente criado no repositório.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 22. Fechamento da Persistência Inicial

- [ ] Arquitetura da persistência documentada.
- [ ] Modelo de dados documentado.
- [ ] Contrato de dados criado.
- [ ] Repositório local criado.
- [ ] Configuração do caminho do banco criada.
- [ ] Integração no Streamlit criada.
- [ ] Histórico Investigativo aparece.
- [ ] Histórico salva somente por clique explícito.
- [ ] Consulta histórica é somente leitura.
- [ ] Carregar histórico não altera investigação atual.
- [ ] Sessão duplicada não é sobrescrita silenciosamente.
- [ ] Banco padrão fica fora do repositório.
- [ ] `.gitignore` protege arquivos `.db`, `.sqlite` e `.sqlite3`.
- [ ] Nenhum banco permanente é commitado.
- [ ] Nenhum JSON funcional é commitado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum arquivo `star_core` foi alterado.
- [ ] Nenhuma regra STAR foi alterada.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Testes manuais passam.
- [ ] Validação visual no Streamlit real deve ser executada.

## 23. Arquitetura da Governança Investigativa e Loop Operacional

- [ ] Arquitetura da Governança Investigativa criada.
- [ ] Modelo Conceitual do Loop Operacional criado.
- [ ] Decisões Arquiteturais da Governança Investigativa criadas.
- [ ] Roadmap da Sprint 6 criado.
- [ ] Nenhum código funcional alterado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Testes manuais continuam passando.

## 24. Registro de Acompanhamento Operacional

- [ ] Pacote `star_governance` criado.
- [ ] Contrato de acompanhamento criado.
- [ ] Registro de acompanhamento é gerado em memória.
- [ ] Registro é serializável com `json.dumps`.
- [ ] Tipos de acompanhamento são normalizados.
- [ ] Status de acompanhamento são normalizados.
- [ ] Contexto do payload histórico é extraído.
- [ ] Registro não altera payload histórico original.
- [ ] Validação estrutural funciona.
- [ ] Pacote de acompanhamento operacional é gerado.
- [ ] Nenhum banco é criado.
- [ ] Nenhuma tabela é criada.
- [ ] Nenhum JSON funcional é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhum arquivo `star_persistence` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 25. Status de Acompanhamento da Investigação

- [ ] Módulo de status de acompanhamento criado.
- [ ] Status permitidos são listados.
- [ ] Transições permitidas são listadas.
- [ ] Status final é identificado.
- [ ] Dependência de evidência é identificada.
- [ ] Dependência de decisão é identificada.
- [ ] Transições são avaliadas.
- [ ] Reabertura de encerrado é controlada.
- [ ] Registros são ordenados por `criado_em`.
- [ ] Status atual é identificado.
- [ ] Consistência da sequência é validada.
- [ ] Snapshot de status é criado em memória.
- [ ] Snapshot é serializável com `json.dumps`.
- [ ] Nenhum banco é criado.
- [ ] Nenhuma tabela é criada.
- [ ] Nenhum JSON funcional é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhum arquivo `star_persistence` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 26. Loop Semanal de Governança

- [ ] Módulo de loop semanal criado.
- [ ] Classificações permitidas são listadas.
- [ ] Pesos técnicos de leitura são listados.
- [ ] Item de loop é criado em memória.
- [ ] Item de loop é serializável com `json.dumps`.
- [ ] Item de loop preserva payload original.
- [ ] Item de loop preserva registros originais.
- [ ] Classificação do loop funciona.
- [ ] Itens são ordenados por leitura técnica.
- [ ] Resumo do loop é gerado.
- [ ] Ciclo semanal é criado em memória.
- [ ] Ciclo semanal é serializável com `json.dumps`.
- [ ] Validação de item funciona.
- [ ] Validação de ciclo funciona.
- [ ] Nenhum banco é criado.
- [ ] Nenhuma tabela é criada.
- [ ] Nenhum JSON funcional é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhum arquivo `star_persistence` é alterado.
- [ ] Nenhum arquivo `star_governance/acompanhamento.py` é alterado.
- [ ] Nenhum arquivo `star_governance/status_acompanhamento.py` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 27. Fechamento da Governança Inicial

- [ ] Arquitetura da Governança Investigativa documentada.
- [ ] Modelo Conceitual do Loop Operacional documentado.
- [ ] Decisões Arquiteturais da Governança documentadas.
- [ ] Registro de Acompanhamento Operacional criado.
- [ ] Status de Acompanhamento da Investigação criado.
- [ ] Loop Semanal de Governança criado.
- [ ] Inventário da Governança Inicial criado.
- [ ] Regressão da Governança Inicial criada.
- [ ] Roadmap pós-governança inicial criado.
- [ ] Nenhum código funcional alterado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela criada.
- [ ] Nenhum botão criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Testes manuais passam.

## 28. Arquitetura da Integração Controlada da Governança

- [ ] Arquitetura da Integração Controlada da Governança criada.
- [ ] Modelo Conceitual da Governança Integrada criado.
- [ ] Decisões Arquiteturais da Integração da Governança criadas.
- [ ] Roadmap da Sprint 7 criado.
- [ ] Nenhum código funcional alterado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela criada.
- [ ] Nenhum botão criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Testes manuais continuam passando.

## 29. Contrato de Persistência da Governança

- [ ] Contrato de persistência da governança criado.
- [ ] Tipos de payload de governança são normalizados.
- [ ] Metadados de persistência são criados com `persistido=False`.
- [ ] Metadados de persistência são criados com `persistencia_habilitada=False`.
- [ ] Payload de Registro de Acompanhamento é criado.
- [ ] Payload de Snapshot de Status é criado.
- [ ] Payload de Item de Loop é criado.
- [ ] Payload de Ciclo de Loop é criado.
- [ ] Payload de Governança Integrada é criado.
- [ ] Payloads são serializáveis com `json.dumps`.
- [ ] Payloads são validados.
- [ ] Payloads com `persistido=True` são bloqueados.
- [ ] Payloads com `persistencia_habilitada=True` são bloqueados.
- [ ] Estruturas originais não são alteradas.
- [ ] Nenhum banco é criado.
- [ ] Nenhuma tabela é criada.
- [ ] Nenhum schema SQLite é alterado.
- [ ] Nenhum JSON funcional é criado.
- [ ] Nenhum repositório é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhum arquivo `star_governance` é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma agenda é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 30. Repositório Local de Governança

- [ ] Repositório local de governança criado.
- [ ] Schema local de governança é inicializado.
- [ ] Schema local de governança é verificado.
- [ ] Payload válido é salvo.
- [ ] Payload inválido é bloqueado.
- [ ] Payload duplicado é bloqueado por padrão.
- [ ] Sobrescrita explícita funciona.
- [ ] Payload salvo é carregado.
- [ ] Payloads são listados.
- [ ] Filtros por tipo, cliente e sessão funcionam.
- [ ] Lote de payloads é salvo.
- [ ] Registros são contados por tipo.
- [ ] Integridade do repositório é validada.
- [ ] Payloads originais não são alterados.
- [ ] Banco temporário de teste é criado fora do repositório.
- [ ] Nenhum banco permanente é criado dentro do repositório.
- [ ] Nenhum JSON funcional é criado.
- [ ] Nenhum `app.py` é alterado.
- [ ] Nenhum arquivo `star_core` é alterado.
- [ ] Nenhum arquivo `star_ingestion` é alterado.
- [ ] Nenhum arquivo `star_intelligence` é alterado.
- [ ] Nenhum arquivo `star_governance` é alterado.
- [ ] Nenhum contrato anterior da Sprint 5 é alterado.
- [ ] Nenhum contrato da Sprint 7.2 é alterado.
- [ ] Nenhuma regra STAR é alterada.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma agenda é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum token é consumido.
- [ ] Testes manuais continuam passando.

## 31. Governança no Streamlit

- [ ] Configuração de banco de governança criada.
- [ ] Configuração não cria banco automaticamente.
- [ ] Seção de governança aparece no Streamlit.
- [ ] Seção fica próxima do fluxo de investigação/histórico.
- [ ] Interface informa que governança não é tarefa.
- [ ] Interface informa que governança não é plano de ação.
- [ ] Interface informa que governança não é agenda.
- [ ] Campos permitidos são apenas tipo, status, observação e usuário opcional.
- [ ] Não há campo de responsável.
- [ ] Não há campo de prazo.
- [ ] Não há campo de tarefa.
- [ ] Não há campo de plano de ação.
- [ ] Não há calendário.
- [ ] Não há agenda.
- [ ] Salvamento exige botão explícito.
- [ ] Payloads são criados via `contrato_governanca.py`.
- [ ] Payloads são salvos via `repositorio_governanca.py`.
- [ ] Consulta é somente leitura.
- [ ] Nenhum dashboard paralelo é criado.
- [ ] Nenhum CRM paralelo é criado.
- [ ] Nenhum gráfico novo é criado.
- [ ] Nenhum PDF é alterado.
- [ ] Nenhum Excel é alterado.
- [ ] Nenhum Motor STAR é alterado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum agente é acionado.
- [ ] Testes manuais continuam passando.

## 32. Fechamento da Governança Integrada

- [ ] Arquitetura da Integração Controlada da Governança documentada.
- [ ] Modelo Conceitual da Governança Integrada documentado.
- [ ] Decisões Arquiteturais da Integração da Governança documentadas.
- [ ] Contrato de Persistência da Governança criado.
- [ ] Repositório Local de Governança criado.
- [ ] Configuração Local de Governança criada.
- [ ] Governança no Streamlit criada.
- [ ] Inventário da Governança Integrada criado.
- [ ] Regressão da Governança Integrada criada.
- [ ] Roadmap pós-governança integrada criado.
- [ ] Limitação do `CICLO_LOOP` documentada.
- [ ] Nenhum código funcional alterado nesta sprint.
- [ ] Nenhum `app.py` alterado nesta sprint.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela nova criada.
- [ ] Nenhum botão novo criado.
- [ ] Nenhum gráfico criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Nenhum agente acionado.
- [ ] Testes manuais passam.

## 33. Arquitetura da Consolidação Operacional da Governança

- [ ] Arquitetura da Consolidação Operacional da Governança criada.
- [ ] Modelo de Validação Visual da Governança criado.
- [ ] Decisões Arquiteturais da Consolidação Operacional criadas.
- [ ] Roadmap da Sprint 8 criado.
- [ ] Limitação do `CICLO_LOOP` documentada.
- [ ] Decisão recomendada de corrigir `CICLO_LOOP` antes da validação visual ampla registrada.
- [ ] Nenhum código funcional alterado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela criada.
- [ ] Nenhum botão criado.
- [ ] Nenhum gráfico criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Nenhum agente acionado.
- [ ] Testes manuais continuam passando.

## 34. Correção Controlada de Identificadores do CICLO_LOOP

- [ ] `CICLO_LOOP` passa a carregar `cliente_id` quando disponível.
- [ ] `CICLO_LOOP` passa a carregar `sessao_id` quando disponível.
- [ ] `CICLO_LOOP` passa a carregar `nome_cliente` quando disponível.
- [ ] `CICLO_LOOP` sem identificadores continua válido com aviso.
- [ ] Payload antigo sem `cliente_id`/`sessao_id` não quebra validação.
- [ ] Repositório lista `CICLO_LOOP` por `cliente_id`.
- [ ] Repositório lista `CICLO_LOOP` por `sessao_id`.
- [ ] Schema SQLite de governança não muda.
- [ ] `app.py` não é alterado.
- [ ] `star_governance` não é alterado.
- [ ] `repositorio_governanca.py` não é alterado.
- [ ] Motor STAR não é alterado.
- [ ] Nenhum PDF é alterado.
- [ ] Nenhum Excel é alterado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma agenda é criada.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum agente é acionado.
- [ ] Testes manuais continuam passando.

## 35. Validação Visual Guiada da Governança no Streamlit

- [ ] Seção Governança investigativa existe no `app.py`.
- [ ] Seção está próxima do fluxo de Raio-X/Histórico Investigativo.
- [ ] Aviso metodológico existe.
- [ ] Campos permitidos existem.
- [ ] Não há campo de responsável.
- [ ] Não há campo de prazo.
- [ ] Não há campo de tarefa.
- [ ] Não há campo de plano de ação.
- [ ] Não há calendário.
- [ ] Não há agenda.
- [ ] Botão de salvamento explícito existe.
- [ ] Botão de consulta read-only existe.
- [ ] Payloads são criados via `contrato_governanca.py`.
- [ ] Payloads são salvos via `repositorio_governanca.py`.
- [ ] Consulta usa `repositorio_governanca.py`.
- [ ] `CICLO_LOOP` corrigido deve aparecer por cliente/sessão.
- [ ] Não há gráfico novo.
- [ ] Não há ranking.
- [ ] Não há dashboard paralelo.
- [ ] Não há CRM paralelo.
- [ ] Não há download novo.
- [ ] Não há chamada de IA.
- [ ] Não há agente.
- [ ] Não há API externa.
- [ ] Nenhum `app.py` alterado nesta sprint.
- [ ] Nenhum código funcional alterado nesta sprint.
- [ ] Nenhum PDF alterado.
- [ ] Nenhum Excel alterado.
- [ ] Teste estático passa.
- [ ] Testes manuais continuam passando.

## 36. Leitura Operacional da Governança sem Tarefas

- [ ] Módulo de leitura operacional criado.
- [ ] Leitura aceita payload puro.
- [ ] Leitura aceita linha do repositório.
- [ ] Leitura identifica `REGISTRO_ACOMPANHAMENTO`.
- [ ] Leitura identifica `SNAPSHOT_STATUS`.
- [ ] Leitura identifica `ITEM_LOOP`.
- [ ] Leitura identifica `CICLO_LOOP`.
- [ ] Leitura identifica `GOVERNANCA_INTEGRADA`.
- [ ] Leitura identifica status.
- [ ] Leitura identifica classificação de loop.
- [ ] Leitura identifica `CICLO_LOOP` com identidade.
- [ ] Leitura identifica consulta completa para cliente/sessão.
- [ ] Leitura vazia é válida com aviso.
- [ ] Formatação textual não recomenda ação.
- [ ] Formatação textual não cria tarefa.
- [ ] `app.py` apenas exibe a leitura dentro da seção existente.
- [ ] Nenhum botão novo é criado.
- [ ] Nenhuma tela nova é criada.
- [ ] Nenhum gráfico é criado.
- [ ] Nenhum ranking é criado.
- [ ] Nenhuma tarefa é criada.
- [ ] Nenhum plano de ação é criado.
- [ ] Nenhuma agenda é criada.
- [ ] Nenhum responsável automático é criado.
- [ ] Nenhum prazo é criado.
- [ ] Nenhuma IA é chamada.
- [ ] Nenhum agente é acionado.
- [ ] Nenhum PDF é alterado.
- [ ] Nenhum Excel é alterado.
- [ ] Testes manuais continuam passando.

## 37. Fechamento da Consolidação Operacional da Governança

- [ ] Fechamento da Consolidação Operacional criado.
- [ ] Inventário da Consolidação Operacional criado.
- [ ] Regressão da Consolidação Operacional criada.
- [ ] Roadmap pós-consolidação operacional criado.
- [ ] Correção do `CICLO_LOOP` inventariada.
- [ ] Validação estática da Governança inventariada.
- [ ] Roteiro visual humano inventariado.
- [ ] Leitura operacional inventariada.
- [ ] Limite de validação visual real pendente documentado.
- [ ] Próxima fase recomendada documentada.
- [ ] Nenhum código funcional alterado nesta sprint.
- [ ] Nenhum `app.py` alterado nesta sprint.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela nova criada.
- [ ] Nenhum botão novo criado.
- [ ] Nenhum gráfico criado.
- [ ] Nenhum ranking criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Nenhum agente acionado.
- [ ] Testes manuais passam.

## 38. Arquitetura da Validação Operacional Local

- [ ] Arquitetura da Validação Operacional Local criada.
- [ ] Protocolo de Validação Local no Streamlit criado.
- [ ] Modelo de Registro de Achados criado.
- [ ] Decisões Arquiteturais da Validação Operacional Local criadas.
- [ ] Roadmap da Sprint 9 criado.
- [ ] Critérios de achado definidos.
- [ ] Critérios de aprovação definidos.
- [ ] Critérios de reprovação definidos.
- [ ] Bloqueio de IA/agentes antes de validação local registrado.
- [ ] Nenhum código funcional alterado.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhum teste alterado.
- [ ] Nenhuma regra STAR alterada.
- [ ] Nenhum banco criado.
- [ ] Nenhuma tabela criada.
- [ ] Nenhum schema SQLite alterado.
- [ ] Nenhum JSON funcional criado.
- [ ] Nenhuma tela criada.
- [ ] Nenhum botão criado.
- [ ] Nenhum gráfico criado.
- [ ] Nenhuma tarefa criada.
- [ ] Nenhum plano de ação criado.
- [ ] Nenhuma agenda criada.
- [ ] Nenhum calendário criado.
- [ ] Nenhuma IA chamada.
- [ ] Nenhum token consumido.
- [ ] Nenhum agente acionado.
- [ ] Testes manuais continuam passando.

## 39. Execução Guiada da Validação Visual Local

- [ ] Streamlit executado localmente contra planilha válida real.
- [ ] Upload processado com sucesso.
- [ ] Matriz STAR gerada corretamente.
- [ ] Cliente selecionado no Raio-X.
- [ ] Seção Governança investigativa localizada.
- [ ] Aviso metodológico íntegro.
- [ ] Campos permitidos corretos (tipo, status, observação, usuário opcional).
- [ ] Nenhum campo proibido encontrado como elemento funcional.
- [ ] Salvamento explícito funciona e cria banco fora do repositório.
- [ ] Achado de bug funcional na consulta de governança registrado (identidade de sessão instável entre reruns).
- [ ] Achado classificado como RISCO METODOLÓGICO registrado (campo de observação, não confirmado como defeito real).
- [ ] Achado classificado como AJUSTE VISUAL registrado (legenda de configuração desatualizada no mesmo rerun).
- [ ] Nenhum gráfico/ranking/dashboard/CRM encontrado na seção de governança.
- [ ] PDF/Excel permaneceram inalterados.
- [ ] Nenhum código funcional alterado durante a validação.
- [ ] Nenhum `app.py` alterado.
- [ ] Nenhum arquivo `star_core` alterado.
- [ ] Nenhum arquivo `star_ingestion` alterado.
- [ ] Nenhum arquivo `star_intelligence` alterado.
- [ ] Nenhum arquivo `star_persistence` alterado.
- [ ] Nenhum arquivo `star_governance` alterado.
- [ ] Nenhum arquivo `tests/manual` alterado.
- [ ] Nenhum banco criado dentro do repositório.
- [ ] IA/agentes seguem bloqueados até correção do achado funcional.
- [ ] Testes manuais continuam passando.
