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


def construire_panier(actions, noeud, invest, cout_noeud):
    """Fonction récursive de parcours d'un arbre binaire avec optimisation de bornes inf/sup"""
    global meilleur_rendement
    global meilleur_panier
    global iteration
    global cout_total
    iteration += 1
    if noeud < len(actions) and invest < 500 and (invest + cout_total - cout_noeud) > 495:
        actions[noeud].panier = 1
        construire_panier(actions, noeud + 1, invest + actions[noeud].cout, cout_noeud + actions[noeud].cout)
        actions[noeud].panier = 0
        construire_panier(actions, noeud + 1, invest, cout_noeud + actions[noeud].cout)
    else:
        rendement_panier = somme_rendement(actions)
        if invest <= 500 and rendement_panier > meilleur_rendement:
            meilleur_rendement = rendement_panier
            meilleur_panier = extraire_panier(actions)
    return


def pandas_extraction(nom_fichier):
    """Lecture fichier CSV + rapport d'extraction + optimisation contextuelle"""
    print('\nINPUT DATASET -', nom_fichier)
    actions_df = pd.read_csv(nom_fichier)
    print(actions_df.info(), "\n", actions_df.describe(percentiles=[0.10, 0.25, 0.50]))
    print('\nOPTIMIZED DATASET')
    actions_opt = actions_df[(actions_df['price'] > 0) & (actions_df['profit'] > 0)].drop_duplicates(subset='name')
    print(actions_opt.info(), "\n", actions_opt.describe(percentiles=[0.10, 0.25, 0.50]))
    actions = []
    for label, row in actions_opt.iterrows():
        actions.append(Action(row['name'], float(row['price']), float(row['profit'] / 100)))
    return actions


def methode_gloutonne(actions, label, invest_max):
    print(f"\nMETHODE GLOUTONNE - {label}\n")

    print(time.ctime())
    cout = 0
    actions.sort(key=attrgetter('benefice', 'cout'), reverse=True)
    for i in range(len(actions)):
        actions[i].panier = 0
        invest = cout + actions[i].cout
        if invest <= invest_max:
            cout = invest
            actions[i].panier = 1
    print(time.ctime())

    print(i + 1, "Itérations")
    print("Investissement de " + "{:.2f}".format(somme_cout(actions)) + " € pour un rendement de " +
          "{:.2f}".format(somme_rendement(actions)) + " € sur deux ans")
    print(afficher_panier(actions))
    return


def prog_dynamique(actions, label, invest_max, centieme):
    print(f"\nPROGRAMMATION DYNAMIQUE - {label}\n")
    print(time.ctime())

    iteration = 0
    tableau = []
    tab_row = []
    nb_row = invest_max + 1

    if centieme:
        for i in range(len(actions)):
            actions[i].cout = round(actions[i].cout * 100)
        nb_row = invest_max * 100 + 1

    for i in range(nb_row):
        tab_row.append(0)
    tableau.append(tab_row)

    for action in range(len(actions)):
        tab_row = []
        tab_row.append(0)
        for invest in range(1, nb_row):
            if invest >= int(actions[action].cout):
                tab_row.append(max(tableau[action][invest],
                                   tableau[action][invest - int(actions[action].cout)] + actions[action].rendement))
            else:
                tab_row.append(tableau[action][invest])
            iteration += 1
        tableau.append(tab_row)

    action = len(actions)
    for i in range(action):
        actions[i].panier = 0
    invest = invest_max
    if centieme:
        invest *= 100
    rendement = tableau[action][invest]

    while action > 0 and invest > 0:
        action -= 1
        while rendement == tableau[action][invest] and rendement > 0:
            action -= 1
        if rendement > 0:
            actions[action].panier = 1
            invest -= int(actions[action].cout)
            rendement = tableau[action][invest]

    if centieme:
        for i in range(len(actions)):
            actions[i].cout = actions[i].cout / 100

    print(time.ctime())
    print(iteration, "Itérations")
    print("Investissement de " + "{:.2f}".format(somme_cout(actions)) + " € pour un rendement de " +
          "{:.2f}".format(somme_rendement(actions)) + " € sur deux ans")
    print(afficher_panier(actions))
    return


actions = pandas_extraction('Data/Exercice.csv')
print("\nPROCEDURE DE SEPARATION ET D'EVALUATION (basique) - EXERCICE\n")

print(time.ctime())
meilleur_rendement = 0
meilleur_panier = bin(0)
iteration = 0
cout_total = 0
actions.sort(key=attrgetter('benefice', 'cout'), reverse=True)
for i in range(len(actions)):
    cout_total += actions[i].cout
construire_panier(actions, 0, 0, 0)
print(time.ctime())

print(iteration, "Itérations")
generer_panier(actions, meilleur_panier)
print("Investissement de " + "{:.2f}".format(somme_cout(actions)) + " € pour un rendement de " +
      "{:.2f}".format(meilleur_rendement) + " € sur deux ans")
print(afficher_panier(actions))

methode_gloutonne(actions, 'EXERCICE', 500)
prog_dynamique(actions, 'EXERCICE', 500, False)

actions = pandas_extraction('Data/dataset1_Python+P7.csv')
methode_gloutonne(actions, 'DATASET1', 500)
prog_dynamique(actions, 'DATASET1', 500, True)

actions = pandas_extraction('Data/dataset2_Python+P7.csv')
methode_gloutonne(actions, 'DATASET2', 500)
prog_dynamique(actions, 'DATASET2', 500, True)
