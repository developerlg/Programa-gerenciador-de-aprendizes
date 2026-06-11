# Relatório da Versão 1.1.3

## Objetivo

Aplicar os ajustes solicitados no documento `PROGRAMA GERENCIADOR DE ATIVIDADES DOS JOVENS V1.1.3.docx`, fortalecendo a base do código e padronizando campos importantes para futuras pesquisas.

## Alterações Aplicadas

- O campo `Setor` no cadastro de aprendizes deixou de ser texto livre e passou a ser menu suspenso.
- Os setores dos aprendizes foram padronizados como: Arquivo, T.I, Financeiro, Compras e Gerência.
- O campo `CPF` passou a aceitar apenas números e exibir automaticamente a máscara `000.000.000-00`.
- O campo `Função` no cadastro de supervisores deixou de ser texto livre e passou a ser menu suspenso.
- As funções dos supervisores foram padronizadas como: Auxiliar de T.I, Auxiliar de ADM, Agente de ADM e Gerente.
- O cadastro de supervisores ganhou o campo `Setor` como menu suspenso.
- Os setores dos supervisores foram padronizados como: Arquivo, Financeiro, Gerência e Compras.
- O banco de dados ganhou a coluna `setor` na tabela `supervisores`.
- As opções de setores e funções foram centralizadas em `data/opcoes.py`.
- A versão do sistema foi atualizada para `1.1.3`.
- Textos visíveis foram revisados para corrigir acentos, cedilha e pontuação.

## Preservação da Versão Anterior

Antes da alteração, a versão anterior foi preservada no GitHub em:

- Tag: `v1.1.2-backup`
- Branch: `backup/v1.1.2`

## Observação

A tela de registro de atividade permanece como placeholder. A tabela `atividades` continua preparada no banco para implementação futura.
