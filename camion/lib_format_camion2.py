"""Description.

Formattage des objets de lib_transport vers des objets rich.
"""

from rich.table import Table
from rich.table import Table
import lib_transport_camion2 as lt
import pandas as pd
import numpy as np


def client_res(
    data: pd.DataFrame, capacite : int ,CF: int
) -> Table():
    """Renvoie un tableau de la liste des clients, les coûts de livraison associés à chacun d'eux, le nombre de d'entrepôt solicités ainsi que le numéro de ces entrepôts.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - resultat (rich.table.Table): un objet Table de la bibliothèque rich contenant les résultats sous forme de tableau.

    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> client_res(data)
                                            Résultat
    ┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Client   ┃ Quantités ┃ Coûts ┃ Nombre d'entrepôt solicité ┃ Numéros des entrepôts solicités ┃
    ┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ Client 1 │ 8.5       │ 17.0  │ 1                          │ [1]                             │
    │ Client 2 │ 21.5      │ 43.0  │ 2                          │ [1, 2]                          │
    └──────────┴───────────┴───────┴────────────────────────────┴─────────────────────────────────┘

    """
    liv = lt.livraison(data)

    resultat = Table(title="Résultat")
    resultat.add_column("Client", style="bold green")
    resultat.add_column("Quantités")
    resultat.add_column("Coûts")
    resultat.add_column("Nombre d'entrepôt solicité")
    resultat.add_column("Numéros des entrepôts solicités")

    compteur = []
    for i in liv.columns:
        nb = 0
        for j in liv[i]:
            if j != 0:
                nb += 1
        compteur.append(nb)

    cout = lt.cout_total(data,capacite,CF)

    k = 0
    for col in liv.columns:
        resultat.add_row(
            str("Client " + str(col)),
            str(sum(liv[col])),
            str(sum(cout[col])),
            str(compteur[k]),
            str(
                ((np.array(np.nonzero(np.array(liv.iloc[:, col - 1]))) + 1)[0].tolist())
            ),
        )
        k = k + 1

    return resultat


def entrepot_res(data: pd.DataFrame, capacite : int ,CF: int) -> Table():
    """Renvoie un tableau de la liste des entrepôts, les coûts associés à chacun d'eux, le nombre de client livré ainsi que les numéro des clients livrés.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - resultat (rich.table.Table): un objet Table de la bibliothèque rich contenant les résultats sous forme de tableau.


    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> entrepot_res(data)
                                                Résultat
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Entrepôt   ┃ Quantités ┃ Coûts ┃ Nombre de client livré ┃ Numéros des clients livrés ┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ Entrepôt 1 │ 10.0      │ 20.0  │ 2                      │ [1, 2]                     │
    │ Entrepôt 2 │ 20.0      │ 40.0  │ 1                      │ [2]                        │
    └────────────┴───────────┴───────┴────────────────────────┴────────────────────────────┘
    """

    liv = lt.livraison(data)
    resultat = Table(title="Résultat")
    resultat.add_column("Entrepôt", style="bold blue")
    resultat.add_column("Quantités")
    resultat.add_column("Coûts")
    resultat.add_column("Nombre de client livré")
    resultat.add_column("Numéros des clients livrés")
    liv = lt.livraison(data)

    compteur = []
    for i in liv.index:
        nb = 0
        for j in liv.iloc[i - 1]:
            if j != 0:
                nb += 1
        compteur.append(nb)
    cout = lt.cout_total(data,capacite,CF)
    k = 0
    for ind in liv.index:
        resultat.add_row(
            str("Entrepôt " + str(ind)),
            str(sum(liv.iloc[ind - 1])),
            str(sum(cout.iloc[ind - 1])),
            str(compteur[k]),
            str((np.array(np.nonzero(np.array(liv.iloc[ind - 1]))) + 1)[0].tolist()),
        )
        k = k + 1
    return resultat


def total_res(data: pd.DataFrame) -> float:
    """
    Calcule les quantités livrés au total pour l'ensemble des entrepôts et clients.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - float: le total des quantités livrées pour l'ensemble des entrepôts et clients.

    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> total_res(data)
    30.0
    """

    livraison = lt.livraison(data)
    return sum(sum(livraison.values))


def total_cout(data: pd.DataFrame, capacite: int, CF: int) -> float:
    """
    Calcule le coût total de livraison pour l'ensemble des entrepôts et clients.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - float: le coût total de livraison pour l'ensemble des entrepôts et clients.

    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> total_cout(data)
    60.0
    """
    cout = lt.cout_total(data,capacite,CF)
    return sum(sum(cout.values))
