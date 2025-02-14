texto1="Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagensdeu-nos este trabalho para fazer.=OfF E deu-nos 7= dias para o fazer... ON Cada trabalho destes vale 0.25 valores da nota final!="

def somador_On_Off(texto):
    soma = 0
    flag = True
    numero = ''
    i = 0
    
    while i < len(texto):    
        char = texto[i]
        
        if char.isdigit() and flag:
            numero += char
            
        else:
            if numero:
                soma += int(numero)
                numero = ''
            if char == '=':
                print(soma)
            elif texto[i:i+2].lower() == "on":
                flag = True
                i += 1
            elif texto[i:i+3].lower() == "off":
                flag = False
                i += 2
        
        i += 1
    
    if numero:
        soma += int(numero)
    

somador_On_Off(texto1)
