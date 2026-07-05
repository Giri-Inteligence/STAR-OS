# MODELO DE VALIDAÇÃO VISUAL DA GOVERNANÇA — STAR OS

## 1. Finalidade

O Modelo de Validação Visual define como validar a seção de Governança
Investigativa no Streamlit sem transformar a experiência em dashboard,
CRM, agenda ou gestor de tarefas.

## 2. O que deve ser validado visualmente

- Seção "Governança investigativa" aparece no fluxo do cliente.
- Seção está próxima do Raio-X/Histórico Investigativo.
- Aviso metodológico é claro.
- Configuração local é compreensível.
- Campos permitidos são tipo, status, observação e usuário opcional.
- Não há campo de responsável.
- Não há campo de prazo.
- Não há campo de tarefa.
- Não há campo de plano de ação.
- Não há agenda.
- Não há calendário.
- Botão de salvamento é explícito.
- Consulta é read-only.
- Payloads salvos aparecem de forma técnica simples.
- Resumo do repositório é compreensível.
- PDF e Excel não mudam.
- Motor STAR não muda.

## 3. O que não deve ser validado como requisito

Não faz parte da validação visual:

- criação de tarefas;
- edição de governança salva;
- exclusão lógica;
- agenda;
- calendário;
- responsável automático;
- prazo;
- envio de mensagem;
- agente;
- IA;
- automação;
- integração com CRM;
- integração com ERP.

## 4. Estados visuais mínimos

Estados que a Sprint 8.3 deve validar futuramente:

### Estado A — sem investigação atual
- Deve informar que a governança depende de investigação atual.
- Não deve criar payload falso.
- Não deve salvar nada.

### Estado B — investigação atual disponível
- Deve permitir preencher registro de acompanhamento.
- Deve permitir salvar governança por botão explícito.
- Deve exibir validação dos payloads.
- Deve exibir resultado do salvamento.

### Estado C — governança salva existente
- Deve permitir consulta read-only.
- Deve listar payloads por cliente/sessão quando possível.
- Deve exibir resumo técnico do repositório.

### Estado D — banco inexistente
- Consulta deve informar ausência de dados.
- Não deve criar banco apenas por consulta.
- Salvamento explícito pode criar banco fora do repositório.

### Estado E — limitação do CICLO_LOOP
- Antes da correção, deve ser documentada como limitação.
- Depois da correção, deve ser validada para garantir que o
  `CICLO_LOOP` aparece no filtro por cliente/sessão.

## 5. Critérios de aceitação visual

- Usuário entende que governança é acompanhamento investigativo.
- Usuário não interpreta como tarefa.
- Usuário não interpreta como agenda.
- Usuário não interpreta como CRM.
- Usuário entende que salvamento é explícito.
- Usuário entende que consulta é read-only.
- Usuário entende que o sistema não executa ação.
- Usuário entende que decisões continuam humanas.

## 6. Riscos de UX

- Usuário interpretar status como tarefa.
- Usuário interpretar loop como prioridade comercial.
- Usuário interpretar observação como plano de ação.
- Usuário esperar responsável/prazo.
- Usuário esperar automação.
- Usuário confundir governança com CRM.
- Usuário confundir consulta com dashboard.
- Usuário não perceber que o salvamento é local.

## 7. Instrumento de validação manual

Checklist visual futura, proposta sem implementação:

- Abrir Streamlit.
- Subir base válida.
- Selecionar cliente.
- Abrir Raio-X.
- Gerar investigação.
- Localizar Governança Investigativa.
- Verificar campos.
- Salvar governança.
- Consultar governança.
- Verificar ausência de tarefa/agenda/responsável/prazo.
- Verificar ausência de alteração em PDF/Excel.
- Verificar ausência de alteração no Motor STAR.

## 8. Limites da Sprint 8.1

- Sprint 8.1 não executa validação visual real.
- Sprint 8.1 não altera interface.
- Sprint 8.1 não corrige `CICLO_LOOP`.
- Sprint 8.1 apenas cria o modelo de validação futura.
