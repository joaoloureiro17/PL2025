# TPC4: Analisador Léxico 
## Autor
- **Nome:** João Silva Loureiro
- **Id:** A100832

## Descrição
Este trabalho implementa um analisador léxico.  

O analisador identifica os seguintes tokens:
- **Palavras-chave**: `select`, `where`, `limit`
- **Variáveis**: identificadores que começam com `?`
- **Identificadores gerais**: nomes de entidades e propriedades
- **Strings**: texto entre aspas `"texto"`
- **Números**: sequências numéricas
- **Linguagem**: como `@en`, `@pt`
- **Definições com namespace**: `dbo:MusicalArtist`
- **Comentários**: linhas iniciadas por `#`
- **Símbolos especiais**: `{ } . ::`

---

## Exemplo de Entrada
```sparql
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
```

---

## Tokens Reconhecidos

### Palavras-chave
- **In:** `select ?nome where { ... } LIMIT 1000`
- **Out:**  
  ```python
  ('SELECT', 'select')
  ('VAR', '?nome')
  ('WHERE', 'where')
  ...
  ('LIMIT', 'LIMIT')
  ```

### Variáveis
- **In:** `?s ?w ?nome`
- **Out:**  
  ```python
  ('VAR', '?s')
  ('VAR', '?w')
  ('VAR', '?nome')
  ```

### Identificadores com Namespace
- **In:** `dbo:MusicalArtist`
- **Out:**  
  ```python
  ('DEFINICAO', 'dbo:MusicalArtist')
  ```

### Strings
- **In:** `"Chuck Berry"`
- **Out:**  
  ```python
  ('STRING', '"Chuck Berry"')
  ```

### Linguagem
- **In:** `"Chuck Berry"@en`
- **Out:**  
  ```python
  ('STRING', '"Chuck Berry"')
  ('LINGUA', '@en')
  ```

### Comentários
- **In:** `# DBPedia: obras de Chuck Berry`


