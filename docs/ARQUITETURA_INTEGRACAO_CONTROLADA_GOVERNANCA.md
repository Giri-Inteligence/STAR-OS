# ARQUITETURA DA INTEGRAÇÃO CONTROLADA DA GOVERNANÇA — STAR OS

## 1. Finalidade

A Integração Controlada da Governança existe para decidir como expor
e/ou persistir a Governança Inicial (Sprint 6) sem transformar o STAR OS
em dashboard, CRM paralelo, agenda, gestor de tarefas ou sistema de
execução automática.

- Integração Controlada não é dashboard.
- Integração Controlada não é CRM.
- Integração Controlada não é agenda.
- Integração Controlada não é gestor de tarefas.
- Integração Controlada não é automação.
- Integração Controlada não é agente.
- Integração Controlada não é IA.
- Integração Controlada não substitui julgamento humano.
- Integração Controlada organiza a passagem da governança em memória
  para uso controlado.

## 2. Problema estrutural resolvido

Após a Sprint 6, o STAR OS já possui Governança Inicial em memória, mas
ainda não possui uma forma controlada de:

- expor a governança na experiência do usuário;
- persistir registros de governança;
- recuperar ciclos anteriores;
- manter continuidade entre sessões;
- auditar decisões operacionais;
- evitar perda de acompanhamento;
- conectar histórico investigativo com governança sem misturar cálculo
  e execução.

## 3. O que já existe parcialmente

- Matriz STAR.
- Inteligência de Carteira.
- Motor de Investigação.
- Histórico Investigativo.
- Repositório Local da Persistência Inicial.
- Registro de Acompanhamento Operacional.
- Status de Acompanhamento da Investigação.
- Loop Semanal de Governança.
- Checklist de Regressão Manual.

Esses componentes criam base analítica, histórica e governável, mas
ainda não definem exposição ou persistência controlada da governança.

## 4. Riscos arquiteturais da integração

- Virar dashboard paralelo.
- Virar CRM paralelo.
- Virar lista de tarefas.
- Virar agenda.
- Criar expectativa de execução automática.
- Misturar recomendação com ação.
- Misturar acompanhamento com responsabilidade.
- Misturar decisão humana com decisão do sistema.
- Contaminar `star_core`.
- Duplicar persistência.
- Criar acoplamento excessivo no `app.py`.
- Persistir dados antes de definir contrato.
- Expor governança sem regra clara de leitura.

## 5. Princípios de integração

- Evoluir por integração, não por acumulação paralela.
- Reutilizar `star_governance`.
- Reutilizar `star_persistence` somente quando houver contrato de
  persistência.
- Manter `star_core` protegido.
- Manter `star_intelligence` separado de governança.
- Manter `app.py` como orquestrador, não como motor de regra.
- Persistir somente depois de contrato explícito.
- Expor no Streamlit somente depois de decidir experiência e limites.
- Não criar tarefa automática.
- Não criar plano de ação automático.
- Não criar agenda automática.
- Não criar agente antes da governança estar madura.
- Não usar IA antes de regras determinísticas suficientes.

## 6. Alternativas arquiteturais avaliadas

### Alternativa A — apenas exibir governança no Streamlit, sem persistir

**Benefícios:**
- menor complexidade;
- valida experiência rapidamente;
- evita novo schema.

**Limitações:**
- perde continuidade;
- não cria histórico de governança;
- depende da sessão atual.

**Riscos:**
- usuário interpretar como painel temporário;
- baixa utilidade longitudinal.

### Alternativa B — persistir governança antes de expor

**Benefícios:**
- cria rastreabilidade;
- fortalece histórico;
- prepara consulta longitudinal.

**Limitações:**
- exige contrato de dados;
- exige repositório;
- aumenta complexidade.

**Riscos:**
- persistir estrutura imatura;
- criar acoplamento prematuro.

### Alternativa C — integrar governança ao Histórico Investigativo existente

**Benefícios:**
- reaproveita infraestrutura da Sprint 5;
- reduz criação de componentes paralelos;
- mantém proximidade com sessão histórica.

**Limitações:**
- risco de misturar histórico investigativo com governança evolutiva;
- exige separação conceitual clara.

**Riscos:**
- schema ficar confuso;
- payload histórico virar depósito genérico.

### Alternativa D — criar camada própria de persistência de governança

**Benefícios:**
- separação clara;
- melhor evolução futura;
- menor risco de contaminar histórico investigativo.

**Limitações:**
- aumenta componentes;
- exige contrato e repositório próprios.

**Riscos:**
- complexidade adicional;
- risco de duplicação se não reutilizar padrões da Sprint 5.

## 7. Direção recomendada

Abordagem em sequência:

1. **Sprint 7.1** — Arquitetura da Integração Controlada da Governança.
2. **Sprint 7.2** — Contrato de Persistência da Governança.
3. **Sprint 7.3** — Repositório Local de Governança.
4. **Sprint 7.4** — Governança no Streamlit.
5. **Sprint 7.5** — Fechamento da Governança Integrada.

Justificativa: primeiro contrato, depois persistência, depois interface,
por fim fechamento e regressão — a mesma sequência que já funcionou na
Sprint 5 (contrato → repositório → Streamlit → fechamento).

## 8. Lei da Evolução Arquitetural

1. **Qual problema estrutural resolve?** A ausência de uma forma
   controlada de expor e/ou persistir a governança já organizada em
   memória pela Sprint 6 — sem essa camada, a governança se perde a cada
   reinício da aplicação.
2. **Já existe algo que resolve parcialmente?** Sim — o Repositório
   Local da Persistência Inicial (Sprint 5.3) já resolve o problema
   análogo para o histórico investigativo, e pode servir de padrão
   técnico a ser avaliado (não necessariamente reutilizado diretamente)
   para a governança.
3. **Aumenta ou reduz a complexidade?** Aumenta a complexidade estrutural
   (novo contrato, possível novo repositório, nova área de interface),
   mas reduz a complexidade operacional do usuário ao preservar
   continuidade de acompanhamento entre sessões.
4. **Preserva coerência metodológica?** Sim, desde que a sequência
   contrato → persistência → interface → fechamento seja respeitada e
   nenhuma automação seja introduzida antes da governança determinística
   estar madura.
5. **Aproxima ou afasta da visão de longo prazo?** Aproxima — é
   pré-requisito para consulta longitudinal de carteira, auditoria de
   decisões e eventual assistência por agentes futuros.

## 9. O que esta Sprint 7.1 não implementa

- Não cria código.
- Não altera `app.py`.
- Não altera `star_governance`.
- Não cria banco.
- Não cria tabela.
- Não cria schema.
- Não cria persistência.
- Não cria Streamlit.
- Não cria tarefa.
- Não cria plano de ação.
- Não cria agenda.
- Não usa IA.
- Não cria agente.
- Não integra CRM.
- Não integra ERP.
- Não integra WhatsApp.
- Não altera Motor STAR.

## 10. Continuidade — Sprint 7.2

A Sprint 7.2 criou o contrato de persistência da governança
(`star_persistence/contrato_governanca.py`), mantendo contrato antes de
banco, repositório e interface (ver
`docs/CONTRATO_PERSISTENCIA_GOVERNANCA.md`).

## 11. Continuidade — Sprint 7.3

A Sprint 7.3 materializou a etapa de persistência local controlada antes
da interface (`star_persistence/repositorio_governanca.py`, ver
`docs/REPOSITORIO_LOCAL_GOVERNANCA.md`).
