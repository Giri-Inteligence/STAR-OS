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
