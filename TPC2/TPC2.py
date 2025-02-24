import re

file = open("obras.csv", "r", encoding="utf-8")

ignoreHeader = file.readline()

musicos =[]
numObras = {}
Obras = {}

while line := file.readline():
    
    reg = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
    while len(reg) < 7:
        newLine = file.readline().strip()
        if not newLine:
            break
        line += " " + newLine
        reg = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
        
    musico = f"{reg[4]}"
    musicos.append(musico)        
    periodo = f"{reg[3]}"
    numObras[periodo] = numObras.get(periodo, 0) + 1
    titulo = f"{reg[0]}"
    Obras[periodo] = Obras.get(periodo, []) + [titulo]
    
    
musicos.sort()
for periodo in Obras:
    Obras[periodo].sort()
    
print(musicos)
print(numObras)
print(Obras)
