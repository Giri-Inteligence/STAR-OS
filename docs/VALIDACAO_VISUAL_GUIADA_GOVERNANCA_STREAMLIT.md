# VALIDAÇÃO VISUAL GUIADA DA GOVERNANÇA NO STREAMLIT — STAR OS

## 1. Finalidade

A Sprint 8.3 valida a experiência da seção "Governança investigativa" no
Streamlit sem criar nova funcionalidade.

- Validação visual não é dashboard.
- Validação visual não é CRM.
- Validação visual não é tarefa.
- Validação visual não é plano de ação.
- Validação visual não é agenda.
- Validação visual não é automação.
- Validação visual não é IA.
- Validação visual não é agente.
- Validação visual não altera o Motor STAR.
- Validação visual não altera o PDF.
- Validação visual não altera o Excel.

## 2. Escopo da validação

A Sprint 8.3 valida:

- presença da seção Governança investigativa;
- localização no fluxo do cliente;
- aviso metodológico;
- campos permitidos;
- ausência de responsável;
- ausência de prazo;
- ausência de tarefa;
- ausência de plano de ação;
- ausência de agenda;
- ausência de calendário;
- botão explícito de salvamento;
- consulta read-only;
- uso do contrato de governança;
- uso do repositório de governança;
- comportamento esperado após correção do `CICLO_LOOP` (Sprint 8.2);
- ausência de gráficos, ranking, dashboard paralelo e CRM paralelo.

## 3. Estados visuais esperados

### Estado A — sem investigação atual
- A interface deve informar dependência de investigação atual.
- Não deve criar payload falso.
- Não deve salvar nada.

### Estado B — investigação atual disponível
- A interface deve permitir registrar acompanhamento.
- Deve gerar payloads.
- Deve validar payloads.
- Deve salvar apenas por botão explícito.

### Estado C — governança já salva
- A consulta deve ser read-only.
- Deve listar payloads.
- Deve exibir resumo técnico simples.

### Estado D — banco inexistente
- A consulta não deve criar banco automaticamente.
- O salvamento explícito pode criar banco local fora do repositório.

### Estado E — CICLO_LOOP corrigido
- O `CICLO_LOOP` deve aparecer na consulta filtrada por cliente/sessão
  quando salvo com o contrato corrigido na Sprint 8.2.

## 4. Critérios de aceitação

- Usuário entende que governança é continuidade investigativa.
- Usuário não interpreta como tarefa.
- Usuário não interpreta como agenda.
- Usuário não interpreta como CRM.
- Usuário não interpreta como dashboard.
- Salvamento é percebido como explícito.
- Consulta é percebida como read-only.
- Decisão continua humana.
- Sistema não executa ação externa.
- Interface não altera PDF/Excel.
- Interface não altera o Motor STAR.

## 5. Riscos observados

- Status ser interpretado como tarefa.
- Loop ser interpretado como prioridade comercial.
- Observação ser interpretada como plano de ação.
- Consulta ser interpretada como dashboard.
- Usuário esperar responsável ou prazo.
- Usuário esperar automação.
- Usuário não perceber que o banco é local.

## 6. Limites da Sprint 8.3

- Não corrige UI.
- Não altera `app.py`.
- Não cria campo novo.
- Não cria botão novo.
- Não cria gráfico.
- Não altera PDF.
- Não altera Excel.
- Não cria IA.
- Não cria agente.
- Não cria integração externa.

## 7. Continuidade — Sprint 8.4

A validação visual futura deve confirmar a leitura operacional
(Sprint 8.4) sem tarefa, sem agenda e sem recomendação de ação (ver
`docs/LEITURA_OPERACIONAL_GOVERNANCA_SEM_TAREFAS.md`).
