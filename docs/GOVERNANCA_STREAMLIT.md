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

## 7. Limite conhecido do payload de Ciclo de Loop

O payload `CICLO_LOOP` (gerado por
`criar_payload_ciclo_loop_persistivel`, Sprint 7.2) não carrega
`cliente_id`/`sessao_id` próprios — o contrato da Sprint 7.2 só extrai
esses campos a partir de registro, snapshot ou item de loop, não do
ciclo isoladamente. Por isso, a consulta filtrada por cliente/sessão
pode não retornar o payload `CICLO_LOOP` salvo, mesmo que ele exista no
repositório (visível na contagem total). Isso é uma característica
herdada do contrato, não uma falha da integração — nenhuma alteração foi
feita em `contrato_governanca.py` ou `repositorio_governanca.py` para
contornar isso nesta sprint.

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
