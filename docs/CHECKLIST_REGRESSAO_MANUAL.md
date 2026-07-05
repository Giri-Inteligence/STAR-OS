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

## 5. Teste de formatos reais

- [ ] `razao_representante_municipio.xlsx` processa.
- [ ] `empresa_consultor_regiao.xlsx` processa.
- [ ] `conta_responsavel_localidade.xlsx` processa.
- [ ] `meses_numericos.xlsx` processa.
- [ ] `valores_monetarios.xlsx` processa.

## 6. Critério de aprovação

- Nenhuma planilha válida pode quebrar.
- Nenhuma planilha inválida pode passar silenciosamente.
- Nenhuma regra STAR pode ser alterada para corrigir problema de ingestão.
- Nenhum arquivo `star_core` pode ser alterado em sprint de ingestão sem autorização explícita.
