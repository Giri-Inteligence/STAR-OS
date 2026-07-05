# Inventário do Motor de Investigação — STAR OS

## 1. Módulos criados

### `star_intelligence/investigacao.py`
- **Responsabilidade:** transformar perguntas de validação em itens
  investigativos, permitir registrar resposta/evidência/status e gerar
  resumo quantitativo.
- **Entrada esperada:** lista de perguntas de validação (das Hipóteses
  Operacionais), cliente/vendedor/cidade, e atualizações de status/resposta/
  evidência por `id_item`.
- **Saída esperada:** pacote com `itens` (id, pergunta, status, resposta,
  evidência) e `resumo` (contagens e status geral da investigação).
- **Não deve:** criar tarefa, plano de ação, persistir dados ou usar IA.

### `star_intelligence/pacote_investigativo.py`
- **Responsabilidade:** consolidar Raio-X, hipóteses, recomendações e itens
  investigativos em um único pacote legível por cliente.
- **Entrada esperada:** `raio_x`, `pacote_hipoteses`, `recomendacoes` e
  `pacote_investigacao`, todos opcionais (aceita `None` com segurança).
- **Saída esperada:** dicionário consolidado com identificação do cliente,
  status STAR, prioridade, hipóteses, recomendações, itens investigativos,
  contagem por status, evidências registradas, maturidade investigativa e
  leitura consolidada.
- **Não deve:** recalcular Matriz STAR, criar hipótese ou recomendação nova,
  nem persistir dados.

### `star_intelligence/conclusao_investigativa.py`
- **Responsabilidade:** classificar o estado conclusivo de cada item
  investigativo do Pacote Investigativo (confirmado, descartado,
  inconclusivo, pendente ou resposta sem classificação).
- **Entrada esperada:** `pacote_investigativo` gerado pela Sprint 4.2
  (usa `pacote_investigativo["itens_investigativos"]`).
- **Saída esperada:** dicionário com classificações por item, resumo
  quantitativo, leitura conclusiva e listas separadas por classificação
  (confirmadas, descartadas, inconclusivas, pendentes, sem classificação).
- **Não deve:** concluir causa raiz automaticamente, criar ação, tarefa ou
  prazo, nem usar IA.

## 2. Testes manuais criados

- **`tests/manual/testar_investigacao_operacional.py`** — valida
  normalização de status investigativo, criação de itens a partir de
  perguntas (com deduplicação e ids determinísticos `INV_001`, `INV_002`...),
  criação e atualização imutável do pacote, resumo quantitativo e leitura
  não prescritiva.
- **`tests/manual/testar_pacote_investigativo.py`** — valida listas seguras,
  contagem por status, extração de evidências, classificação de maturidade
  investigativa, geração do pacote completo (sem alterar objetos originais)
  e formatação para exibição.
- **`tests/manual/testar_conclusao_investigativa.py`** — valida
  normalização de classificação conclusiva, classificação de item e de
  lista de itens, resumo conclusivo, leitura conclusiva, geração da
  conclusão completa (sem alterar o pacote original) e ausência de termos
  proibidos (IA, token, API, comandos de execução, "causa raiz confirmada").

## 3. Documentos criados

- `docs/MOTOR_INVESTIGACAO_OPERACIONAL.md`
- `docs/PACOTE_INVESTIGATIVO_CLIENTE.md`
- `docs/CONCLUSAO_INVESTIGATIVA.md`
- `docs/FECHAMENTO_MOTOR_INVESTIGACAO.md`
- `docs/INVENTARIO_MOTOR_INVESTIGACAO.md`
- `docs/DECISOES_ARQUITETURAIS_MOTOR_INVESTIGACAO.md`
- `docs/ROADMAP_SPRINT_4_MOTOR_INVESTIGACAO.md`

## 4. Dados usados pelo Motor de Investigação

- Cliente selecionado.
- Vendedor.
- Cidade, se disponível.
- Raio-X Operacional.
- Hipóteses Operacionais.
- Perguntas de validação.
- Recomendações por Papel.
- Itens investigativos.
- Respostas textuais.
- Evidências textuais.
- Status investigativos.
- Pacote Investigativo.
- Classificação conclusiva.

Registrado explicitamente:

- O Motor de Investigação não deve presumir nomes fixos para cliente,
  vendedor e cidade.
- Cliente, vendedor e cidade devem continuar usando as variáveis dinâmicas
  do `app.py` (`clie_col`, `vend_col`, `cida_col`).
- O Motor de Investigação não deve recalcular Matriz STAR.
- O Motor de Investigação não deve alterar o Motor STAR.
- O Motor de Investigação não deve criar persistência antes de uma sprint
  específica para isso.

## 5. Como usar na regressão

- Os testes Python (`testar_*.py`) validam os módulos determinísticos de
  forma isolada, sem depender do Streamlit.
- O Streamlit valida o comportamento real da aplicação (upload, Matriz
  STAR, Fila, Raio-X, Hipóteses, Recomendações, Investigação, Pacote e
  Conclusão).
- A regressão deve confirmar que Matriz STAR, Fila, Raio-X, Hipóteses,
  Recomendações, Investigação, Pacote e Conclusão aparecem corretamente e
  que Excel/PDF continuam sendo gerados sem erro.
- O GitHub Desktop deve ser usado para dar push somente depois que o
  commit local tiver sido validado (compilação + testes + regressão manual
  no Streamlit).
