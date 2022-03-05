import pandas as pd
from pandas_profiling import ProfileReport


def pandasProfiling(nomFichier):
    """Lecture fichier CSV + rapport d'extraction détaillé"""
    actionsDF = pd.read_csv(nomFichier)
    prof = ProfileReport(actionsDF)
    prof.to_file(output_file=nomFichier.split('.')[0]+'.html')
    return


pandasProfiling('Data/Exercice.csv')
pandasProfiling('Data/dataset1_Python+P7.csv')
pandasProfiling('Data/dataset2_Python+P7.csv')
