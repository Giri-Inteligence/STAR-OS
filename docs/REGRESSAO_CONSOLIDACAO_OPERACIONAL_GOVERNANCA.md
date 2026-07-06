# REGRESSÃO DA CONSOLIDAÇÃO OPERACIONAL DA GOVERNANÇA — STAR OS

## 1. Finalidade

Este documento consolida os testes e critérios de regressão da Sprint 8
(Consolidação Operacional da Governança).

## 2. Regressão técnica obrigatória

Compilação:

```
python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py star_governance/*.py tests/manual/*.py
```

Testes principais da Sprint 8:

```
python tests/manual/testar_leitura_operacional_governanca.py
python tests/manual/testar_validacao_estatica_governanca_streamlit.py
python tests/manual/testar_contrato_persistencia_governanca.py
python tests/manual/testar_repositorio_local_governanca.py
python tests/manual/testar_configuracao_governanca.py
python tests/manual/testar_loop_semanal_governanca.py
python tests/manual/testar_status_acompanhamento.py
python tests/manual/testar_acompanhamento_operacional.py
```

## 3. Regressão ampliada

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

## 4. Regressão arquitetural

- `app.py` deve atuar apenas como orquestrador.
- `star_core` não deve ser alterado.
- `star_ingestion` não deve ser alterado.
- `star_intelligence` não deve ser alterado.
- `star_persistence` não deve ser alterado nesta sprint.
- `star_governance` não deve ser alterado nesta sprint.
- Motor STAR permanece protegido.
- Governança não recalcula nada.
- Leitura operacional não cria tarefa.
- Leitura operacional não cria plano de ação.
- Leitura operacional não cria agenda.
- Leitura operacional não usa IA.
- Leitura operacional não aciona agente.

## 5. Regressão visual pendente

- Streamlit não estava instalado no ambiente da Sprint 8.3.
- Validação visual real permanece pendente de execução local.
- Roteiro oficial está em
  `docs/ROTEIRO_VALIDACAO_VISUAL_GOVERNANCA_STREAMLIT.md`.
- Antes de IA/agentes, a validação visual real deve ser executada ou
  formalmente registrada como pendente aceita.

**Atualização — Sprint 9.2:** a validação visual real foi executada em
navegador contra um servidor Streamlit local. Um achado de bug
funcional foi confirmado (identidade de sessão da investigação não
estável entre reruns, afetando a consulta de governança salva) — ver
`docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`,
`docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md` e
`docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`. IA/agentes seguem
bloqueados até correção e reconfirmação.

**Atualização — Sprint 9.3:** a regressão passa a incluir
`tests/manual/testar_identidade_sessao_governanca_streamlit.py`,
protegendo a estabilização de `sessao_id` que corrigiu o
ACHADO-9-2-001 (ver `docs/CORRECAO_IDENTIDADE_SESSAO_GOVERNANCA.md`).

## 6. Regressão de artefatos

- Não deve haver `.db`, `.sqlite` ou `.sqlite3` dentro do repositório.
- Não deve haver JSON funcional dentro do repositório.
- Não deve haver diretório de dados criado dentro do repositório.
- Não deve haver arquivo de agenda.
- Não deve haver arquivo de calendário.
- Não deve haver arquivo de tarefa.
- Não deve haver alteração de schema SQLite do histórico.
- Não deve haver alteração de schema SQLite da governança.

## 7. Regressão conceitual

- `CICLO_LOOP` com identidade não é tarefa.
- Leitura operacional não é recomendação.
- Síntese operacional não é plano de ação.
- Consulta read-only não é dashboard.
- Resumo quantitativo não é ranking.
- Status não é execução.
- Classificação de loop não é prioridade comercial.
- Decisão operacional exige humano.
- IA futura não deve substituir governança determinística.
- Agente futuro não deve decidir sozinho.

**Atualização:** a Sprint 9.1 iniciou a organização da regressão
operacional local futura (ver
`docs/PROTOCOLO_VALIDACAO_LOCAL_STREAMLIT.md`).
