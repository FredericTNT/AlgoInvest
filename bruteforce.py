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


def somme_rendement(actions):
    """Rendement du panier d'action"""
    rendement = 0
    for i in range(0, len(actions)):
        rendement += actions[i].rendement * actions[i].panier
    return rendement


def somme_cout(actions):
    """Cout du panier d'action"""
    cout = 0
    for i in range(0, len(actions)):
        cout += actions[i].cout * actions[i].panier
    return cout


def generer_panier(actions, panier):
    """Reporter la représentation binaire du panier dans la liste des actions"""
    k = len(actions)-1
    for j in range(len(panier) - 1, 1, -1):
        actions[k].panier = int(panier[j])
        k -= 1
    for j in range(0, k + 1):
        actions[j].panier = 0
    return


def extraire_panier(actions):
    """Extraire la représentation binaire du panier à partir de la liste des actions choisies"""
    panier = "0b"
    for i in range(len(actions)):
        panier += str(actions[i].panier)
    return panier


def afficher_panier(actions):
    """Liste des actions du panier d'action"""
    page = "Liste des actions à acquérir :\n"
    for i in range(0, len(actions)):
        if actions[i].panier != 0:
            page += f"- {actions[i].panier}x {actions[i].nom} {actions[i].cout}\n"
    return page


def afficher_resultat(actions, meilleur_panier, meilleur_rendement):
    """Afficher le résultat de la recherche"""
    generer_panier(actions, meilleur_panier)
    print(f"Investissement de {somme_cout(actions)} € pour un rendement de " +
          "{:.2f}".format(meilleur_rendement) + " € sur deux ans")
    print(afficher_panier(actions))


def construire_panier(actions, noeud):
    """Fonction récursive de parcours d'un arbre binaire"""
    global meilleur_rendement
    global meilleur_panier
    global iteration
    iteration += 1
    if noeud < len(actions):
        actions[noeud].panier = 1
        construire_panier(actions, noeud + 1)
        actions[noeud].panier = 0
        construire_panier(actions, noeud + 1)
    else:
        rendement_panier = somme_rendement(actions)
        if somme_cout(actions) <= 500 and rendement_panier > meilleur_rendement:
            meilleur_rendement = rendement_panier
            meilleur_panier = extraire_panier(actions)
    return


def lire_dataset(nom_fichier):
    """Création de la liste d'objet Action à partir du Dataset"""
    actions = []
    with open(nom_fichier, 'r', newline='') as f:
        lecteur = csv.reader(f, delimiter=',')
        entete = True
        for row in lecteur:
            if not entete:
                actions.append(Action(row[0], float(row[1]), float(row[2]) / 100))
            entete = False
    return actions


actions = lire_dataset('Data/Exercice.csv')

print("\nFORME ITERATIVE\n")
print(time.ctime())

meilleur_rendement = 0
meilleur_panier = bin(0)

for i in range(1, 2**len(actions)):
    binary = bin(i)
    generer_panier(actions, binary)
    rendement_panier = somme_rendement(actions)
    if somme_cout(actions) <= 500 and rendement_panier > meilleur_rendement:
        meilleur_rendement = rendement_panier
        meilleur_panier = binary

print(time.ctime())
print(i, "Itérations")
afficher_resultat(actions, meilleur_panier, meilleur_rendement)

for i in range(len(actions)):
    actions[i].panier = 0

print("\nFORME RECURSIVE\n")
print(time.ctime())

meilleur_rendement = 0
meilleur_panier = bin(0)
iteration = 0

construire_panier(actions, 0)

print(time.ctime())
print(iteration, "Itérations")
afficher_resultat(actions, meilleur_panier, meilleur_rendement)
