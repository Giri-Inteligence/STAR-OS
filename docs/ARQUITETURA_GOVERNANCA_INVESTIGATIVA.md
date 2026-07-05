# ARQUITETURA DA GOVERNANÇA INVESTIGATIVA — STAR OS

## 1. Finalidade

A Governança Investigativa existe para transformar histórico
investigativo em acompanhamento estruturado, sem transformar
recomendação em execução automática.

- Governança Investigativa não é dashboard.
- Governança Investigativa não é Motor STAR.
- Governança Investigativa não recalcula Matriz STAR.
- Governança Investigativa não cria ação automática.
- Governança Investigativa não cria tarefa automática.
- Governança Investigativa não envia mensagem.
- Governança Investigativa não aciona agente.
- Governança Investigativa não substitui julgamento humano.
- Governança Investigativa organiza acompanhamento, pendências, retorno
  e evolução da investigação.

## 2. Problema estrutural resolvido

Após a Sprint 5, o STAR OS já consegue salvar histórico investigativo,
mas ainda não possui uma camada para acompanhar a evolução das
investigações ao longo do tempo. Problemas atuais:

- histórico existe, mas ainda não há loop operacional;
- conclusões investigativas não possuem acompanhamento estruturado;
- hipóteses inconclusivas podem ficar paradas;
- pendências não possuem ciclo de retorno;
- evidências podem ser registradas, mas ainda não há governança semanal;
- recomendações ainda não possuem acompanhamento formal;
- não há registro conceitual de decisão operacional;
- não há separação formal entre acompanhamento e execução.

## 3. O que já existe parcialmente

- Matriz STAR.
- Inteligência de Carteira.
- Hipóteses Operacionais.
- Investigação Operacional.
- Pacote Investigativo.
- Conclusão Investigativa.
- Histórico Investigativo.
- Repositório Local.
- Checklist de Regressão Manual.

Esses componentes criam base analítica e histórica, mas ainda não criam
governança operacional — não há acompanhamento ao longo do tempo, apenas
um registro pontual de cada sessão investigativa.

## 4. Impacto de complexidade

Governança Investigativa aumenta complexidade porque introduz:

- ciclo de acompanhamento;
- estado de acompanhamento;
- decisões registradas;
- retorno periódico;
- histórico de evolução;
- separação entre decisão e execução;
- risco de virar gestor de tarefas;
- risco de virar CRM paralelo;
- risco de virar dashboard paralelo.

Por outro lado, reduz complexidade operacional para o usuário porque:

- reduz esquecimento;
- reduz retrabalho;
- aumenta rastreabilidade;
- melhora continuidade da consultoria;
- melhora disciplina de acompanhamento;
- transforma investigação em rotina.

## 5. Coerência metodológica

Governança Investigativa é coerente com o Método STAR porque:

- preserva a sequência evidência → hipótese → validação → conclusão →
  acompanhamento;
- impede que recomendação vire execução automática;
- preserva julgamento humano;
- reforça disciplina comercial;
- conecta diagnóstico a rotina;
- fortalece governança sem alterar cálculo STAR.

## 6. Visão de longo prazo

Governança Investigativa aproxima o STAR OS da visão de longo prazo
porque cria base para:

- acompanhamento semanal de carteira;
- evolução longitudinal por cliente;
- gestão de pendências investigativas;
- aprendizado operacional;
- futuras recomendações assistidas;
- agentes futuros;
- integrações futuras com CRM, ERP, WhatsApp e MCP;
- inteligência longitudinal da carteira.

## 7. Lei da Evolução Arquitetural

1. **Qual problema estrutural resolve?** A ausência de um ciclo de
   acompanhamento sobre o histórico investigativo já salvo — hoje o
   histórico é gravado, mas nada garante que uma hipótese pendente ou uma
   conclusão inconclusiva seja revisitada.
2. **Já existe algo que resolve parcialmente?** Sim — a Conclusão
   Investigativa já classifica o estado de cada hipótese, e o Histórico
   Investigativo já preserva sessões passadas; falta apenas a camada que
   conecta essas sessões ao longo do tempo e sinaliza o que precisa de
   retorno.
3. **Aumenta ou reduz a complexidade?** Aumenta a complexidade estrutural
   do sistema (novos conceitos de estado e acompanhamento), mas reduz a
   complexidade operacional do usuário (menos retrabalho e esquecimento).
4. **Preserva coerência metodológica?** Sim — mantém a sequência
   evidência → hipótese → validação → conclusão → acompanhamento sem
   pular etapas nem automatizar decisão.
5. **Aproxima ou afasta da visão de longo prazo?** Aproxima — é
   pré-requisito conceitual para governança de carteira, aprendizado
   operacional e futura assistência por agentes.

## 8. Princípios arquiteturais

- Governança deve ser camada própria.
- Governança não deve contaminar `star_core`.
- Governança não deve recalcular Matriz STAR.
- Governança deve consumir histórico e pacotes já existentes.
- Governança não deve criar execução automática.
- Governança deve preservar rastreabilidade.
- Governança deve diferenciar acompanhamento de ação.
- Governança deve ser testável sem Streamlit.
- Governança deve permitir integração futura com agentes, mas não
  depender deles.
- Governança deve evoluir por integração, não por acumulação paralela.

## 9. O que esta Sprint 6.1 não implementa

- Não cria código.
- Não altera `app.py`.
- Não cria banco.
- Não cria tabela.
- Não cria tarefa.
- Não cria plano de ação.
- Não cria automação.
- Não usa IA.
- Não cria agente.
- Não integra CRM.
- Não integra ERP.
- Não integra WhatsApp.
- Não altera Motor STAR.

## 10. Continuidade — Sprint 6.2

A Sprint 6.2 criou o contrato de Registro de Acompanhamento Operacional
em memória (`star_governance/acompanhamento.py`), ainda sem persistência
e sem integração com o Streamlit (ver
`docs/REGISTRO_ACOMPANHAMENTO_OPERACIONAL.md`).

## 11. Continuidade — Sprint 6.3

A Sprint 6.3 consolidou o status determinístico de acompanhamento
(`star_governance/status_acompanhamento.py`), mantendo a governança
separada de execução (ver `docs/STATUS_ACOMPANHAMENTO_INVESTIGACAO.md`).
