# Taille de la grille
GRID_SIZE = 4

# État objectif
GOAL_STATE = (3, 3)


def actions(state):
    """
    Retourne la liste des actions possibles depuis un état donné.
    Un état est un tuple (row, col), par exemple (1, 2).
    """
    row, col = state
    possible_actions = []

    # Si on n'est pas déjà tout en haut, on peut monter
    if row > 0:
        possible_actions.append("up")

    # Si on n'est pas déjà tout en bas, on peut descendre
    if row < GRID_SIZE - 1:
        possible_actions.append("down")

    # Si on n'est pas déjà tout à gauche, on peut aller à gauche
    if col > 0:
        possible_actions.append("left")

    # Si on n'est pas déjà tout à droite, on peut aller à droite
    if col < GRID_SIZE - 1:
        possible_actions.append("right")

    return possible_actions


def result(state, action):
    """
    Retourne le nouvel état après avoir appliqué une action.
    Si l'action est invalide depuis cet état, on lève une erreur.
    """
    row, col = state

    # On vérifie d'abord que l'action est autorisée
    if action not in actions(state):
        raise ValueError(f"Action '{action}' impossible depuis l'état {state}")

    if action == "up":
        return (row - 1, col)
    elif action == "down":
        return (row + 1, col)
    elif action == "left":
        return (row, col - 1)
    elif action == "right":
        return (row, col + 1)

    # Sécurité supplémentaire
    raise ValueError(f"Action inconnue : {action}")


def goal_test(state):
    """
    Retourne True si l'état est l'objectif, sinon False.
    """
    return state == GOAL_STATE


def main():
    """
    Fonction principale pour tester le programme.
    """
    state = (0, 0)

    print("=== TEST DE L'AGENT ===")
    print(f"État de départ : {state}")
    print(f"But à atteindre : {GOAL_STATE}")
    print()

    # Afficher les actions possibles
    available_actions = actions(state)
    print(f"Actions possibles depuis {state} : {available_actions}")
    print()

    # Faire quelques déplacements
    state = result(state, "down")
    print(f"Après 'down'  -> {state}")

    state = result(state, "right")
    print(f"Après 'right' -> {state}")

    state = result(state, "down")
    print(f"Après 'down'  -> {state}")

    state = result(state, "right")
    print(f"Après 'right' -> {state}")
    print()

    state = result(state, "down")
    print(f"Après 'down'  -> {state}")

    state = result(state, "right")
    print(f"Après 'right' -> {state}")
    print()

    # Vérifier si on a atteint le but
    print(f"Est-ce l'objectif ? {goal_test(state)}")


if __name__ == "__main__":
    main()