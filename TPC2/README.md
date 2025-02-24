# TPC2 - Análise de um dataset de obras musicais

## Objetivo
Desenvolver um programa em Python que processe um dataset de obras musicais, sem o uso do módulo CSV, para gerar os seguintes resultados:
Lista ordenada alfabeticamente dos compositores musicais.
Distribuição das obras por período, contando quantas obras há em cada um.
Dicionário associando cada período a uma lista alfabética dos títulos das obras.

## Autor
João Silva Loureiro  
A100832

## Resumo
O programa lê o ficheiro obras.csv, ignora o cabeçalho e processa os dados utilizando expressões regulares para separar os campos corretamente.
Cada linha é analisada e os dados extraídos são armazenados em estruturas adequadas.
Os compositores são organizados alfabeticamente.
A contagem de obras por período é realizada.
As obras são agrupadas por período e organizadas alfabeticamente.

## Input
Título;Compositor;Ano;Período;Estilo;Instrumentação
"Nocturne in C minor";"Chopin, Frédéric";1837;Romântico;Piano Solo;Piano
"Toccata";"Bach, Johann Sebastian";1707;Barroco;Órgão;Órgão


## Resultado
Lista de Compositores:
['Alessandro Stradella', 'Antonio Maria Abbatini', 'Bach, Johann Christoph', ...]

Distribuição de Obras por Período:
{'Barroco': 26, 'Clássico': 15, 'Medieval': 48, 'Renascimento': 41, 'Século XX': 18, 'Romântico': 19, 'Contemporâneo': 7}

Dicionário de Obras por Período:
{'Barroco': ['Ab Irato', 'Die Ideale, S.106', 'Fantasy No. 2', ...], 'Clássico': ['Bamboula, Op. 2', 'Capriccio Italien', ...]}