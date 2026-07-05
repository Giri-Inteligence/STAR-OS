# DECISÕES ARQUITETURAIS DA PERSISTÊNCIA INVESTIGATIVA — STAR OS

## 1. Persistência como camada própria

- Persistência deve nascer como camada própria.
- Não deve ficar embutida no `app.py`.
- Não deve contaminar `star_core`.
- Não deve contaminar `star_ingestion`.
- Não deve alterar regras da Matriz STAR.

## 2. Snapshot em vez de recálculo

- A persistência deve armazenar o estado investigativo e snapshots.
- Não deve recalcular a Matriz STAR no repositório.
- `star_core` continua sendo fonte de cálculo.
- Histórico deve preservar o que o usuário viu no momento.

## 3. Histórico versionado

- Investigações futuras devem permitir múltiplas sessões por cliente.
- Pacotes concluídos não devem ser sobrescritos silenciosamente.
- Correções futuras devem gerar nova versão ou atualização rastreável.
- A Sprint 5.1 não implementa versionamento, apenas documenta a
  necessidade.

## 4. Identificação do cliente

- Nome do cliente não é identificador suficiente no longo prazo.
- O MVP pode começar com identificador determinístico, mas isso exige
  sprint própria.
- Futuras integrações poderão trazer ID de CRM ou ERP.
- Enquanto não houver ID externo, deve haver cuidado com duplicidade.

## 5. JSON versus SQLite

**JSON local:**
- mais simples;
- melhor para protótipo rápido;
- pior para concorrência e consulta.

**SQLite:**
- mais estruturado;
- melhor para histórico local;
- adequado ao Python padrão;
- exige schema e migração.

A decisão final deve ser tomada na Sprint 5.2 ou 5.3, não nesta sprint.

**Decisão registrada na Sprint 5.3: SQLite**, via módulo padrão `sqlite3`
(ver `docs/REPOSITORIO_LOCAL_HISTORICO_INVESTIGATIVO.md`), por ser
transacional, não exigir pacote novo e reduzir o risco de sobrescrita
silenciosa em relação a um arquivo JSON solto.

## 6. Sem IA na persistência inicial

- Persistência inicial deve ser determinística.
- IA não deve decidir o que salvar.
- IA não deve alterar histórico.
- IA futura pode ajudar a interpretar histórico, mas não substituir
  rastreabilidade.

## 7. Segurança e privacidade

- Histórico investigativo pode conter informações comerciais sensíveis.
- Persistência futura deve considerar diretório seguro.
- Persistência futura deve considerar anonimização ou controle de acesso.
- Persistência futura deve evitar expor dados em logs.
- Login e permissões ficam fora desta sprint.

## 8. Governança futura

- Persistência é base para governança.
- Governança exige histórico confiável.
- Histórico confiável exige separação entre hipótese, evidência,
  recomendação, ação e acompanhamento.
- Registro de ações futuras deve ser sprint própria.

## 9. Continuidade — Sprint 5.2

O payload canônico (`star_persistence/contrato_historico.py`) passa a ser a
fronteira entre o Motor de Investigação e a futura camada de repositório —
sem salvamento nesta sprint.

## 10. Fechamento — Sprint 5.5

A Sprint 5 foi fechada preservando a decisão de SQLite local controlado,
o payload canônico e o salvamento explícito por ação do usuário (ver
`docs/FECHAMENTO_PERSISTENCIA_INICIAL.md`).
