# STATUS DE ACOMPANHAMENTO DA INVESTIGAÇÃO — STAR OS

## 1. Finalidade

O Status de Acompanhamento da Investigação cria uma camada determinística
para organizar o estado de continuidade da investigação, a partir dos
registros de acompanhamento criados na Sprint 6.2.

## 2. O que o status faz

- Define status permitidos (`obter_status_acompanhamento_permitidos`).
- Define transições conceituais permitidas
  (`obter_transicoes_status_permitidas`).
- Avalia transições (`avaliar_transicao_status`).
- Identifica status final (`status_eh_final`).
- Identifica dependência de evidência (`status_exige_evidencia`).
- Identifica dependência de decisão humana (`status_exige_decisao`).
- Ordena registros (`ordenar_registros_por_criado_em`).
- Identifica status atual (`obter_status_atual_acompanhamento`).
- Valida consistência da sequência
  (`validar_consistencia_status_acompanhamento`).
- Cria snapshot em memória (`criar_snapshot_status_acompanhamento`).
- Gera leitura textual não prescritiva
  (`gerar_leitura_status_acompanhamento`).

## 3. O que o status não faz

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

## 4. Status permitidos

- `NAO_INICIADO`
- `EM_ACOMPANHAMENTO`
- `AGUARDANDO_EVIDENCIA`
- `AGUARDANDO_DECISAO`
- `DECISAO_REGISTRADA`
- `ENCERRADO`
- `SUSPENSO`

## 5. Transições conceituais

- `ENCERRADO` é final por padrão — não permite transição sem autorização
  explícita (`permitir_reabertura=True` no contexto).
- `SUSPENSO` é pausa, não é final; pode retomar para
  `EM_ACOMPANHAMENTO` ou encerrar.
- Reabertura de `ENCERRADO` é exceção controlada: mesmo autorizada,
  só permite ir para `EM_ACOMPANHAMENTO` — nunca direto para outro status.
- Transição para `AGUARDANDO_EVIDENCIA` sem evidência complementar no
  contexto gera aviso.
- Transição para `DECISAO_REGISTRADA` sem decisão operacional no
  contexto gera aviso.
- Transição para `AGUARDANDO_DECISAO` sempre gera aviso de dependência de
  decisão humana.
- Aviso não é tarefa.
- Aviso não é plano de ação.
- Aviso não é execução.

## 6. Relação com Registro de Acompanhamento Operacional

Esta sprint consome os registros criados pela Sprint 6.2
(`star_governance/acompanhamento.py`), mas não altera o contrato do
registro — apenas lê os campos `status_acompanhamento` e `criado_em` para
avaliar estado e ordem temporal.

## 7. Relação com Loop Operacional

O status de acompanhamento é pré-condição para o futuro Loop Semanal de
Governança (Sprint 6.4), porque organiza o estado da continuidade
investigativa que o loop precisará consultar.

## 8. Limites atuais

- Status existe apenas em memória.
- Não há persistência de status.
- Não há tela no Streamlit.
- Não há edição.
- Não há exclusão.
- Não há envio de mensagem.
- Não há tarefa.
- Não há automação.
- Não há agente.
