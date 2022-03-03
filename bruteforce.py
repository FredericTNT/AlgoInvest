import time
import csv

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
            page += f"- {actions[i].panier}x {actions[i].nom} {actions[i].cout}\n"
    return page


def afficherResultat(actions, meilleurPanier, meilleurRendement):
    """Afficher le résultat de la recherche"""
    genererPanier(actions, meilleurPanier)
    print(f"Investissement de {sommeCout(actions)} € pour un rendement de " +
          "{:.2f}".format(meilleurRendement) + " € sur deux ans")
    print(afficherPanier(actions))


def construirePanier(actions, noeud):
    """Fonction récursive de parcours d'un arbre binaire"""
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


def lireDataset(nomFichier):
    """Création de la liste d'objet Action à partir du Dataset"""
    actions = []
    with open(nomFichier, 'r', newline='') as f:
        lecteur = csv.reader(f, delimiter=',')
        entete = True
        for row in lecteur:
            if not entete:
                actions.append(Action(row[0], float(row[1]), float(row[2]) / 100))
            entete = False
    return actions


actions = lireDataset('Data/Exercice.csv')

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
print(i, "Itérations")
afficherResultat(actions, meilleurPanier, meilleurRendement)

for i in range(len(actions)): actions[i].panier = 0

print("\nFORME RECURSIVE\n")
print(time.ctime())

meilleurRendement = 0
meilleurPanier = bin(0)
iteration = 0

construirePanier(actions, 0)

print(time.ctime())
print(iteration, "Itérations")
afficherResultat(actions, meilleurPanier, meilleurRendement)
