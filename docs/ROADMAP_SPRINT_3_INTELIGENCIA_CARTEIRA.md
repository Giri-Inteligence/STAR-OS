# ROADMAP — SPRINT 3 INTELIGÊNCIA DE CARTEIRA

## Sequência proposta

### Sprint 3.1 — Inventário e Integração Conceitual da Inteligência de Carteira — CONCLUÍDA
- Documentar integração.
- Mapear componentes.
- Definir ordem segura.

### Sprint 3.2 — Fila de Prioridade da Carteira — CONCLUÍDA
- Criar regra determinística inicial para ordenar clientes por prioridade.
- Usar Matriz STAR como entrada.
- Não alterar cálculo.
- Implementada em `star_intelligence/priorizacao.py`, integrada de forma
  discreta em `app.py` via `st.expander("Fila de Prioridade da Carteira")`.

### Sprint 3.3 — Raio-X Operacional do Cliente — CONCLUÍDA
- Gerar leitura individual por cliente.
- Exibir dados principais.
- Não criar IA.
- Implementada em `star_intelligence/raio_x_cliente.py`, integrada de forma
  discreta em `app.py` via `st.expander("Raio-X Operacional do Cliente")`,
  logo após a Fila de Prioridade.

### Sprint 3.4 — Hipóteses Operacionais por Status — EM IMPLEMENTAÇÃO
- Criar hipóteses determinísticas por status STAR, curva, recência e erosão.
- Não substituir diagnóstico humano.
- Sistema especialista determinístico, sem IA, sem chamada de API externa.
- Implementada em `star_intelligence/hipoteses.py`, integrada dentro do
  mesmo expander do Raio-X Operacional do Cliente em `app.py`.

### Sprint 3.5 — Recomendações por Papel
- Separar leitura para vendedor, gestor, sócio e consultor.
- Manter baixa carga cognitiva por papel.

### Sprint 3.6 — Fechamento da Inteligência de Carteira
- Documentar.
- Regressão.
- Critérios de aceite.

## Critério de não avanço

Não avançar para a próxima sub-sprint se:

- a regressão manual da ingestão (Sprint 2) parar de passar;
- qualquer regra do Motor STAR precisar ser alterada para viabilizar a nova
  camada;
- a saída proposta não puder ser gerada só com dados já existentes na
  Matriz STAR;
- não houver forma de testar a mudança sem alterar `star_core`.

## Critério de regressão

Antes de cada sub-sprint da Sprint 3, repetir:

- `python -m py_compile app.py star_ingestion/*.py tests/manual/*.py`;
- os testes manuais de ingestão (`testar_relatorio_ingestao.py`,
  `testar_diagnostico_mapeamento.py`, `testar_normalizacao_meses.py`,
  `testar_normalizacao_valores.py`, `testar_qualidade_linhas.py`);
- validação manual no Streamlit de que a Matriz STAR, o Excel e o PDF
  continuam funcionando.

## Arquivos que não podem ser alterados sem autorização explícita

- `star_core/calculos.py`
- `star_core/curva.py`
- `star_core/recencia.py`
- Exportação PDF.
- Exportação Excel.
- Layout/estética principal do `app.py`.

## Regra de proteção do Motor STAR

A Inteligência de Carteira é consumidora da Matriz STAR, nunca sua
substituta. Qualquer necessidade de alterar uma regra de cálculo, status,
curva, recência ou erosão para "encaixar" uma funcionalidade de
Inteligência de Carteira deve ser tratada como sinal de alerta arquitetural
e discutida explicitamente antes de qualquer código — não deve ser feita
silenciosamente dentro de uma sprint de inteligência.

## Critério de sucesso da Sprint 3

- A Matriz STAR continua sendo a fonte de verdade dos dados.
- Cada sub-sprint entrega uma camada pequena, testável e reversível.
- Nenhuma regra determinística existente é substituída por IA.
- Nenhum arquivo `star_core` é alterado sem autorização explícita.
- A Inteligência de Carteira permanece integrada ao STAR OS, sem virar
  aplicação ou dashboard paralelo.
