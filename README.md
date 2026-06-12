# Sistema de Acompanhamento de Jovens Aprendizes

Aplicação desktop para acompanhamento interno de jovens aprendizes no Windows.

## Para Usuário Comum

1. Acesse a página de Releases do GitHub.
2. Baixe o arquivo `SistemaAprendizes-v1.3.0-windows.zip`.
3. Extraia o `.zip` em uma pasta do computador, por exemplo `Documentos`.
4. Abra a pasta extraída `SistemaAprendizes`.
5. Execute `SistemaAprendizes.exe`.

Não é necessário instalar Python.

Na primeira abertura, o sistema cria o banco de dados em uma pasta gravável do usuário:

```text
%LOCALAPPDATA%\SistemaAprendizes\data\aprendizes.db
```

Por isso o programa pode ser executado mesmo quando a pasta do aplicativo estiver em um local protegido do Windows.

## Para Desenvolvedor

1. Clone o repositório.
2. Abra o PowerShell na pasta do projeto.
3. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Rode pelo Python:

```powershell
python main.py
```

Ao rodar pelo Python, o banco de uso fica em:

```text
data\aprendizes.db
```

## Build Da Release Windows

O projeto usa PyInstaller em modo `onedir`. A pasta final gerada é:

```text
dist\SistemaAprendizes
```

O executável final fica em:

```text
dist\SistemaAprendizes\SistemaAprendizes.exe
```

Build recomendado pelo arquivo `.spec`:

```powershell
python -m PyInstaller --noconfirm --clean SistemaAprendizes.spec
```

Comando direto equivalente:

```powershell
pyinstaller --onedir --windowed --name SistemaAprendizes --icon "assets\icons\app.ico" --add-data "assets;assets" --add-data "data;data" --add-data "database;database" --add-data "views;views" --add-data "controllers;controllers" --add-data "services;services" --add-data "models;models" --add-data "config.py;." main.py
```

Se o Windows não reconhecer o comando `pyinstaller`, use:

```powershell
python -m PyInstaller --onedir --windowed --name SistemaAprendizes --icon "assets\icons\app.ico" --add-data "assets;assets" --add-data "data;data" --add-data "database;database" --add-data "views;views" --add-data "controllers;controllers" --add-data "services;services" --add-data "models;models" --add-data "config.py;." main.py
```

Para gerar o `.zip` da release:

```powershell
Compress-Archive -Path "dist\SistemaAprendizes" -DestinationPath "dist\SistemaAprendizes-v1.3.0-windows.zip" -Force
```

## Arquivos Incluídos No Pacote

- `assets\`: ícones e imagens da interface.
- `assets\icons\app.ico`: ícone do aplicativo.
- `data\aprendizes_inicial.db`: banco SQLite inicial vazio.
- `data\opcoes.py`: listas padronizadas usadas pela interface.
- `database\`: conexão, criação de tabelas e consultas SQL.
- `views\`: telas e componentes visuais.
- `controllers\`: ponte entre interface e serviços.
- `services\`: regras de validação e fluxo de negócio.
- `models\`: modelos de dados.
- `config.py`: configuração de caminhos, recursos e banco.
- `backups\` e `reports\`: pastas reservadas para versões futuras.

O banco local `data\aprendizes.db` não é empacotado nem versionado.

## Escopo Da V1.3

- Janela principal com menu lateral fixo.
- Dashboard com contadores reais do banco e áreas de atividades ainda vazias.
- Cadastro de supervisores com nome, função, setor e status.
- Cadastro de aprendizes com nome, CPF, setor, observação e status.
- Cadastro de aprendizes sem vínculo fixo com supervisor.
- Campo CPF com máscara automática no formato `000.000.000-00`.
- Campos de setor e função padronizados por menus suspensos.
- Estrutura inicial da tabela de atividades no SQLite.
- Exclusão lógica por inativação.
- Telas futuras como placeholders com a mensagem `Tela em desenvolvimento`.

Não há login, relatórios reais, histórico, avaliações ou registro funcional de atividades nesta versão.

## Checklist De Validação Em Outro Computador

1. Baixar `SistemaAprendizes-v1.3.0-windows.zip` pela release do GitHub.
2. Extrair o `.zip`.
3. Abrir `SistemaAprendizes.exe`.
4. Confirmar que a janela abre sem terminal aparente.
5. Confirmar que o ícone aparece na janela ou na barra de tarefas.
6. Cadastrar um supervisor.
7. Fechar e abrir o programa novamente.
8. Confirmar que o supervisor continua salvo.
9. Cadastrar um aprendiz.
10. Confirmar que `%LOCALAPPDATA%\SistemaAprendizes\data\aprendizes.db` foi criado.
11. Mover a pasta `SistemaAprendizes` para outro local e abrir novamente.
12. Testar em uma conta comum, sem permissões de administrador.
