# MODELO CONCEITUAL DA GOVERNANÇA INTEGRADA — STAR OS

## 1. Finalidade

O Modelo Conceitual da Governança Integrada define como a governança em
memória (Sprint 6) poderá evoluir para persistência e interface sem
perder coerência metodológica.

## 2. Fluxo conceitual da governança integrada

1. Matriz STAR.
2. Inteligência de Carteira.
3. Motor de Investigação.
4. Histórico Investigativo.
5. Registro de Acompanhamento Operacional.
6. Status de Acompanhamento.
7. Loop Semanal de Governança.
8. Contrato de Governança Integrada.
9. Persistência Controlada da Governança.
10. Consulta de Governança.
11. Exposição Controlada no Streamlit.
12. Integrações futuras.

## 3. Separação entre camadas

- **Camada STAR Core** — calcula regras, status, curva, recência e
  erosão.
- **Camada de Ingestão** — saneia, normaliza e valida a base.
- **Camada de Inteligência** — interpreta carteira e estrutura
  investigação.
- **Camada de Persistência Investigativa** — salva histórico
  investigativo.
- **Camada de Governança** — organiza acompanhamento, status e loop.
- **Camada de Integração Controlada** — decide como persistir e expor
  governança.
- **Camada de Experiência** — apresenta informação ao usuário sem
  transformar em dashboard paralelo.
- **Camada futura de Agentes** — poderá executar apenas quando houver
  governança, rastreabilidade e validação humana.

## 4. Entidades conceituais futuras

### Contrato de Persistência da Governança
- **Finalidade:** transformar registro, status e ciclo de governança em
  payload canônico serializável, análogo ao contrato da Sprint 5.2.
- **Entrada esperada:** registro de acompanhamento, snapshot de status e
  item/ciclo de loop já criados em memória.
- **Saída esperada:** payload determinístico, seguro para `json.dumps`.
- **O que não deve fazer:** não deve salvar em disco, não deve
  recalcular nada.

### Sessão de Governança
- **Finalidade:** agrupar conceitualmente os registros de governança
  associados a uma sessão investigativa.
- **Entrada esperada:** sessão histórica já existente (Sprint 5).
- **Saída esperada:** referência estável entre governança e histórico.
- **O que não deve fazer:** não deve duplicar dados do histórico
  investigativo.

### Registro Persistido de Acompanhamento
- **Finalidade:** versão persistida do Registro de Acompanhamento
  Operacional (Sprint 6.2).
- **Entrada esperada:** registro em memória já validado.
- **Saída esperada:** linha persistida com referência à sessão.
- **O que não deve fazer:** não deve sobrescrever silenciosamente.

### Snapshot Persistido de Status
- **Finalidade:** versão persistida do snapshot de status (Sprint 6.3).
- **Entrada esperada:** snapshot em memória já validado.
- **Saída esperada:** registro persistido consultável por sessão.
- **O que não deve fazer:** não deve recalcular status.

### Ciclo Persistido de Governança
- **Finalidade:** versão persistida do ciclo de loop semanal (Sprint
  6.4).
- **Entrada esperada:** ciclo em memória já validado.
- **Saída esperada:** registro persistido consultável por período.
- **O que não deve fazer:** não deve gerar tarefa ou agenda.

### Consulta Histórica de Governança
- **Finalidade:** permitir consultar ciclos e registros de governança
  já persistidos.
- **Entrada esperada:** identificador de cliente, sessão ou período.
- **Saída esperada:** lista ou registro único, somente leitura.
- **O que não deve fazer:** não deve alterar dados consultados.

### Leitura Comparativa de Ciclos
- **Finalidade:** comparar o estado de governança entre dois ou mais
  ciclos do mesmo cliente.
- **Entrada esperada:** dois ou mais ciclos persistidos.
- **Saída esperada:** leitura textual comparativa, não prescritiva.
- **O que não deve fazer:** não deve recomendar ação.

### Evento de Decisão Humana
- **Finalidade:** registrar formalmente que uma decisão operacional foi
  tomada por uma pessoa.
- **Entrada esperada:** decisão textual e identificação de quem
  decidiu.
- **Saída esperada:** registro imutável vinculado ao ciclo/sessão.
- **O que não deve fazer:** não deve ser gerado automaticamente.

### Trilha de Auditoria de Governança
- **Finalidade:** preservar histórico de alterações e decisões da
  governança ao longo do tempo.
- **Entrada esperada:** eventos de criação, atualização e decisão já
  registrados.
- **Saída esperada:** sequência cronológica consultável.
- **O que não deve fazer:** não deve permitir remoção silenciosa de
  eventos passados.

## 5. Regras de separação

- Governança não recalcula STAR.
- Governança não altera histórico investigativo original.
- Governança não cria ação automática.
- Governança não cria tarefa automática.
- Governança não define responsável automático.
- Governança não cria prazo automático.
- Governança não envia mensagem.
- Governança não substitui decisão humana.
- Governança não aciona agente sem camada futura própria.

## 6. Integração com Streamlit

A futura integração no Streamlit deve:

- ser discreta;
- estar próxima do Histórico Investigativo ou da área de Governança;
- não criar página paralela inicialmente;
- não transformar loop em dashboard;
- não expor ordenação técnica como prioridade comercial;
- não permitir edição destrutiva sem regra futura;
- não salvar automaticamente;
- exigir ação explícita do usuário se houver persistência;
- deixar claro que loop não é tarefa.

## 7. Integração com persistência

Persistência futura deve:

- ter contrato próprio;
- ser serializável;
- ser testável sem Streamlit;
- ser compatível com SQLite local controlado;
- evitar duplicação do histórico investigativo;
- preservar referência à sessão histórica;
- separar registro, status e ciclo;
- bloquear sobrescrita silenciosa;
- registrar origem e timestamps.

## 8. Integração com agentes futuros

Agentes futuros:

- não devem decidir sozinhos;
- não devem criar tarefa sem validação;
- não devem enviar mensagem sem autorização;
- não devem alterar histórico sem rastreabilidade;
- não devem transformar loop em automação invisível;
- devem operar sobre contratos e estados já definidos;
- devem ser fase posterior, não requisito da Sprint 7.

## 9. Limites atuais

- Sprint 7.1 não cria código.
- Sprint 7.1 não cria persistência.
- Sprint 7.1 não cria interface.
- Sprint 7.1 não cria agente.
- Sprint 7.1 não cria IA.
- Sprint 7.1 não cria tarefa.
- Sprint 7.1 não cria plano de ação.
