import time
import pandas as pd
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


def pandasExtraction(nomFichier):
    """Lecture fichier CSV + rapport d'extraction + optimisation contextuelle"""
    print('\nINPUT DATASET -', nomFichier)
    actionsDF = pd.read_csv(nomFichier)
    print(actionsDF.info(), "\n", actionsDF.describe(percentiles=[0.10, 0.25, 0.50]))
    print('\nOPTIMIZED DATASET')
    actionsOpt = actionsDF[(actionsDF['price'] > 0) & (actionsDF['profit'] > 0) &
                           (actionsDF['price'] * actionsDF['profit'] >= 1)]
    print(actionsOpt.info(), "\n", actionsOpt.describe(percentiles=[0.10, 0.25, 0.50]))
    actions = []
    for label, row in actionsOpt.iterrows():
        actions.append(Action(row['name'], float(row['price']), float(row['profit'] / 100)))
    return actions


def methodeGloutonne(actions, label):
    print(f"\nMETHODE GLOUTONNE - {label}\n")

    print(time.ctime())
    cout = 0
    actions.sort(key=attrgetter('benefice', 'cout'), reverse=True)
    for i in range(len(actions)):
        actions[i].panier = 0
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


def progDynamiqueCentieme(actions, label):
    print(f"\nPROGRAMMATION DYNAMIQUE - {label}\n")
    print(time.ctime())

    iteration = 0
    tableau = []
    tabRow = []

    for i in range(len(actions)):
        actions[i].cout = round(actions[i].cout * 100)
        actions[i].panier = 0

    for i in range(50001):
        tabRow.append(0)
    tableau.append(tabRow)

    for action in range(len(actions)):
        tabRow = []
        for invest in range(50001):
            if invest >= int(actions[action].cout):
                tabRow.append(max(tableau[action][invest],
                                  tableau[action][invest - int(actions[action].cout)] + actions[action].rendement))
            else:
                tabRow.append(tableau[action][invest])
            iteration += 1
        tableau.append(tabRow)

    action = len(actions)
    for i in range(action): actions[i].panier = 0
    invest = 50000
    rendement = tableau[action][invest]

    while action > 0 and invest > 0:
        action -= 1
        while rendement == tableau[action][invest] and rendement > 0:
            action -= 1
        if rendement > 0:
            actions[action].panier = 1
            invest -= int(actions[action].cout)
            rendement = tableau[action][invest]

    for i in range(len(actions)):
        actions[i].cout = actions[i].cout / 100

    print(time.ctime())
    print(iteration, "Itérations")
    print("Investissement de " + "{:.2f}".format(sommeCout(actions)) + " € pour un rendement de " +
          "{:.2f}".format(sommeRendement(actions)) + " € sur deux ans")
    print(afficherPanier(actions))
    return


actions = pandasExtraction('Data\Exercice.csv')
print("\nPROCEDURE DE SEPARATION ET D'EVALUATION (basique) - EXERCICE\n")

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

methodeGloutonne(actions, 'EXERCICE')

actions = pandasExtraction('Data\dataset1_Python+P7.csv')
methodeGloutonne(actions, 'DATASET1')
progDynamiqueCentieme(actions, 'DATASET1')

actions = pandasExtraction('Data\dataset2_Python+P7.csv')
methodeGloutonne(actions, 'DATASET2')
progDynamiqueCentieme(actions, 'DATASET2')


