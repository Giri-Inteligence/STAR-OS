# DECISÕES ARQUITETURAIS DA CONSOLIDAÇÃO OPERACIONAL DA GOVERNANÇA — STAR OS

## 1. Consolidação antes de expansão

A Governança Integrada deve ser consolidada antes de qualquer expansão
para IA, agentes, tarefas, agenda ou integrações externas.

## 2. Identidade antes de leitura operacional

A consistência de identificadores deve ser corrigida antes de melhorias
de leitura operacional.

## 3. Correção controlada antes de validação visual ampla

A limitação do `CICLO_LOOP` deve ser tratada em sprint própria antes da
validação visual ampla.

## 4. Validação visual antes de novas funcionalidades

A experiência real deve ser validada antes de criar novas capacidades.

## 5. Leitura operacional não é tarefa

Qualquer melhoria de leitura deve continuar separada de tarefa,
responsável, prazo e agenda.

## 6. app.py como orquestrador

`app.py` pode expor e organizar a experiência, mas não deve concentrar
regras de contrato, repositório, status, loop ou governança.

## 7. Motor STAR protegido

A consolidação operacional não pode alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 8. Determinístico antes de IA

- Sprint 8.1 não usa IA.
- Sprint 8 não deve começar por IA.
- IA futura pode apoiar leitura, mas não substituir governança.
- Agente futuro deve operar apenas sobre contratos, estados e validação
  humana.

## 9. Risco de expansão prematura

- Criar dashboard paralelo.
- Criar CRM paralelo.
- Criar tarefa.
- Criar agenda.
- Criar automação invisível.
- Criar agente sem rastreabilidade.
- Usar IA para substituir decisão humana.
- Misturar recomendação com execução.

## 10. Próximas decisões pendentes

- Como corrigir o `CICLO_LOOP` sem quebrar compatibilidade?
- A correção exigirá migração de payloads antigos?
- A consulta deve priorizar `cliente_id` ou `sessao_id`?
- Como validar visualmente sem Streamlit instalado no ambiente de
  desenvolvimento?
- Quais critérios mínimos de aceitação visual?
- Que melhorias de leitura são permitidas sem criar tarefa?
- Quando IA poderá apoiar leitura?
- Quando agentes poderão operar?
