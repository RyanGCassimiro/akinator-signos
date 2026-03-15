from collections import deque

def bfs(root):
    """
    Realiza a Busca em Largura (BFS) na árvore de decisão.
    Percorre todos os nós nível por nível, da raiz até as folhas.
    Retorna uma lista com todos os nós visitados em ordem de nível.

    Args:
        raiz: Nó raiz da árvore (objeto Node)

    Returns:
        list: Lista de nós visitados em ordem BFS
    """
    if root is None:
        return []

    visited = []
    queue = deque()
    queue.append(root)

    while queue:
        current_node = queue.popleft()
        visited.append(current_node)

        # Adiciona filhos na fila (esquerda = sim, direita = não)
        if current_node.yes is not None:
            queue.append(current_node.yes)
        if current_node.no is not None:
            queue.append(current_node.no)

    return visited


def bfs_search_sign(root, target_sign):
    """
    Busca um signo específico na árvore usando BFS.

    Args:
        raiz: Nó raiz da árvore
        signo_alvo (str): Nome do signo a ser encontrado

    Returns:
        Node | None: O nó folha correspondente ao signo, ou None se não encontrado
    """
    if root is None:
        return None

    queue = deque()
    queue.append(root)

    while queue:
        current_node = queue.popleft()

        # Verifica se é o signo que estamos procurando
        if current_node.eh_folha() and current_node.answer == target_sign:
            return current_node

        if current_node.yes is not None:
            queue.append(current_node.yes)
        if current_node.no is not None:
            queue.append(current_node.no)

    return None

def bfs_level_by_level(root):
    """
    Retorna os nós da árvore organizados por nível.
    Útil para visualização da árvore no Streamlit.

    Args:
        raiz: Nó raiz da árvore

    Returns:
        list[list]: Lista de listas, onde cada sublista contém os nós de um nível
    """
    if root is None:
        return []

    levels = []
    queue = deque()
    queue.append(root)

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)

            if node.yes is not None:
                queue.append(node.yes)
            if node.no is not None:
                queue.append(node.no)

        levels.append(current_level)

    return levels