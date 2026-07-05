# MAPA DE COMPONENTES — INTELIGÊNCIA DE CARTEIRA

## 1. Componentes existentes a reutilizar

- **`app.py`** — orquestra o fluxo de upload, mapeamento e geração da Matriz
  STAR. A Inteligência de Carteira deve consumir o `df_raw` já calculado por
  ele, sem duplicar essa lógica.
- **`star_core/calculos.py`** — calcula `STATUS`, `META`, `ACAO` e erosão.
  Fonte de verdade para status e ação; a Inteligência de Carteira lê esses
  campos, não os recalcula.
- **`star_core/curva.py`** — calcula `CURVA` (ABC). Fonte de verdade para
  classificação de curva; usada como entrada de priorização.
- **`star_core/recencia.py`** — calcula meses sem compra. Fonte de verdade
  para recência; usada para hipóteses de reativação.
- **`star_ingestion/*`** — garante que a base chegue saneada, mapeada,
  normalizada e validada antes da Matriz STAR. A Inteligência de Carteira
  depende dessa robustez para não interpretar sujeira como sinal comercial.
- **Documentos da robustez de ingestão** (`docs/ROBUSTEZ_INGESTAO.md`,
  `docs/INVENTARIO_TESTES_INGESTAO.md`,
  `docs/DECISOES_ARQUITETURAIS_INGESTAO.md`) — registram o que já foi
  validado e quais limites existem, evitando retrabalho.
- **Testes manuais existentes** (`tests/manual/testar_*.py`) — servem de
  modelo para os futuros testes da Inteligência de Carteira (assert-based,
  executáveis por `python`, sem pytest).

## 2. Dados necessários

Campos mínimos esperados da base após a Matriz STAR ser gerada em `app.py`:

- Cliente — coluna dinâmica, escolhida no mapeamento (`clie_col`); não tem
  nome fixo.
- Vendedor — coluna dinâmica, escolhida no mapeamento (`vend_col`); não tem
  nome fixo.
- Cidade, se disponível — coluna dinâmica, escolhida no mapeamento
  (`cida_col`); pode ser `None`.
- Meses de venda — colunas dinâmicas (`meses_col`), nomes variam por
  planilha.
- `TOTAL LP` — soma de todos os meses selecionados.
- `MEDIA LP` — média de todos os meses selecionados.
- `MEDIA CP` — média dos últimos 3 meses selecionados.
- **Total CP — não existe hoje como coluna** (a confirmar no código antes da
  implementação, caso a Sprint 3.2 precise dele; hoje só `MEDIA CP` é
  calculada).
- `CURVA` — classificação ABC.
- `STATUS` — status STAR (ex.: crescimento, queda, inativo).
- `MESES_SEM_COMPRA` — recência.
- `EROSAO STAR` — erosão calculada.

Os nomes acima foram confirmados lendo `app.py` (bloco de cálculo da Matriz
STAR); os nomes de cliente/vendedor/cidade/meses são sempre dinâmicos e
dependem do mapeamento feito pelo usuário em cada upload.

## 3. Possíveis componentes futuros

Nenhum destes deve ser criado nesta sprint — são apenas hipóteses de
nomeação para as sprints seguintes.

### `star_intelligence/priorizacao.py`
- **Responsabilidade futura:** ordenar clientes por prioridade operacional.
- **Entrada esperada:** DataFrame já processado pela Matriz STAR (com
  `STATUS`, `CURVA`, `MEDIA CP`, `MESES_SEM_COMPRA`, `EROSAO STAR`).
- **Saída esperada:** o mesmo DataFrame com uma coluna adicional de
  prioridade/ordem, sem alterar as colunas existentes.
- **Não deve:** recalcular status, curva, recência ou erosão.

### `star_intelligence/raio_x_cliente.py`
- **Responsabilidade futura:** montar uma leitura individual e consolidada
  de um único cliente.
- **Entrada esperada:** uma linha (ou subconjunto) do DataFrame da Matriz
  STAR referente a um cliente específico.
- **Saída esperada:** estrutura de dados simples (dict) com os campos já
  calculados, organizados para leitura humana.
- **Não deve:** inferir dados que não estejam na base.

### `star_intelligence/hipoteses.py`
- **Responsabilidade futura:** gerar hipóteses operacionais determinísticas
  a partir de combinações de status, curva, recência e erosão.
- **Entrada esperada:** linha ou DataFrame da Matriz STAR.
- **Saída esperada:** lista de textos (hipóteses), sem HTML.
- **Não deve:** substituir diagnóstico humano nem usar IA.

### `star_intelligence/recomendacoes.py`
- **Responsabilidade futura:** transformar hipóteses em recomendação textual
  de ação, prazo e responsável.
- **Entrada esperada:** hipóteses geradas por `hipoteses.py` mais os campos
  da Matriz STAR.
- **Saída esperada:** lista de recomendações estruturadas (texto).
- **Não deve:** criar automação nem forecast.

### `star_intelligence/visoes_por_papel.py`
- **Responsabilidade futura:** filtrar/organizar as recomendações conforme o
  papel do usuário (vendedor, gestor, sócio, consultor).
- **Entrada esperada:** recomendações já geradas.
- **Saída esperada:** subconjunto/organização das recomendações por papel.
- **Não deve:** gerar novo cálculo ou nova regra de negócio.

## 4. Riscos de arquitetura

- Duplicar lógica do Motor STAR.
- Criar dashboard paralelo.
- Misturar cálculo com recomendação.
- Criar recomendação genérica, sem base nos dados.
- Usar IA cedo demais.
- Perder rastreabilidade.
- Aumentar complexidade antes da necessidade.
- Criar componentes sem teste manual.

## 5. Critérios para iniciar código na Sprint 3.2

Só se deve iniciar código quando estiver claro:

- qual saída será gerada;
- qual DataFrame será usado como entrada;
- quais colunas são necessárias;
- quais regras são determinísticas;
- quais recomendações são apenas textuais;
- como testar sem alterar cálculo STAR;
- como validar no Streamlit.
