# AlgoInvest

## Table des matières
1. [Informations générales](#Informations_générales)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Exécution](#Exécution)

## Informations_générales
***
Analyse des approches algorithmiques au service des stratégies d'investissement
+ Méthode brute (itérative & récursive)
+ Optimisations (PSE, gloutonne et programmation dynamique)
+ Exploration de données avec pandas_profiling

## Technologies
***
Technologies utilisées dans ce projet :
* [Windows 10 Famille](https://docs.microsoft.com/fr-fr/windows/whats-new/whats-new-windows-10-version-21h2) : version 21H2 
* [Python](https://docs.python.org/fr/3.10/) : version 3.10.0
* [Library - pandas](https://pandas.pydata.org/pandas-docs/stable/) : version 1.4.1
* [Library - pandas_profiling](https://pypi.org/project/pandas-profiling/) : version 3.1.0
* [Library - matplotlib](https://matplotlib.org/) : version 3.5.1
* [module - operator(attrgetter)](https://docs.python.org/fr/3/library/operator.html)

## Installation
***
Réaliser l'installation avec le terminal Windows PowerShell 

Le clonage (git clone) se fait dans un répertoire AlgoInvest et son sous-répertoire Data qui comprend 3 jeux de données
(nomFichier.csv)
```
$ git clone https://github.com/FredericTNT/AlgoInvest
$ cd AlgoInvest
$ python -m venv <nom environnement>
$ <nom environnement>/scripts/activate
$ pip install -r requirements.txt
```

## Exécution
***
L'exécution des 3 programmes s'effectue dans l'environnement virtuel activé
```
$ python bruteforce.py
$ python optimized.py
$ python report.py
```

Les rapports d'exploration des données sont générés dans le répertoire AlgoInvest/Data/nomFichier.html
<!---
## FAQs
-->