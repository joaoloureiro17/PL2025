# TPC5: Máquina de Vending

## Autor

**Nome:** João Silva Loureiro
**Id:** a100832

## Descrição

Este trabalho implementa uma máquina de vending simulada.

A máquina permite:

- **Listar produtos**: Mostrar os produtos disponíveis no stock.
- **Inserir moedas**: Permite ao utilizador inserir moedas de diferentes valores.
- **Selecionar produtos**: Verifica a disponibilidade do produto e o saldo do utilizador.
- **Fornecer troco**: Calcula e devolve o troco ao utilizador.
- **Manter o estado**: O stock é armazenado num ficheiro `stock.json`, garantindo persistência entre execuções.

---

## Exemplo de Entrada e Saída

```bash
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod  | nome        | quantidade | preço
--------------------------------------
A23  | água 0.5L  | 8          | 0.7€
...
>> MOEDA 1e, 20c, 5c, 5c.
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```

---

## Comandos Reconhecidos

### Listar Produtos

**Comando:**

```bash
LISTAR
```

**Saída:** Exibe os produtos disponíveis no stock.

### Inserir Moedas

**Comando:**

```bash
MOEDA 1e, 50c, 10c
```

**Saída:**

```python
('MOEDA', '1e')
('MOEDA', '50c')
('MOEDA', '10c')
```

Atualiza o saldo do utilizador.

### Selecionar Produto

**Comando:**

```bash
SELECIONAR A23
```

**Saída:**

```python
('SELECIONAR', 'A23')
```

Se houver saldo suficiente, dispensa o produto e atualiza o stock.

### Troco

**Comando:**

```bash
SAIR
```

**Saída:**

```python
('TROCO', {'50c': 1, '20c': 1, '2c': 2})
```

Devolve o troco e encerra a sessão.

### Produto Inexistente

**Comando:**

```bash
SELECIONAR Z99
```

**Saída:**

```bash
maq: Produto inexistente.
```

### Saldo Insuficiente

**Comando:**

```bash
SELECIONAR A23
```

(se o saldo for insuficiente) **Saída:**

```bash
maq: Saldo insuficiente para satisfazer o seu pedido.
```

---

## Persistência de Dados

O stock é armazenado num ficheiro `stock.json`, garantindo que os produtos e quantidades são mantidos entre execuções do programa.

## Funcionalidades Extras

- **Adicionar Produtos**: Um comando extra `ADICIONAR` pode ser implementado para aumentar o stock de produtos existentes ou adicionar novos produtos.

---

Este projeto simula uma interação realista com uma máquina de vending, tratando corretamente as condições de erro e garantindo a persistência do stock.

