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

    # Criando os nós de perguntas RAMO AR (Gêmeos, Libra e Aquário)
    # Gêmeos -> antes de Junho | Libra -> Setembro a Outubro | Aquário -> Janeiro a Fevereiro; Todos são signos de ar
    n_libra_aquarius = Node(question="Seu aniversário é antes de Novembro?")
    n_libra_aquarius.yes = libra
    n_libra_aquarius.no = aquarius

    n_air = Node(question="Seu anversário é antes de Julho?")
    n_air.yes = gemini
    n_air.no = n_libra_aquarius

    # Criando RAMO FOGO ou AR

    n_fire_air = Node(question="É do elemento fogo? (Áries, Leão, Sagitário)")
    n_fire_air.yes = n_fire
    n_fire_air.no = n_air

    # Criando os nós de perguntas RAMO TERRA (Touro, Virgem e Capricórnio)
    # Touro -> antes de Maio | Virgem -> Agosto a Setembro | Capricórnio -> Dezembro a Janeiro; Todos são signos de terra
    n_virgo_cap = Node(question="Seu aniversário é antes de Outubro?")
    n_virgo_cap.yes = virgo
    n_virgo_cap.no = capricorn

    n_earth = Node(question="Seu aniversário é antes de Julho?")
    n_earth.yes = taurus
    n_earth.no = n_virgo_cap

    # Criando os nós de perguntas RAMO ÁGUA (Câncer, Escorpião e Peixes)
    # Câncer -> antes de Julho | Escorpião -> Outubro a Novembro | Peixes -> Fevereiro a Março; Todos são signos de água
    n_scorpion_pisces = Node(question="Seu aniversário é antes de Dezembro?")
    n_scorpion_pisces.yes = scorpion
    n_scorpion_pisces.no = pisces

    n_water = Node(question="Seu aniversário é antes de agosto?")
    n_water.yes = cancer
    n_water.no = n_scorpion_pisces

    # Criando RAMO TERRA ou ÁGUA
    n_earth_water = Node(question="É do elemento terra? (Touro, Virgem, Capricórnio)")
    n_earth_water.yes = n_earth
    n_earth_water.no = n_water

    # Criando a raiz da árvore

    root = Node(question="É do elemento fogo ou ar? (Áries, Leão, Sagitário, Gêmeos, Libra, Aquário)")
    root.yes = n_fire_air
    root.no = n_earth_water

    return root