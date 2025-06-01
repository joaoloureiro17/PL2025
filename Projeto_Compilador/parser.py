import ply.yacc as yacc
from ana_lex import tokens 
import sys

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children or []
        self.leaf = leaf

    def __repr__(self):
        if isinstance(self.leaf, str):
            leaf_repr = f'"{self.leaf}"'
        else:
            leaf_repr = str(self.leaf) 
        return f"Node(type='{self.type}', leaf={leaf_repr}, children={self.children})"

# Regras da gramática com construção da AST
def p_programa(p):
    'programa : PROGRAM NOME PV bloco PONTO'
    p[0] = Node('programa', [p[4]], p[2])

def p_bloco(p):
    '''bloco : VAR declaracoes BEGIN comandos END
             | BEGIN comandos END'''
    if len(p) == 6:
        p[0] = Node('bloco', [p[2], p[4]])
    else:
        p[0] = Node('bloco', [Node('declaracoes', []), p[2]])  #declarações vazias

def p_declaracoes(p):
    """declaracoes : declaracoes declaracao
                   | declaracao"""
    if len(p) == 2:
        p[0] = Node('declaracoes', [p[1]])
    else:
        #adiciona a nova declaração à lista de declarações existentes
        p[0] = Node('declaracoes', p[1].children + [p[2]])

def p_declaracao(p):
    """declaracao : listVar DPONTOS TIPO PV
                  | listVar DPONTOS ARRAY RETOSABRIR INT PONTO PONTO INT RETOSFECHAR OF TIPO PV"""
    if len(p) == 5:
        #se for uma declaração simples (ex.: i: integer;)
        p[0] = Node('declaracao', [p[1]], p[3])
    else:
        #se for uma declaração de array (ex.: numeros: array[1..5] of integer;)
        p[0] = Node('declaracao_array', [], {
            'variaveis': p[1],  #lista de variáveis
            'limites': (p[5], p[8]),  #limites do array (ex.: 1 e 5)
            'tipo': p[11]  #tipo do array (ex.: integer)
        })

def p_listVar(p):
    """listVar : VARIAVEL
               | listVar VIRGULA VARIAVEL"""
    if len(p) == 2:
        p[0] = Node('variaveis', [Node('variavel', [], p[1])])
    else:
        p[0] = Node('variaveis', p[1].children + [Node('variavel', [], p[3])])

def p_comandos(p):
    """comandos : comando
                | comando PV
                | comando PV comandos"""
    if len(p) == 2:
        p[0] = Node('comandos', [p[1]])
    elif len(p) == 3:
        p[0] = Node('comandos', [p[1]])
    else:
        p[0] = Node('comandos', [p[1]] + p[3].children)

def p_comando_funcao(p):
    """comando : FUNCAO PA lista_parametros PF"""
    p[0] = Node('funcao', [p[3]], p[1])

def p_comando_begin(p):
    "comando : BEGIN comandos END"
    p[0] = Node('bloco', [p[2]])

def p_lista_parametros(p):
    """lista_parametros : expressao
                        | lista_parametros VIRGULA expressao"""
    if len(p) == 2:
        p[0] = Node('parametro', [p[1]])
    else:
        p[0] = Node('parametro', p[1].children + [p[3]])

def p_comando_atribuicao(p):
    """comando : VARIAVEL ATRIBUICAO expressao"""
    var_node = Node('variavel', [], p[1])
    p[0] = Node('atribuicao', [var_node, p[3]])

def p_comando_if_then(p):
    'comando : IF expressao THEN comando %prec IFX'
    p[0] = Node('if', [p[2], p[4], None])

def p_comando_if_then_else(p):
    'comando : IF expressao THEN comando ELSE comando'
    p[0] = Node('if_else', [p[2], p[4], p[6]])


