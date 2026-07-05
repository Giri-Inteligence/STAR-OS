# DECISÕES ARQUITETURAIS DA INTEGRAÇÃO CONTROLADA DA GOVERNANÇA — STAR OS

## 1. Governança integrada como fase posterior

A integração da governança só deve ocorrer após a consolidação em
memória realizada na Sprint 6.

## 2. Contrato antes de persistência

Nenhuma governança deve ser persistida sem contrato explícito.

## 3. Persistência antes de interface completa

A interface não deve permitir consulta longitudinal real sem uma base
persistida confiável.

## 4. Interface antes de automação

Qualquer automação futura só deve vir depois de interface, regras,
histórico e validação humana.

## 5. Motor STAR protegido

A integração da governança não pode alterar:

- cálculo STAR;
- curva ABC;
- status STAR;
- recência;
- erosão;
- PDF;
- Excel de saída.

## 6. app.py como orquestrador

`app.py` pode futuramente orquestrar interface, mas não deve concentrar
regras de governança, persistência ou transições.

## 7. Risco de dashboard paralelo

- Dashboard exibe indicadores.
- STAR OS organiza diagnóstico, investigação, histórico, governança e
  decisão.

## 8. Risco de CRM paralelo

- CRM registra pipeline, relacionamento e atividades.
- STAR OS registra maturidade, investigação, evidência, conclusão,
  acompanhamento e governança.

## 9. Risco de gestor de tarefas

- Gestor de tarefas controla execução.
- STAR OS, nesta fase, controla raciocínio operacional, continuidade
  investigativa e governança.

## 10. Determinístico antes de IA

- Sprint 7.1 não usa IA.
- Persistência e interface devem nascer determinísticas.
- IA futura pode apoiar leitura, mas não substituir governança.
- Agente futuro deve operar sobre regras, contratos e validação humana.

## 11. Próximas decisões pendentes

- Qual contrato persistirá governança?
- O repositório será novo ou extensão controlada do repositório
  existente?
- Qual será o caminho do banco?
- Governança será exibida no mesmo fluxo do cliente ou em seção própria?
- Haverá consulta por ciclo?
- Haverá comparação entre ciclos?
- Haverá edição?
- Haverá exclusão lógica?
- Haverá trilha de auditoria?
- Haverá usuário responsável?
- Quando agentes poderão operar?

## 12. Continuidade — Sprint 7.2

A Sprint 7.2 preservou a decisão de contrato antes de persistência (ver
`docs/CONTRATO_PERSISTENCIA_GOVERNANCA.md`).
