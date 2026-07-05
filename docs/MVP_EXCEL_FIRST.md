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

## 4.1 Rastreabilidade da ingestão

Desde a Sprint 2.1, cada upload gera um relatório estruturado de ingestão
(`star_ingestion/relatorio.py`), exibido de forma discreta no Streamlit em
"Relatório de ingestão". Ele registra estado inicial/final da base, ações de
saneamento, mapeamento aplicado e erros/avisos — sem alterar nenhuma decisão
do sistema, apenas documentando o que já acontece.

Desde a Sprint 2.2, um diagnóstico determinístico de mapeamento
(`star_ingestion/diagnostico_mapeamento.py`) explica, antes do bloqueio, qual
campo (cliente, vendedor, cidade ou meses) não foi reconhecido e sugere como
corrigir a planilha.

Desde a Sprint 2.3, uma normalização avançada de meses
(`star_ingestion/normalizacao_meses.py`) reconhece formatos variados de
coluna mensal (texto, numérico, com prefixo, fora de ordem), ordena os meses
cronologicamente e avisa sobre períodos duplicados, sem alterar valores ou
nomes de colunas.

Desde a Sprint 2.4, uma normalização avançada de valores monetários
(`star_ingestion/normalizacao_valores.py`) reconhece formatos brasileiro,
americano e mistos (moeda, milhar, decimal, vazio, hífen), convertendo
valores inválidos ou ausentes para 0.0 e registrando avisos — sem criar
regra de negócio nova nem alterar o cálculo do Motor STAR.

Desde a Sprint 2.5, uma camada de qualidade de linhas
(`star_ingestion/qualidade_linhas.py`) remove apenas resíduos evidentes de
identidade de cliente (vazio, "-", TOTAL, SUBTOTAL, cabeçalho repetido, etc.)
e preserva sempre clientes reais zerados ou com compra parcial — zero em
mês é dado comercial válido, nunca motivo de remoção.

Com a Sprint 2.6, a robustez avançada de ingestão (saneamento, validação,
relatório, diagnóstico de mapeamento, normalização de meses, normalização de
valores e qualidade de linhas) foi formalmente documentada em
`docs/ROBUSTEZ_INGESTAO.md`, `docs/INVENTARIO_TESTES_INGESTAO.md` e
`docs/DECISOES_ARQUITETURAIS_INGESTAO.md`, fechando a Sprint 2 antes de
avançar para a Inteligência de Carteira.

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
