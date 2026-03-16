import pytest
from tree import build_tree
from dfs import dfs, dfs_search_sign, dfs_path
from bfs import bfs, bfs_search_sign, bfs_level_by_level

@pytest.fixture
def tree():
    return build_tree()

# --- Testes para o DFS ----

def test_dfs_none_returns_empty():
    assert dfs(None) == []

def test_dfs_visits_all_nodes(tree):
    assert len(dfs(tree)) == 23           # 11 perguntas + 12 signos = 23 nós

def test_dfs_root_is_first(tree):
    assert dfs(tree)[0] is tree

def test_dfs_search_sign_finds_aries(tree):
    result = dfs_search_sign(tree, "Áries 21/03 - 20/04")
    assert result is not None and "Áries" in result.answer

def test_dfs_search_sign_not_found(tree):
    assert dfs_search_sign(tree, "Signo Inexistente") is None

def test_dfs_path_starts_at_root(tree):
    path = dfs_path(tree, "Áries 21/03 - 20/04")
    assert path[0] is tree

def test_dfs_path_ends_at_sign(tree):
    path = dfs_path(tree, "Áries 21/03 - 20/04")
    assert path[-1].answer

# --- Testes para o BFS ----

def test_bfs_none_returns_empty():
    assert bfs(None) == []

def test_bfs_visits_all_nodes(tree):
    assert len(bfs(tree)) == 23           # 11 perguntas + 12 signos = 23 nós

def test_bfs_root_is_first(tree):
    assert bfs(tree)[0] is tree

def test_bfs_search_sign_finds_pisces(tree):
    result = bfs_search_sign(tree, "Peixes 20/02 - 20/03")
    assert result is not None and "Peixes" in result.answer

def test_bfs_search_sign_not_found(tree):
    assert bfs_search_sign(tree, "Signo Inexistente") is None

def test_bfs_level_by_level_root_is_first(tree):
    levels = bfs_level_by_level(tree)
    assert levels[0][0] is tree

def test_bfs_level_by_level_total_nodes(tree):
    levels = bfs_level_by_level(tree)
    assert sum(len(l) for l in levels) == 23         # 11 perguntas + 12 signos = 23 nós 

