# MODELO DE DADOS DO HISTÓRICO INVESTIGATIVO — STAR OS

## 1. Finalidade do modelo

O modelo define a estrutura mínima para persistir investigações futuras de
forma rastreável, sem implementar persistência funcional nesta sprint.

## 2. Entidades conceituais

- Cliente Investigado.
- Sessão Investigativa.
- Item Investigativo.
- Evidência Investigativa.
- Pacote Investigativo.
- Conclusão Investigativa.
- Snapshot STAR.
- Metadados da Execução.

## 3. Cliente Investigado

Campos mínimos:

- `cliente_id`
- `nome_cliente`
- `vendedor`
- `cidade`
- `origem_cliente_coluna`
- `origem_vendedor_coluna`
- `origem_cidade_coluna`
- `criado_em`
- `atualizado_em`

Registrado:

- `cliente_id` não deve depender apenas do nome.
- `cliente_id` futuro pode ser hash determinístico ou identificador
  externo.
- Não implementar hash nesta sprint.

## 4. Sessão Investigativa

Campos mínimos:

- `sessao_id`
- `cliente_id`
- `data_sessao`
- `origem`
- `usuario_responsavel`
- `status_sessao`
- `versao_modelo`
- `criado_em`
- `atualizado_em`

Status possíveis: `ABERTA`, `EM_ANDAMENTO`, `CONCLUIDA`, `ARQUIVADA`.

Esses status são de **sessão**, não status STAR — não devem ser
confundidos com `STATUS` da Matriz STAR.

## 5. Item Investigativo

Campos mínimos:

- `item_id`
- `sessao_id`
- `origem`
- `pergunta`
- `status_investigativo`
- `resposta`
- `evidencia_textual`
- `criado_em`
- `atualizado_em`

Status investigativos: `PENDENTE`, `CONFIRMADA`, `DESCARTADA`,
`INCONCLUSIVA`.

## 6. Evidência Investigativa

Campos mínimos:

- `evidencia_id`
- `item_id`
- `tipo_evidencia`
- `descricao`
- `origem`
- `criado_em`

Tipos conceituais: `TEXTO`, `OBSERVACAO`, `DADO_COMERCIAL`,
`ANEXO_FUTURO`, `CRM_FUTURO`, `ERP_FUTURO`.

Não implementar anexos nesta sprint.

## 7. Pacote Investigativo

Campos mínimos:

- `pacote_id`
- `sessao_id`
- `cliente_id`
- `status_star`
- `curva`
- `nivel_prioridade`
- `tipo_prioridade`
- `resumo_hipotese`
- `resumo_investigacao`
- `maturidade_investigacao`
- `leitura_consolidada`
- `criado_em`

## 8. Conclusão Investigativa

Campos mínimos:

- `conclusao_id`
- `pacote_id`
- `sessao_id`
- `status_conclusivo_geral`
- `leitura_conclusao`
- `hipoteses_confirmadas_count`
- `hipoteses_descartadas_count`
- `hipoteses_inconclusivas_count`
- `pendentes_validacao_count`
- `respostas_sem_classificacao_count`
- `criado_em`

Registrado:

- Conclusão Investigativa não é causa raiz.
- Conclusão Investigativa não é plano de ação.
- Conclusão Investigativa organiza estado conclusivo.

## 9. Snapshot STAR

Campos mínimos:

- `snapshot_id`
- `sessao_id`
- `cliente_id`
- `status_star`
- `curva`
- `media_lp`
- `media_cp`
- `meses_sem_compra`
- `erosao_star`
- `meta`
- `acao`
- `criado_em`

Registrado:

- Snapshot STAR preserva o estado da Matriz STAR no momento da
  investigação.
- Snapshot não recalcula regra.
- Snapshot não substitui `star_core`.

## 10. Metadados da Execução

Campos mínimos:

- `execucao_id`
- `sessao_id`
- `arquivo_origem_nome`
- `data_upload`
- `versao_star_os`
- `versao_modelo_persistencia`
- `ambiente`
- `observacoes`

## 11. Relações conceituais

- Um cliente pode ter várias sessões investigativas.
- Uma sessão investigativa pertence a um cliente.
- Uma sessão pode ter vários itens investigativos.
- Uma sessão pode gerar um pacote investigativo.
- Um pacote pode gerar uma conclusão investigativa.
- Uma sessão deve preservar um snapshot STAR.
- Evidências podem estar ligadas a itens investigativos.

## 12. Regras de integridade conceitual

- Não persistir item sem sessão.
- Não persistir sessão sem cliente.
- Não persistir conclusão sem pacote.
- Não persistir snapshot sem sessão.
- Não alterar histórico antigo silenciosamente.
- Preferir nova versão a sobrescrever pacote concluído.
- Separar dados gerados pelo sistema de dados preenchidos pelo usuário.

## 13. Campos fora de escopo nesta sprint

- autenticação;
- permissões;
- multiempresa;
- anexos reais;
- integração CRM;
- integração ERP;
- WhatsApp;
- MCP;
- plano de ação;
- tarefas;
- responsáveis;
- prazos;
- IA;
- score automático de causa raiz.
