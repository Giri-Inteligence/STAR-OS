# PACOTE INVESTIGATIVO DO CLIENTE — STAR OS

## 1. Finalidade

O Pacote Investigativo consolida, para o cliente selecionado, a leitura
operacional (Raio-X), as hipóteses, as recomendações, os itens
investigativos, as respostas, as evidências e o resumo investigativo — tudo
em um único lugar legível e rastreável.

## 2. O que usa

- Raio-X Operacional.
- Hipóteses Operacionais.
- Recomendações por Papel.
- Itens da Investigação Operacional.
- Respostas textuais.
- Evidências textuais.
- Status investigativos.
- Resumo da investigação.

## 3. O que entrega

- Identificação do cliente.
- Status STAR.
- Prioridade.
- Hipóteses.
- Recomendações já geradas.
- Itens investigativos.
- Contagem por status investigativo.
- Evidências registradas.
- Maturidade investigativa.
- Leitura consolidada não prescritiva.

## 4. O que não faz

- Não usa IA.
- Não consome token.
- Não chama API externa.
- Não altera Motor STAR.
- Não altera cálculo.
- Não altera status.
- Não altera curva.
- Não altera recência.
- Não altera erosão.
- Não cria plano de ação.
- Não cria tarefa.
- Não cria prazo.
- Não salva em banco nesta sprint.
- Não cria histórico persistente nesta sprint.
- Não envia mensagem.
- Não aciona agente.
- Não substitui diagnóstico humano.

## 5. Limites atuais

- Pacote é temporário na sessão.
- Ao recarregar a aplicação, dados podem ser perdidos.
- Não há versionamento do pacote.
- Não há histórico por cliente.
- Não há governança persistente.
- Não há exportação específica do pacote.
- Persistência será tratada em sprint futura.

## 6. Princípio metodológico

- Pacote organiza evidências, não encerra diagnóstico.
- Evidência vem antes de intervenção.
- Maturidade investigativa não é maturidade STAR.
- Recomendação não é execução.
- Investigação prepara governança futura.

## 7. Continuidade — Sprint 4.3

A Sprint 4.3 classifica o estado conclusivo da investigação
(`star_intelligence/conclusao_investigativa.py`) a partir dos itens deste
pacote, sem concluir causa raiz automaticamente e sem criar execução (ver
`docs/CONCLUSAO_INVESTIGATIVA.md`).

## 8. Fechamento — Sprint 4.4

O Pacote Investigativo compõe o Motor de Investigação consolidado na
Sprint 4.4 (ver `docs/FECHAMENTO_MOTOR_INVESTIGACAO.md`).
