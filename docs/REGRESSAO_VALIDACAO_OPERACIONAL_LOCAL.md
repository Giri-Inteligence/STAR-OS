# REGRESSÃO DA VALIDAÇÃO OPERACIONAL LOCAL — STAR OS

## 1. Finalidade

Este documento consolida a regressão obrigatória após a Sprint 9
(Validação Operacional Local e Estabilização da Experiência).

## 2. Regressão técnica obrigatória

Compilação:

```
python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py star_governance/*.py tests/manual/*.py
```

Testes principais da Sprint 9:

```
python tests/manual/testar_estabilizacao_experiencia_governanca_streamlit.py
python tests/manual/testar_identidade_sessao_governanca_streamlit.py
python tests/manual/testar_validacao_estatica_governanca_streamlit.py
python tests/manual/testar_leitura_operacional_governanca.py
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

## 4. Regressão visual/manual recomendada

Roteiro resumido para qualquer revalidação humana futura:

- abrir Streamlit;
- subir planilha válida;
- abrir Raio-X;
- salvar governança;
- consultar governança;
- confirmar 5 payloads;
- confirmar `CICLO_LOOP`;
- confirmar leitura operacional;
- confirmar observação;
- confirmar legenda pós-salvamento;
- confirmar ausência de tarefa/agenda/plano/IA/agente.

## 5. Regressão arquitetural

- `app.py` deve seguir como orquestrador.
- `star_core` não deve ser alterado.
- `star_ingestion` não deve ser alterado.
- `star_intelligence` não deve ser alterado.
- `star_persistence` não deve ser alterado sem sprint própria.
- `star_governance` não deve ser alterado sem sprint própria.
- Motor STAR permanece protegido.
- Governança não recalcula nada.
- Leitura operacional não recomenda ação.
- Governança não cria tarefa.
- Governança não cria agenda.
- Governança não cria plano de ação.
- Governança não usa IA.
- Governança não aciona agente.

## 6. Regressão de artefatos

- Não deve haver `.db`, `.sqlite` ou `.sqlite3` dentro do repositório.
- Não deve haver JSON funcional dentro do repositório.
- Não deve haver diretório de dados criado dentro do repositório.
- Não deve haver arquivo de agenda.
- Não deve haver arquivo de calendário.
- Não deve haver arquivo de tarefa.
- Não deve haver alteração de schema SQLite do histórico.
- Não deve haver alteração de schema SQLite da governança.
- `.claude/` não deve ser commitado.

## 7. Regressão conceitual

- Sessão estável não é persistência permanente.
- Consulta read-only não é dashboard.
- Resumo quantitativo não é ranking.
- Leitura operacional não é recomendação.
- Observação não é plano de ação.
- Status não é tarefa.
- `CICLO_LOOP` não é execução.
- Decisão operacional exige humano.
- IA futura não deve substituir regras determinísticas.
- Agente futuro não deve decidir sozinho.

**Atualização:** esta regressão consolida e substitui, para efeitos de
fechamento da Sprint 9, a regressão registrada em
`docs/REGRESSAO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md` (Sprint 8),
que permanece válida como histórico.
