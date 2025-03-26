# TPC6: Recursivo Descendente para Expressões Aritméticas

**Autor:**  
Nome: João Silva Loureiro  
ID: A100832

## Descrição

Este tpc implementa um parser recursivo descendente **LL(1)** para avaliar expressões aritméticas. O parser pode lidar com operações de soma (`+`), subtração (`-`), multiplicação (`*`), divisão (`/`) e parênteses para agrupamento. O parser é capaz de analisar expressões simples e mais complexas com o uso de recursão.


- **Números**: Inteiros (por exemplo, `2`, `67`, `3`, etc.)
- **Operadores**: `+`, `-`, `*`, `/`
- **Parênteses**: `(`, `)`

**Exemplos de expressões aceitas:**

- `2 + 3`
- `67 - (2 + 3 * 4)`
- `(9 - 2) * (13 - 4)`


## Tokens Reconhecidos

- **Números**: `2`, `67`, `3`, `9`
- **Operadores**: `+`, `-`, `*`, `/`
- **Parênteses**: `(`, `)`



