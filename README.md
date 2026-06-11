# Sistema de Acompanhamento de Jovens Aprendizes

Aplicação desktop para acompanhamento interno de jovens aprendizes.

## Escopo da V1.1.3

- Janela principal com menu lateral fixo.
- Dashboard limpo com contadores reais do banco e áreas de atividades ainda vazias.
- Cadastro de supervisores com nome, função, setor e status.
- Cadastro de aprendizes com nome, CPF, setor, observação e supervisor.
- Campo CPF com máscara automática no formato `000.000.000-00`.
- Campos de setor e função padronizados por menus suspensos.
- Atualização automática da lista de supervisores no cadastro de aprendizes.
- Estrutura inicial da tabela de atividades no SQLite.
- Exclusão lógica por inativação.
- Telas futuras como placeholders com a mensagem `Tela em desenvolvimento`.

Não há login, relatórios reais, histórico, avaliações ou registro funcional de atividades nesta versão.

## Como rodar

1. Abra o PowerShell na pasta do projeto.
2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

4. Inicie o sistema:

```powershell
python main.py
```

Também é possível abrir pelo arquivo:

```powershell
.\Abrir Sistema.bat
```

O banco SQLite será criado automaticamente em `data/aprendizes.db` na primeira execução.

## Estrutura

- `main.py`: ponto de entrada da aplicação.
- `database/`: conexão, migração/criação de tabelas e consultas SQL.
- `models/`: modelos de dados.
- `services/`: regras de validação e fluxo de negócio.
- `controllers/`: ponte entre interface e serviços.
- `views/`: telas e componentes visuais.
- `data/opcoes.py`: listas padronizadas de setores e funções.
- `backups/` e `reports/`: pastas reservadas para versões futuras.
