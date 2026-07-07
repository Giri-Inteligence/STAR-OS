# Decisões Arquiteturais de Ingestão — STAR OS

## 1. Excel-first

O STAR OS continua orientado a upload de Excel como entrada inicial, antes
de qualquer integração com sistemas externos.

## 2. Motor STAR protegido

A ingestão não deve alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 3. Separação de responsabilidades

- `star_ingestion` trata entrada, saneamento, normalização e validação.
- `star_core` trata cálculo e regras STAR.
- `app.py` orquestra o fluxo e a interface.
- `tests/manual` valida o comportamento operacional.

## 4. Regra sobre zero

- Zero em coluna mensal é dado comercial válido.
- Cliente real zerado deve permanecer.
- Cliente com compra parcial deve permanecer.
- Linha residual deve ser removida pela identidade inválida do cliente,
  nunca por ausência de venda.

## 5. Determinístico antes de IA

- Regras determinísticas devem resolver o que for objetivo.
- IA não deve substituir regra determinística sem justificativa.
- IA poderá ser usada no futuro para campos ambíguos, explicações e
  investigação, não para alterar cálculo STAR.

## 6. Evolução futura

- Perfis de mapeamento por cliente.
- Confirmação humana de mapeamento.
- Persistência de padrões.
- Relatório de ingestão exportável.
- Histórico de ingestões.
- Integrações futuras com ERP/CRM.
- Inteligência de Carteira Integrada.
