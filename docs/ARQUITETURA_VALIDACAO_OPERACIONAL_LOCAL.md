# ARQUITETURA DA VALIDAÇÃO OPERACIONAL LOCAL — STAR OS

## 1. Finalidade

A Validação Operacional Local existe para confirmar, em ambiente real de
uso, se a Governança Investigativa está compreensível, estável e
metodologicamente segura antes de qualquer IA, agente, automação ou
integração externa.

- Validação Operacional Local não é dashboard.
- Validação Operacional Local não é CRM.
- Validação Operacional Local não é agenda.
- Validação Operacional Local não é calendário.
- Validação Operacional Local não é tarefa.
- Validação Operacional Local não é plano de ação.
- Validação Operacional Local não é automação.
- Validação Operacional Local não é agente.
- Validação Operacional Local não é IA.
- Validação Operacional Local não substitui julgamento humano.
- Validação Operacional Local não altera o Motor STAR.
- Validação Operacional Local valida experiência, coerência e segurança
  operacional.

## 2. Problema estrutural resolvido

Após a Sprint 8, o STAR OS já possui governança operacionalmente
consolidada em nível técnico, mas ainda falta validar:

- experiência real em navegador;
- clareza da seção Governança Investigativa;
- compreensão do aviso metodológico;
- leitura operacional como interpretação, não como recomendação;
- ausência de indução a tarefa, agenda ou plano de ação;
- comportamento real do salvamento explícito;
- comportamento real da consulta read-only;
- exibição do `CICLO_LOOP` por cliente/sessão;
- estabilidade visual da leitura operacional;
- percepção do usuário sobre banco local;
- riscos de UX antes de avançar para IA/agentes.

## 3. O que já existe parcialmente

- Motor de Ingestão.
- Matriz STAR.
- Inteligência de Carteira.
- Motor de Investigação.
- Histórico Investigativo.
- Governança Inicial.
- Contrato de Persistência da Governança.
- Repositório Local de Governança.
- Configuração Local de Governança.
- Governança no Streamlit.
- Correção de Identificadores do `CICLO_LOOP`.
- Validação Estática da Governança no Streamlit.
- Leitura Operacional da Governança sem Tarefas.
- Roteiro de Validação Visual da Sprint 8.3.

Esses componentes criam base técnica, mas não substituem validação real
de experiência.

## 4. O que precisa ser validado localmente

- Execução real do app Streamlit.
- Upload de planilha válida.
- Geração da Matriz STAR.
- Abertura do Raio-X.
- Geração de investigação.
- Exibição da seção Governança Investigativa.
- Salvamento explícito.
- Consulta read-only.
- Exibição da leitura operacional.
- Presença do `CICLO_LOOP` na consulta filtrada.
- Ausência de campos proibidos.
- Ausência de gráficos/ranking/dashboard.
- Ausência de tarefa/agenda/plano de ação.
- Preservação de PDF e Excel.
- Ausência de alterações no Motor STAR.

## 5. Princípios da validação local

- Validar antes de expandir.
- Observar antes de corrigir.
- Registrar achado antes de alterar.
- Corrigir UX sem criar nova capacidade.
- Preservar `app.py` como orquestrador.
- Preservar regras em módulos especializados.
- Preservar o Motor STAR protegido.
- Preservar a leitura operacional como não prescritiva.
- Não usar IA antes de validação humana.
- Não criar agente antes de estados, permissões e rastreabilidade.

## 6. Classificação dos achados

- **APROVADO** — comportamento adequado e coerente.
- **AJUSTE VISUAL** — problema de clareza, texto, ordem ou apresentação,
  sem falha funcional.
- **RISCO METODOLÓGICO** — elemento que pode induzir tarefa, agenda,
  execução, CRM, dashboard ou recomendação prescritiva.
- **BUG FUNCIONAL** — comportamento que impede fluxo, salva errado,
  consulta errado, exibe dado incorreto ou quebra regressão.
- **BLOQUEIO ARQUITETURAL** — achado que exigiria mudar regra, contrato,
  persistência, governança ou Motor STAR.

## 7. Critérios de bloqueio

A Sprint 9 não deve avançar para IA/agentes se houver:

- usuário interpretando leitura como recomendação;
- usuário interpretando status como tarefa;
- usuário esperando responsável/prazo;
- usuário confundindo consulta com dashboard;
- usuário confundindo governança com CRM;
- `CICLO_LOOP` não aparecendo por cliente/sessão após salvamento;
- salvamento criando comportamento implícito;
- consulta alterando dados;
- banco sendo criado dentro do repositório;
- PDF ou Excel sendo alterados indevidamente;
- qualquer alteração no Motor STAR.

## 8. Lei da Evolução Arquitetural

1. **Qual problema estrutural resolve?** A ausência de confirmação real,
   em navegador, de que a governança consolidada tecnicamente (Sprint 8)
   é de fato compreensível e segura para o usuário final — todo o
   trabalho até aqui foi validado estaticamente (código-fonte), nunca
   visualmente.
2. **Já existe algo que resolve parcialmente?** Sim — o roteiro de
   validação visual da Sprint 8.3 e o teste estático já cobrem a
   estrutura de código; falta apenas a execução real e o registro de
   achados de experiência.
3. **Aumenta ou reduz a complexidade?** Aumenta ligeiramente a
   complexidade de processo (protocolo, modelo de achados), mas reduz o
   risco de acumular problemas de UX não percebidos antes de expandir o
   sistema.
4. **Preserva coerência metodológica?** Sim — a validação apenas observa
   e registra, sem alterar cálculo, contrato ou persistência; qualquer
   correção fica para sprint própria, controlada.
5. **Aproxima ou afasta da visão de longo prazo?** Aproxima — é
   pré-requisito para qualquer evolução futura confiável (IA, agentes,
   integrações), pois confirma que a base atual é sólida antes de
   construir em cima dela.

## 9. O que esta Sprint 9.1 não implementa

- Não executa validação real.
- Não abre Streamlit.
- Não instala pacote.
- Não altera `app.py`.
- Não altera código.
- Não cria banco.
- Não cria tela.
- Não cria botão.
- Não cria tarefa.
- Não cria agenda.
- Não cria plano de ação.
- Não cria IA.
- Não cria agente.
- Não integra CRM.
- Não integra ERP.
- Não integra WhatsApp.
- Não altera Motor STAR.

## 10. Fechamento — Sprint 9.5

A Sprint 9.5 fechou formalmente a Validação Operacional Local (ver
`docs/FECHAMENTO_VALIDACAO_OPERACIONAL_LOCAL.md` e
`docs/GATE_GOVERNANCA_OPERACIONAL_LOCAL_VALIDADA.md`).
