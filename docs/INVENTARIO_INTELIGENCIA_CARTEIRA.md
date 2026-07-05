# Inventário da Inteligência de Carteira — STAR OS

## 1. Módulos criados

### `star_intelligence/__init__.py`
- **Responsabilidade:** marcar `star_intelligence` como pacote Python.
- **Entrada esperada:** nenhuma.
- **Saída esperada:** nenhuma.
- **Não deve:** conter lógica.

### `star_intelligence/priorizacao.py`
- **Responsabilidade:** calcular pontuação e ordenar clientes por prioridade
  operacional a partir da Matriz STAR.
- **Entrada esperada:** DataFrame já calculado pela Matriz STAR (colunas
  `CURVA`, `STATUS`, `MESES_SEM_COMPRA`, `EROSAO STAR`, `MEDIA LP`,
  `MEDIA CP`).
- **Saída esperada:** cópia do DataFrame com `PONTUACAO_PRIORIDADE`,
  `NIVEL_PRIORIDADE`, `TIPO_PRIORIDADE`, `MOTIVOS_PRIORIDADE`, ordenada por
  prioridade decrescente.
- **Não deve:** remover clientes, recalcular campos STAR ou alterar nomes de
  colunas existentes.

### `star_intelligence/raio_x_cliente.py`
- **Responsabilidade:** montar leitura individual e determinística de um
  cliente (variação de médias, sinais operacionais, leitura textual não
  prescritiva).
- **Entrada esperada:** uma linha (Series) da Matriz STAR/Fila de
  Prioridade, mais os nomes dinâmicos das colunas de cliente/vendedor/cidade.
- **Saída esperada:** dicionário estruturado (`gerar_raio_x_cliente`) e lista
  de strings para exibição (`formatar_raio_x_texto`).
- **Não deve:** recalcular Motor STAR, gerar recomendação ou plano de ação.

### `star_intelligence/hipoteses.py`
- **Responsabilidade:** gerar hipóteses determinísticas, perguntas de
  validação e alertas de investigação por status/sinais — sistema
  especialista, sem IA.
- **Entrada esperada:** uma linha (Series) com `STATUS`, `CURVA`,
  `MESES_SEM_COMPRA`, `EROSAO STAR`, `MEDIA LP`, `MEDIA CP`,
  `NIVEL_PRIORIDADE`, `TIPO_PRIORIDADE`.
- **Saída esperada:** dicionário (`gerar_hipoteses_cliente`) com
  `hipoteses_status`, `hipoteses_sinais`, `perguntas_validacao`,
  `alertas_investigacao`, `resumo_hipotese`.
- **Não deve:** chamar API externa, usar IA, criar recomendação completa ou
  plano de ação.

### `star_intelligence/recomendacoes.py`
- **Responsabilidade:** adaptar a leitura operacional por papel (VENDEDOR,
  GESTOR, SOCIO, CONSULTOR) a partir do foco definido pelo status e das
  hipóteses já geradas.
- **Entrada esperada:** uma linha (Series) da Matriz STAR/Fila de
  Prioridade, o papel desejado, e opcionalmente o pacote de hipóteses.
- **Saída esperada:** dicionário com `papel`, `foco_operacional`,
  `recomendacoes`, `observacoes` (um papel) ou dicionário por papel
  (`gerar_recomendacoes_multiplos_papeis`).
- **Não deve:** criar tarefa, prazo, responsável automático, mensagem
  automática ou qualquer execução — apenas orientação textual.

## 2. Testes manuais criados

- **`tests/manual/testar_priorizacao_carteira.py`** — valida pontuação,
  nível e tipo de prioridade, geração e ordenação da fila, preservação de
  todos os clientes e consistência do resumo (P1+P2+P3+P4 = total).
- **`tests/manual/testar_raio_x_cliente.py`** — valida cálculo de variação
  de médias, classificação de sinal, sinais operacionais, leitura
  operacional e o dicionário estruturado completo do Raio-X.
- **`tests/manual/testar_hipoteses_operacionais.py`** — valida hipóteses por
  status, hipóteses por sinais, perguntas de validação, alertas de
  investigação e ausência de comandos de ação ("ligue", "visite" etc.).
- **`tests/manual/testar_recomendacoes_por_papel.py`** — valida
  normalização de papel, foco operacional, recomendações para os 4 papéis,
  agregação "TODOS" e ausência de termos proibidos (IA, token, API,
  automação).

## 3. Documentos criados

- `docs/INTELIGENCIA_CARTEIRA_INTEGRADA.md`
- `docs/MAPA_COMPONENTES_INTELIGENCIA_CARTEIRA.md`
- `docs/ROADMAP_SPRINT_3_INTELIGENCIA_CARTEIRA.md`
- `docs/FILA_PRIORIDADE_CARTEIRA.md`
- `docs/RAIO_X_OPERACIONAL_CLIENTE.md`
- `docs/HIPOTESES_OPERACIONAIS.md`
- `docs/RECOMENDACOES_POR_PAPEL.md`

## 4. Campos usados da Matriz STAR

- `CURVA`
- `STATUS`
- `MEDIA LP`
- `MEDIA CP`
- `MESES_SEM_COMPRA`
- `EROSAO STAR`
- `META`
- `ACAO`
- Cliente, como coluna dinâmica escolhida no mapeamento (`clie_col`).
- Vendedor, como coluna dinâmica escolhida no mapeamento (`vend_col`).
- Cidade, se existir, como coluna dinâmica escolhida no mapeamento
  (`cida_col`).

Registrado explicitamente:

- A Inteligência de Carteira não deve presumir nomes fixos para cliente,
  vendedor e cidade.
- Cliente, vendedor e cidade devem continuar usando as variáveis dinâmicas
  do `app.py`.
- O campo "Total CP" não deve ser assumido, pois não existe hoje como
  coluna consolidada confirmada no código (apenas `MEDIA CP` é calculada).

## 5. Como usar na regressão

- Os testes Python (`testar_*.py`) validam os módulos determinísticos de
  forma isolada, sem depender do Streamlit.
- O Streamlit valida o comportamento real da aplicação (upload, Matriz
  STAR, Fila de Prioridade, Raio-X, Hipóteses, Recomendações, downloads).
- A regressão deve confirmar que Matriz STAR, Fila de Prioridade, Raio-X,
  Hipóteses e Recomendações aparecem corretamente e que Excel/PDF
  continuam sendo gerados sem erro.
- O GitHub Desktop deve ser usado para dar push somente depois que o
  commit local tiver sido validado (compilação + testes + regressão manual
  no Streamlit).
