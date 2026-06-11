# Relatório V1.3

## Objetivo

Remover o supervisor como dado fixo do cadastro de aprendizes e preparar a estrutura de atividades para receber o supervisor responsável pela solicitação ou execução da atividade.

## Alterações realizadas

- Removido o campo supervisor da tela de cadastro de aprendizes.
- Removida a coluna supervisor da tabela visual de aprendizes.
- Removida a obrigatoriedade de supervisor nas regras de cadastro e edição de aprendizes.
- Removidos `supervisor_id` e `supervisor_nome` do modelo e do fluxo de aprendizes.
- Ajustadas as consultas de aprendizes para buscar apenas por nome, CPF e setor.
- Ajustada a migração do SQLite para recriar `aprendizes` sem `supervisor_id`.
- Preparada a tabela `atividades` com `supervisor_id`, chave estrangeira para `supervisores` e índice de consulta.
- Mantida a tela de registro de atividade como placeholder com a mensagem `Tela em desenvolvimento`.
- Atualizada a versão do sistema para `1.3.0`.
- Atualizado o README com o escopo atual.

## Resultado esperado

O jovem aprendiz passa a ser cadastrado apenas com seus próprios dados. O supervisor deixa de ser uma característica fixa do jovem e passa a ser uma informação preparada para uso futuro em cada atividade registrada.

## Observações

A tela de atividades ainda não registra dados reais. A estrutura do banco já está pronta para que, em uma próxima versão, cada atividade possa informar o aprendiz, o supervisor solicitante, a atividade executada, a descrição, a observação e o prazo estimado.
