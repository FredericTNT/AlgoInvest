import pandas as pd
from pandas_profiling import ProfileReport


def pandas_report(nom_fichier):
    """Lecture fichier CSV + rapport d'extraction détaillé"""
    actions_df = pd.read_csv(nom_fichier)
    prof = ProfileReport(actions_df)
    prof.to_file(output_file=nom_fichier.split('.')[0]+'.html')
    return


pandas_report('Data/Exercice.csv')
pandas_report('Data/dataset1_Python+P7.csv')
pandas_report('Data/dataset2_Python+P7.csv')
