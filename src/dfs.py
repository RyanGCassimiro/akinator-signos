from node import Node

def dfs(root):
    if root is None:
        return []
    visited = []
    
    # Faz a visita no nó atual
    def _traverse(node):
        if node is None:
            return
        visited.append(node)
        _traverse(node.yes)
        _traverse(node.no)
    
    _traverse(root)
    return visited

def dfs_search_sign(root, target_sign):
    if root is None:
        return None

    if root.is_leaf() and root.answer == target_sign:
        return root

    result = dfs_search_sign(root.yes, target_sign)
    if result is not None:
        return result

    return dfs_search_sign(root.no, target_sign)  # ← root.no


def dfs_path(root, target_sign):
    if root is None:
        return []  # ← [] não None

    if root.is_leaf():
        if root.answer == target_sign:
            return [root]
        return []

    path_yes = dfs_path(root.yes, target_sign)
    if path_yes:
        return [root] + path_yes

    path_no = dfs_path(root.no, target_sign)
    if path_no:
        return [root] + path_no

    return []