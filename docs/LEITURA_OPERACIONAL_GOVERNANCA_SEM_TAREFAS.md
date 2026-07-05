# LEITURA OPERACIONAL DA GOVERNANÇA SEM TAREFAS — STAR OS

## 1. Finalidade

A Sprint 8.4 melhora a leitura operacional dos payloads de governança
sem criar tarefa, agenda, plano de ação, responsável, prazo, CRM,
dashboard, IA ou agente.

## 2. Problema resolvido

Após a Sprint 8.3, a seção "Governança investigativa" estava
tecnicamente correta, mas a leitura dos payloads consultados ainda
poderia exigir esforço cognitivo do usuário. A Sprint 8.4 resolve:

- leitura resumida;
- presença dos tipos de payload;
- status identificados;
- classificação de loop identificada;
- completude de cliente/sessão;
- leitura sintética não prescritiva.

## 3. O que a leitura faz

- Normaliza payloads consultados.
- Aceita payload puro ou linha do repositório (com chave `payload`).
- Conta payloads por tipo.
- Identifica status de acompanhamento.
- Identifica classificação de loop.
- Verifica se o `CICLO_LOOP` tem identidade completa (cliente/sessão).
- Informa se a consulta está completa para cliente/sessão.
- Formata leitura simples para o Streamlit.

## 4. O que a leitura não faz

- Não cria tarefa.
- Não cria plano de ação.
- Não cria agenda.
- Não cria calendário.
- Não cria responsável.
- Não cria prazo.
- Não recomenda ação.
- Não envia mensagem.
- Não executa automação.
- Não usa IA.
- Não aciona agente.
- Não altera o Motor STAR.
- Não altera o PDF.
- Não altera o Excel.
- Não altera banco.
- Não altera schema SQLite.

## 5. Arquitetura

- Regras de leitura ficam em `star_governance/leitura_operacional.py`.
- `app.py` apenas orquestra a exibição.
- `repositorio_governanca.py` continua responsável por listar payloads.
- `contrato_governanca.py` continua responsável por gerar payloads.
- A leitura operacional não depende de Streamlit.
- A leitura operacional não depende de SQLite.
- A leitura operacional não depende de IA.

## 6. Impactos

- **Metodologia:** melhora continuidade investigativa sem criar
  execução.
- **Arquitetura:** adiciona camada determinística de leitura, separada
  de persistência e interface.
- **Complexidade:** pequena elevação controlada em módulo isolado.
- **Manutenção:** testes protegem a leitura contra virar tarefa.
- **Escalabilidade:** prepara leitura futura sem alterar banco.
- **Experiência do usuário:** reduz esforço cognitivo na consulta de
  governança.
- **Governança comercial:** melhora clareza sem transformar
  acompanhamento em tarefa.

## 7. Relação com Sprint 8.5

A Sprint 8.5 deverá fechar a Consolidação Operacional da Governança,
inventariando:

- correção do `CICLO_LOOP`;
- validação estática/visual guiada;
- leitura operacional;
- regressão;
- limites ainda existentes;
- critérios para futuras evoluções de IA/agentes.
