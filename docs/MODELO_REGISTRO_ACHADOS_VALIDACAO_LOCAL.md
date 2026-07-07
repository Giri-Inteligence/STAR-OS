# MODELO DE REGISTRO DE ACHADOS DA VALIDAÇÃO LOCAL — STAR OS

## 1. Finalidade

Este modelo padroniza o registro de achados da validação operacional
local.

## 2. Campos do registro

- **ID do achado.**
- **Data.**
- **Responsável pela validação.**
- **Branch.**
- **Commit.**
- **Planilha utilizada.**
- **Cliente testado.**
- **Etapa do fluxo.**
- **Categoria do achado.**
- **Descrição objetiva.**
- **Evidência observada.**
- **Impacto metodológico.**
- **Impacto técnico.**
- **Impacto na experiência do usuário.**
- **Severidade.**
- **Reprodutibilidade.**
- **Decisão recomendada.**
- **Sprint sugerida para tratamento.**
- **Observações.**

## 3. Categorias permitidas

- APROVADO.
- AJUSTE VISUAL.
- RISCO METODOLÓGICO.
- BUG FUNCIONAL.
- BLOQUEIO ARQUITETURAL.

## 4. Severidade

- **BAIXA** — não bloqueia uso nem método.
- **MÉDIA** — gera ruído ou ambiguidade, mas não quebra fluxo.
- **ALTA** — compromete interpretação, fluxo ou governança.
- **CRÍTICA** — quebra método, cálculo, persistência, segurança ou
  separação entre governança e execução.

## 5. Decisão recomendada

- Sem ação.
- Documentar apenas.
- Corrigir texto.
- Corrigir UX.
- Corrigir bug funcional.
- Criar sprint corretiva.
- Bloquear avanço para IA/agentes.
- Reavaliar arquitetura.

## 6. Exemplo de registro

Exemplo fictício, ilustrativo (sem dado real do sistema):

- **ID:** ACHADO-EXEMPLO-001
- **Categoria:** AJUSTE VISUAL
- **Descrição:** o texto da seção pode ser interpretado como orientação
  operacional.
- **Decisão:** revisar texto em sprint de UX, sem criar nova
  funcionalidade.

## 7. O que não registrar como achado

Não devem ser tratados como achado:

- preferências estéticas subjetivas sem impacto;
- pedido de nova funcionalidade;
- desejo de CRM;
- desejo de tarefa automática;
- desejo de IA;
- desejo de agente;
- desejo de agenda;
- expectativa comercial fora do escopo metodológico.

## 8. Aplicação — Sprint 9.2

Este modelo foi aplicado na prática pela primeira vez na Sprint 9.2 —
ver `docs/ACHADOS_VALIDACAO_LOCAL_STREAMLIT.md` (4 achados
registrados: ACHADO-9-2-001 a ACHADO-9-2-004).

## 9. Fechamento — Sprint 9.5

O modelo de achados foi utilizado ao longo da Sprint 9 e consolidado no
fechamento (ver `docs/FECHAMENTO_VALIDACAO_OPERACIONAL_LOCAL.md`).
