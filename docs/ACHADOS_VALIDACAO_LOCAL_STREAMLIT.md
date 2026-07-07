# ACHADOS DA VALIDAÇÃO LOCAL NO STREAMLIT — STAR OS

## 1. Finalidade

Este documento registra, segundo o modelo definido em
`docs/MODELO_REGISTRO_ACHADOS_VALIDACAO_LOCAL.md`, os achados reais da
execução da Sprint 9.2, descrita em
`docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`.

## 2. Resumo dos achados por categoria

- **APROVADO:** 1 (ACHADO-9-2-004 — fluxo geral, aviso metodológico,
  campos permitidos, ausência de campos/telas proibidos, preservação
  de PDF/Excel e do Motor STAR).
- **AJUSTE VISUAL:** 1 (ACHADO-9-2-003).
- **RISCO METODOLÓGICO:** 1 (ACHADO-9-2-002).
- **BUG FUNCIONAL:** 1 (ACHADO-9-2-001).
- **BLOQUEIO ARQUITETURAL:** 0.

## 3. Lista detalhada de achados

### ACHADO-9-2-001

- **ID do achado:** ACHADO-9-2-001.
- **Data:** 2026-07-05.
- **Responsável pela validação:** Claude (execução guiada, autorizada
  pelo usuário Giri-Inteligence).
- **Branch:** `sprint-1-giri-star`.
- **Commit:** `f416d2c` (anterior ao commit desta sprint).
- **Planilha utilizada:** `tests/manual/planilha_suja_star.xlsx`.
- **Cliente testado:** Casa do Construtor Sul.
- **Etapa do fluxo:** Consultar a governança salva (etapa 11 do
  protocolo).
- **Categoria do achado:** BUG FUNCIONAL.
- **Descrição objetiva:** o identificador de sessão da investigação
  (`sessao_id`, dentro de `payload_historico`) é recalculado a cada
  execução do script Streamlit, porque `criar_payload_historico_investigativo`
  é chamado sem `criado_em` fixo e `contrato_historico.py` gera
  `sessao_id` a partir de um hash determinístico que inclui o timestamp
  corrente (`gerar_id_deterministico("SESSAO", [cliente_id, origem,
  usuario_responsavel, timestamp])`). Como `payload_historico` não é
  armazenado em `st.session_state`, cada rerun (cada clique em qualquer
  botão da página) gera um novo `sessao_id` para o mesmo cliente. O
  botão "Consultar governança salva deste cliente" filtra
  `listar_payloads_governanca` pelo `sessao_id` do rerun atual — que
  quase nunca coincide com o `sessao_id` usado no rerun em que
  "Salvar governança desta investigação" foi clicado.
- **Evidência observada:** ao salvar duas vezes a governança do mesmo
  cliente (mesma sessão de navegador, mesmo cliente), foram gravados
  dois `sessao_id` diferentes no banco
  (`SESSAO_7BF4537C430D` e `SESSAO_50AD1447B3C1`, ambos para
  `CLIENTE_B1A2AA5DA0A9`). O clique subsequente em "Consultar
  governança salva deste cliente" retornou "Nenhum payload de
  governança encontrado para este cliente/sessão." e "Total de
  payloads consultados: 0", mesmo com os 5 payloads confirmadamente
  salvos. Chamando diretamente
  `listar_payloads_governanca(caminho, cliente_id="CLIENTE_B1A2AA5DA0A9",
  sessao_id="SESSAO_7BF4537C430D")` fora da interface, os 5 payloads
  (incluindo `CICLO_LOOP`) foram retornados corretamente — confirmando
  que o repositório e o contrato funcionam bem, e que o problema está
  isolado na regeneração do `sessao_id` em `app.py`.
- **Impacto metodológico:** nenhum — não induz tarefa, IA ou execução
  automática; é um problema de identidade de dado, não de método de
  governança.
- **Impacto técnico:** alto — a consulta de governança salva, na
  prática, quase nunca encontra os dados que foram salvos minutos
  antes para o mesmo cliente, pois qualquer nova interação do usuário
  gera uma nova "sessão" para efeitos de filtro.
- **Impacto na experiência do usuário:** alto — o usuário salva a
  governança, tenta consultar em seguida e recebe "nenhum payload
  encontrado", podendo concluir (incorretamente) que o salvamento
  falhou ou que os dados foram perdidos.
- **Severidade:** ALTA — compromete a interpretação e o fluxo da
  funcionalidade de consulta (não compromete cálculo, Motor STAR nem
  segurança, por isso não é CRÍTICA).
- **Reprodutibilidade:** alta — reproduzido de forma determinística
  duas vezes nesta sessão, e explicável de forma completa pela leitura
  do código-fonte (`app.py`, `star_persistence/contrato_historico.py`).
- **Decisão recomendada:** corrigir bug funcional, em sprint própria e
  controlada (não nesta Sprint 9.2).
- **Sprint sugerida para tratamento:** Sprint 9.3 (escopo dedicado,
  restrito à estabilidade do identificador de sessão da investigação).
