# Decisões Arquiteturais da Inteligência de Carteira — STAR OS

## 1. Inteligência de Carteira integrada, não paralela

A Inteligência de Carteira deve evoluir como camada sobre a Matriz STAR,
não como aplicação separada.

## 2. Motor STAR protegido

A Inteligência de Carteira não pode alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 3. Separação de responsabilidades

- `star_core` calcula regras STAR.
- `star_ingestion` prepara e valida a entrada.
- `star_intelligence` interpreta a Matriz STAR.
- `app.py` orquestra fluxo e interface.
- `tests/manual` valida comportamento operacional.

## 4. Determinístico antes de IA

- Sprint 3 não usa IA.
- Sprint 3 não consome token.
- Sprint 3 não chama API externa.
- Regras determinísticas resolvem o que é objetivo.
- IA poderá entrar no futuro como camada assistiva, não como substituta da
  lógica STAR.

## 5. Hipótese não é conclusão

- Hipóteses devem ser validadas por evidência.
- Perguntas vêm antes de recomendações.
- Recomendações não devem encerrar diagnóstico.
- Recomendações não devem gerar execução automática nesta fase.

## 6. Recomendações não são execução

- Recomendação por papel orienta interpretação.
- Não cria tarefa.
- Não cria prazo.
- Não cria responsável automático.
- Não envia mensagem.
- Não aciona agente.
- Não registra ação ainda.

## 7. Evolução futura

- Sprint 4 — Motor de Investigação.
- Registro de respostas às perguntas de validação.
- Registro de ações.
- Histórico por cliente.
- Loop de governança.
- Aprendizado operacional.
- IA assistiva futura.
- Agentes futuros.
- Integrações futuras com CRM, ERP, WhatsApp e MCP.
