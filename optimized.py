import time
import csv
from operator import attrgetter


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


def construirePanier(actions, noeud, invest, coutNoeud):
    """Fonction récursive de parcours d'un arbre binaire avec optimisation de bornes inf/sup"""
    global meilleurRendement
    global meilleurPanier
    global iteration
    global coutTotal
    iteration += 1
    if noeud < len(actions) and invest < 500 and (invest + coutTotal - coutNoeud) > 498:
        actions[noeud].panier = 1
        construirePanier(actions, noeud + 1, invest + actions[noeud].cout, coutNoeud + actions[noeud].cout)
        actions[noeud].panier = 0
        construirePanier(actions, noeud + 1, invest, coutNoeud + actions[noeud].cout)
    else:
        rendementPanier = sommeRendement(actions)
        if invest <= 500 and rendementPanier > meilleurRendement:
            meilleurRendement = rendementPanier
            meilleurPanier = extrairePanier(actions)
    return


def verifDataset(row):
    if float(row[1]) <= 0:
        return False
    else:
        return True


def lireDataset(nomFichier):
    """Création de la liste d'objet Action à partir du Dataset"""
    actions = []
    with open(nomFichier, 'r', newline='') as f:
        lecteur = csv.reader(f, delimiter=',')
        entete = True
        for row in lecteur:
            if not entete and verifDataset(row):
                actions.append(Action(row[0], float(row[1]), float(row[2]) / 100))
            entete = False
    return actions


def methodeGloutonne(dataset):
    actions = lireDataset(dataset)
    print(f"\nMETHODE GLOUTONNE {dataset}\n")

    print(time.ctime())
    cout = 0
    actions.sort(key=attrgetter('benefice', 'cout'), reverse=True)
    for i in range(len(actions)):
        invest = cout + actions[i].cout
        if invest <= 500:
            cout = invest
            actions[i].panier = 1
    print(time.ctime())

    print(i + 1, "Itérations")
    print("Investissement de " + "{:.2f}".format(sommeCout(actions)) + " € pour un rendement de " +
          "{:.2f}".format(sommeRendement(actions)) + " € sur deux ans")
    print(afficherPanier(actions))
    return

methodeGloutonne('Data\Exercice.csv')

actions = lireDataset('Data\Exercice.csv')
print("\nPROCEDURE DE SEPARATION ET D'EVALUATION (basique) Data\Exercice.csv\n")

print(time.ctime())
meilleurRendement = 0
meilleurPanier = bin(0)
iteration = 0
coutTotal = 0
actions.sort(key=attrgetter('benefice', 'cout'), reverse=True)
for i in range(len(actions)):
    coutTotal += actions[i].cout
construirePanier(actions, 0, 0, 0)
print(time.ctime())

print(iteration, "Itérations")
genererPanier(actions, meilleurPanier)
print("Investissement de " + "{:.2f}".format(sommeCout(actions)) + " € pour un rendement de " +
      "{:.2f}".format(meilleurRendement) + " € sur deux ans")
print(afficherPanier(actions))

methodeGloutonne('Data\dataset1_Python+P7.csv')
