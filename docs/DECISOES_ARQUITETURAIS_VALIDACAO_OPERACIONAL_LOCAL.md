# DECISÕES ARQUITETURAIS DA VALIDAÇÃO OPERACIONAL LOCAL — STAR OS

## 1. Validação real antes de expansão

A experiência local real deve ser validada antes de IA, agentes,
automações ou integrações externas.

## 2. Evidência antes de correção

Achados devem ser registrados antes de qualquer alteração.

## 3. Correção de UX não é nova funcionalidade

Ajustes de texto, ordem e clareza não devem virar novos módulos,
botões, telas ou capacidades.

## 4. Leitura não é recomendação

A leitura operacional deve continuar descritiva e não prescritiva.

## 5. Governança não é execução

Governança não pode virar tarefa, agenda, CRM, dashboard ou plano de
ação automático.

## 6. app.py como orquestrador

`app.py` pode expor fluxo e leitura, mas não deve concentrar regra de
negócio, contrato, persistência, status, loop ou governança.

## 7. Motor STAR protegido

Nenhuma validação local pode alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 8. IA e agentes bloqueados temporariamente

IA e agentes permanecem bloqueados até:

- validação local real registrada;
- achados críticos resolvidos;
- UX estabilizada;
- estados e permissões definidos;
- separação entre recomendação e execução preservada.

## 9. Riscos de avanço prematuro

- Automatizar fluxo ainda não validado.
- Criar agente sobre ambiguidade.
- Usar IA para compensar UX confusa.
- Criar tarefa antes de definir governança.
- Criar CRM paralelo.
- Criar dashboard paralelo.
- Perder rastreabilidade metodológica.

## 10. Próximas decisões pendentes

- Como executar validação visual local com evidência suficiente?
- Quem deve validar: desenvolvedor, consultor, usuário final ou todos?
- Qual planilha padrão será usada?
- Quantos clientes devem ser testados?
- Qual severidade bloqueia avanço?
- Quais ajustes entram na Sprint 9.3?
- Quando IA poderá entrar como apoio de leitura?
- Quando agentes poderão operar sobre contratos validados?

## 11. Fechamento — Sprint 9.5

As decisões acima foram preservadas no fechamento da Sprint 9,
especialmente o bloqueio de IA/agentes sem arquitetura própria (ver
`docs/GATE_GOVERNANCA_OPERACIONAL_LOCAL_VALIDADA.md`).
