# tests/manual

## Finalidade

Esta pasta reúne as planilhas e scripts usados para testar manualmente, dentro
do Streamlit, o fluxo de ingestão do STAR OS (upload, mapeamento protegido,
saneamento e validação) antes de qualquer evolução sobre o MVP Excel-first.
Não é uma suíte de testes automatizados — os testes reais acontecem abrindo o
app no navegador e subindo cada uma dessas planilhas.

## Scripts geradores de planilhas de teste

- `gerar_planilha_suja.py` — gera `planilha_suja_star.xlsx`, uma planilha
  válida com sujeiras controladas (linha vazia, coluna vazia, cabeçalho
  repetido, linhas TOTAL/SUBTOTAL e um cliente real com "Total" no nome).
- `gerar_planilhas_invalidas.py` — gera as planilhas da pasta `invalidas/`.
- `gerar_planilhas_formatos_reais.py` — gera as planilhas da pasta
  `formatos_reais/`.

## Pasta `invalidas/`

Contém planilhas propositalmente inválidas, usadas para confirmar que o STAR
OS bloqueia bases sem estrutura mínima:

- `sem_cliente.xlsx`
- `sem_vendedor.xlsx`
- `sem_meses.xlsx`
- `cliente_vazio.xlsx`
- `base_vazia.xlsx`
- `meses_invalidos.xlsx`

## Pasta `formatos_reais/`

Contém planilhas com variações reais de nomes de colunas e formatos de
valores (como as exportadas por ERP, CRM ou controles internos), usadas para
confirmar que o mapeamento guiado reconhece esses formatos:

- `razao_representante_municipio.xlsx`
- `empresa_consultor_regiao.xlsx`
- `conta_responsavel_localidade.xlsx`
- `meses_numericos.xlsx`
- `valores_monetarios.xlsx`

## Como usar

1. Rode o script correspondente (`python tests/manual/gerar_*.py`) para gerar
   ou regerar as planilhas.
2. Abra o STAR OS no Streamlit.
3. Faça upload de cada planilha e siga o
   [Checklist de Regressão Manual](../../docs/CHECKLIST_REGRESSAO_MANUAL.md)
   para conferir o comportamento esperado.

Essas planilhas existem para dar suporte à regressão manual do MVP
Excel-first do STAR OS — devem ser mantidas e reutilizadas a cada nova sprint
de ingestão, em vez de recriadas do zero.
