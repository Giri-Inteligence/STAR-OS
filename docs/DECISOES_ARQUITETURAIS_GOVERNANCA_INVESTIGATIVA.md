# DECISÕES ARQUITETURAIS DA GOVERNANÇA INVESTIGATIVA — STAR OS

## 1. Governança como camada posterior à persistência

A Governança Investigativa deve consumir o Histórico Investigativo, não
substituir o histórico. O histórico continua sendo a fonte de verdade
sobre o que foi salvo; a governança apenas organiza acompanhamento sobre
esses registros já existentes.

## 2. Motor STAR protegido

A Governança Investigativa não pode alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 3. Separação de responsabilidades

- `star_core` calcula regras STAR.
- `star_ingestion` prepara e valida entrada.
- `star_intelligence` interpreta e investiga.
- `star_persistence` persiste histórico.
- futura camada de governança deverá acompanhar evolução.
- `app.py` apenas orquestra interface.

## 4. Acompanhamento não é execução

- Acompanhamento registra evolução.
- Acompanhamento registra pendência.
- Acompanhamento registra decisão.
- Acompanhamento não executa tarefa.
- Acompanhamento não envia mensagem.
- Acompanhamento não cria automação.
- Acompanhamento não aciona agente.

## 5. Decisão operacional exige humano

- Sistema pode organizar contexto.
- Sistema pode expor pendência.
- Sistema pode sugerir leitura.
- Sistema não deve decidir sozinho.
- Sistema não deve concluir causa raiz automaticamente.
- Sistema não deve converter recomendação em ação sem validação humana.

## 6. Determinístico antes de IA

- Sprint 6.1 não usa IA.
- Estados e regras de acompanhamento devem nascer determinísticos.
- IA futura poderá auxiliar na leitura, mas não substituir governança.
- Agentes futuros devem atuar depois da governança, não antes.

## 7. Risco de CRM paralelo

A Governança Investigativa deve evitar virar CRM paralelo.

- CRM registra relacionamento, atividades e pipeline.
- STAR OS registra diagnóstico, hipótese, evidência, conclusão e
  governança investigativa.

## 8. Risco de dashboard paralelo

A Governança Investigativa deve evitar virar dashboard paralelo.

- Dashboard exibe indicadores.
- STAR OS organiza decisão, investigação, acompanhamento e coerência
  metodológica.

## 9. Evolução futura

- Sprint 6.2 — Registro de Acompanhamento Operacional.
- Sprint 6.3 — Status de Acompanhamento da Investigação.
- Sprint 6.4 — Loop Semanal de Governança.
- Sprint 6.5 — Fechamento da Governança Inicial.

## 10. Continuidade — Sprint 6.2

A Sprint 6.2 preservou a separação entre acompanhamento e execução: o
Registro de Acompanhamento Operacional registra evolução, pendência e
decisão humana, mas não executa tarefa, não envia mensagem e não aciona
agente (ver `docs/REGISTRO_ACOMPANHAMENTO_OPERACIONAL.md`).

## 11. Continuidade — Sprint 6.3

A Sprint 6.3 preservou a decisão de ser determinística antes de IA: as
regras de status e transição nascem como código auditável, sem
inferência probabilística (ver `docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`).

## 12. Continuidade — Sprint 6.4

A Sprint 6.4 preservou determinismo antes de IA e acompanhamento
separado de execução: o Loop Semanal de Governança apenas classifica e
ordena leitura, sem decidir ou executar nada (ver
`docs/LOOP_SEMANAL_GOVERNANCA.md`).
