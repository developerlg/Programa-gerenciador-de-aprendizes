# Sistema de Acompanhamento de Jovens Aprendizes

Aplicacao desktop para acompanhamento interno de jovens aprendizes.

## Escopo da V1

- Janela principal com menu lateral fixo.
- Dashboard visual com dados ficticios.
- Cadastro de aprendizes com SQLite.
- Exclusao logica por inativacao.
- Telas futuras como placeholders com a mensagem `Tela em desenvolvimento`.

Nao ha login, relatorios reais, historico, avaliacoes ou registro real de atividades nesta versao.

## Como rodar

1. Abra o PowerShell na pasta do projeto.
2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

4. Inicie o sistema:

```powershell
python main.py
```

O banco SQLite sera criado automaticamente em `data/aprendizes.db` na primeira execucao.

## Estrutura

- `main.py`: ponto de entrada da aplicacao.
- `database/`: conexao, criacao de tabelas e consultas SQL.
- `models/`: modelos de dados.
- `services/`: regras de validacao e fluxo de negocio.
- `controllers/`: ponte entre interface e servicos.
- `views/`: telas e componentes visuais.
- `data/dashboard_mock.py`: dados ficticios do dashboard.
- `backups/` e `reports/`: pastas reservadas para versoes futuras.
