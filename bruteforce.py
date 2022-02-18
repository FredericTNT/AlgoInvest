import time


class Action:
    """Action"""

    def __init__(self, nom, cout, benefice):
        self.nom = nom
        self.cout = cout
        self.benefice = benefice
        self.rendement = cout * benefice
        self.panier = 0


def sommeRendement(actions):
    """Rendement du panier d'action"""
    rendement = 0
    for i in range(0, len(actions)):
        rendement += actions[i].rendement * actions[i].panier
    return rendement


def sommeCout(actions):
    """Cout du panier d'action"""
    cout = 0
    for i in range(0, len(actions)):
        cout += actions[i].cout * actions[i].panier
    return cout


def genererPanier(actions, panier):
    """Reporter la représentation binaire du panier dans la liste des actions"""
    k = len(actions)-1
    for j in range(len(panier) - 1, 1, -1):
        actions[k].panier = int(panier[j])
        k -= 1
    for j in range(0, k + 1):
        actions[j].panier = 0
    return


def extrairePanier(actions):
    """Extraire la représentation binaire du panier à partir de la liste des actions choisies"""
    panier = "0b"
    for i in range(len(actions)):
        panier += str(actions[i].panier)
    return panier


def afficherPanier(actions):
    """Liste des actions du panier d'action"""
    page = "Liste des actions à acquérir :\n"
    for i in range(0, len(actions)):
        if actions[i].panier != 0:
            page += f"- {actions[i].panier}x {actions[i].nom}\n"
    return page


def afficherResultat(actions, meilleurPanier, meilleurRendement):
    """Afficher le résultat de la recherche"""
    genererPanier(actions, meilleurPanier)
    print(f"Investissement de {sommeCout(actions)} € pour un rendement de " +
          "{:.2f}".format(meilleurRendement) + " € sur deux ans")
    print(afficherPanier(actions))


def construirePanier(actions, noeud):
    global meilleurRendement
    global meilleurPanier
    global iteration
    iteration += 1
    if noeud < len(actions):
        actions[noeud].panier = 1
        construirePanier(actions, noeud + 1)
        actions[noeud].panier = 0
        construirePanier(actions, noeud + 1)
    else:
        rendementPanier = sommeRendement(actions)
        if sommeCout(actions) <= 500 and rendementPanier > meilleurRendement:
            meilleurRendement = rendementPanier
            meilleurPanier = extrairePanier(actions)
    return


actions = []
actions.append(Action("Action-1", 20, 0.05))
actions.append(Action("Action-2", 30, 0.1))
actions.append(Action("Action-3", 50, 0.15))
actions.append(Action("Action-4", 70, 0.20))
actions.append(Action("Action-5", 60, 0.17))
actions.append(Action("Action-6", 80, 0.25))
actions.append(Action("Action-7", 22, 0.07))
actions.append(Action("Action-8", 26, 0.11))
actions.append(Action("Action-9", 48, 0.13))
actions.append(Action("Action-10", 34, 0.27))
actions.append(Action("Action-11", 42, 0.17))
actions.append(Action("Action-12", 110, 0.09))
actions.append(Action("Action-13", 38, 0.23))
actions.append(Action("Action-14", 14, 0.01))
actions.append(Action("Action-15", 18, 0.03))
actions.append(Action("Action-16", 8, 0.08))
actions.append(Action("Action-17", 4, 0.12))
actions.append(Action("Action-18", 10, 0.14))
actions.append(Action("Action-19", 24, 0.21))
actions.append(Action("Action-20", 114, 0.18))


print("\nFORME ITERATIVE\n")
print(time.ctime())

meilleurRendement = 0
meilleurPanier = bin(0)

for i in range(1, 2**len(actions)):
    binary = bin(i)
    genererPanier(actions, binary)
    rendementPanier = sommeRendement(actions)
    if sommeCout(actions) <= 500 and rendementPanier > meilleurRendement:
        meilleurRendement = rendementPanier
        meilleurPanier = binary

print(time.ctime())
afficherResultat(actions, meilleurPanier, meilleurRendement)

for i in range(20): actions[i].panier = 0

print("\nFORME RECURSIVE\n")
print(time.ctime())

meilleurRendement = 0
meilleurPanier = bin(0)
iteration = 0

construirePanier(actions, 0)

print(time.ctime())
afficherResultat(actions, meilleurPanier, meilleurRendement)
print(iteration)
