# ROTEIRO DE VALIDAÇÃO VISUAL DA GOVERNANÇA NO STREAMLIT — STAR OS

Roteiro operacional para validação humana futura, quando o Streamlit
estiver disponível no ambiente de execução.

## 1. Preparação

- Abrir a branch correta (`sprint-1-giri-star`).
- Confirmar `git status` limpo.
- Executar o app Streamlit localmente (`streamlit run app.py`).
- Usar uma planilha válida já utilizada nos testes do STAR OS.
- Evitar alterar código durante a validação.

## 2. Fluxo de navegação

- Subir a planilha.
- Validar a Matriz STAR.
- Selecionar um cliente.
- Abrir o Raio-X.
- Confirmar hipóteses/recomendações/investigação/pacote/conclusão.
- Localizar a seção "Governança investigativa".

## 3. Validação da seção

Confirmar:

- título correto;
- aviso metodológico;
- configuração local visível;
- campos permitidos;
- ausência de responsável;
- ausência de prazo;
- ausência de tarefa;
- ausência de plano de ação;
- ausência de agenda;
- ausência de calendário;
- botão explícito de salvamento;
- botão de consulta read-only.

## 4. Validação do salvamento

Confirmar:

- preencher tipo/status/observação/usuário opcional;
- clicar em "Salvar governança desta investigação";
- payloads são validados;
- resultado de salvamento aparece;
- não há tarefa;
- não há plano de ação;
- não há agenda;
- não há execução externa.

## 5. Validação da consulta

Confirmar:

- clicar em "Consultar governança salva deste cliente";
- payloads aparecem;
- `CICLO_LOOP` aparece por cliente/sessão após a Sprint 8.2;
- resumo técnico aparece;
- consulta não altera dados;
- consulta não cria tarefa;
- consulta não cria agenda.

## 6. Validação negativa

Confirmar que não existem:

- responsável;
- prazo;
- data;
- horário;
- calendário;
- tarefa;
- plano de ação;
- agenda;
- gráfico;
- ranking;
- prioridade comercial nova;
- recomendação de ação nova;
- botão de execução;
- envio de mensagem;
- agente;
- IA.

## 7. Validação de artefatos

Confirmar:

- PDF permanece igual.
- Excel permanece igual.
- Motor STAR permanece igual.
- Nenhum banco é criado dentro do repositório.
- Banco local, se criado por salvamento, fica fora do repositório.
- Nenhum JSON funcional é criado dentro do repositório.

## 8. Registro de achados

Registrar achados em quatro categorias:

- **APROVADO**
- **AJUSTE VISUAL**
- **RISCO METODOLÓGICO**
- **BUG FUNCIONAL**

Não corrigir achados dentro da validação.
