# REGISTRO DE ACOMPANHAMENTO OPERACIONAL — STAR OS

## 1. Finalidade

O Registro de Acompanhamento Operacional cria uma estrutura
determinística para documentar continuidade da investigação, sem
transformar acompanhamento em execução.

## 2. O que o registro faz

- Extrai contexto do payload histórico (`extrair_contexto_payload_historico`).
- Cria registro de acompanhamento (`criar_registro_acompanhamento`).
- Normaliza tipo de acompanhamento (`normalizar_tipo_acompanhamento`).
- Normaliza status de acompanhamento (`normalizar_status_acompanhamento`).
- Registra observação de acompanhamento.
- Registra evidência complementar.
- Registra decisão operacional humana.
- Gera leitura determinística (`gerar_leitura_acompanhamento`).
- Valida estrutura (`validar_registro_acompanhamento`).
- Permite agrupamento em pacote de acompanhamento
  (`gerar_pacote_acompanhamento_operacional`).

## 3. O que o registro não faz

- Não salva dados.
- Não cria banco.
- Não cria tabela.
- Não altera schema SQLite.
- Não altera `app.py`.
- Não integra com Streamlit.
- Não cria tarefa.
- Não cria plano de ação.
- Não cria prazo.
- Não cria responsável automático.
- Não envia mensagem.
- Não aciona agente.
- Não usa IA.
- Não consome token.
- Não chama API externa.
- Não altera o Motor STAR.
- Não recalcula a Matriz STAR.
- Não altera o Excel de saída.
- Não altera o PDF.

## 4. Tipos de acompanhamento

- `OBSERVACAO`
- `RETORNO`
- `COMPLEMENTO_EVIDENCIA`
- `REVISAO`
- `DECISAO_OPERACIONAL`
- `PENDENCIA_INVESTIGATIVA`

## 5. Status de acompanhamento

- `NAO_INICIADO`
- `EM_ACOMPANHAMENTO`
- `AGUARDANDO_EVIDENCIA`
- `AGUARDANDO_DECISAO`
- `DECISAO_REGISTRADA`
- `ENCERRADO`
- `SUSPENSO`

## 6. Relação com Histórico Investigativo

O Registro de Acompanhamento consome o payload histórico da Sprint 5
(`star_persistence.contrato_historico`), mas não altera o histórico
salvo — o payload é lido apenas para extrair contexto (cliente, sessão,
snapshot, conclusão), nunca modificado.

## 7. Relação com Governança futura

O Registro de Acompanhamento é a base para futuras sprints de status,
loop semanal e governança inicial (ver
`docs/MODELO_CONCEITUAL_LOOP_OPERACIONAL.md`).

## 8. Limites atuais

- Registro existe apenas em memória.
- Não há persistência de acompanhamento.
- Não há tela no Streamlit.
- Não há edição.
- Não há exclusão.
- Não há envio de mensagem.
- Não há tarefa.
- Não há automação.
- Não há agente.

## 9. Continuidade — Sprint 6.3

A Sprint 6.3 criou regras de status e transição sobre estes registros de
acompanhamento (`star_governance/status_acompanhamento.py`), sem alterar
este contrato (ver `docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`).

## 10. Continuidade — Sprint 6.4

Os registros de acompanhamento alimentam o Loop Semanal de Governança da
Sprint 6.4 (ver `docs/LOOP_SEMANAL_GOVERNANCA.md`).

## 11. Fechamento — Sprint 6.5

O Registro de Acompanhamento Operacional compõe a Governança Inicial
fechada na Sprint 6.5 (ver `docs/FECHAMENTO_GOVERNANCA_INICIAL.md`).
