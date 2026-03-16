from tree import build_tree

def play():
    print("=" * 45)
    print("   🔮 Akinator Signos — Adivinhe seu signo!")
    print("=" * 45)
    print("Responda com  s  (sim)  ou  n  (não).\n")

    root = build_tree()
    current = root
    history = []

    while not current.is_leaf():
        print(f"❓ {current.question}")

        answer = input("   Sua resposta (s/n): ").strip().lower()

        while answer not in ("s", "n"):
            print("   ⚠️  Digite apenas 's' para sim ou 'n' para não.")
            answer = input("   Sua resposta (s/n): ").strip().lower()

        history.append((current.question, "Sim" if answer == "s" else "Não"))

        if answer == "s":
            current = current.yes
        else:
            current = current.no

    # Chegou num nó folha — signo encontrado
    print("\n" + "=" * 45)
    print(f"  ✨ Seu signo é: {current.answer}")
    print("=" * 45)

    print("\n📋 Histórico da partida:")
    for i, (question, resp) in enumerate(history, start=1):
        print(f"  {i}. {question} → {resp}")

    print("\nDeseja jogar novamente? (s/n): ", end="")
    again = input().strip().lower()
    if again == "s":
        print()
        play()
    else:
        print("\nAté a próxima! 🌟\n")


if __name__ == "__main__":
    play()