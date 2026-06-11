# Relatório da Versão 1.2

## Objetivo

Corrigir o total exibido na área `Atividades por situação` do dashboard.

## Problema Encontrado

Mesmo sem atividades cadastradas, o gráfico exibia `1` como total. A origem do problema estava no componente visual do gráfico: para evitar divisão por zero, o código transformava a soma zero em `1` e acabava mostrando esse valor na tela.

## Correção Aplicada

- O gráfico agora mantém o total real separado do divisor interno.
- Quando não há atividades, o total exibido permanece `0`.
- O divisor interno só usa `1` para evitar erro matemático, sem alterar o número mostrado ao usuário.
- Quando o total é zero, o gráfico mostra um anel neutro, sem simular atividades.
- A versão do sistema foi atualizada para `1.2.0`.

## Preservação da Versão Anterior

Antes da alteração, a versão anterior foi preservada no GitHub em:

- Tag: `v1.1.3-backup`
- Branch: `backup/v1.1.3`

## Observação

A tabela `atividades` já existe preparada no banco, mas a tela de registro de atividade continua como placeholder para implementação futura.
