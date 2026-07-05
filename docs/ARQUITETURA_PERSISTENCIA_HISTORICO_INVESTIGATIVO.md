# ARQUITETURA DE PERSISTÊNCIA E HISTÓRICO INVESTIGATIVO — STAR OS

## 1. Finalidade

A persistência existe para transformar registros temporários de
investigação em histórico rastreável por cliente.

- Persistência não é dashboard.
- Persistência não é recomendação.
- Persistência não é plano de ação.
- Persistência não é execução automática.
- Persistência não altera o Motor STAR.
- Persistência não recalcula Matriz STAR.
- Persistência deve preservar evidência, contexto e versionamento.
- Persistência deve permitir governança futura.
- Persistência deve preservar separação entre diagnóstico, hipótese,
  evidência, recomendação, ação e acompanhamento.

## 2. Problema estrutural resolvido

Hoje o STAR OS já consegue investigar, consolidar e classificar, mas os
dados permanecem temporários em `st.session_state`. Problemas atuais:

- perda de respostas ao recarregar;
- ausência de histórico por cliente;
- ausência de versionamento;
- impossibilidade de comparar investigações ao longo do tempo;
- impossibilidade de gerar governança semanal real;
- impossibilidade de auditar decisões passadas;
- dependência da memória do usuário.

## 3. O que já existe parcialmente

- Investigação Operacional.
- Pacote Investigativo do Cliente.
- Conclusão Investigativa.
- `docs/CHECKLIST_REGRESSAO_MANUAL.md`.
- Documentação da Sprint 4.

Esses componentes geram estrutura lógica determinística, mas ainda não
persistem dados — todo o estado desaparece ao recarregar a aplicação.

## 4. Impacto de complexidade

Persistência aumenta complexidade porque introduz:

- modelo de dados;
- versionamento;
- integridade;
- identificação única de cliente;
- risco de duplicidade;
- privacidade;
- migração futura;
- compatibilidade com Streamlit;
- futura autenticação;
- futura governança multiusuário.

Por outro lado, reduz complexidade operacional para o usuário porque
preserva histórico e reduz retrabalho.

## 5. Coerência metodológica

Persistência é coerente com o Método STAR porque permite:

- preservar hipóteses;
- registrar evidências;
- acompanhar evolução investigativa;
- diferenciar hipótese de conclusão;
- diferenciar recomendação de execução;
- preparar governança comercial.

## 6. Visão de longo prazo

Persistência aproxima o STAR OS da visão de longo prazo porque cria a base
para:

- histórico por cliente;
- governança de carteira;
- acompanhamento semanal;
- aprendizado operacional;
- agentes futuros;
- integrações futuras;
- IA assistiva futura;
- inteligência longitudinal de carteira.

## 7. Princípios arquiteturais

- Persistência deve ser camada própria.
- Persistência não deve ficar misturada ao `app.py`.
- Persistência não deve alterar `star_core`.
- Persistência não deve alterar `star_ingestion`.
- Persistência não deve alterar `star_intelligence` sem necessidade.
- Persistência deve consumir pacotes já gerados.
- Persistência deve armazenar snapshots, não recalcular regras.
- Persistência deve permitir versionamento.
- Persistência deve ser reversível no início.
- Persistência deve ser testável sem Streamlit.

## 8. Alternativas técnicas avaliadas

### A. JSON local

**Benefícios:**
- simples;
- sem pacote novo;
- fácil de inspecionar;
- adequado para MVP local;
- baixo custo de implementação.

**Limitações:**
- pouca robustez concorrencial;
- risco de sobrescrita;
- não ideal para multiusuário;
- exige cuidado com diretórios no Streamlit.

### B. SQLite

**Benefícios:**
- mais estruturado;
- transacional;
- bom para MVP avançado;
- já disponível no Python padrão;
- permite consultas futuras.

**Limitações:**
- exige schema;
- exige camada de repositório;
- exige migração futura;
- aumenta complexidade inicial.

### C. Banco externo futuro

Exemplos conceituais: PostgreSQL, Supabase, banco relacional gerenciado.

**Benefícios:**
- preparado para multiusuário;
- escalável;
- adequado para produto SaaS.

**Limitações:**
- aumenta dependência externa;
- exige autenticação;
- exige segurança;
- exige governança de acesso.

## 9. Recomendação arquitetural inicial

Abordagem em fases:

- **Fase 5.1** — documentação e modelo canônico.
- **Fase 5.2** — contrato de dados e serialização determinística, ainda sem
  `app.py`.
- **Fase 5.3** — persistência local controlada, preferencialmente JSON ou
  SQLite após decisão explícita.
- **Fase 5.4** — histórico investigativo no Streamlit.
- **Fase 5.5** — fechamento da persistência inicial.

A decisão entre JSON local e SQLite deve ser feita apenas após o modelo
canônico estar documentado (ver `docs/DECISOES_ARQUITETURAIS_PERSISTENCIA_INVESTIGATIVA.md`).

## 10. O que esta Sprint 5.1 não implementa

- Não salva dados.
- Não cria banco.
- Não cria arquivo persistente.
- Não altera `app.py`.
- Não cria histórico funcional.
- Não cria login.
- Não cria multiusuário.
- Não cria plano de ação.
- Não cria automação.
- Não usa IA.

## 11. Continuidade — Sprint 5.2

A Sprint 5.2 criou o contrato de dados e a serialização em memória
(`star_persistence/contrato_historico.py`), ainda sem persistência
funcional (ver `docs/CONTRATO_DADOS_HISTORICO_INVESTIGATIVO.md`).
