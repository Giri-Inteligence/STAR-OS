# REGRESSÃO DA PERSISTÊNCIA INICIAL — STAR OS

## 1. Finalidade

Este documento consolida os critérios de regressão da Persistência
Inicial (Sprint 5), reunindo a regressão técnica, visual, de artefatos e
arquitetural em um único ponto de referência.

## 2. Regressão técnica

Compilação:

```
python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py tests/manual/*.py
```

Testes da Persistência Inicial:

```
python tests/manual/testar_configuracao_persistencia.py
python tests/manual/testar_repositorio_local_historico.py
python tests/manual/testar_contrato_historico_investigativo.py
```

Testes anteriores de regressão:

```
python tests/manual/testar_conclusao_investigativa.py
python tests/manual/testar_pacote_investigativo.py
python tests/manual/testar_investigacao_operacional.py
python tests/manual/testar_recomendacoes_por_papel.py
python tests/manual/testar_hipoteses_operacionais.py
python tests/manual/testar_raio_x_cliente.py
python tests/manual/testar_priorizacao_carteira.py
python tests/manual/testar_relatorio_ingestao.py
python tests/manual/testar_diagnostico_mapeamento.py
python tests/manual/testar_normalizacao_meses.py
python tests/manual/testar_normalizacao_valores.py
python tests/manual/testar_qualidade_linhas.py
```

## 3. Regressão visual no Streamlit

- [ ] Upload Excel funciona.
- [ ] Matriz STAR gera corretamente.
- [ ] Relatório de ingestão aparece.
- [ ] Fila de Prioridade aparece.
- [ ] Raio-X Operacional aparece.
- [ ] Hipóteses Operacionais aparecem.
- [ ] Recomendações por Papel aparecem.
- [ ] Investigação Operacional aparece.
- [ ] Pacote Investigativo aparece.
- [ ] Conclusão Investigativa aparece.
- [ ] Histórico Investigativo aparece.
- [ ] Caminho do banco aparece discretamente.
- [ ] Banco não é criado apenas por abrir a tela.
- [ ] Histórico só é salvo ao clicar no botão.
- [ ] Sessão duplicada não é sobrescrita silenciosamente.
- [ ] Sessões históricas do cliente aparecem.
- [ ] Carregar histórico exibe resumo simples.
- [ ] Carregar histórico não altera investigação atual.
- [ ] Excel baixa.
- [ ] PDF baixa.
- [ ] Planilha inválida continua bloqueando.

## 4. Regressão de artefatos

- Não deve haver `.db`, `.sqlite` ou `.sqlite3` dentro do repositório.
- Não deve haver JSON funcional de persistência dentro do repositório.
- `.gitignore` deve conter proteção contra bancos locais.
- Banco de teste deve ser criado apenas em `tempfile`.
- Banco real deve ficar fora do repositório.

## 5. Regressão arquitetural

- `app.py` apenas orquestra a integração.
- `star_core` não foi alterado.
- `star_ingestion` não foi alterado.
- `star_intelligence` não foi alterado.
- `star_persistence` concentra a persistência.
- Motor STAR permanece protegido.
- Persistência não recalcula nada.
- Histórico não gera plano de ação.
- Histórico não cria tarefa.
- Histórico não usa IA.
