from node import Node

# Função DFS, percorre todos os nós em pré-ordem (raiz -> yes -> no)
def dfs(root):
    if root is None:
        # Lista de nós visitados, wm ordem DFS pré-ordem
        return []
    visited = []
    
    # Faz a visita no nó atual
    def _traverse(node):
        if node is None:
            return
        # Visita o nó atual antes dos filhos
        visited.append(node)
        # Percorre recurssivamente o ramo sim primeiro
        _traverse(node.yes)
        # Depois percorre o ramo não
        _traverse(node.no)
    
    _traverse(root)
    return visited

# Função para buscar um signo específico usando DFS
def dfs_search_sign(root, target_sign):
    if root is None:
        return None

    # Caso base: verifica se o nó atual é o signo procurado
    if root.is_leaf() and root.answer == target_sign:
        return root

    # Busca no ramo sim primeiro
    result = dfs_search_sign(root.yes, target_sign)
    if result is not None:
        return result

    # Se não encontrou no ramo sim, busca no ramo não
    return dfs_search_sign(root.no, target_sign)  # ← root.no

# Função para encontrar o caminho até um signo específico usando DFS
def dfs_path(root, target_sign):
    if root is None:
        return []  # ← [] não None

    # Caso base: nó folha encontrado, verifica se é o signo alvo
    if root.is_leaf():
        if root.answer == target_sign:
            return [root]
        return []

    # Busca no ramo sim primeiro
    path_yes = dfs_path(root.yes, target_sign)
    if path_yes:
        return [root] + path_yes
    
    # Se não encontrou no ramo sim, tenta no ramo não
    path_no = dfs_path(root.no, target_sign)
    if path_no:
        return [root] + path_no

    # Se não encontrou o signo em nenhum dos ramos, retorna lista vazia
    return []