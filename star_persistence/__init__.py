"""
star_persistence

Pacote que concentra contratos de dados e futuras capacidades de
persistência do Histórico Investigativo do STAR OS.

Nesta fase (Sprint 7.2), o pacote contém o contrato de dados/serialização
em memória do payload canônico do Histórico Investigativo
(`contrato_historico.py`), o repositório local SQLite
(`repositorio_local.py`), a configuração de caminho do banco
(`configuracao.py`) e o contrato de persistência da Governança
(`contrato_governanca.py`) — este último ainda sem repositório ou
persistência real. Nenhum banco é criado automaticamente neste import —
a criação do schema exige chamada explícita com caminho de banco
informado. Nenhuma integração com Streamlit é feita aqui.
"""
