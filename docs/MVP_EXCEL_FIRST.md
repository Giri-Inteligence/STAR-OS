# MVP Excel-first — STAR OS

## 1. Nome do marco

MVP Excel-first — STAR OS

## 2. Escopo validado

- Upload de Excel.
- Aba única Consolidado.
- Abas por vendedor.
- Mapeamento protegido.
- Bloqueio de duplicidade.
- Saneamento leve.
- Bloqueio de planilhas inválidas.
- Reconhecimento de formatos reais simples.
- Matriz STAR.
- Performance por vendedor.
- Download Excel.
- Download PDF.

## 3. Critério de sucesso consolidado

- Planilha válida processa.
- Planilha suja recuperável é saneada e processa.
- Planilha inválida é bloqueada.
- Planilha com formatos reais simples é reconhecida e processa.
- Planilhas reais testadas processam conforme esperado.

## 4. Arquivos de teste existentes

- `tests/manual/planilha_suja_star.xlsx`
- `tests/manual/invalidas/sem_cliente.xlsx`
- `tests/manual/invalidas/sem_vendedor.xlsx`
- `tests/manual/invalidas/sem_meses.xlsx`
- `tests/manual/invalidas/cliente_vazio.xlsx`
- `tests/manual/invalidas/base_vazia.xlsx`
- `tests/manual/invalidas/meses_invalidos.xlsx`
- `tests/manual/formatos_reais/razao_representante_municipio.xlsx`
- `tests/manual/formatos_reais/empresa_consultor_regiao.xlsx`
- `tests/manual/formatos_reais/conta_responsavel_localidade.xlsx`
- `tests/manual/formatos_reais/meses_numericos.xlsx`
- `tests/manual/formatos_reais/valores_monetarios.xlsx`

## 5. Decisões de arquitetura preservadas

- Excel-first.
- Ingestão antes de inteligência.
- Normalização antes de IA.
- Motor STAR protegido.
- Regras determinísticas preservadas.
- IA e integrações como evolução futura, não pré-requisito.

## 6. Fora de escopo do MVP

- Estética.
- Layout avançado.
- IA.
- Agentes.
- Integrações.
- CRM.
- ERP.
- WhatsApp.
- MCP.
- Aprendizado operacional automático.
- Sistema de login.
- Banco de dados.
