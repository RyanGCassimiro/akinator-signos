# Akinator Signos ♈

Sistema de adivinhação de signos do zodíaco inspirado no Akinator.
Desenvolvido com árvore binária de decisão, BFS e DFS em Python.

## Tecnologias

- Python 3
- Streamlit
- pytest
- graphviz

## Como rodar

```bash
# Clone o repositório
git clone https://github.com/RyanGCassimiro/akinator-signos.git
cd akinator-signos

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o Streamlit
streamlit run src/app.py
```

## Estrutura do Projeto

```
akinator-signos/
├── venv/               ← ambiente virtual (não vai pro GitHub)
├── src/
│   ├── node.py         ← Classe Node
│   ├── arvore.py       ← Montagem da árvore de signos
│   ├── bfs.py          ← Algoritmo BFS
│   ├── dfs.py          ← Algoritmo DFS
│   ├── jogo.py         ← Simulação do jogo (input s/n)
│   └── app.py          ← Interface Streamlit
├── tests/
│   └── test_arvore.py  ← Testes com pytest
├── .gitignore
├── requirements.txt
└── README.md
```

## Algoritmos

### BFS (Busca em Largura)
Percorre a árvore nível por nível usando uma fila (`deque`). Útil para encontrar o caminho mais curto até um signo.

### DFS (Busca em Profundidade)
Percorre a árvore seguindo um caminho até o fim antes de voltar. Simula o fluxo natural de perguntas do jogo.

## Integrantes

- Wanessa Costa
- Ryan Cassimiro
