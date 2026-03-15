from collections import deque

def bfs(raiz):
    """
    Realiza a Busca em Largura (BFS) na árvore de decisão.
    Percorre todos os nós nível por nível, da raiz até as folhas.
    Retorna uma lista com todos os nós visitados em ordem de nível.

    Args:
        raiz: Nó raiz da árvore (objeto Node)

    Returns:
        list: Lista de nós visitados em ordem BFS
    """
    if raiz is None:
        return []

    visitados = []
    fila = deque()
    fila.append(raiz)

    while fila:
        no_atual = fila.popleft()
        visitados.append(no_atual)

        # Adiciona filhos na fila (esquerda = sim, direita = não)
        if no_atual.sim is not None:
            fila.append(no_atual.sim)
        if no_atual.nao is not None:
            fila.append(no_atual.nao)

    return visitados


def bfs_buscar_signo(raiz, signo_alvo):
    """
    Busca um signo específico na árvore usando BFS.

    Args:
        raiz: Nó raiz da árvore
        signo_alvo (str): Nome do signo a ser encontrado

    Returns:
        Node | None: O nó folha correspondente ao signo, ou None se não encontrado
    """
    if raiz is None:
        return None

    fila = deque()
    fila.append(raiz)

    while fila:
        no_atual = fila.popleft()

        # Verifica se é o signo que estamos procurando
        if no_atual.eh_folha() and no_atual.resposta == signo_alvo:
            return no_atual

        if no_atual.sim is not None:
            fila.append(no_atual.sim)
        if no_atual.nao is not None:
            fila.append(no_atual.nao)

    return None

def bfs_nivel_por_nivel(raiz):
    """
    Retorna os nós da árvore organizados por nível.
    Útil para visualização da árvore no Streamlit.

    Args:
        raiz: Nó raiz da árvore

    Returns:
        list[list]: Lista de listas, onde cada sublista contém os nós de um nível
    """
    if raiz is None:
        return []

    niveis = []
    fila = deque()
    fila.append(raiz)

    while fila:
        tamanho_nivel = len(fila)
        nivel_atual = []

        for _ in range(tamanho_nivel):
            no = fila.popleft()
            nivel_atual.append(no)

            if no.sim is not None:
                fila.append(no.sim)
            if no.nao is not None:
                fila.append(no.nao)

        niveis.append(nivel_atual)

    return niveis
