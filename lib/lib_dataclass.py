from dataclasses import dataclass
import pandas as pd


@dataclass
class Verif_Chemin:
    "Classe pour vérifier le chemin d'accès aux données indiquant les erreurs de bases"
    chemin: str

    def __post_init__(self):
        if not self.chemin.endswith("csv"):
            raise ValueError('ERREUR CHEMIN : Le chemin doit se terminer par "csv"')
        if self.chemin[-4] != ".":
            raise ValueError('ERREUR CHEMIN : Il doit avoir un "." avant "csv"')
        if self.chemin[0] == " ":
            raise ValueError(
                'ERREUR CHEMIN : Attention, le premier caractère est un "ESPACE"'
            )


@dataclass
class Verif_Data:
    "Classe pour vérifier la forme du dataframe"
    data: pd.DataFrame

    def __post_init__(self):
        # données
        for i in range(0, len(self.data.columns)):
            if not self.data.iloc[:, i].str.endswith("$/T").all():
                raise ValueError(
                    'ERREUR DATA : Les données doivent être de la forme : "x$/T"'
                )
        # index
        for i in range(0, len(self.data.index)):
            if not self.data.index[i].endswith("T"):
                raise ValueError(
                    'ERREUR DATA : Les index doivent être de la forme : "xT"'
                )
        # colonnes
        if not self.data.columns.str.contains("..T|.T.").all():
            raise ValueError(
                'ERREUR DATA : Les noms de colonnes doivent-être de la forme : "xT" ou "xT.1"'
            )