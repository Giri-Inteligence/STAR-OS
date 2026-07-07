# Inventário de Testes de Ingestão — STAR OS

## 1. Scripts manuais

Geradores de planilhas de teste:

- `tests/manual/gerar_planilha_suja.py`
- `tests/manual/gerar_planilhas_invalidas.py`
- `tests/manual/gerar_planilhas_formatos_reais.py`
- `tests/manual/gerar_planilhas_meses_avancados.py`
- `tests/manual/gerar_planilhas_valores_avancados.py`
- `tests/manual/gerar_planilhas_qualidade_linhas.py`

Testes de módulo (assert-based, executáveis por `python`, sem pytest):

- `tests/manual/testar_relatorio_ingestao.py`
- `tests/manual/testar_diagnostico_mapeamento.py`
- `tests/manual/testar_normalizacao_meses.py`
- `tests/manual/testar_normalizacao_valores.py`
- `tests/manual/testar_qualidade_linhas.py`

## 2. Pastas de planilhas de teste

- `tests/manual/invalidas/`
- `tests/manual/formatos_reais/`
- `tests/manual/meses_avancados/`
- `tests/manual/valores_avancados/`
- `tests/manual/qualidade_linhas/`

Além de `tests/manual/planilha_suja_star.xlsx` (arquivo único, gerado por
`gerar_planilha_suja.py`).

## 3. Tipos de validação cobertos

### Planilha suja controlada
`planilha_suja_star.xlsx` — linha vazia, coluna vazia, cabeçalho repetido,
linhas TOTAL/SUBTOTAL e um cliente real com "Total" no nome que deve ser
preservado.

### Planilhas inválidas
Pasta `invalidas/` — bases sem cliente, sem vendedor, sem meses, com cliente
vazio, totalmente vazias ou com meses só com valores inválidos. Todas devem
ser bloqueadas por `star_ingestion/validacao.py`.

### Formatos reais de colunas
Pasta `formatos_reais/` — variações de nome de coluna (RAZÃO SOCIAL,
EMPRESA, CONTA, MUNICÍPIO, REGIÃO, LOCALIDADE, REPRESENTANTE, CONSULTOR,
RESPONSÁVEL) e meses em formato numérico.

### Meses avançados
Pasta `meses_avancados/` — meses por extenso, numéricos variados
(`1/25`, `2025-04`), com prefixo (`VENDAS JAN/25`), fora de ordem e
parcialmente inválidos (`13/25`, `00/25`, `TOTAL` como nome de coluna).

### Valores monetários avançados
Pasta `valores_avancados/` — formato brasileiro (`R$ 10.000,00`), americano
(`10,000.50`), misto, vazios/hífen e parcialmente inválidos (`abc`, `erro`).

### Qualidade de linhas
Pasta `qualidade_linhas/` — cobre os cenários abaixo.

### Clientes zerados
`clientes_zerados_validos.xlsx` e `cliente_compra_parcial.xlsx` — clientes
reais com todos os meses zerados, apenas um mês de venda, ou quinze meses
zerados e um preenchido. Todos devem permanecer na base.

### Linhas residuais
`linhas_residuais_obvias.xlsx` e `misto_zero_residuo.xlsx` — linhas com
identidade de cliente claramente inválida (TOTAL, SUBTOTAL, vazio, "-",
cabeçalho repetido) devem ser removidas, preservando clientes reais mesmo
quando o nome contém a palavra "Total" (ex.: `Total Distribuidora Ltda`).

### Regressão de módulos
Os 5 scripts `testar_*.py` cobrem, com `assert`, o comportamento de cada
módulo isoladamente (relatório, diagnóstico, normalização de meses,
normalização de valores, qualidade de linhas), independentemente do
Streamlit.

## 4. Como usar

- Os scripts Python (`testar_*.py`) validam os módulos isoladamente e
  imprimem um marcador de sucesso ao final (ex.: `NORMALIZACAO_MESES_OK`).
- Os scripts `gerar_planilhas_*.py` recriam as planilhas de teste sempre que
  necessário — elas também ficam versionadas no repositório.
- O Streamlit valida o comportamento real da aplicação (upload, mapeamento,
  relatório de ingestão, Matriz STAR, downloads) — os testes Python não
  substituem essa validação manual na interface.
- A regressão (rodar os `testar_*.py` e conferir o
  `docs/CHECKLIST_REGRESSAO_MANUAL.md` no Streamlit) deve ser feita antes de
  qualquer sprint futura que toque em ingestão ou no Motor STAR.
- O GitHub Desktop deve ser usado para dar push somente depois que o commit
  local tiver sido validado (compilação + testes + regressão manual no
  Streamlit).
