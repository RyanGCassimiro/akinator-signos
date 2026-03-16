import pytest
from tree import build_tree

@pytest.fixture
def tree():
    return build_tree()

# ── Estrutura da raiz ──────────────────────────────────────────────────────────

def test_root_is_not_leaf(tree):
    assert not tree.is_leaf()

def test_root_has_question(tree):
    assert tree.question is not None

def test_root_has_children(tree):
    assert tree.yes is not None
    assert tree.no is not None


# ── Todos os 12 signos estão acessíveis ───────────────────────────────────────

def get_all_leaves(node, leaves=None):
    if leaves is None:
        leaves = []
    if node is None:
        return leaves
    if node.is_leaf():
        leaves.append(node.answer)
    else:
        get_all_leaves(node.yes, leaves)
        get_all_leaves(node.no, leaves)
    return leaves

def test_tree_has_12_leaves(tree):
    leaves = get_all_leaves(tree)
    assert len(leaves) == 12

def test_all_signs_present(tree):
    leaves = get_all_leaves(tree)
    expected_signs = [
        "Áries", "Touro", "Gêmeos", "Câncer",
        "Leão", "Virgem", "Libra", "Escorpião",
        "Sagitário", "Capricórnio", "Aquário", "Peixes"
    ]
    for sign in expected_signs:
        assert any(sign in leaf for leaf in leaves), f"{sign} não encontrado na árvore"


# ── Caminhos corretos para cada signo ─────────────────────────────────────────
# Convenção: True = sim, False = não

def navigate(tree, answers):
    """Percorre a árvore seguindo a lista de respostas e retorna o nó folha."""
    current = tree
    for answer in answers:
        assert not current.is_leaf(), "Árvore terminou antes das respostas acabarem"
        current = current.yes if answer else current.no
    assert current.is_leaf(), "Respostas acabaram antes de chegar num signo"
    return current.answer


# Fogo ou Ar? Fogo? Antes de Maio?
def test_aries(tree):
    result = navigate(tree, [True, True, True])
    assert "Áries" in result

# Fogo ou Ar? Fogo? Não antes de Maio. Antes de Setembro?
def test_leo(tree):
    result = navigate(tree, [True, True, False, True])
    assert "Leão" in result

# Fogo ou Ar? Fogo? Não antes de Maio. Não antes de Setembro.
def test_sagittarius(tree):
    result = navigate(tree, [True, True, False, False])
    assert "Sagitário" in result

# Fogo ou Ar? Ar? Depois de Agosto? (sim = Libra)
def test_libra(tree):
    result = navigate(tree, [True, False, True])
    assert "Libra" in result

# Fogo ou Ar? Ar? Não depois de Agosto. Antes de Março? (sim = Aquário)
def test_aquarius(tree):
    result = navigate(tree, [True, False, False, True])
    assert "Aquário" in result

# Fogo ou Ar? Ar? Não depois de Agosto. Não antes de Março. (= Gêmeos)
def test_gemini(tree):
    result = navigate(tree, [True, False, False, False])
    assert "Gêmeos" in result

# Terra ou Água? Terra? Antes de Julho? (sim = Touro)
def test_taurus(tree):
    result = navigate(tree, [False, True, True])
    assert "Touro" in result

# Terra ou Água? Terra? Não antes de Julho. Antes de Outubro? (sim = Virgem)
def test_virgo(tree):
    result = navigate(tree, [False, True, False, True])
    assert "Virgem" in result

# Terra ou Água? Terra? Não antes de Julho. Não antes de Outubro. (= Capricórnio)
def test_capricorn(tree):
    result = navigate(tree, [False, True, False, False])
    assert "Capricórnio" in result

# Terra ou Água? Água? Antes de Julho? Antes de Abril? (sim = Peixes)
def test_pisces(tree):
    result = navigate(tree, [False, False, True, True])
    assert "Peixes" in result

# Terra ou Água? Água? Antes de Julho? Não antes de Abril. (= Câncer)
def test_cancer(tree):
    result = navigate(tree, [False, False, True, False])
    assert "Câncer" in result

# Terra ou Água? Água? Não antes de Julho. (= Escorpião)
def test_scorpion(tree):
    result = navigate(tree, [False, False, False])
    assert "Escorpião" in result


# ── Propriedades dos nós internos ─────────────────────────────────────────────

def test_internal_nodes_have_no_answer(tree):
    def check(node):
        if node is None:
            return
        if not node.is_leaf():
            assert node.answer is None
            check(node.yes)
            check(node.no)
    check(tree)

def test_leaf_nodes_have_no_question(tree):
    def check(node):
        if node is None:
            return
        if node.is_leaf():
            assert node.question is None
        else:
            check(node.yes)
            check(node.no)
    check(tree)