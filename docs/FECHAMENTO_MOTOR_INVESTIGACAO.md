# FECHAMENTO DO MOTOR DE INVESTIGAÇÃO — STAR OS

## 1. Finalidade

O Motor de Investigação existe para transformar hipóteses e perguntas de
validação em uma estrutura investigativa organizada, permitindo registrar
respostas, evidências, status investigativos, pacote consolidado e
conclusão investigativa.

- Não é dashboard paralelo.
- Não substitui a Inteligência de Carteira.
- Não altera a Matriz STAR.
- Não altera o Motor STAR.
- Não usa IA nesta fase.
- Não consome token.
- Não cria agentes.
- Não cria integrações.
- Não cria banco de dados nesta fase.
- Não cria histórico persistente nesta fase.
- Opera como sistema especialista determinístico.
- Atua sobre dados já processados pela Matriz STAR e pela Inteligência de
  Carteira.

## 2. Escopo consolidado da Sprint 4

- Motor de Investigação Operacional (Sprint 4.1).
- Pacote Investigativo do Cliente (Sprint 4.2).
- Conclusão Investigativa (Sprint 4.3).

## 3. Fluxo conceitual consolidado

1. Upload Excel.
2. Motor de Ingestão.
3. Matriz STAR.
4. Inteligência de Carteira.
5. Hipóteses Operacionais.
6. Perguntas de Validação.
7. Investigação Operacional.
8. Pacote Investigativo do Cliente.
9. Conclusão Investigativa.
10. Persistência futura.
11. Governança futura.

## 4. Critérios de sucesso consolidados

- Perguntas de validação viram itens investigativos.
- É possível registrar resposta textual temporária.
- É possível registrar evidência textual temporária.
- É possível classificar status investigativo como PENDENTE, CONFIRMADA,
  DESCARTADA ou INCONCLUSIVA.
- O resumo da investigação é gerado.
- O Pacote Investigativo consolida Raio-X, hipóteses, recomendações, itens,
  respostas, evidências e resumo.
- A Conclusão Investigativa separa hipóteses confirmadas, descartadas,
  inconclusivas, pendentes e respostas sem classificação.
- Nenhuma causa raiz é concluída automaticamente.
- Nenhum plano de ação é criado.
- Nenhuma tarefa é criada.
- Nenhuma automação é criada.
- Nenhum banco de dados é criado.
- PDF e Excel continuam funcionando.
- Nenhuma regra STAR foi alterada.
- Nenhum arquivo `star_core` foi alterado.

## 5. Limites atuais

- Registro é temporário na sessão do Streamlit.
- Ao recarregar a aplicação, respostas podem ser perdidas.
- Ainda não existe persistência.
- Ainda não existe histórico por cliente.
- Ainda não existe versionamento da investigação.
- Ainda não existe governança semanal dentro do sistema.
- Ainda não existe registro formal de ação.
- Ainda não existe acompanhamento de execução.
- Ainda não existe banco de dados.
- Ainda não existe login ou perfil de usuário.
- Ainda não existe IA assistiva.
- Ainda não existem agentes.
- Ainda não existem integrações com CRM, ERP, WhatsApp ou MCP.
- Conclusão investigativa não é causa raiz automática.
- Hipótese confirmada não é plano de ação.
- Recomendação não é execução.

## 6. Condição de avanço

O STAR OS só deve avançar para a próxima fase se:

- A regressão manual continuar passando.
- O Motor STAR permanecer protegido.
- O Motor de Investigação não virar dashboard paralelo.
- A investigação permanecer separada da execução.
- A conclusão investigativa não for tratada como causa raiz automática.
- A persistência futura preservar rastreabilidade.
- A governança futura preservar a separação entre diagnóstico, hipótese,
  evidência, recomendação, ação e acompanhamento.

## 7. Transição — Sprint 5

A Sprint 5 inicia a arquitetura da persistência e histórico investigativo
como evolução natural do Motor de Investigação (ver
`docs/ARQUITETURA_PERSISTENCIA_HISTORICO_INVESTIGATIVO.md`).
