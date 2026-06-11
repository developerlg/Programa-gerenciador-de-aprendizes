# Sistema de Acompanhamento de Jovens Aprendizes

Aplicacao desktop para acompanhamento interno de jovens aprendizes.

## Escopo da V1.1.2

- Janela principal com menu lateral fixo.
- Dashboard limpo com contadores reais do banco e areas de atividades ainda vazias.
- Cadastro de supervisores com nome, funcao e status.
- Cadastro de aprendizes com nome, CPF, setor, observacao e supervisor.
- Atualizacao automatica da lista de supervisores no cadastro de aprendizes.
- Estrutura inicial da tabela de atividades no SQLite.
- Exclusao logica por inativacao.
- Telas futuras como placeholders com a mensagem `Tela em desenvolvimento`.

Nao ha login, relatorios reais, historico, avaliacoes ou registro funcional de atividades nesta versao.

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

Tambem e possivel abrir pelo arquivo:

```powershell
.\Abrir Sistema.bat
```

O banco SQLite sera criado automaticamente em `data/aprendizes.db` na primeira execucao.

## Estrutura

- `main.py`: ponto de entrada da aplicacao.
- `database/`: conexao, migracao/criacao de tabelas e consultas SQL.
- `models/`: modelos de dados.
- `services/`: regras de validacao e fluxo de negocio.
- `controllers/`: ponte entre interface e servicos.
- `views/`: telas e componentes visuais.
- `backups/` e `reports/`: pastas reservadas para versoes futuras.
