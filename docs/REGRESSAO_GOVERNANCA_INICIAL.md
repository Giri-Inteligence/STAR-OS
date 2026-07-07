# REGRESSÃO DA GOVERNANÇA INICIAL — STAR OS

## 1. Finalidade

Este documento consolida os critérios de regressão da Governança Inicial
(Sprint 6), reunindo a regressão técnica, arquitetural, de artefatos e
conceitual em um único ponto de referência.

## 2. Regressão técnica

Compilação:

```
python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py star_governance/*.py tests/manual/*.py
```

Testes da Governança Inicial:

```
python tests/manual/testar_loop_semanal_governanca.py
python tests/manual/testar_status_acompanhamento.py
python tests/manual/testar_acompanhamento_operacional.py
```

Testes anteriores de regressão:

```
python tests/manual/testar_configuracao_persistencia.py
python tests/manual/testar_repositorio_local_historico.py
python tests/manual/testar_contrato_historico_investigativo.py
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

## 3. Regressão arquitetural

- `app.py` não deve ser alterado.
- `star_core` não deve ser alterado.
- `star_ingestion` não deve ser alterado.
- `star_intelligence` não deve ser alterado.
- `star_persistence` não deve ser alterado.
- `star_governance/acompanhamento.py` não deve ser alterado nesta sprint.
- `star_governance/status_acompanhamento.py` não deve ser alterado nesta
  sprint.
- `star_governance/loop_semanal.py` não deve ser alterado nesta sprint.
- Motor STAR permanece protegido.
- Governança não recalcula nada.
- Governança não cria tarefa.
- Governança não cria plano de ação.
- Governança não usa IA.

## 4. Regressão de artefatos

- Não deve haver `.db`, `.sqlite` ou `.sqlite3` dentro do repositório.
- Não deve haver JSON funcional de governança dentro do repositório.
- Não deve haver diretório de dados criado.
- Não deve haver arquivo de agenda.
- Não deve haver arquivo de calendário.
- Não deve haver arquivo de tarefa.
- Não deve haver alteração de schema SQLite.

## 5. Regressão conceitual

- Registro de acompanhamento não é tarefa.
- Status de acompanhamento não é execução.
- Loop semanal não é agenda.
- Loop semanal não é calendário.
- Ordenação técnica não é prioridade comercial.
- Aviso não é plano de ação.
- Decisão operacional exige humano.
- Agente futuro não deve decidir sozinho.
- IA futura não deve substituir governança determinística.
