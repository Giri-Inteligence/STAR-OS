# ROBUSTEZ AVANÇADA DO MOTOR DE INGESTÃO — STAR OS

## 1. Finalidade

O Motor de Ingestão existe para transformar planilhas Excel heterogêneas
(exportadas de ERP, CRM ou controles internos) em uma base minimamente
confiável para a Matriz STAR.

- A ingestão vem antes da inteligência.
- A normalização vem antes da IA.
- O Motor STAR permanece protegido.
- O Excel-first continua sendo a estratégia da fase atual.

## 2. Escopo consolidado da Sprint 2

- Relatório Estruturado de Ingestão (Sprint 2.1).
- Diagnóstico de Falhas de Mapeamento (Sprint 2.2).
- Normalização Avançada de Meses (Sprint 2.3).
- Normalização Avançada de Valores Monetários (Sprint 2.4).
- Qualidade de Linhas, Clientes Zerados e Resíduos (Sprint 2.5).

## 3. Módulos do Motor de Ingestão

### `star_ingestion/saneamento.py`
- **Responsabilidade:** remover linhas/colunas totalmente vazias, cabeçalhos
  repetidos dentro da tabela e linhas de TOTAL/SUBTOTAL exatas.
- **Pode:** limpar sujeiras estruturais óbvias da planilha bruta.
- **Não deve:** remover cliente real, alterar valores de venda ou decidir
  sobre qualidade de identidade do cliente (isso é papel de
  `qualidade_linhas.py`).

### `star_ingestion/validacao.py`
- **Responsabilidade:** validar se a base tem estrutura mínima (colunas
  obrigatórias, colunas mensais existentes e numéricas, pelo menos uma linha
  com cliente e uma venda registrada).
- **Pode:** bloquear a ingestão quando a base é claramente insuficiente.
- **Não deve:** aplicar regra de negócio do Motor STAR nem decidir status,
  curva ou erosão.

### `star_ingestion/relatorio.py`
- **Responsabilidade:** consolidar um relatório estruturado do que aconteceu
  na ingestão (estado inicial/final, mapeamento, saneamento, erros, avisos).
- **Pode:** registrar e formatar informações para exibição discreta no
  Streamlit.
- **Não deve:** tomar decisões — apenas documentar o que os outros módulos já
  decidiram.

### `star_ingestion/diagnostico_mapeamento.py`
- **Responsabilidade:** explicar, antes do bloqueio, qual campo (cliente,
  vendedor, cidade, meses) não foi reconhecido e sugerir como corrigir.
- **Pode:** gerar erros, avisos e sugestões textuais determinísticas.
- **Não deve:** bloquear por ausência de cidade (opcional) nem substituir a
  validação de conteúdo feita por `validacao.py`.

### `star_ingestion/normalizacao_meses.py`
- **Responsabilidade:** reconhecer variações de nome de coluna mensal (texto,
  numérico, com prefixo, ISO) e ordená-las cronologicamente.
- **Pode:** reordenar e ampliar a lista de colunas de mês reconhecidas; avisar
  sobre períodos duplicados.
- **Não deve:** renomear colunas, alterar valores ou bloquear por duplicidade
  (apenas avisa).

### `star_ingestion/normalizacao_valores.py`
- **Responsabilidade:** converter valores monetários em formatos variados
  (brasileiro, americano, misto, vazio, hífen) para float.
- **Pode:** transformar valores vazios/hífen/inválidos em 0.0 e registrar
  estatísticas de conversão.
- **Não deve:** criar regra de negócio nova nem alterar a fórmula de cálculo
  do Motor STAR.

### `star_ingestion/qualidade_linhas.py`
- **Responsabilidade:** diferenciar cliente real (mesmo zerado ou com compra
  parcial) de linha residual/placeholder evidente.
- **Pode:** remover linhas cuja identidade de cliente seja claramente
  inválida (vazio, "-", TOTAL, SUBTOTAL, cabeçalho repetido como valor etc.).
- **Não deve:** remover cliente por ausência de venda, baixa frequência de
  compra ou qualquer critério que não seja a identidade do cliente.

## 4. Fluxo conceitual da ingestão

1. Leitura do Excel (aba única ou consolidação de abas).
2. Saneamento leve (linhas/colunas vazias, cabeçalho repetido).
3. Identificação/mapeamento de colunas (cliente, vendedor, cidade, meses).
4. Diagnóstico de mapeamento.
5. Normalização de meses.
6. Normalização de valores monetários.
7. Qualidade de linhas (remoção de resíduos, preservação de clientes reais).
8. Validação da base mínima.
9. Geração da Matriz STAR.
10. Exportação Excel/PDF.

## 5. Critérios de sucesso consolidados

- Planilha válida processa.
- Planilha suja recuperável é saneada e processa.
- Planilha inválida é bloqueada.
- Formatos reais de colunas são reconhecidos.
- Meses avançados são reconhecidos e ordenados.
- Valores monetários avançados são convertidos.
- Clientes reais zerados permanecem.
- Linhas residuais evidentes são removidas.
- Cliente com compra parcial permanece.
- Cliente com muitos meses zerados permanece.
- PDF e Excel continuam funcionando.
- Nenhuma regra STAR foi alterada.

## 6. Limites conhecidos

- O sistema ainda não salva perfis de mapeamento por cliente.
- O sistema ainda não aprende padrões recorrentes automaticamente.
- O sistema ainda não possui banco de dados.
- O sistema ainda não integra com ERP/CRM.
- O sistema ainda não usa IA para inferir campos ambíguos.
- A validação ainda é determinística.
- Casos ambíguos devem ser tratados por confirmação humana ou sprint
  específica.

## 7. Condição de avanço

O STAR OS pode avançar para a próxima fase apenas se:

- A regressão manual continuar passando.
- O Motor STAR permanecer protegido.
- A ingestão continuar tratando planilhas reais sem quebrar cálculo.
- As falhas forem documentadas antes de qualquer correção.

A robustez de ingestão é pré-condição para a Inteligência de Carteira,
porque a interpretação operacional depende de dados saneados, normalizados
e validados (ver `docs/INTELIGENCIA_CARTEIRA_INTEGRADA.md`).
