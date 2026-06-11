# Relatorio da Versao 1.1.2

## Objetivo

Corrigir o cadastro de jovens aprendizes para que o campo Supervisor mostre os supervisores cadastrados no banco de dados.

## Problema Encontrado

A tela de cadastro de aprendizes carregava a lista de supervisores apenas quando o programa era aberto. Se um supervisor fosse cadastrado depois, a tela de aprendizes continuava com a lista antiga ate o sistema ser reiniciado ou ate o botao Atualizar ser usado.

## Correcao Aplicada

- O sistema agora atualiza a tela ativa sempre que uma opcao do menu lateral e aberta.
- A tela de Cadastro de Aprendizes recarrega os supervisores ativos do SQLite ao ser exibida.
- O menu suspenso de Supervisor agora mostra diretamente o nome salvo no cadastro de supervisores.
- A versao do sistema foi atualizada para `1.1.2`.

## Preservacao da Versao Anterior

Antes da correcao, a versao anterior foi preservada no GitHub em:

- Tag: `v1.1.1-backup`
- Branch: `backup/v1.1.1`

## Observacao

A tabela de atividades continua preparada no banco, mas a tela de registro de atividade permanece como placeholder para implementacao futura.
