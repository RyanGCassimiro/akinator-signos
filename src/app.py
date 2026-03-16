import streamlit as st
import graphviz
from pathlib import Path
import base64
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from node import Node
from tree import build_tree
from dfs import dfs, dfs_search_sign, dfs_path
from bfs import bfs, bfs_search_sign, bfs_level_by_level

st.set_page_config(
    page_title="Akinator Signos",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "no_atual" not in st.session_state:
    st.session_state.no_atual = None
if "historico" not in st.session_state:
    st.session_state.historico = []
if "nos_visitados" not in st.session_state:
    st.session_state.nos_visitados = []
if "algoritmo" not in st.session_state:
    st.session_state.algoritmo = "DFS"
if "jogo_encerrado" not in st.session_state:
    st.session_state.jogo_encerrado = False
if "tema" not in st.session_state:
    st.session_state.tema = "Escuro"

TEMAS = {
    "Escuro": {
        "bg": "#0a0a14",
        "sidebar_bg": "#0f0f1e",
        "sidebar_border": "#1e1e35",
        "sidebar_text": "#c4b5fd",
        "card_bg": "#12122a",
        "card_border": "#1e1e40",
        "card_text": "#c4b5fd",
        "section_title": "#e0d7ff",
        "accent": "#a78bfa",
        "accent2": "#60a5fa",
        "muted": "#4a4a6a",
        "muted2": "#6b7280",
        "step_bg": "#0f0f24",
        "step_border": "#1e1e35",
        "debug_bg": "#0d0d1f",
        "debug_border": "#1e1e35",
        "history_border": "#1a1a2e",
        "node_bg": "#12122a",
        "graph_bg": "#0d0d1f",
        "result_bg": "linear-gradient(135deg,#1a0a3e,#2d1b69)",
        "result_border": "#a78bfa",
        "result_text": "#e0d7ff",
        "header_gradient": "rgba(10,10,20,0.95)",
        "header_title": "#e0d7ff",
        "header_sub": "#a78bfa",
    },
    "Claro": {
        "bg": "#f8f7ff",
        "sidebar_bg": "#ede9fe",
        "sidebar_border": "#c4b5fd",
        "sidebar_text": "#3b0764",
        "card_bg": "#ffffff",
        "card_border": "#c4b5fd",
        "card_text": "#3b0764",
        "section_title": "#3b0764",
        "accent": "#6d28d9",
        "accent2": "#2563eb",
        "muted": "#6d28d9",
        "muted2": "#7c3aed",
        "step_bg": "#f3e8ff",
        "step_border": "#c4b5fd",
        "debug_bg": "#f3e8ff",
        "debug_border": "#c4b5fd",
        "history_border": "#ddd6fe",
        "node_bg": "#ffffff",
        "graph_bg": "#f3e8ff",
        "result_bg": "linear-gradient(135deg,#ede9fe,#ddd6fe)",
        "result_border": "#6d28d9",
        "result_text": "#3b0764",
        "header_gradient": "rgba(248,247,255,0.95)",
        "header_title": "#3b0764",
        "header_sub": "#6d28d9",
    },
}

t = TEMAS[st.session_state.tema]

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Raleway:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Raleway', sans-serif; }
    .stButton > button { font-family: 'Raleway', sans-serif !important; font-weight: 600 !important; border-radius: 10px !important; border: none !important; padding: 14px 20px !important; font-size: 16px !important; transition: all 0.2s !important; }
    .btn-sim .stButton > button { background: linear-gradient(135deg, #166534, #16a34a) !important; color: white !important; }
    .btn-nao .stButton > button { background: linear-gradient(135deg, #7f1d1d, #dc2626) !important; color: white !important; }
    .icon-sim { background: #14532d; color: #4ade80; }
    .icon-nao { background: #7f1d1d; color: #f87171; }
    .icon-info { background: #1e3a5f; color: #60a5fa; }
    .history-icon { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
    #MainMenu, footer { visibility: hidden; }
    header { background: transparent !important; }
    .block-container { padding-top: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<style>
    .stApp {{ background: {t['bg']}; }}
    section[data-testid="stSidebar"] {{ background: {t['sidebar_bg']} !important; border-right: 1px solid {t['sidebar_border']}; }}
    section[data-testid="stSidebar"] * {{ color: {t['sidebar_text']} !important; }}
    .sidebar-title {{ font-family: 'Cinzel', serif; font-size: 13px; font-weight: 700; color: {t['accent']} !important; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; }}
    .header-banner {{ position: relative; width: 100%; height: 400px; border-radius: 16px; overflow: hidden; margin-bottom: 28px; }}
    .header-banner img {{ width: 100%; height: 100%; object-fit: cover; object-position: center 40%; filter: brightness(0.65); }}
    .header-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 28px 32px; background: linear-gradient(to top, {t['header_gradient']} 0%, transparent 100%); }}
    .header-title {{ font-family: 'Cinzel', serif; font-size: 32px; font-weight: 900; color: {t['header_title']}; text-shadow: 0 0 30px rgba(167,139,250,0.5); margin: 0; }}
    .header-subtitle {{ font-family: 'Raleway', sans-serif; font-size: 15px; color: {t['header_sub']}; font-style: italic; margin: 6px 0 0 0; }}
    .stat-card {{ background: {t['card_bg']}; border: 1px solid {t['card_border']}; border-radius: 14px; padding: 24px 20px; text-align: center; }}
    .stat-number {{ font-family: 'Cinzel', serif; font-size: 36px; font-weight: 900; color: {t['accent']}; display: block; }}
    .stat-label {{ font-size: 11px; color: {t['muted']}; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px; display: block; }}
    .info-card {{ background: {t['card_bg']}; border: 1px solid {t['card_border']}; border-radius: 14px; padding: 24px; margin-bottom: 20px; color: {t['card_text']}; font-size: 15px; line-height: 1.8; }}
    .section-title {{ font-family: 'Cinzel', serif; font-size: 16px; color: {t['section_title']}; margin: 24px 0 12px 0; padding-left: 12px; border-left: 3px solid {t['accent']}; }}
    .step-item {{ display: flex; gap: 14px; align-items: flex-start; margin-bottom: 14px; padding: 14px; background: {t['step_bg']}; border-radius: 10px; border: 1px solid {t['step_border']}; }}
    .step-num {{ width: 28px; height: 28px; background: {t['accent']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 13px; flex-shrink: 0; }}
    .step-text {{ color: {t['card_text']}; font-size: 14px; padding-top: 3px; line-height: 1.5; }}
    .dira-header {{ background: {t['card_bg']}; border: 1px solid {t['accent']}; border-radius: 14px; padding: 20px; display: flex; gap: 18px; align-items: center; margin-bottom: 16px; }}
    .dira-question {{ font-family: 'Cinzel', serif; font-size: 20px; color: {t['section_title']}; line-height: 1.4; }}
    .dira-label {{ font-size: 12px; color: {t['accent']}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }}
    .debug-panel {{ background: {t['debug_bg']}; border: 1px solid {t['debug_border']}; border-radius: 14px; padding: 20px; }}
    .debug-title {{ font-size: 11px; color: {t['muted']}; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px; }}
    .history-item {{ display: flex; gap: 10px; margin-bottom: 14px; padding-bottom: 14px; border-bottom: 1px solid {t['history_border']}; }}
    .history-q {{ color: {t['muted2']}; font-size: 12px; }}
    .history-a {{ color: {t['section_title']}; font-size: 13px; font-weight: 600; margin-top: 2px; }}
    .icon-current {{ background: {t['accent']}; color: white; }}
    .node-stats {{ background: {t['node_bg']}; border: 1px solid {t['debug_border']}; border-radius: 10px; padding: 14px; margin-top: 16px; }}
    .node-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; }}
    .node-key {{ color: {t['muted2']}; }}
    .node-val {{ color: {t['accent']}; font-weight: 700; }}
    .result-card {{ background: {t['result_bg']}; border: 2px solid {t['result_border']}; border-radius: 16px; padding: 32px; text-align: center; margin: 20px 0; }}
    .result-sign {{ font-family: 'Cinzel', serif; font-size: 40px; color: {t['result_text']}; text-shadow: 0 0 30px rgba(167,139,250,0.6); }}
    .result-label {{ font-size: 13px; color: {t['accent']}; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }}
</style>
""",
    unsafe_allow_html=True,
)


def get_img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def initial_history(algoritmo, raiz_question):
    raiz_preview = raiz_question[:20]
    return [
        {
            "tipo": "info",
            "pergunta": "Inicio da sessao",
            "resposta": algoritmo + " ativo - raiz: " + raiz_preview,
        }
    ]


@st.cache_resource
def get_tree():
    return build_tree()


tree = get_tree()
ASSETS_PATH = Path(__file__).parent.parent / "assets" / "madame_dira.png"


def render_tree(root, current_node=None, visited_nodes=None):
    dot = graphviz.Digraph()
    dot.attr(bgcolor=t["graph_bg"], rankdir="TB")
    dot.attr("node", fontname="Raleway", fontsize="10")
    dot.attr("edge", color="#2d2d4e", penwidth="1.2")
    if visited_nodes is None:
        visited_nodes = []
    counter = [0]

    def add_nodes(node):
        if node is None:
            return None
        my_id = str(counter[0])
        counter[0] += 1
        label = node.question if node.question else node.answer
        if label and len(label) > 22:
            label = label[:20] + "..."
        is_current = node is current_node
        is_visited = any(n is node for n in visited_nodes)
        is_leaf = node.is_leaf()
        if is_current:
            dot.node(
                my_id,
                label,
                shape="circle" if not is_leaf else "box",
                style="filled",
                fillcolor="#2d1b69",
                color="#a78bfa",
                fontcolor="#e0d7ff",
                penwidth="2.5",
            )
        elif is_visited:
            dot.node(
                my_id,
                label,
                shape="circle" if not is_leaf else "box",
                style="filled",
                fillcolor="#1a1a35",
                color="#6d28d9",
                fontcolor="#c4b5fd",
                penwidth="1.5",
            )
        elif is_leaf:
            dot.node(
                my_id,
                label,
                shape="box",
                style="filled,rounded",
                fillcolor="#0f0f22",
                color="#2d2d4e",
                fontcolor="#6b7280",
            )
        else:
            dot.node(
                my_id,
                label,
                shape="circle",
                style="filled",
                fillcolor="#0f0f22",
                color="#2d2d4e",
                fontcolor="#6b7280",
            )
        if node.yes:
            yes_id = add_nodes(node.yes)
            edge_color = "#4ade80" if (is_visited or is_current) else "#1e3a2e"
            dot.edge(
                my_id,
                yes_id,
                label="Sim",
                color=edge_color,
                fontcolor="#4ade80",
                fontsize="9",
            )
        if node.no:
            no_id = add_nodes(node.no)
            edge_color = "#f87171" if (is_visited or is_current) else "#3a1e1e"
            dot.edge(
                my_id,
                no_id,
                label="Nao",
                color=edge_color,
                fontcolor="#f87171",
                fontsize="9",
            )
        return my_id

    add_nodes(root)
    return dot


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">✨ Akinator Signos</div>', unsafe_allow_html=True
    )
    if st.button("🏠  Início", use_container_width=True):
        st.session_state.pagina = "inicio"
    if st.button("🎮  Jogar", use_container_width=True):
        st.session_state.pagina = "jogar"
        st.session_state.no_atual = tree
        st.session_state.historico = initial_history(
            st.session_state.algoritmo, tree.question
        )
        st.session_state.nos_visitados = []
        st.session_state.jogo_encerrado = False
    if st.button("🌳  Ver Árvore", use_container_width=True):
        st.session_state.pagina = "arvore"
    st.markdown("---")
    if st.button("📊  BFS vs DFS", use_container_width=True):
        st.session_state.pagina = "comparacao"
    if st.button("ℹ️  Sobre", use_container_width=True):
        st.session_state.pagina = "sobre"
    st.markdown("---")
    st.markdown(
        f'<div style="color:{t["muted2"]};font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Algoritmo ativo</div>',
        unsafe_allow_html=True,
    )
    algo = st.selectbox(
        "",
        ["DFS", "BFS"],
        label_visibility="collapsed",
        index=0 if st.session_state.algoritmo == "DFS" else 1,
    )
    st.session_state.algoritmo = algo
    st.markdown("---")
    st.markdown(
        f'<div style="color:{t["muted2"]};font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">🎨 Tema</div>',
        unsafe_allow_html=True,
    )
    tema_escolhido = st.selectbox(
        "tema",
        ["Escuro", "Claro"],
        label_visibility="collapsed",
        index=0 if st.session_state.tema == "Escuro" else 1,
    )
    if tema_escolhido != st.session_state.tema:
        st.session_state.tema = tema_escolhido
        st.rerun()

# ── PAGINA INICIAL ────────────────────────────────────────────────────────────
if st.session_state.pagina == "inicio":
    if ASSETS_PATH.exists():
        img_b64 = get_img_b64(ASSETS_PATH)
        st.markdown(
            '<div class="header-banner"><img src="data:image/png;base64,'
            + img_b64
            + '" />'
            '<div class="header-overlay"><p class="header-title">✨ Madame Dira te desafia</p>'
            '<p class="header-subtitle">Pense em um signo... e ela vai adivinhar.</p></div></div>',
            unsafe_allow_html=True,
        )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="stat-card"><span class="stat-number">12</span><span class="stat-label">Signos na árvore</span></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="stat-card"><span class="stat-number">23</span><span class="stat-label">Nós no total</span></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="stat-card"><span class="stat-number">2</span><span class="stat-label">Algoritmos (BFS & DFS)</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown("")
    st.markdown(
        '<div class="section-title">Sobre o sistema</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card">Madame Dira usa uma <strong style="color:{t["accent"]}">arvore binária de decisão</strong> para adivinhar o seu signo do zodíaco através de perguntas sobre seu aniversário e características do signo.<br><br>Cada resposta que você da navega por um caminho da árvore usando <strong style="color:{t["accent"]}">BFS</strong> (busca em largura) ou <strong style="color:{t["accent"]}">DFS</strong> (busca em profundidade) até chegar na resposta final.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title">Como jogar</div>', unsafe_allow_html=True)
    steps = [
    "Pense em um signo do zodíaco — pode ser o seu ou qualquer outro.",
    "Responda às perguntas de Madame Dira com Sim ou Não.",
    "Veja a árvore se atualizar em tempo real enquanto o caminho é percorrido.",
    "Descubra se Madame Dira acertou e compare os algoritmos!",
    ]
    for i, step in enumerate(steps, 1):
        st.markdown(
            '<div class="step-item"><div class="step-num">'
            + str(i)
            + '</div><div class="step-text">'
            + step
            + "</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("")
    if st.button("🔮  Iniciar Jogo"):
        st.session_state.pagina = "jogar"
        st.session_state.no_atual = tree
        st.session_state.historico = initial_history(
            st.session_state.algoritmo, tree.question
        )
        st.session_state.nos_visitados = []
        st.session_state.jogo_encerrado = False
        st.rerun()

# ── PAGINA JOGAR ──────────────────────────────────────────────────────────────
elif st.session_state.pagina == "jogar":
    no_atual = st.session_state.no_atual
    if no_atual is None:
        st.session_state.no_atual = tree
        no_atual = tree
    col_game, col_debug = st.columns([2.2, 1])
    with col_game:
        if st.session_state.jogo_encerrado or (no_atual and no_atual.is_leaf()):
            answer = no_atual.answer if no_atual else "?"
            st.markdown(
                '<div class="result-card"><div class="result-label">🔮 Madame Dira adivinhou...</div><div class="result-sign">'
                + answer
                + "</div></div>",
                unsafe_allow_html=True,
            )
            if st.button("🔄  Jogar novamente", use_container_width=True):
                st.session_state.no_atual = tree
                st.session_state.historico = initial_history(
                    st.session_state.algoritmo, tree.question
                )
                st.session_state.nos_visitados = []
                st.session_state.jogo_encerrado = False
                st.rerun()
        else:
            if ASSETS_PATH.exists():
                img_b64 = get_img_b64(ASSETS_PATH)
                avatar_html = f'<img src="data:image/png;base64,{img_b64}" style="width:72px;height:72px;border-radius:50%;object-fit:cover;object-position:center 15%;border:2px solid {t["accent"]};" />'
            else:
                avatar_html = f'<div style="width:72px;height:72px;border-radius:50%;background:{t["accent"]};display:flex;align-items:center;justify-content:center;font-size:28px;">🔮</div>'
            st.markdown(
                '<div class="dira-header">'
                + avatar_html
                + '<div><div class="dira-label">🔮 Madame Dira pergunta...</div><div class="dira-question">'
                + no_atual.question
                + "</div></div></div>",
                unsafe_allow_html=True,
            )
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.markdown('<div class="btn-sim">', unsafe_allow_html=True)
                if st.button("✓  Sim", use_container_width=True, key="btn_sim"):
                    st.session_state.nos_visitados.append(no_atual)
                    st.session_state.historico.append(
                        {
                            "tipo": "sim",
                            "pergunta": no_atual.question,
                            "resposta": "Sim → ramo esquerdo",
                        }
                    )
                    st.session_state.no_atual = no_atual.yes
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with btn_col2:
                st.markdown('<div class="btn-nao">', unsafe_allow_html=True)
                if st.button("✗  Nao", use_container_width=True, key="btn_nao"):
                    st.session_state.nos_visitados.append(no_atual)
                    st.session_state.historico.append(
                        {
                            "tipo": "nao",
                            "pergunta": no_atual.question,
                            "resposta": "Nao → ramo direito",
                        }
                    )
                    st.session_state.no_atual = no_atual.no
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="color:{t["muted"]};font-size:11px;letter-spacing:1.5px;text-transform:uppercase;margin:20px 0 10px 0;">🌳 Arvore de decisao — no atual destacado</div>',
            unsafe_allow_html=True,
        )
        dot = render_tree(
            tree, current_node=no_atual, visited_nodes=st.session_state.nos_visitados
        )
        st.graphviz_chart(dot, use_container_width=True)
    with col_debug:
        st.markdown('<div class="debug-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="debug-title">📋 Painel de debug</div>', unsafe_allow_html=True
        )
        algo_col1, algo_col2 = st.columns(2)
        with algo_col1:
            s = (
                f"background:{t['accent']};color:white;border:1px solid {t['accent']};"
                if st.session_state.algoritmo == "DFS"
                else f"background:{t['card_bg']};color:{t['muted']};border:1px solid {t['card_border']};"
            )
            st.markdown(
                f'<div style="padding:8px;border-radius:8px;text-align:center;font-size:13px;font-weight:700;{s}">DFS</div>',
                unsafe_allow_html=True,
            )
        with algo_col2:
            s = (
                f"background:{t['accent']};color:white;border:1px solid {t['accent']};"
                if st.session_state.algoritmo == "BFS"
                else f"background:{t['card_bg']};color:{t['muted']};border:1px solid {t['card_border']};"
            )
            st.markdown(
                f'<div style="padding:8px;border-radius:8px;text-align:center;font-size:13px;font-weight:700;{s}">BFS</div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<hr style="border:none;border-top:1px solid {t["history_border"]};margin:14px 0;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="color:{t["muted2"]};font-size:11px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;">Historico de perguntas</div>',
            unsafe_allow_html=True,
        )
        icon_map = {
            "sim": '<div class="history-icon icon-sim">S</div>',
            "nao": '<div class="history-icon icon-nao">N</div>',
            "info": '<div class="history-icon icon-info">→</div>',
        }
        for item in st.session_state.historico:
            icon_html = icon_map.get(item["tipo"], icon_map["info"])
            st.markdown(
                '<div class="history-item">'
                + icon_html
                + '<div><div class="history-q">'
                + item["pergunta"]
                + '</div><div class="history-a">'
                + item["resposta"]
                + "</div></div></div>",
                unsafe_allow_html=True,
            )
        if no_atual and not no_atual.is_leaf():
            preview = no_atual.question[:40]
            st.markdown(
                f'<div class="history-item" style="border-bottom:none;"><div class="history-icon icon-current">?</div><div><div class="history-q" style="color:{t["accent"]};">Pergunta atual</div><div class="history-a">{preview}...</div></div></div>',
                unsafe_allow_html=True,
            )
        nivel = len(st.session_state.nos_visitados)
        total = len(dfs(tree))
        st.markdown(
            f'<div class="node-stats"><div class="node-row"><span class="node-key">Nos visitados</span><span class="node-val">{nivel} / {total}</span></div><div class="node-row"><span class="node-key">Profundidade atual</span><span class="node-val">Nivel {nivel}</span></div><div class="node-row" style="margin-bottom:0;"><span class="node-key">Algoritmo</span><span class="node-val">{st.session_state.algoritmo} · pre-ordem</span></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ── PAGINA VER ARVORE ─────────────────────────────────────────────────────────
elif st.session_state.pagina == "arvore":
    st.markdown(
        '<div class="section-title">🌳 Arvore de decisao completa</div>',
        unsafe_allow_html=True,
    )
    dot = render_tree(tree)
    st.graphviz_chart(dot, use_container_width=True)
    st.markdown(
        '<div class="section-title">Ordem de visita — DFS</div>', unsafe_allow_html=True
    )
    dfs_order = dfs(tree)
    dfs_labels = [n.question or n.answer for n in dfs_order]
    st.markdown(
        '<div class="info-card">'
        + " → ".join(
            [
                f'<span style="color:{t["accent"]}">' + l[:20] + "</span>"
                for l in dfs_labels
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">Ordem de visita — BFS</div>', unsafe_allow_html=True
    )
    bfs_order = bfs(tree)
    bfs_labels = [n.question or n.answer for n in bfs_order]
    st.markdown(
        '<div class="info-card">'
        + " → ".join(
            [
                f'<span style="color:{t["accent2"]}">' + l[:20] + "</span>"
                for l in bfs_labels
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

# ── PAGINA COMPARACAO ─────────────────────────────────────────────────────────
elif st.session_state.pagina == "comparacao":
    st.markdown(
        '<div class="section-title">📊 BFS vs DFS — Analise comparativa</div>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="info-card"><div style="font-family:Cinzel,serif;font-size:16px;color:{t["accent2"]};margin-bottom:12px;">BFS — Busca em Largura</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">ESTRUTURA</div><div style="margin-bottom:12px;">Fila (deque) — explora nÍvel por nÍvel</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">VANTAGENS</div><div style="margin-bottom:12px;">Garante o caminho mais curto. Boa para árvores rasas.</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">DESVANTAGENS</div><div>Usa mais memória — guarda todos os nós do nÍvel atual na fila.</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="info-card"><div style="font-family:Cinzel,serif;font-size:16px;color:{t["accent"]};margin-bottom:12px;">DFS — Busca em Profundidade</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">ESTRUTURA</div><div style="margin-bottom:12px;">Recursão (pilha implícita), desce por um ramo até o fim</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">VANTAGENS</div><div style="margin-bottom:12px;">Usa menos memória. Ideal para árvores profundas como esta.</div><div style="color:{t["muted2"]};font-size:12px;margin-bottom:8px;">DESVANTAGENS</div><div>Pode demorar mais em árvores largas. Não garante caminho mínimo.</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="section-title">Nesta árvore de signos</div>',
        unsafe_allow_html=True,
    )
    dfs_count = len(dfs(tree))
    bfs_count = len(bfs(tree))
    st.markdown(
        f'<div class="info-card">Ambos os algoritmos visitam os mesmos <strong style="color:{t["accent"]}">{dfs_count} nós</strong> no total, porém em <strong style="color:{t["accent"]}">ordens diferentes</strong>.<br><br>O <strong style="color:{t["accent"]}">DFS</strong> desce por um ramo completo antes de voltar; ideal para o jogo, pois segue o caminho das respostas diretamente ate o signo.<br><br>O <strong style="color:{t["accent2"]}">BFS</strong> avalia todas as perguntas do mesmo nível antes de descer, útil para garantir que nenhuma pergunta de mesmo nível seja ignorada.</div>',
        unsafe_allow_html=True,
    )

    # ── PAGINA SOBRE ──────────────────────────────────────────────────────────────
elif st.session_state.pagina == "sobre":
    st.markdown(
        '<div class="section-title">ℹ️ Sobre o projeto</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><strong style="color:{t["accent"]}">Akinator Signos</strong> é um projeto acadêmico desenvolvido para a disciplina de <strong>Estrutura de Dados Avançada</strong>.<br><br>O sistema implementa uma <strong style="color:{t["accent"]}">árvore binária de decisão</strong> com 12 signos do zodíaco, percorrida pelos algoritmos <strong>BFS</strong> e <strong>DFS</strong>.<br><br><strong style="color:{t["muted2"]}">Desenvolvido por:</strong><br>Wanessa Costa & Ryan Cassimiro<br><br><strong style="color:{t["muted2"]}">Tecnologias:</strong><br>Python · Streamlit · Graphviz · pytest</div>',
        unsafe_allow_html=True,
    )