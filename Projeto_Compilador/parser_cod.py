class Node:
    def __init__(self, type, leaf=None, children=None):
        self.type = type
        self.leaf = leaf
        self.children = children or []

    def __repr__(self):
        return f"Node(type='{self.type}', leaf={self.leaf}, children={self.children})"

class CodeGenerator:
    
    posicao = 0

    def __init__(self):
        self.code = []
        self.incrementador=0
        self.symbol_increment = 0  
        self.label_increment = 0 
        self.symbol_table = {}  #tabela de símbolos

    def generate_code(self, node):
        global posicao

        if node.type == 'programa':
            self.code.append("start")
            for child in node.children:
                self.generate_code(child)
            self.code.append("stop")

        elif node.type == 'bloco':
            for child in node.children:
                self.generate_code(child)

        elif node.type == 'declaracoes':
            for child in node.children:
                self.generate_code(child)

        elif node.type == 'declaracao':
            tipo = node.leaf.lower()  #normalizamos o tipo para letras minúsculas
            for var_group in node.children:
                if var_group.type == 'variaveis':
                    for var_node in var_group.children:
                        if var_node.type == 'variavel':
                            # Adiciona a variável à tabela de símbolos
                            self.symbol_table[var_node.leaf] = {'tipo': tipo, 'index': self.symbol_increment}
                            self.symbol_increment += 1
                            # Inicialização da variável com um valor padrão
                            if tipo == "integer":
                                self.code.append("pushi 0")
                            elif tipo == "real":
                                self.code.append("pushf 0.0")
                            elif tipo == "boolean":
                                self.code.append("pushi 0")  
                            elif tipo == "string":
                                self.code.append('pushs ""')
                            elif tipo == "char":
                                self.code.append("pushi 0")        
                            else:
                                raise ValueError(f"Tipo inválido para a variável: {tipo}")
        elif node.type == 'comandos':
            for child in node.children:
                self.generate_code(child)

        elif node.type == 'funcao':
            nome_funcao = node.leaf.lower()
            if nome_funcao in ['writeln', 'write']:
                for parametro in node.children:
                    if parametro.type == 'parametro':
                        for valor in parametro.children:
                            if valor.type == 'variavel':
                                simbolo = self.symbol_table.get(valor.leaf)
                                if simbolo is not None:
                                    index = simbolo['index']
                                    tipo = simbolo['tipo']
                                    if tipo== 'char':
                                        # procura os indices com base nos tipos
                                        bin_index = next((v['index'] for k, v in self.symbol_table.items() if v['tipo'] == 'string'), None)
                                        pos_index = next((v['index'] for k, v in self.symbol_table.items() if v['tipo'] == 'integer'), None)
                                        
                                        if bin_index is None or pos_index is None:
                                            raise ValueError("Não foi possível encontrar índices para os tipos 'array' e 'integer'.")

                                        self.code.append(f"pushl {bin_index}")  # dá push do índice da string
                                        self.code.append(f"pushl {pos_index}")  # dá push do índice do inteiro
                                        self.code.append("charat")  # acede a um caractere na posição x da string
                                        self.code.append("writechr")
                                    self.code.append(f"pushl {index}")
                                    if tipo == 'integer':
                                        self.code.append("writei")
                                    elif tipo == 'real':
                                        self.code.append("writef")
                                    elif tipo == 'boolean':
                                        self.code.append("writei")
                                    elif tipo == 'string':
                                        self.code.append("writes")
                                else:
                                    raise ValueError(f"Variável '{valor.leaf}' não encontrada na tabela de símbolos.")
                            elif valor.type == 'string':
                                if isinstance(valor.leaf, list): 
                                    texto_sem_aspas = ''.join(valor.leaf)  #reconstrução da string para ser imprimida direito
                                else:
                                    texto_sem_aspas = valor.leaf[1:-1]  #removemos as aspas se for uma string normal
                                self.code.append(f'pushs "{texto_sem_aspas}"')
                                self.code.append("writes")
                            elif valor.type == 'inteiro':
                                self.code.append(f"pushi {valor.leaf}")
                                self.code.append("writei")
                            elif valor.type == 'real':
                                self.code.append(f"pushf {valor.leaf}")
                                self.code.append("writef")
                            elif valor.type == 'binop':
                                self.generate_code(valor)
                                self.code.append("writei")
                            elif valor.type == 'acesso_array':
                                nome_array = valor.leaf
                                indice_node = valor.children[0]
                                #aceder a um elemento do array
                                self.code.append(f"pushgp")
                                self.code.append(f"pushg {posicao}")
                                self.code.append("loadn")
                                self.code.append("writei")
                            else:
                                raise ValueError(f"Tipo de valor inválido para escrita: {valor.type}")
                if nome_funcao == 'writeln':
                    self.code.append("writeln")
                    
            elif nome_funcao == 'readln':
                if node.children:
                    parametro = node.children[0]
                    if parametro.type == 'parametro' and parametro.children:
                        var_node = parametro.children[0]
                        if (var_node.type == 'variavel'):
                            var_name = var_node.leaf
                            simbolo = self.symbol_table.get(var_name)
                            if simbolo is not None:
                                index = simbolo['index']
                                tipo = simbolo['tipo']
                                self.code.append('read')
                                #fazemos as conversões consoante o tipo da variavel
                                if tipo == 'integer':
                                    self.code.append('atoi')
                                    self.code.append(f'storeg {index}')
                                    posicao=index 
                                elif tipo == 'real':
                                    self.code.append('atof')
                                    self.code.append(f'storeg {index}')
                                    posicao=index 
                                elif tipo == 'boolean':
                                    self.code.append('atoi')
                                    self.code.append(f'storeg {index}')
                                    posicao=index 
                                elif tipo == 'string':
                                    self.code.append(f'storeg {index}')
                                    posicao=index 
                                else:
                                    raise ValueError(f"Tipo '{tipo}' não suportado na leitura com readln.")
                        elif var_node.type == 'acesso_array':
                            nome_array = var_node.leaf
                            indice_node = var_node.children[0]

                            if nome_array not in self.symbol_table:
                                raise ValueError(f"Array '{nome_array}' não declarado.")

                            array_info = self.symbol_table[nome_array]
                            base_index = array_info['index'] 

                            self.code.append('read')
                            self.code.append('atoi')
            elif nome_funcao == 'length':
                if node.children:
                    parametro = node.children[0]
                    if isinstance(parametro, Node): 
                        if parametro.type == 'parametro' and parametro.children:
                            valor_node = parametro.children[0]
                            if isinstance(valor_node, Node):
                                self.generate_code(valor_node)
                                
                                self.code.append("strlen") 
                            else:
                                raise ValueError(f"Esperado um objeto Node, mas encontrado: {type(valor_node)}")
                        else:
                            raise ValueError(f"Estrutura inesperada para o nó 'length': {parametro}")
                    elif isinstance(parametro, str):
                        simbolo = self.symbol_table[parametro]
                        index = simbolo['index']  
                        self.code.append(f"pushg {index}")  #usa pushg para aceder ao valor da variável
                        self.code.append("strlen") #calcula o tamanho de uma string
                    else:
                        raise ValueError(f"Tipo inesperado para 'parametro': {type(parametro)}")
                else:
                    raise ValueError("Nó 'length' não possui filhos.")

        elif node.type == 'if':

            # rótulos únicos para o bloco else e done
            else_label = f"else{self.label_increment}"
            done_label = f"done{self.label_increment}"
            self.label_increment += 1

            condicao = node.children[0]  #condição
            self.generate_code(condicao)  
            self.code.append(f"jz {else_label}")  #salta para o else se a condição for falsa

            bloco_if = node.children[1]  #bloco do if
            self.generate_code(bloco_if)
            self.code.append(f"jump {done_label}")  #salta para o final depois de executar o bloco if

            # rótulo do bloco else 
            self.code.append(f"{else_label}:")
            self.code.append(f"{done_label}:")  # rótulo final

        elif node.type == 'if_else':

            else_label = f"else{self.label_increment}"
            done_label = f"done{self.label_increment}"
            self.label_increment += 1

            condicao = node.children[0]  
            self.generate_code(condicao)  
            self.code.append(f"jz {else_label}")  
            

            bloco_if = node.children[1]  
            self.generate_code(bloco_if)
            self.code.append(f"jump {done_label}") 

            self.code.append(f"{else_label}:")
            if len(node.children) > 2:  # verifica se existe bloco else, e caso exista gera o codigo
                bloco_else = node.children[2]
                self.generate_code(bloco_else)

            self.code.append(f"{done_label}:")             
        elif node.type == 'atribuicao':
            variavel = node.children[0]  # variável
            valor = node.children[1]  # valor

            self.generate_code(valor)

            simbolo = self.symbol_table.get(variavel.leaf)
            if simbolo is not None:
                index = simbolo['index']
                self.code.append(f"storel {index}")  # guarda o valor no indice da variavel defenida
            else:
                raise ValueError(f"Variável '{variavel.leaf}' não encontrada na tabela de símbolos.")

        elif node.type == 'binop':
            op = node.leaf
            esq = node.children[0]
            dir = node.children[1] if len(node.children) > 1 else None

            self.generate_code(esq)
            if dir:
                self.generate_code(dir)

            tipo_esq = self.get_tipo_expressao(esq)
            tipo_dir = self.get_tipo_expressao(dir) if dir else None

            # Operadores
            if op == '+':
                if tipo_esq == 'real' or tipo_dir == 'real': #caso um dos valores seja real faz fadd
                    self.code.append('fadd')
                else:
                    self.code.append('add') #se forem ambos integer faz add
            elif op == '-':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('fsub')
                else:
                    self.code.append('sub')
            elif op == '*':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('fmul')
                else:
                    self.code.append('mul')
            elif op == '/':
                self.code.append('fdiv') #divisao
            elif op == 'div':
                self.code.append('div') #divisao inteira
            elif op == 'mod':
                self.code.append('mod')
            elif op == '>':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('fsup')
                else:
                    self.code.append('sup')
            elif op == '<':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('finf')
                else:
                    self.code.append('inf')
            elif op == '=':
                if tipo_dir == 'string' and tipo_esq != 'string':
                    simbolo_esq = self.symbol_table.get(esq.leaf)
                    if simbolo_esq is not None:
                        self.code.append(f"pushg {simbolo_esq['index']}")
                    else:
                        raise ValueError(f"Variável '{esq.leaf}' não encontrada na tabela de símbolos.")

                    if isinstance(dir.leaf, str):
                        simbolo_dir = self.symbol_table.get(dir.leaf)
                        if simbolo_dir is not None:
                            self.code.append(f"pushl {simbolo_dir['index']}")
                        else:
                            raise ValueError(f"Variável '{dir.leaf}' não encontrada na tabela de símbolos.")
                    elif isinstance(dir.leaf, list):
                        for elemento in dir.leaf:
                            if isinstance(elemento, str):
                                if elemento.isdigit():  # verifica se é um número
                                    self.code.append(f"pushl {elemento}")
                                else:
                                    simbolo_elemento = self.symbol_table.get(elemento)
                                    if simbolo_elemento is not None:
                                        self.code.append(f"pushl {simbolo_elemento['index']}")
                                    else:
                                        raise ValueError(f"Variável '{elemento}' não encontrada na tabela de símbolos.")
                            else:
                                raise ValueError(f"Tipo inesperado para elemento em dir.leaf: {type(elemento)}")
                    else:
                        raise ValueError(f"Tipo inesperado para dir.leaf: {type(dir.leaf)}")

                    self.code.append("pushi 1")
                    self.code.append("sub")

                    self.code.append("charat")

                    # converte o caractere para inteiro (char -> int)
                    self.code.append("pushi 48")
                    self.code.append("sub")  

                    if dir.type == 'inteiro':  
                        if isinstance(dir.leaf, list):  
                            if len(dir.leaf) == 1 and dir.leaf[0].isdigit():  
                                self.code.append(f"pushi {dir.leaf[0]}") 
                            else:
                                raise ValueError(f"Lista inesperada em dir.leaf: {dir.leaf}")
                        else:
                            self.code.append(f"pushi {dir.leaf}") 
                    elif dir.type == 'string': 
                        if isinstance(dir.leaf, list):  
                            if len(dir.leaf) == 1 and isinstance(dir.leaf[0], str) and dir.leaf[0].isdigit():
                                self.code.append(f"pushi {dir.leaf[0]}") 
                            else:
                                texto_sem_aspas = ''.join(dir.leaf) 
                                self.code.append(f'pushs "{texto_sem_aspas}"') 
                        elif isinstance(dir.leaf, str) and len(dir.leaf) == 1 and dir.leaf.isdigit(): 
                            self.code.append(f"pushi {dir.leaf}") 
                        else:
                            self.code.append(f'pushs "{dir.leaf}"') 
                    else:
                        self.generate_code(dir)

                    self.code.append("equal")
                else:
                    self.code.append("equal")   
            elif op == '>=':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('fsupeq')
                else:
                    self.code.append('supeq')
            elif op == '<=':
                if tipo_esq == 'real' or tipo_dir == 'real':
                    self.code.append('finfeq')
                else:
                    self.code.append('infeq')        
            elif op == 'and':
                self.code.append('and')
            elif op == 'or':
                self.code.append('or')
            elif op == 'not':
                self.code.append('not')
            
        elif node.type == 'not':
            self.generate_code(node.children[0])
            self.code.append("not")
        elif node.type == 'expressao_parenteses':
            self.generate_code(node.children[0])
        elif node.type == 'acesso_array':
        
            nome_array = node.leaf
            indice = node.children[0]

            if nome_array not in self.symbol_table:
                raise ValueError(f"Array '{nome_array}' não declarado.")

            array_info = self.symbol_table[nome_array]
            base_index = array_info['index'] 

        elif node.type == 'while':
            # rótulos únicos para o início e o fim do loop
            start_label = f"start{self.label_increment}"
            end_label = f"end{self.label_increment}"
            self.label_increment += 1

            self.code.append(f"{start_label}:")
            self.generate_code(node.children[0])
            self.code.append(f"jz {end_label}")

            self.generate_code(node.children[1])
            self.code.append(f"jump {start_label}") 

            self.code.append(f"{end_label}:")
        elif node.type == 'variavel':
            simbolo = self.symbol_table.get(node.leaf)
            if simbolo is not None:
                index = simbolo['index']  
                self.code.append(f"pushl {index}") 
            else:
                raise ValueError(f"Variável '{node.leaf}' não encontrada na tabela de símbolos.")
        elif node.type == 'inteiro':
            self.code.append(f"pushi {node.leaf}")
        elif node.type == 'real':
            self.code.append(f"pushf {node.leaf}")
        elif node.type == 'boolean':
            if node.leaf.lower() == "true":
                self.code.append("pushi 1")
            elif node.leaf.lower() == "false":
                self.code.append("pushi 0")
            else:
                raise ValueError(f"Valor booleano inválido: {node.leaf}")
        elif node.type == 'string':
            if isinstance(node.leaf, list):  
                texto_sem_aspas = ''.join(node.leaf)  
            else:
                texto_sem_aspas = node.leaf[1:-1]
            self.code.append(f'pushs "{texto_sem_aspas}"')
        
        elif node.type == 'for':
            atribuicao_inicial = node.children[0]
            direcao = node.children[1].leaf.lower()
            limite = node.children[2]
            corpo = node.children[3]

            self.generate_code(atribuicao_inicial)

            # Variável de controle
            var_name = atribuicao_inicial.children[0].leaf
            simbolo = self.symbol_table.get(var_name)
            if simbolo is None:
                raise ValueError(f"Variável '{var_name}' não encontrada na tabela de símbolos.")
            var_index = simbolo['index']  

            start_label = f"start{self.label_increment}"
            end_label = f"end{self.label_increment}"
            self.label_increment += 1

            self.code.append(f"{start_label}:")

            #condição do loop
            self.code.append(f"pushl {var_index}") 
            self.generate_code(limite)  
            if direcao == 'to':
                self.code.append("infeq")  #verifica se i <= limite
            elif direcao == 'downto':
                self.code.append("sup")  #verifica se i >= limite
            else:
                raise ValueError(f"Direção de 'for' desconhecida: {direcao}")
            self.code.append(f"jz {end_label}")

            self.generate_code(corpo)

            # incrementa ou decrementa a variável de controle
            self.code.append(f"pushl {var_index}")  
            self.code.append("pushi 1")
            if direcao == 'to':
                self.code.append("add")  #incrementa
            elif direcao == 'downto':
                self.code.append("sub")  #decrementa
            self.code.append(f"storel {var_index}")  #atualiza o valor

            self.code.append(f"jump {start_label}")

            self.code.append(f"{end_label}:")
        elif node.type == 'declaracao_array':
            variaveis = node.leaf['variaveis']  #variáveis declaradas
            limites = node.leaf['limites']  #limites do array (ex.: (1, 5))
            tipo = node.leaf['tipo'].lower()  #tipo do array (ex.: integer)

            #calculo do tamanho do array
            limite_inferior, limite_superior = limites
            tamanho = int(limite_superior) - int(limite_inferior) + 1

            #adiciona cada variável do array à tabela de símbolos
            for var_node in variaveis.children:
                if var_node.type == 'variavel':
                    nome_array = var_node.leaf

                    if nome_array in self.symbol_table:
                        raise ValueError(f"Array '{nome_array}' já foi inicializado.")

                    self.symbol_table[nome_array] = {
                        'tipo': tipo,
                        'inicio': int(limite_inferior),
                        'fim': int(limite_superior),
                        'tamanho': tamanho,
                        'index': self.symbol_increment  
                    }

                    # inicialização do array na memória
                    if tipo == "integer":
                        self.code.append(f"pushn {tamanho}")  #usamos pushn com o tamanho do array que é equivalente a fazer x vexes o pushi 0
                    elif tipo == "real":
                        for _ in range(tamanho): #aqui temos que usar range(tamanho) para ele imprimir pushf 0.0 para cada elemento do array
                            self.code.append("pushf 0.0")  #inicializamos reais com 0.0
                    elif tipo == "boolean":
                        for _ in range(tamanho):
                            self.code.append("pushi 0")  #inicializamos booleanos a falso (0)
                    else:
                        raise ValueError(f"Tipo inválido para o array: {tipo}")

                    self.symbol_increment += tamanho
        elif node.type == 'atribuicao_array':
            array_node = node.children[0]  # array
            indice_node = node.children[1]  # indice
            valor_node = node.children[2]  # valor

            nome_array = array_node.leaf

            # verificamos se o array está na tabela de símbolos
            if nome_array not in self.symbol_table:
                raise ValueError(f"Array '{nome_array}' não declarado.")

            array_info = self.symbol_table[nome_array]
            base_index = array_info['index']  # indice base na memória

            # Gera o código para o valor a ser armazenado
            self.generate_code(valor_node)

            self.code.append(f"storeg {self.incrementador}")
            self.incrementador += 1  # Incrementa o índice para a próxima atribuição


    def get_tipo_expressao(self, node):
        if node.type == 'inteiro':
            return 'integer'
        elif node.type == 'real':
            return 'real'
        elif node.type == 'booleano':
            return 'boolean'
        elif node.type == 'string':
            return 'string'
        elif node.type == 'variavel':
            simbolo = self.symbol_table.get(node.leaf)
            if simbolo:
                return simbolo['tipo']
            else:
                raise ValueError(f"Variável '{node.leaf}' não encontrada.")
        elif node.type == 'binop':
            op = node.leaf
            tipos = [self.get_tipo_expressao(child) for child in node.children]
            if op in ['and', 'or', 'not']:
                return 'boolean'
            if any(t == 'real' for t in tipos):
                return 'real'
            return 'integer'
        elif node.type == "acesso_array":
            nome_array = node.leaf
            
            # procura na tabela de símbolos o tipo do array
            tipo_array = self.symbol_table.get(nome_array)
            
            if tipo_array and isinstance(tipo_array, dict) and "tipo_elemento" in tipo_array:
                return tipo_array["tipo_elemento"]
            return None
        else:
            raise ValueError(f"Tipo desconhecido de nó: {node.type}")

    def get_code(self):
        return '\n'.join(self.code)

# Lê AST do ficheiro gerado
with open("AST", "r") as f:
    ast_text = f.read()
    ast = eval(ast_text) 

# Geração de código
cg = CodeGenerator()
cg.generate_code(ast)
print(cg.get_code())