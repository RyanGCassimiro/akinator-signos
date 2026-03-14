from node import Node

def build_tree():

    # Criando todos os nós folhas, os 12 signos
    aries = Node(answer="Áries 21/03 - 20/04")
    taurus = Node(answer="Touro 21/04 - 20/05")
    gemini = Node(answer="Gêmeos 21/05 - 20/06")
    cancer = Node(answer="Câncer 21/06 - 22/07")
    leo = Node(answer="Leão 23/07 - 22/08")
    virgo = Node(answer="Virgem 23/08 - 22/09")
    libra = Node(answer="Libra 23/09 - 22/10")
    scorpion = Node(answer="Escorpião 23/10 - 21/11")
    sagittarius = Node(answer="Sagitário 22/11 - 21/12")
    capricorn = Node(answer="Capricórnio 22/12 - 20/01")
    aquarius = Node(answer="Aquário 21/01 - 19/02")
    pisces = Node(answer="Peixes 20/02 - 20/03")

    # Criando os nós de perguntas RAMO FOGO (Áries, Leão e Sagitário)
    # Áries -> antes de Maio | Leão -> Julho a Agosto | Sagitário -> Novembro a Dezembro; Todos são signos de fogo
    n_leo_sag = Node(question="Seu aniversário é entre é no segundo semestre? (Julho - Dezembro)")
    n_leo_sag.yes = leo
    n_leo_sag.no = sagittarius
    
    n_fire = Node(question="Seu aniversário é antes de Maio?")
    n_fire.yes = aries
    n_fire.no = n_leo_sag