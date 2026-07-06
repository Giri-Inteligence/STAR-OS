# GOVERNANÇA NO STREAMLIT — STAR OS

## 1. Finalidade

A Governança no Streamlit permite registrar, salvar e consultar
continuidade investigativa de forma controlada.

- Não é dashboard.
- Não é CRM.
- Não é agenda.
- Não é calendário.
- Não é tarefa.
- Não é plano de ação.
- Não é automação.
- Não é agente.
- Não é IA.
- Não altera o Motor STAR.

## 2. O que a interface faz

- Exibe seção de Governança investigativa, dentro do mesmo fluxo do
  Raio-X/Histórico Investigativo do cliente selecionado.
- Mostra configuração local do banco de governança (caminho, se o
  diretório/arquivo já existem).
- Permite registro de acompanhamento (tipo, status, observação, usuário
  opcional).
- Gera snapshot de status.
- Gera item de loop.
- Gera ciclo de loop (com uma entrada, referente à investigação atual).
- Gera payloads persistíveis via `contrato_governanca.py`.
- Valida payloads antes de salvar.
- Salva no repositório local por ação explícita do usuário (botão
  "Salvar governança desta investigação").
- Consulta payloads salvos por ação explícita (botão "Consultar
  governança salva deste cliente").
- Exibe resumo técnico simples do repositório.

## 3. O que a interface não faz

- Não cria tarefa.
- Não cria plano de ação.
- Não cria prazo.
- Não cria responsável automático.
- Não cria agenda.
- Não cria calendário.
- Não envia mensagem.
- Não chama API externa.
- Não aciona agente.
- Não usa IA.
- Não gera recomendação nova.
- Não recalcula STAR.
- Não altera Excel.
- Não altera PDF.

## 4. Local da persistência

- O caminho padrão é `Path.home() / ".star_os" / "governanca.sqlite"`.
- A variável de ambiente `STAR_OS_GOVERNANCA_DB` pode sobrescrever o
  caminho.
- A configuração (`configuracao_governanca.py`) não cria banco sozinha.
- O banco só é criado quando o usuário executa a ação explícita de
  salvamento ("Salvar governança desta investigação").

## 5. Relação com contrato e repositório

- A interface usa `contrato_governanca.py` (Sprint 7.2).
- A interface usa `repositorio_governanca.py` (Sprint 7.3).
- A interface não cria contrato novo.
- A interface não cria repositório paralelo.
- Payload inválido não é salvo — a validação ocorre antes do
  `salvar_lote_payloads_governanca`.

## 6. Relação com histórico investigativo

- Governança depende de uma investigação atual (o payload histórico já
  construído no fluxo do Raio-X, Sprint 5.4).
- Governança referencia cliente e sessão a partir desse payload.
- Governança não altera o histórico investigativo original.
- Governança não altera o schema SQLite do histórico investigativo.

## 7. Limitação do payload de Ciclo de Loop (corrigida na Sprint 8.2)

O payload `CICLO_LOOP` (gerado por `criar_payload_ciclo_loop_persistivel`)
antes não carregava `cliente_id`/`sessao_id` próprios — o contrato da
Sprint 7.2 só extraía esses campos a partir de registro, snapshot ou
item de loop, não do ciclo isoladamente. Por isso, a consulta filtrada
por cliente/sessão podia não retornar o payload `CICLO_LOOP` salvo,
mesmo que ele existisse no repositório.

Essa limitação foi tratada de forma controlada no contrato de governança
na Sprint 8.2 (ver `docs/CORRECAO_IDENTIFICADORES_CICLO_LOOP.md`) — o
`CICLO_LOOP` passou a extrair `cliente_id`/`sessao_id`/`nome_cliente` a
partir dos itens do ciclo, sem alterar `app.py`, `repositorio_governanca.py`
ou o schema SQLite. A validação visual da Sprint 8.3 deve confirmar esse
comportamento na interface.

## 8. Limites atuais

- Interface inicial é controlada.
- Não há edição de registros salvos.
- Não há exclusão lógica.
- Não há trilha de auditoria completa.
- Não há multiusuário.
- Não há permissões.
- Não há CRM.
- Não há ERP.
- Não há WhatsApp.
- Não há MCP.
- Não há agente.
- Não há IA.

## 9. Validação manual esperada

- A seção aparece no fluxo do cliente (dentro do Raio-X).
- A mensagem metodológica aparece.
- Os campos não incluem responsável, prazo, tarefa ou agenda.
- O botão de salvamento é explícito.
- A consulta é somente leitura.
- O salvamento cria banco apenas fora do repositório
  (`Path.home() / ".star_os"`).
- PDF e Excel não mudam.
- O Motor STAR não muda.

## 10. Fechamento — Sprint 7.5

A exposição no Streamlit compõe a Governança Integrada fechada na
Sprint 7.5 (ver `docs/FECHAMENTO_GOVERNANCA_INTEGRADA.md`).

## 11. Continuidade — Sprint 8.1

A validação visual guiada será tratada na Sprint 8.3, após decisão e
correção controlada do `CICLO_LOOP` na Sprint 8.2 (ver
`docs/MODELO_VALIDACAO_VISUAL_GOVERNANCA.md`).

## 12. Continuidade — Sprint 8.3

A Sprint 8.3 validou estaticamente a seção e documentou roteiro de
validação visual humana (ver
`docs/RESULTADO_VALIDACAO_VISUAL_GOVERNANCA_STREAMLIT.md`).

## 13. Continuidade — Sprint 8.4

A Sprint 8.4 passou a exibir leitura operacional não prescritiva após
consulta de governança salva (ver
`docs/LEITURA_OPERACIONAL_GOVERNANCA_SEM_TAREFAS.md`).

## 14. Fechamento — Sprint 8.5

A seção Governança Investigativa entra na próxima fase (Sprint 9) como
objeto de validação local real (ver
`docs/FECHAMENTO_CONSOLIDACAO_OPERACIONAL_GOVERNANCA.md`).

## 15. Continuidade — Sprint 9.1

A seção Governança Investigativa será objeto de validação local real na
Sprint 9 (ver `docs/PROTOCOLO_VALIDACAO_LOCAL_STREAMLIT.md`).

## 16. Continuidade — Sprint 9.2

A validação local real, executada em navegador contra um servidor
Streamlit local, confirmou que o salvamento explícito, o aviso
metodológico e os campos permitidos funcionam corretamente. Também
confirmou um achado de bug funcional: o botão "Consultar governança
salva deste cliente" pode não localizar payloads recém-salvos para o
mesmo cliente, porque o identificador de sessão da investigação
(`sessao_id`) é recalculado a cada execução do script Streamlit em vez
de permanecer estável durante a investigação (ver
`docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md`, ACHADO-9-2-001, e
`docs/DECISAO_POS_VALIDACAO_LOCAL_STREAMLIT.md`). O contrato e o
repositório de governança não são afetados por este achado — a causa
raiz está isolada em `app.py`.

## 17. Continuidade — Sprint 9.3

A identidade da sessão investigativa usada pela Governança foi
estabilizada na Sprint 9.3 via `st.session_state` em `app.py`,
corrigindo o ACHADO-9-2-001. Consulta e salvamento passam a usar o
mesmo `sessao_id` durante a investigação do mesmo cliente (ver
`docs/CORRECAO_IDENTIDADE_SESSAO_GOVERNANCA.md`).
