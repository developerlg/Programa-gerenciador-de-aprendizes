# Sistema de Acompanhamento de Jovens Aprendizes

Aplicação desktop para acompanhamento interno de jovens aprendizes no Windows.

## Escopo da V1.3

- Janela principal com menu lateral fixo.
- Dashboard limpo com contadores reais do banco e áreas de atividades ainda vazias.
- Cadastro de supervisores com nome, função, setor e status.
- Cadastro de aprendizes com nome, CPF, setor, observação e status.
- O cadastro de aprendizes não possui mais vínculo fixo com supervisor.
- Campo CPF com máscara automática no formato `000.000.000-00`.
- Campos de setor e função padronizados por menus suspensos.
- Estrutura inicial da tabela de atividades no SQLite, já preparada com supervisor da atividade.
- Exclusão lógica por inativação.
- Telas futuras como placeholders com a mensagem `Tela em desenvolvimento`.

Não há login, relatórios reais, histórico, avaliações ou registro funcional de atividades nesta versão.

## Como Rodar Pelo Python

1. Abra o PowerShell na pasta do projeto.
2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
python -m pip install --upgrade pip
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

Ao rodar pelo Python, o banco de uso fica em `data\aprendizes.db`.

## Distribuição Windows

O projeto está preparado para PyInstaller usando o modo `onedir`, com janela sem console e nome final `ProgramaAprendizes`.

O executável gerado fica em:

```text
dist\ProgramaAprendizes\ProgramaAprendizes.exe
```

No executável, o banco de uso não fica dentro da pasta interna do PyInstaller. Na primeira abertura, o sistema copia o banco inicial para:

```text
%LOCALAPPDATA%\ProgramaAprendizes\data\aprendizes.db
```

Isso evita erro de permissão quando o programa for colocado em uma pasta protegida do Windows.

## Arquivos Empacotados

- `assets\`: ícones e imagens da interface.
- `assets\icons\app.ico`: ícone do aplicativo e do executável.
- `data\aprendizes_inicial.db`: banco SQLite inicial vazio, usado como modelo.
- `backups\`: pasta reservada para backups futuros.
- `reports\`: pasta reservada para relatórios futuros.
- `config.py`: configurações carregadas como módulo da aplicação.
- Pacotes Python do sistema: `controllers`, `database`, `models`, `services` e `views`.

O arquivo `data\aprendizes.db` é banco de uso local e não deve ser versionado.

## Build Com PyInstaller

Instale as dependências antes do build:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Comando direto completo:

```powershell
pyinstaller --onedir --windowed --name ProgramaAprendizes --icon "assets\icons\app.ico" --add-data "assets;assets" --add-data "data\aprendizes_inicial.db;data" --add-data "backups;backups" --add-data "reports;reports" main.py
```

Também é possível usar a configuração versionada:

```powershell
pyinstaller --clean ProgramaAprendizes.spec
```

Se o Windows não reconhecer o comando `pyinstaller`, use a chamada pelo Python:

```powershell
python -m PyInstaller --clean ProgramaAprendizes.spec
```

Para refazer do zero, apague as pastas antigas antes:

```powershell
Remove-Item -Recurse -Force build, dist
python -m PyInstaller --clean ProgramaAprendizes.spec
```

## Estrutura

- `main.py`: ponto de entrada da aplicação.
- `config.py`: caminhos do projeto, recursos empacotados e pastas de execução.
- `database/`: conexão, migração/criação de tabelas e consultas SQL.
- `models/`: modelos de dados.
- `services/`: regras de validação e fluxo de negócio.
- `controllers/`: ponte entre interface e serviços.
- `views/`: telas e componentes visuais.
- `data/opcoes.py`: listas padronizadas de setores e funções.
- `data/aprendizes_inicial.db`: banco inicial para distribuição.
- `assets/`: ícones e imagens.
- `backups/` e `reports/`: pastas reservadas para versões futuras.

## Checklist De Validação Em Outro Computador

1. Copie a pasta inteira `dist\ProgramaAprendizes` para um computador Windows sem Python instalado.
2. Abra `ProgramaAprendizes.exe`.
3. Confirme que a janela abre sem terminal aparente.
4. Confirme que o ícone aparece na janela ou na barra de tarefas.
5. Cadastre um supervisor e feche o programa.
6. Abra o programa novamente e confirme que o supervisor continua salvo.
7. Cadastre um aprendiz e confirme que aparece na tabela.
8. Confirme que a pasta `%LOCALAPPDATA%\ProgramaAprendizes\data` foi criada.
9. Confirme que `%LOCALAPPDATA%\ProgramaAprendizes\data\aprendizes.db` existe.
10. Mova a pasta `dist\ProgramaAprendizes` para outro local e abra o executável novamente.
11. Teste em uma conta de usuário comum, sem permissões de administrador.
12. Se o Windows Defender bloquear a execução, libere o aplicativo e repita o teste.
