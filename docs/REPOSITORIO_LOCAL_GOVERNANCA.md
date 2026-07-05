# REPOSITÓRIO LOCAL DE GOVERNANÇA — STAR OS

## 1. Finalidade

O Repositório Local de Governança permite persistir localmente payloads
de governança validados pelo contrato da Sprint 7.2.

- Repositório não é Streamlit.
- Repositório não é dashboard.
- Repositório não é CRM.
- Repositório não é agenda.
- Repositório não é tarefa.
- Repositório não é plano de ação.
- Repositório não cria responsável.
- Repositório não envia mensagem.
- Repositório não aciona agente.
- Repositório não usa IA.
- Repositório não altera Motor STAR.

## 2. Problema estrutural resolvido

A Governança Inicial (Sprint 6) e o Contrato de Persistência (Sprint 7.2)
já existiam, mas ainda faltava mecanismo local controlado para armazenar
payloads validados. O repositório resolve:

- continuidade da governança;
- armazenamento local dos payloads;
- recuperação futura;
- listagem por tipo, cliente e sessão;
- contagem por tipo;
- validação de integridade;
- preparação para futura exposição no Streamlit.

## 3. Relação com o contrato da Sprint 7.2

- O repositório não cria contrato novo.
- O repositório usa `contrato_governanca.py`.
- Payload inválido não é salvo.
- Payload duplicado é bloqueado por padrão.
- Sobrescrita só ocorre quando explicitamente solicitada
  (`sobrescrever=True`).
- O payload salvo não é alterado para simular execução — os metadados de
  persistência do payload permanecem exatamente como validados pelo
  contrato.

## 4. Schema local de governança

**`governanca_schema_info`:**
- `chave`
- `valor`
- `criado_em`

**`governanca_payloads`:**
- `id`
- `tipo_payload_governanca`
- `payload_id`
- `cliente_id`
- `sessao_id`
- `nome_cliente`
- `origem`
- `criado_em_payload`
- `criado_em_repositorio`
- `payload_json`

O schema é próprio da governança e não altera o schema do Histórico
Investigativo (Sprint 5.3).

## 5. Operações disponíveis

- Inicializar schema.
- Verificar schema.
- Preparar linha de payload.
- Salvar payload.
- Carregar payload.
- Listar payloads.
- Salvar lote.
- Contar registros.
- Validar integridade.
- Formatar resumo.
- Formatar validação.

## 6. O que o repositório não faz

- Não altera `app.py`.
- Não integra no Streamlit.
- Não cria tela.
- Não cria botão.
- Não cria download.
- Não cria tarefa.
- Não cria plano de ação.
- Não cria agenda.
- Não cria calendário.
- Não cria responsável automático.
- Não envia mensagem.
- Não chama API externa.
- Não usa IA.
- Não cria agente.
- Não altera Motor STAR.
- Não recalcula Matriz STAR.
- Não altera Excel.
- Não altera PDF.

## 7. Relação com Sprint 7.4

A Sprint 7.4 poderá usar o Repositório Local de Governança para expor
governança no Streamlit de forma discreta e controlada.

- A Sprint 7.4 não deve criar repositório paralelo.
- A Sprint 7.4 deve usar `contrato_governanca.py` e
  `repositorio_governanca.py`.
- A Sprint 7.4 deve manter `app.py` como orquestrador.
- A Sprint 7.4 não deve transformar governança em dashboard paralelo.
- A Sprint 7.4 não deve transformar loop em tarefa.

## 8. Limites atuais

- Não há integração visual.
- Não há tela.
- Não há edição pela interface.
- Não há exclusão lógica.
- Não há multiusuário.
- Não há permissões.
- Não há auditoria completa.
- Não há CRM.
- Não há ERP.
- Não há WhatsApp.
- Não há MCP.
- Não há agente.
- Não há IA.

## 9. Continuidade — Sprint 7.4

A Sprint 7.4 passou a usar este repositório na interface Streamlit de
forma controlada (ver `docs/GOVERNANCA_STREAMLIT.md`).