- **Observações:** este achado aciona o critério de bloqueio previsto
  em `docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md`, Seção 7
  ("`CICLO_LOOP` não aparecendo por cliente/sessão após salvamento").
- **Status de tratamento:** **CORRIGIDO NA SPRINT 9.3** — estabilização
  do `sessao_id` via `st.session_state` em `app.py`, revalidada em
  navegador real com resultado aprovado. Ver
  `docs/CORRECAO_IDENTIDADE_SESSAO_GOVERNANCA.md` e
  `docs/RESULTADO_REVALIDACAO_SESSAO_GOVERNANCA_STREAMLIT.md`. Este
  registro original é preservado para histórico e não foi apagado.

### ACHADO-9-2-002

- **ID do achado:** ACHADO-9-2-002.
- **Data:** 2026-07-05.
- **Responsável pela validação:** Claude (execução guiada, autorizada
  pelo usuário Giri-Inteligence).
- **Branch:** `sprint-1-giri-star`.
- **Commit:** `f416d2c` (anterior ao commit desta sprint).
- **Planilha utilizada:** `tests/manual/planilha_suja_star.xlsx`.
- **Cliente testado:** Casa do Construtor Sul.
- **Etapa do fluxo:** Preencher observação / Salvar a governança
  (etapas 9-10 do protocolo).
- **Categoria do achado:** RISCO METODOLÓGICO (da validação, não do
  produto — ver descrição).
- **Descrição objetiva:** o campo "Observação de acompanhamento" foi
  preenchido no navegador (duas tentativas, incluindo o uso do setter
  nativo de `value` do `HTMLTextAreaElement` seguido de eventos
  `input`, `change` e `blur`, com espera de 1,5s antes de salvar), mas
  o payload salvo no banco (`dados_registro.observacao_acompanhamento`)
  ficou vazio em ambas as tentativas. A leitura do trecho relevante de
  `app.py` (linhas 1192-1210) mostra que o valor do widget
  `st.text_area("Observação de acompanhamento", key=...)` é lido
  diretamente e passado a `criar_registro_acompanhamento`, sem lógica
  intermediária suspeita — ou seja, não foi encontrado nenhum defeito
  de código que explique a perda do valor.
- **Evidência observada:** consulta direta ao banco
  (`governanca_payloads`) mostrou
  `"observacao_acompanhamento": ""` nos dois registros salvos, apesar
  do valor preenchido ser lido corretamente como não-vazio no DOM
  (`textarea.value`) imediatamente antes de cada clique em "Salvar".
- **Impacto metodológico:** nenhum confirmado — não há evidência de
  que isso ocorra com interação humana real.
- **Impacto técnico:** desconhecido — não confirmado como defeito real
  do STAR OS; pode ser limitação da técnica de automação sintética de
  eventos do navegador usada nesta validação (o widget `text_area` do
  Streamlit depende de sincronização de estado via sua própria camada
  de front-end, que pode não reconhecer eventos disparados
  sinteticamente da mesma forma que reconhece digitação real).
- **Impacto na experiência do usuário:** não avaliável nesta execução.
- **Severidade:** MÉDIA — insuficiente para classificar como bug
  confirmado, mas relevante o bastante para exigir nova confirmação
  antes de qualquer decisão.
- **Reprodutibilidade:** confirmada dentro do ambiente de automação
  (2 de 2 tentativas), mas não testada com interação humana real nesta
  sessão.
- **Decisão recomendada:** documentar apenas nesta sprint; reconfirmar
  com interação humana real (clique e digitação manuais) antes de
  decidir se é bug funcional.
- **Sprint sugerida para tratamento:** reavaliação dentro da Sprint 9.3
  ou 9.4, junto com a correção do ACHADO-9-2-001 (mesma tela).
- **Observações:** este achado não deve ser tratado como confirmado —
  registrado por transparência metodológica, não como acusação de
  defeito do STAR OS.
- **Status após Sprint 9.4:** **NÃO REPRODUZIDO EM REVALIDAÇÃO LOCAL /
  LIMITAÇÃO DA AUTOMAÇÃO SINTÉTICA.** Revalidado em navegador real com
  clique nativo da ferramenta de preview (em vez do clique sintético
  via JavaScript usado nas Sprints 9.2/9.3): o valor digitado foi salvo
  corretamente no payload, em duas tentativas. `app.py` não foi
  alterado por causa deste achado. Ver
  `docs/RESULTADO_ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_STREAMLIT.md`.
  Este registro original é preservado para histórico.

### ACHADO-9-2-003

- **ID do achado:** ACHADO-9-2-003.
- **Data:** 2026-07-05.
- **Responsável pela validação:** Claude (execução guiada, autorizada
  pelo usuário Giri-Inteligence).
