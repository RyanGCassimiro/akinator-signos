from node import Node

def dfs(node, path=None):
    if path is None:
        path = []

    if node is None:
        return path
    
    # Faz a visita no nó atual
    if node.is_leaf():
        path.append(f"Resposta: {node.answer}")
    else:
        path.append(f"Resposta: {node.question}")
    
    # Recurssão: vai para o filho esquerdo primeiro, "yes"
    dfs(node.yes, path)

    # Depois vai para o filho direito, "no"
    dfs(node.no, path)

    return path