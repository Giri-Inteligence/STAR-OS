# Decisões Arquiteturais do Motor de Investigação — STAR OS

## 1. Motor de Investigação integrado, não paralelo

O Motor de Investigação deve evoluir como camada sobre a Inteligência de
Carteira, não como aplicação separada.

## 2. Motor STAR protegido

O Motor de Investigação não pode alterar:

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
- `star_intelligence` interpreta, investiga e consolida.
- `app.py` orquestra fluxo e interface.
- `tests/manual` valida comportamento operacional.

## 4. Determinístico antes de IA

- Sprint 4 não usa IA.
- Sprint 4 não consome token.
- Sprint 4 não chama API externa.
- Regras determinísticas resolvem o que é objetivo.
- IA poderá entrar no futuro como camada assistiva, não como substituta da
  lógica STAR.

## 5. Investigação não é execução

- Investigação registra validação.
- Investigação organiza evidência.
- Investigação não cria ação.
- Investigação não cria tarefa.
- Investigação não cria prazo.
- Investigação não envia mensagem.
- Investigação não aciona agente.

## 6. Conclusão investigativa não é causa raiz automática

- Hipótese confirmada não é diagnóstico final.
- Hipótese descartada não encerra todo o diagnóstico.
- Hipótese inconclusiva exige mais evidência.
- Pendência deve permanecer visível.
- A causa raiz continua dependendo de julgamento humano e evidência
  suficiente.

## 7. Persistência futura deve ser planejada

- A Sprint 4 usa `session_state` temporário.
- Persistência exige sprint própria.
- Histórico por cliente exige modelo de dados.
- Governança operacional exige rastreabilidade.
- A persistência futura deve preservar separação entre hipótese, evidência,
  recomendação, ação e acompanhamento.

## 8. Evolução futura

- Sprint 5 — Persistência e Histórico Investigativo.
- Registro persistente de investigação por cliente.
- Versionamento de pacotes investigativos.
- Histórico de conclusões investigativas.
- Registro de ações futuras.
- Loop de governança.
- IA assistiva futura.
- Agentes futuros.
- Integrações futuras com CRM, ERP, WhatsApp e MCP.