- **Branch:** `sprint-1-giri-star`.
- **Commit:** `f416d2c` (anterior ao commit desta sprint).
- **Planilha utilizada:** `tests/manual/planilha_suja_star.xlsx`.
- **Cliente testado:** Casa do Construtor Sul.
- **Etapa do fluxo:** Salvar a governança (etapa 10 do protocolo).
- **Categoria do achado:** AJUSTE VISUAL.
- **Descrição objetiva:** após clicar em "Salvar governança desta
  investigação" (ação que cria o arquivo do banco com sucesso), a
  legenda de configuração exibida na mesma tela ("Diretório existe:
  NAO", "Arquivo existe: NAO") continuou mostrando o estado anterior
  ao salvamento, dentro do mesmo rerun do Streamlit.
- **Evidência observada:** a legenda "Diretório existe: NAO / Arquivo
  existe: NAO" apareceu junto da mensagem de sucesso "Governança
  salva: 5 payload(s) gravado(s)."; verificação direta no sistema de
  arquivos confirmou que
  `C:\Users\Willi\.star_os\governanca.sqlite` foi de fato criado
  (45.056 bytes) no momento do salvamento.
- **Impacto metodológico:** nenhum.
- **Impacto técnico:** nenhum — é apenas ordem de renderização (a
  legenda é calculada antes do bloco do botão, no mesmo script run);
  o próximo rerun já mostraria o estado correto.
- **Impacto na experiência do usuário:** baixo — pode gerar confusão
  momentânea sobre se o banco foi realmente criado, mas a mensagem de
  sucesso ao lado já confirma o salvamento.
- **Severidade:** BAIXA — não bloqueia uso nem método.
- **Reprodutibilidade:** alta (esperado a cada primeira salvamento de
  um cliente na sessão).
- **Decisão recomendada:** documentar apenas nesta sprint; considerar
  recalcular a legenda após o salvamento em sprint futura de UX, sem
  criar nova funcionalidade.
- **Sprint sugerida para tratamento:** Sprint 9.4 — Estabilização da
  Experiência de Governança (opcional, baixa prioridade).
- **Observações:** nenhuma.
- **Status após Sprint 9.4:** **AJUSTE VISUAL TRATADO.** `app.py`
  passou a exibir, logo após a mensagem de sucesso do salvamento, o
  estado atualizado da legenda ("Após este salvamento — Diretório
  existe: SIM, Arquivo existe: SIM."), usando a função já existente
  `gerar_resumo_configuracao_governanca()`. Nenhum contrato,
  repositório ou schema foi alterado. Ver
  `docs/RESULTADO_ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_STREAMLIT.md`.

### ACHADO-9-2-004

- **ID do achado:** ACHADO-9-2-004.
- **Data:** 2026-07-05.
- **Responsável pela validação:** Claude (execução guiada, autorizada
  pelo usuário Giri-Inteligence).
- **Branch:** `sprint-1-giri-star`.
- **Commit:** `f416d2c` (anterior ao commit desta sprint).
- **Planilha utilizada:** `tests/manual/planilha_suja_star.xlsx`.
- **Cliente testado:** Casa do Construtor Sul.
- **Etapa do fluxo:** Fluxo completo (etapas 1-10, 12, 14-15 do
  protocolo).
- **Categoria do achado:** APROVADO.
- **Descrição objetiva:** upload, geração da Matriz STAR, abertura do
  Raio-X, geração de investigação, localização da seção "Governança
  investigativa", aviso metodológico, campos permitidos (exatamente
  quatro: tipo, status, observação, usuário opcional), ausência de
  campos proibidos, ausência de gráfico/ranking/dashboard/CRM,
  salvamento explícito funcional, preservação de PDF/Excel e do Motor
  STAR — tudo funcionou conforme esperado.
- **Evidência observada:** ver `docs/RESULTADO_VALIDACAO_LOCAL_STREAMLIT.md`,
  Seção 3 (tabela de resultado do fluxo).
- **Impacto metodológico:** positivo — confirma que a base da
  Governança Investigativa é sólida na experiência real.
- **Impacto técnico:** nenhum problema encontrado.
- **Impacto na experiência do usuário:** positivo.
- **Severidade:** BAIXA (não aplicável — achado positivo).
- **Reprodutibilidade:** alta.
- **Decisão recomendada:** sem ação.
- **Sprint sugerida para tratamento:** não aplicável.
- **Observações:** nenhuma.

## 4. Bloqueios constatados

**Sim — um critério de bloqueio foi acionado.**

O ACHADO-9-2-001 aciona formalmente o critério de bloqueio previsto em
`docs/ARQUITETURA_VALIDACAO_OPERACIONAL_LOCAL.md` (Seção 7):
"`CICLO_LOOP` não aparecendo por cliente/sessão após salvamento".
Isso reforça — sem alterar — a condição já vigente no roadmap: IA e
agentes continuam bloqueados até o fechamento completo da Sprint 9 e
decisão arquitetural específica (ver
`docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`).

Nenhum outro bloqueio arquitetural foi identificado. Nenhum achado
desta validação exige mudança de contrato, persistência, governança ou
Motor STAR — a causa raiz do ACHADO-9-2-001 está isolada em `app.py`
(orquestração), não nos módulos protegidos.

## 5. Fechamento — Sprint 9.5

O histórico de achados acima foi consolidado no fechamento da Sprint 9
(ver `docs/FECHAMENTO_VALIDACAO_OPERACIONAL_LOCAL.md`).
