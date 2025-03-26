import ply.yacc as yacc

from calc_lex import tokens 

def p_operacao(p): ##parser
    "operacao : calc"
    p[0]=p[1]

def p_operacao_1(p):
    "operacao : operacao PLUS calc"
    p[0]=p[1] + p[3] 
  
def p_operacao_2(p):
    "operacao : operacao MINUS calc"
    p[0]= p[1] - p[3]      

def p_calc_1(p):
    "calc : expressao"
    p[0]=p[1]

def p_calc_2(p):
    "calc : calc TIMES expressao"
    p[0]=p[1] * p[3]

def p_calc_3(p):
    "calc : calc DIVIDE expressao"
    p[0]=p[1] / p[3]        

def p_expressao_1(p):
    "expressao : NUMBER"
    p[0]=p[1]

def p_expressao(p):
    "expressao : LPAREN operacao RPAREN"
    p[0]=p[2]


def p_error(p):
    print("Erro sintático no input!")

parser=yacc.yacc()

r=parser.parse("2+3")
r1=parser.parse("67-(2+3*4)")
r2=parser.parse("(9-2)*(13-4)")
print("Resultado:", r)
print("Resultado:", r1)
print("Resultado:", r2)
