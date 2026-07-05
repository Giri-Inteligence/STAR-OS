# REGRESSÃO DA GOVERNANÇA INTEGRADA — STAR OS

## 1. Finalidade

Este documento consolida os critérios de regressão da Governança
Integrada (Sprint 7), reunindo a regressão técnica, arquitetural, visual,
de artefatos e conceitual em um único ponto de referência.

## 2. Regressão técnica

Compilação:

```
python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py star_governance/*.py tests/manual/*.py
```

Testes da Governança Integrada:

```
python tests/manual/testar_configuracao_governanca.py
python tests/manual/testar_repositorio_local_governanca.py
python tests/manual/testar_contrato_persistencia_governanca.py
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

- `app.py` deve atuar apenas como orquestrador.
- `star_core` não deve ser alterado.
- `star_ingestion` não deve ser alterado.
- `star_intelligence` não deve ser alterado.
- `star_governance` não deve ser alterado nesta sprint.
- `star_persistence` não deve ser alterado nesta sprint.
- Motor STAR permanece protegido.
- Governança não recalcula nada.
- Governança não cria tarefa.
- Governança não cria plano de ação.
- Governança não usa IA.
- Governança não aciona agente.

## 4. Regressão visual manual

A validação visual futura deve confirmar:

- Seção "Governança investigativa" aparece no fluxo do cliente.
- A seção está próxima do Raio-X/Histórico Investigativo.
- A seção informa que governança não é tarefa.
- A seção informa que governança não é plano de ação.
- A seção informa que governança não é agenda.
- Campos disponíveis são somente tipo, status, observação e usuário
  opcional.
- Não há campo de responsável.
- Não há campo de prazo.
- Não há campo de tarefa.
- Não há campo de plano de ação.
- Não há calendário.
- Não há agenda.
- O salvamento exige botão explícito.
- A consulta é read-only.
- Não há gráfico novo.
- Não há ranking.
- Não há prioridade comercial.
- Não há recomendação de ação.

## 5. Regressão de artefatos

- Não deve haver `.db`, `.sqlite` ou `.sqlite3` dentro do repositório.
- Não deve haver JSON funcional dentro do repositório.
- Não deve haver diretório de dados criado dentro do repositório.
- Não deve haver arquivo de agenda.
- Não deve haver arquivo de calendário.
- Não deve haver arquivo de tarefa.
- Não deve haver alteração de schema SQLite do histórico.
- Não deve haver alteração de schema SQLite da governança.

## 6. Regressão conceitual

- Registro de acompanhamento não é tarefa.
- Status de acompanhamento não é execução.
- Loop semanal não é agenda.
- Loop semanal não é calendário.
- Payload persistível não é execução.
- Repositório local não é CRM.
- Configuração local não cria banco.
- Consulta read-only não altera governança.
- Ordenação técnica não é prioridade comercial.
- Aviso não é plano de ação.
- Decisão operacional exige humano.
- Agente futuro não deve decidir sozinho.
- IA futura não deve substituir governança determinística.

**Atualização:** a Sprint 8.1 iniciou a organização da regressão
operacional e visual futura (ver
`docs/MODELO_VALIDACAO_VISUAL_GOVERNANCA.md`).
