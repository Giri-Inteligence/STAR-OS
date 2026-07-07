# MOTOR DE INVESTIGAÇÃO OPERACIONAL — STAR OS

## 1. Finalidade

O Motor de Investigação transforma as perguntas de validação das Hipóteses
Operacionais em itens investigativos estruturados, permitindo registrar
resposta e status para cada uma antes de qualquer recomendação virar ação.

## 2. O que usa

- Cliente selecionado.
- Vendedor.
- Cidade, se disponível.
- Perguntas de validação das Hipóteses Operacionais.
- Status investigativo.
- Resposta textual.
- Evidência textual.

## 3. O que entrega

- Itens investigativos.
- Registro temporário de resposta.
- Classificação de status por item.
- Resumo quantitativo da investigação.
- Leitura investigativa não prescritiva.

## 4. Status investigativos

- **PENDENTE** — ainda não avaliado.
- **CONFIRMADA** — hipótese validada por evidência.
- **DESCARTADA** — hipótese descartada por evidência.
- **INCONCLUSIVA** — não há evidência suficiente para concluir.

## 5. O que não faz

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
- Não envia mensagem.
- Não aciona agente.
- Não salva em banco de dados nesta sprint.
- Não cria histórico persistente nesta sprint.

## 6. Limites atuais

- Registro é temporário na sessão do Streamlit.
- Ao recarregar a aplicação, as respostas podem ser perdidas.
- Persistência será tratada em sprint futura.
- Histórico por cliente será tratado em sprint futura.
- Governança operacional será tratada em sprint futura.

## 7. Princípio metodológico

- Hipótese precisa de validação.
- Validação exige evidência.
- Evidência vem antes da intervenção.
- Investigação não é execução.
- Investigação prepara governança futura.

## 8. Continuidade — Sprint 4.2

A Sprint 4.2 consolida o Pacote Investigativo do Cliente
(`star_intelligence/pacote_investigativo.py`), reunindo Raio-X, hipóteses,
recomendações e itens investigativos deste módulo em um único pacote
legível — ainda como organização temporária e não persistente da
investigação (ver `docs/PACOTE_INVESTIGATIVO_CLIENTE.md`).

## 9. Continuidade — Sprint 4.3

A Sprint 4.3 classifica o estado conclusivo da investigação sem concluir
causa raiz automaticamente e sem criar execução (ver
`docs/CONCLUSAO_INVESTIGATIVA.md`).

## 10. Fechamento — Sprint 4.4

Após a Sprint 4.4, o Motor de Investigação foi consolidado com Investigação
Operacional, Pacote Investigativo e Conclusão Investigativa (ver
`docs/FECHAMENTO_MOTOR_INVESTIGACAO.md`).
