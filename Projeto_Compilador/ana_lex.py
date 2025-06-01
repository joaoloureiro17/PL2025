import ply.lex as lex
import sys

tokens= [
    "PROGRAM",
    "NOME", #nome programa
    "VAR",
    "BEGIN",
    "END",
    "FUNCAO", #writeln e readln 
    "PA", #(
    "PF", #)
    "CONST",
    "STRING", #'Ola'
    "PV", #;
    "PONTO",#.
    "VARIAVEL", #num1, num2, ...
    "DPONTOS", #:
    "TIPO", #integer, boolean, char
    "COMENTARIO", #{comentario}
    "IF",
    "THEN",
    "ELSE",
    "FOR",
    "TO",
    "DOWNTO",
    "DO",
    "WHILE",
    "MAIOR", #>
    "MENOR", #<
    "IGUAL", #= (usado para as comparações no if)
    "MAIORIGUAL", #<=
    "MENORIGUAL", #=>
    "DIFERENTE", #<>
    "VIRGULA", #,
    "ATRIBUICAO", #:= (usado para atribuir valor as variaveis)
    "INT", #e.g.:5
    "REAL", #e.g.:3.14
    "ADD", #+
    "SUB", #-
    "MULT", #*
    "DIVISAO", #/
    "DIV", #divisão inteira
    "MOD",
    "AND",
    "OR",
    "NOT",
    "BOOLEAN", #true, false
    "ARRAY", # e.g.: array[1..5] ou array ['a'..'d']
    "OF",
    "RETOSABRIR",
    "RETOSFECHAR"
]

t_RETOSABRIR=r'\['
t_RETOSFECHAR=r'\]'
t_PA= r'\('
t_PF= r'\)'
t_PV= r'\;'
t_PONTO= r'\.'
t_DPONTOS= r'\:'
t_DIFERENTE= r'\<\>'
t_MAIORIGUAL= r'\>\='
t_MENORIGUAL= r'\<\='
t_MAIOR= r'\>'
t_MENOR= r'\<'
t_IGUAL= r'\='
t_VIRGULA= r'\,'
t_ADD= r"\+"
t_SUB= r"\-"
t_MULT= r"\*"
t_DIVISAO= r"/"

t_ignore= " \t" 

def t_PROGRAM(t):
    r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm]' 
    return t

def t_VAR(t):
    r'[Vv][Aa][Rr]' 
    return t

def t_BEGIN(t):
    r'[Bb][Ee][Gg][Ii][Nn]'
    return t

def t_END(t):
    r'[Ee][Nn][Dd]'  
    return t

def t_CONST(t):
    r'[Cc][Oo][Nn][Ss][Tt]'  
    return t

def t_IF(t):
    r'[Ii][Ff]'
    return t

def t_THEN(t):
    r'[Tt][Hh][Ee][Nn]'  
    return t

def t_ELSE(t):
    r'[Ee][Ll][Ss][Ee]'  
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr]'  
    return t

def t_DOWNTO(t):
    r'[Dd][Oo][Ww][Nn][Tt][Oo]'  
    return t

def t_TO(t):
    r'[Tt][Oo]'  
    return t

def t_DO(t):
    r'[Dd][Oo]'  
    return t

def t_WHILE(t):
    r'[Ww][Hh][Ii][Ll][Ee]' 
    return t

def t_DIV(t):
    r'[Dd][Ii][Vv]'  
    return t

def t_MOD(t):
    r'[Mm][Oo][Dd]'  
    return t

def t_AND(t):
    r'[Aa][Nn][Dd]'  
    return t

def t_OR(t):
    r'[Oo][Rr]'
    return t

def t_NOT(t):
    r'[Nn][Oo][Tt]'
    return t

def t_OF(t):
    r'[Oo][Ff]'  
    return t

def t_FUNCAO(t):
     r"([wW]rite[lL]n|Write|[rR]ead[lL]n|length)"
     return t

def t_TIPO(t):
     r"([iI]nteger|[bB]oolean|[sS]tring|[cC]har|[rR]eal|[dD]ouble)"
     return t

def t_BOOLEAN(t):
    r'\b(true|false)\b'
    return t

def t_REAL(t):
    r'\d+\.\d+'
    t.value=float(t.value) #passamos string para float
    return t

def t_INT(t):
    r'\d+'
    t.value= int(t.value) #passamos string para inteiro
    return t

def t_NOME(t):
    r"[A-Z]\w+" 
    return t

def t_ARRAY (t):
    r"array"
    return t

def t_VARIAVEL(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    return t

def t_STRING(t):
    r"'([^']*)'"
    t.value = list(t.value[1:-1])  #removemos as aspas e convertemos em lista de caracteres
    return t

def t_ATRIBUICAO(t):
     r":="
     return t

def t_COMENTARIO(t):
    r'(\{(.|\n)*?\})|(\/\/.*)|(\(\*.*?\))' #{...}, //..., (*...*) 
    t.lexer.lineno += t.value.count('\n') #atualiza contagem de linhas
    pass #ignoramos os comentarios 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Símbolo inválido na linha {t.lineno}: {t.value[0]}")
    t.lexer.skip(1)
    pass

lexer= lex.lex()

# Lê o conteúdo de um ficheiro passado por argumento
def ler_codigo_ficheiro(nome_ficheiro):
    try:
        with open(nome_ficheiro, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Erro: Ficheiro '{nome_ficheiro}' não encontrado.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ana_lex.py <ficheiro_pascal>")
        sys.exit(1)

    codigo = ler_codigo_ficheiro(sys.argv[1])
    lexer.input(codigo)

    #Lê tds os tokens
    while tok := lexer.token():
        print(tok)