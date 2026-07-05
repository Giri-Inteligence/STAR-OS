# CORREÇÃO CONTROLADA DE IDENTIFICADORES DO CICLO_LOOP — STAR OS

## 1. Finalidade

A Sprint 8.2 corrige a identidade do payload `CICLO_LOOP` para que ele
carregue `cliente_id`, `sessao_id` e `nome_cliente` quando disponíveis.

- A correção não cria nova funcionalidade.
- A correção não altera governança.
- A correção não altera loop.
- A correção não altera status.
- A correção não altera acompanhamento.
- A correção não altera o Motor STAR.
- A correção não altera o Streamlit.
- A correção não cria tarefa.
- A correção não cria plano de ação.
- A correção não cria agenda.
- A correção não usa IA.
- A correção não aciona agente.

## 2. Problema corrigido

- Antes, o payload `CICLO_LOOP` podia não carregar `cliente_id`/`sessao_id`
  próprios.
- Isso fazia com que a consulta filtrada por cliente/sessão não
  retornasse o `CICLO_LOOP`, embora ele fosse salvo e contado no total.
- O problema era de identidade de payload, não de cálculo, não de loop
  e não de persistência.

## 3. Decisão de correção

- A correção foi feita no contrato de governança
  (`star_persistence/contrato_governanca.py`).
- O repositório não precisou mudar — confirmado pelos testes
  (`repositorio_governanca.py` inalterado).
- O schema SQLite não mudou.
- O payload `CICLO_LOOP` passou a expor `cliente_id`, `sessao_id` e
  `nome_cliente` no topo quando disponíveis.
- Payloads antigos sem esses campos continuam válidos, com aviso.

A extração busca identificadores, em ordem de prioridade:
`item_loop` → `snapshot_status` → `registro_acompanhamento` → `ciclo_loop`.
Dentro do `ciclo_loop`, a busca considera campos diretos do ciclo e,
na ausência deles, percorre a lista `itens` do ciclo (primeira ocorrência
de `cliente_id`/`sessao_id`/`nome_cliente` em cada item, incluindo
subestruturas conhecidas como `snapshot_status`), de forma limitada e
segura, sem alterar o objeto original.

## 4. Impacto arquitetural

- **Metodologia:** melhora rastreabilidade da governança sem alterar o
  Método STAR.
- **Arquitetura:** corrige identidade na camada correta — o contrato de
  payload — evitando lógica corretiva no repositório ou no Streamlit.
- **Complexidade:** pequena elevação local no contrato; redução de
  ambiguidade na consulta.
- **Manutenção:** testes passam a proteger a extração de identificadores
  do `CICLO_LOOP`.
- **Escalabilidade:** melhora o filtro por cliente/sessão sem alterar
  schema.
- **Experiência do usuário:** prepara validação visual mais limpa na
  Sprint 8.3.
- **Governança comercial:** melhora continuidade investigativa sem
  transformar loop em tarefa.

## 5. O que não foi alterado

- `app.py` não foi alterado.
- `star_governance` não foi alterado.
- `repositorio_governanca.py` não foi alterado.
- Schema SQLite não foi alterado.
- Motor STAR não foi alterado.
- PDF não foi alterado.
- Excel não foi alterado.
- Nenhum dashboard foi criado.
- Nenhum CRM foi criado.
- Nenhuma tarefa foi criada.
- Nenhuma IA foi usada.
- Nenhum agente foi acionado.

## 6. Regressão esperada

- Contrato de governança passa.
- Repositório local de governança passa.
- Configuração de governança passa.
- Acompanhamento passa.
- Status passa.
- Loop semanal passa.
- Histórico investigativo passa.
- Ingestão passa.
- Inteligência passa.
- Nenhum banco permanente é criado.
- Nenhum JSON funcional é criado.

## 7. Relação com Sprint 8.3

A Sprint 8.3 deve validar visualmente se:

- O `CICLO_LOOP` aparece na consulta filtrada por cliente/sessão.
- A seção Governança Investigativa permanece sem tarefa.
- A seção permanece sem agenda.
- A seção permanece sem plano de ação.
- A consulta continua read-only.
- PDF e Excel continuam inalterados.
