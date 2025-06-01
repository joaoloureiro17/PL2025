from collections import namedtuple

Node = namedtuple("Node", ["type", "leaf", "children"])

with open("AST", "r") as f:
    ast_text = f.read()
    ast = eval(ast_text)

def construir_tabela_simbolos(node, tabela):
    if not isinstance(node, Node):
        return

    if node.type == "declaracoes":
        for declaracao in node.children:
            if declaracao.type == "declaracao":
                tipo = declaracao.leaf  # Ex: "integer", "string"
                lista_vars = declaracao.children[0]  # Node(type='variaveis')
                for var_node in lista_vars.children:
                    nome = var_node.leaf
                    if nome in tabela:
                        print(f"Erro: Variável '{nome}' já foi declarada.")
                    else:
                        tabela[nome] = tipo

            elif declaracao.type == "declaracao_array":
                info = declaracao.leaf  # dicionário com 'variaveis', 'limites', 'tipo'
                tipo_elemento = info["tipo"]
                lista_vars = info["variaveis"]
                for var_node in lista_vars.children:
                    nome = var_node.leaf
                    if nome in tabela:
                        print(f"Erro: Array '{nome}' já foi declarado.")
                    else:
                        # guardamos como tipo "array de tipo_elemento"
                        tabela[nome] = f"array[{info['limites'][0]}..{info['limites'][1]}] of {tipo_elemento}"
    else:
        for child in node.children:
            construir_tabela_simbolos(child, tabela)


def verificar_uso_variaveis(node, tabela, erros):
    if not isinstance(node, Node):
        return
    if node.type == "variavel":
        nome = node.leaf
        if nome not in tabela:
            erros.add(f"Erro: Variável '{nome}' usada mas não declarada.")
    elif node.type == "acesso_array":
        nome = node.leaf
        if nome not in tabela:
            erros.add(f"Erro: Array '{nome}' usado mas não declarado.")
    for child in node.children:
        if isinstance(child, Node):
            verificar_uso_variaveis(child, tabela, erros)

def inferir_tipo(node, tabela):
    if not isinstance(node, Node):
        return None
    if node.type == "inteiro":
        return "integer"
    elif node.type == "real":
        return "real"
    elif node.type == "string":
        return "string"
    elif node.type in ["boolean", "booleano"]:
        return "boolean"
    elif node.type == "variavel":
        return tabela.get(node.leaf)
    elif node.type == "not":
        tipo_expr = inferir_tipo(node.children[0], tabela)
        if tipo_expr == "boolean":
            return "boolean"
    elif node.type == "acesso_array":
        tipo_array = tabela.get(node.leaf)
        if tipo_array and tipo_array.startswith("array"):
            partes = tipo_array.split("of") # extraimos o tipo base a partir do "of"
            if len(partes) == 2:
                tipo_base = partes[1].strip()
                return tipo_base
        return None
    elif node.type == "binop":
        op = node.leaf
        lhs = inferir_tipo(node.children[0], tabela)
        rhs = inferir_tipo(node.children[1], tabela)

        if op in ["+", "-", "*", "div", "mod"]:
            if lhs == "integer" and rhs == "integer": #se ambos forem inteiros o resultado é inteiro
                return "integer"
            elif (lhs in ["integer", "real"]) and (rhs in ["integer", "real"]): #se pelo menos 1 for real o resultado é real
                return "real"
            else:
                return ("erro_operacao", op, lhs, rhs)
        elif op in ["=", "<", ">", "<=", ">=", "<>"]:
            if lhs == rhs:
                return "boolean"
            else:
                return ("erro_comparacao", lhs, rhs)
    elif node.type == "funcao":
        if node.leaf == "length":
            if len(node.children) != 1:
                return ("erro_funcao_length_uso", node.children)
            arg = node.children[0]
            if isinstance(arg, str):
                tipo = tabela.get(arg)
            elif isinstance(arg, Node):
                tipo = inferir_tipo(arg, tabela)
            else:
                tipo = None

            if tipo == "string":
                return "integer"
            else:
                return ("erro_funcao_length_tipo", tipo)
        
    return None

def verificar_tipos(node, tabela, erros):
    if not isinstance(node, Node):
        return

    if node.type == "atribuicao":
        var = node.children[0]
        expr = node.children[1]
        tipo_var = tabela.get(var.leaf)
        tipo_expr = inferir_tipo(expr, tabela)

        if isinstance(tipo_expr, tuple) and tipo_expr[0] == "erro_operacao":
            _, op, lhs, rhs = tipo_expr
            erros.add(f"Erro: operação '{op}' requer inteiros, mas recebeu '{lhs}' e '{rhs}'.")
            tipo_expr = "integer"  # evitar propagação do erro

        elif isinstance(tipo_expr, tuple) and tipo_expr[0] == "erro_comparacao":
            _, lhs, rhs = tipo_expr
            erros.add(f"Erro: comparação entre tipos diferentes: '{lhs}' e '{rhs}'.")
            tipo_expr = "boolean"

        if tipo_var != tipo_expr:
            erros.add(f"Erro: atribuição inválida '{var.leaf}' (esperado {tipo_var}, recebeu {tipo_expr})")
        return

    for child in node.children:
        if isinstance(child, Node):
            verificar_tipos(child, tabela, erros)

def analise_semantica(ast):
    tabela_simbolos = {}
    erros = set()  # usamos set para evitar repetições

    construir_tabela_simbolos(ast, tabela_simbolos)
    verificar_uso_variaveis(ast, tabela_simbolos, erros)
    verificar_tipos(ast, tabela_simbolos, erros)

    print("Tabela de Símbolos:")
    for var, tipo in tabela_simbolos.items():
        print(f"  {var}: {tipo}")

    print("\nErros encontrados:")
    if erros:
        for erro in sorted(erros):
            print(" -", erro)
    else:
        print(" Nenhum erro encontrado.")

analise_semantica(ast)
