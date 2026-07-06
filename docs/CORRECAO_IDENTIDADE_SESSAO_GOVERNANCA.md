# CORREÇÃO CONTROLADA DA IDENTIDADE DE SESSÃO DA GOVERNANÇA — STAR OS

## 1. Finalidade

A Sprint 9.3 corrige o ACHADO-9-2-001, identificado na validação local
real da Sprint 9.2, estabilizando a identidade da sessão investigativa
usada pela Governança Investigativa entre reruns do Streamlit.

Registrado explicitamente:

- A correção não cria nova funcionalidade.
- A correção não altera Motor STAR.
- A correção não altera cálculo STAR.
- A correção não altera `contrato_governanca.py`.
- A correção não altera `repositorio_governanca.py`.
- A correção não altera schema SQLite.
- A correção não altera `star_governance`.
- A correção não cria tarefa.
- A correção não cria agenda.
- A correção não cria plano de ação.
- A correção não cria IA.
- A correção não cria agente.

## 2. Problema corrigido

- O Streamlit reroda o script inteiro do `app.py` a cada interação do
  usuário (clique em botão, preenchimento de campo com envio ao
  backend, etc.).
- O `sessao_id` da investigação era recalculado em cada rerun, porque
  `payload_historico` era reconstruído do zero a cada execução, sem
  fixar o parâmetro `criado_em` de `criar_payload_historico_investigativo`
  — e `sessao_id` é derivado, dentro de `contrato_historico.py`
  (protegido, não alterado), de um hash determinístico que inclui esse
  timestamp.
- Como consequência, a Governança podia ser salva com um `sessao_id` e
  consultada, na interação seguinte, com outro `sessao_id` diferente
  para o mesmo cliente — fazendo "Consultar governança salva deste
  cliente" não localizar os dados que tinham acabado de ser gravados.
- O repositório (`repositorio_governanca.py`) estava correto: consultado
  diretamente com o `sessao_id` certo, sempre retornou os payloads
  esperados, incluindo o `CICLO_LOOP`.
- O contrato (`contrato_governanca.py`) estava correto: os payloads
  eram criados e validados sem problema.
- O problema era exclusivamente de orquestração em `app.py` — a
  ausência de estabilização da identidade de sessão entre reruns.

## 3. Decisão de correção

- A identidade da sessão investigativa passou a ser preservada em
  `st.session_state`, usando a chave
  `sessao_investigativa::{cliente}::{vendedor}::{arquivo}` (nome do
  cliente selecionado no Raio-X, vendedor e nome do arquivo enviado).
- Na primeira vez que essa chave é usada para um cliente/arquivo, um
  timestamp (`criado_em`) é gerado e armazenado em
  `st.session_state`. Em reruns seguintes, para o mesmo
  cliente/arquivo, o mesmo timestamp é reaproveitado.
- Esse `criado_em` estabilizado é passado para
  `criar_payload_historico_investigativo(..., criado_em=...)` — uma
  chamada que já aceitava esse parâmetro antes da Sprint 9.3, sem
  qualquer alteração em `star_persistence`.
- Como o `sessao_id` (e os demais identificadores derivados do mesmo
  timestamp, como `snapshot_id`, `pacote_id` e `conclusao_id`) são
  gerados de forma determinística a partir desse `criado_em`, eles
  passam a ser estáveis entre reruns para o mesmo cliente/arquivo.
- Salvamento e consulta de governança passam a usar o mesmo
  `payload_historico`, e portanto o mesmo `sessao_id`, durante toda a
  investigação do cliente.
- Se o cliente selecionado ou o arquivo enviado mudar, uma nova chave
  de sessão é usada automaticamente — nenhuma sessão de outro cliente é
  reaproveitada.
- A correção ficou inteiramente em `app.py` porque o problema estava
  na orquestração do fluxo visual, não nos contratos, repositórios ou
  regras de governança.

## 4. Impacto arquitetural

**Metodologia:** preserva a Governança Investigativa como continuidade
investigativa — a correção apenas estabiliza um identificador técnico,
sem alterar o significado metodológico de nenhum campo ou fluxo.

**Arquitetura:** mantém `contrato_governanca.py`, `repositorio_governanca.py`,
`configuracao_governanca.py`, `leitura_operacional.py` e o schema
SQLite intactos; corrige somente a orquestração em `app.py`.

**Complexidade:** pequena elevação controlada em `app.py` (uma chave de
`st.session_state` e um parâmetro adicional em uma chamada já
existente); reduz ambiguidade operacional ao tornar a consulta
confiável.

**Manutenção:** o novo teste estático
(`tests/manual/testar_identidade_sessao_governanca_streamlit.py`)
protege a presença da estabilização de sessão contra regressões
futuras, sem depender de execução do Streamlit.

**Escalabilidade:** prepara uma base estável para validação por
cliente/sessão, útil para qualquer evolução futura de UX (Sprint 9.4)
sem exigir nova arquitetura de identidade.

**Experiência do usuário:** a consulta de governança salva passa a
encontrar, de forma confiável, os dados que o próprio usuário acabou
de salvar para o cliente em investigação.

**Governança comercial:** preserva rastreabilidade da investigação sem
criar tarefa, plano de ação, agenda ou qualquer forma de execução
automática.

## 5. O que não foi alterado

- `star_core` não foi alterado.
- `star_ingestion` não foi alterado.
- `star_intelligence` não foi alterado.
- `star_persistence` não foi alterado.
- `star_governance` não foi alterado.
- `contrato_governanca.py` não foi alterado.
- `repositorio_governanca.py` não foi alterado.
- `configuracao_governanca.py` não foi alterado.
- `leitura_operacional.py` não foi alterado.
- Schema SQLite (histórico ou governança) não foi alterado.
- PDF não foi alterado.
- Excel não foi alterado.
- Nenhuma tarefa foi criada.
- Nenhuma agenda foi criada.
- Nenhum plano de ação foi criado.
- Nenhuma IA foi chamada.
- Nenhum agente foi acionado.
- Nenhum botão novo foi criado.
- Nenhuma tela nova foi criada.
- Nenhum gráfico, ranking ou dashboard foi criado.

## 6. Relação com Sprint 9.2

Esta correção responde diretamente ao ACHADO-9-2-001, registrado na
validação local real da Sprint 9.2 (ver
`docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md` e
`docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`). Os demais achados da
Sprint 9.2 (ACHADO-9-2-002 — risco metodológico não confirmado, e
ACHADO-9-2-003 — ajuste visual de baixa severidade) não foram
corrigidos nesta sprint, por decisão explícita do escopo da Sprint 9.3.
O ACHADO-9-2-002 (campo de observação salvo vazio) foi observado
novamente durante a revalidação desta sprint, sob a mesma técnica de
automação de navegador, e permanece sem confirmação como defeito real
do STAR OS — ver `docs/RESULTADO_REVALIDACAO_SESSAO_GOVERNANCA_STREAMLIT.md`.

## 7. Relação com Sprint 9.4

Se a revalidação desta sprint for aprovada, a próxima sprint
recomendada é a **Sprint 9.4 — Estabilização da Experiência de
Governança**.
