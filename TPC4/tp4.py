import ply.lex as lex

dado = '''
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

tokens= (
    "SELECT", 
    "WHERE", 
    "LIMIT",
    "COMENTARIO",
    "VAR", 
    "PALAVRA", 
    "STRING",
    "NUMERO", 
    "DOISPONTOS", 
    "PONTO",
    "OB", 
    "CB",
    "LINGUA",
    "DEFINICAO"
)


#def t_Number(t):
#    r"/d+"
#    t.value=int(t.value)
#    return t

# Funções para palavras-chave (case-insensitive)
def t_SELECT(t):
    r'select'
    return t

def t_WHERE(t):
    r'where'
    return t

def t_LIMIT(t):
    r'LIMIT'
    return t

t_DEFINICAO = r'[a-zA-Z_]*:[a-zA-Z0-9_:]*'
t_COMENTARIO = r'\#.*'
t_DOISPONTOS = r'::'
t_PONTO = r'\.'
t_OB = r'\{'
t_CB = r'\}'
t_VAR = r'\?[a-zA-Z_]\w*'
t_STRING = r'"[^"]*"'
t_NUMERO = r'\d+'
t_LINGUA = r'@[a-zA-Z]+'
t_PALAVRA = r'[a-zA-Z_][a-zA-Z0-9_:]*'

t_ignore= " "

def t_newLine(t):
    r"\n"
    t.lexer.lineno +=1

def t_error(t):
    print(f"Simbolo invalido na linha {t.lineno}:{t.value[0]}")
    t.lexer.skip(1)
    pass

lexer= lex.lex()

lexer.input(dado)

#r=lexer.token()
#print(r)

while tok := lexer.token():
    print(tok)