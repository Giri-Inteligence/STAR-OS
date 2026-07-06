# PROTOCOLO DE VALIDAÇÃO LOCAL NO STREAMLIT — STAR OS

## 1. Finalidade

Este protocolo orienta a execução local real da validação da seção
"Governança investigativa" no Streamlit.

## 2. Pré-condições

- Branch correta: `sprint-1-giri-star`.
- `git status` limpo.
- Último commit sincronizado com `origin`.
- Ambiente Python funcional.
- Streamlit instalado localmente, se já fizer parte do ambiente do
  desenvolvedor.
- Não instalar pacote durante a validação sem decisão explícita.
- Planilha válida disponível.
- Nenhuma alteração de código durante a validação.

## 3. Comandos preparatórios

```
git status
git branch --show-current

python -m py_compile app.py star_ingestion/*.py star_intelligence/*.py star_persistence/*.py star_governance/*.py tests/manual/*.py

python tests/manual/testar_leitura_operacional_governanca.py
python tests/manual/testar_validacao_estatica_governanca_streamlit.py
```

## 4. Execução local

Comando esperado:

```
streamlit run app.py
```

Se o Streamlit não estiver instalado localmente, isso deve ser
registrado como impedimento operacional — não instalar automaticamente
dentro desta validação.

## 5. Fluxo de validação

1. Abrir a aplicação.
2. Subir planilha válida.
3. Confirmar a Matriz STAR.
4. Selecionar um cliente.
5. Abrir o Raio-X.
6. Gerar investigação.
7. Confirmar pacote/conclusão.
8. Localizar a seção "Governança investigativa".
9. Preencher tipo/status/observação/usuário (opcional).
10. Salvar a governança.
11. Consultar a governança salva.
12. Verificar a leitura operacional.
13. Verificar o `CICLO_LOOP` por cliente/sessão.
14. Verificar ausência de tarefa/agenda/plano de ação.
15. Verificar PDF/Excel inalterados.

## 6. Evidências mínimas

A validação deve coletar:

- data da validação;
- branch;
- commit;
- planilha usada;
- cliente testado;
- prints ou descrição objetiva das telas;
- resultado do salvamento;
- resultado da consulta;
- se o `CICLO_LOOP` apareceu;
- se a leitura operacional apareceu;
- achados classificados.

## 7. Critérios de aprovação

- Fluxo executado sem erro.
- Seção localizada.
- Salvamento explícito funciona.
- Consulta read-only funciona.
- Leitura operacional aparece.
- `CICLO_LOOP` aparece quando esperado.
- Nenhum campo proibido aparece.
- Nenhuma tarefa/agenda/plano aparece.
- PDF/Excel permanecem inalterados.
- Testes continuam passando.

## 8. Critérios de reprovação

- Erro de execução.
- Seção não aparece.
- Salvamento falha.
- Consulta falha.
- Leitura operacional não aparece.
- `CICLO_LOOP` não aparece após salvamento.
- Campo de responsável/prazo/tarefa/agenda aparece.
- Usuário é induzido a execução.
- PDF/Excel mudam indevidamente.
- Banco é criado dentro do repositório.

## 9. Encerramento da validação

- Não corrigir durante a validação.
- Registrar achados.
- Classificar achados.
- Decidir se a próxima sprint é correção de UX, correção funcional ou
  estabilização.