def p_comando_for(p):
    """comando : FOR VARIAVEL ATRIBUICAO expressao direcao expressao DO comando"""
    #for i := 1 to 10 do <comando>
    p[0] = Node('for',[Node('atribuicao', [Node('variavel', [], p[2]), p[4] ]),Node('direcao', [], p[5]), p[6], p[8] ])


#direcao para a qual é feita a contagem to(crescente) ou downto(descrescente)
def p_direcao(p):
    """direcao : TO
               | DOWNTO"""
    p[0]=p[1]

def p_comando_while(p):
    """comando : WHILE expressao DO comando"""
    p[0] = Node('while', [p[2], p[4]])

# Expressões, que podem ser variáveis ou literais
def p_expressao_unaria(p):
    """expressao : NOT expressao"""
    p[0] = Node('not', [p[2]])

def p_expressao_binaria(p):
    """expressao : expressao ADD expressao
                 | expressao SUB expressao
                 | expressao MULT expressao
                 | expressao DIVISAO expressao
                 | expressao DIV expressao
                 | expressao MOD expressao
                 | expressao MAIOR expressao
                 | expressao MENOR expressao
                 | expressao IGUAL expressao
                 | expressao DIFERENTE expressao
                 | expressao MAIORIGUAL expressao
                 | expressao MENORIGUAL expressao
                 | expressao AND expressao
                 | expressao OR expressao"""
    p[0] = Node('binop', [p[1], p[3]], p[2])

def p_expressao_length(p):
    "expressao :  FUNCAO PA VARIAVEL PF"
    p[0] = Node('funcao', [p[3]], p[1])

def p_expressao_variavel(p):
    "expressao : VARIAVEL"
    p[0] = Node('variavel', [], p[1])

def p_expressao_valor(p):
    "expressao : INT"
    p[0] = Node('inteiro', [], p[1])

def p_expressao_real(p):
    "expressao : REAL"
    p[0] = Node('real', [], p[1])

def p_expressao_string(p):
    "expressao : STRING"
    p[0] = Node('string', [], p[1])

def p_expressao_boolean(p):
    "expressao : BOOLEAN"
    p[0] = Node('boolean', [], p[1])

def p_expressao_parenteses(p):
    "expressao : PA expressao PF"
    p[0] = p[2]

def p_expressao_array(p):
    "expressao : VARIAVEL RETOSABRIR expressao RETOSFECHAR"
    p[0] = Node('acesso_array', [p[3]], p[1])

def p_comando_atribuicao_array(p):
    "comando : VARIAVEL RETOSABRIR expressao RETOSFECHAR ATRIBUICAO expressao"
    p[0] = Node('atribuicao_array', [Node('variavel', [], p[1]), p[3], p[6]])

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}, token inesperado: {p.value} (Tipo: {p.type})")
    else:
        print("Erro de sintaxe: fim de ficheiro inesperado")

# Precedências para resolucao dos conflitos 
precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MULT', 'DIVISAO', 'DIV', 'MOD'),
    ('left', 'MAIOR', 'MENOR', 'IGUAL', 'DIFERENTE', 'MAIORIGUAL', 'MENORIGUAL'),
    ('right', 'ATRIBUICAO'),  
    ('left', 'AND', 'OR'),
    ('right', 'NOT'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
)

# Criamos o parser
parser = yacc.yacc()

def main():
    if len(sys.argv) != 2:
        print("Uso: python parser_completo.py <ficheiro>")
        return

    caminho = sys.argv[1]
    try:
        with open(caminho, 'r') as f:
            codigo = f.read()
        resultado = parser.parse(codigo)
        if resultado:
            print("AST gerada com sucesso:\n")
            print(resultado)
            with open("AST", "w") as out_file:
                out_file.write(repr(resultado))   #imprime a AST num ficheiro "AST" e caso este não exista cria-o
            print("AST escrita no ficheiro 'AST'.")
        else:
            print("Erro: não foi possível gerar AST.")
    except FileNotFoundError:
        print(f"Erro: ficheiro '{caminho}' não encontrado.")

if __name__ == "__main__":
    main()