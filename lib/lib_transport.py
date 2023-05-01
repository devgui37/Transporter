"""Description.

librairie qui permet de résoudre les problèmes de transports afin de minimiser les coût de transports.
"""


import pandas as pd
from scipy.optimize import linprog
import numpy as np
import re

def import_data(chemin: str) -> pd.DataFrame:
    """Importe un fichier CSV.

    Args:
    chemin (str) : le chemin du fichier CSV à importer.

    Returns:
    (pd.DataFrame) : un DataFrame Pandas contenant les données du fichier CSV.

    """
    # importation
    data = pd.read_csv(chemin, index_col=0)
    return data



def _sup_doublons(data: pd.DataFrame) -> pd.DataFrame:
    """Supprime les '.i' lorsqu'il y a des doublons au niveau des noms de colonnes de la base de données.

    Args:
    - data (pd.DataFrame): Un DataFrame contenant les données à nettoyer

    Returns:
    - pd.DataFrame: Un DataFrame nettoyé où les doublons ont été corrigés

    Example:
    >>> data.columns
    Index(['19T', '20T', '19T.1', '19T.2']
    >>> _sup_doublons(data).columns
    Index(['19T', '20T', '19T', '19T']
    """
    for col_name in data.columns.str[:]:
        # Trouver l'index du T dans le nom de colonne
        t_index = col_name.find("T")
        # Vérifier si un caractère suit le T
        if t_index != len(col_name) - 1:
            # Supprimer tout ce qui se trouve après le T
            new_col_name = col_name[: t_index + 1]
            # Renommer la colonne dans le DataFrame
            data.rename(columns={col_name: new_col_name}, inplace=True)

    return data


def _modif_data(data: pd.DataFrame) -> dict:
    """Permet de vérifier la conformité des valeurs de disponibilités et de besoins données et de renommer les colonnes et les lignes.

    Args:
    - data (pd.DataFrame): Un dataframe pandas qui contient les valeurs de disponibilités et de besoins.

    Returns:
    - dict: Un dictionnaire contenant les valeurs de disponibilités et de besoins converties en listes, les coûts de transport convertis en un tableau numpy et le dataframe modifié.

    Raises:
    - ValueError: Si les besoins des clients, les disponibilités d'entrepôts ou les coûts de transport ne sont pas sous forme d'entiers ou de décimaux.
    - ValueError: Si la somme des produits disponible est inférieure à la demande des clients. Tous les clients ne peuvent pas être servis.

    Examples:
        >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
        >>> _modif_data(data)['client']
        [8.5, 21.5]
        >>> _modif_data(data)['produit']
        [10.0, 20.0]
        >>> _modif_data(data)['cout']
        [[2. 2.]
        [2. 2.]]
        >>> _modif_data(data)['data']
              8.5  21.5
        10.0  2.0   2.0
        20.0  2.0   2.0

    """

    # variables pour la suite
    _sup_doublons(data)

    produit = []
    client = []

    # création des objets produit et client
    for element in data.columns.str[:]:
        valeurs = re.findall(r"\d+", element)
        if len(valeurs) > 2:
            raise ValueError(
                "Les besoins des clients doivent entiers être ou décimaux. Par exemple: '10T' ou '20.5T'."
            )
        if len(valeurs) == 2:
            valeurs = [valeurs[0] + "." + valeurs[1]]

        client += [float(valeurs[0])]

    for element in data.index.str[:]:
        valeurs = re.findall(r"\d+", element)
        if len(valeurs) > 2:
            raise ValueError(
                "Les disponibilités d'entrepots doivent être entières ou décimales. Par exemple: '10T' ou '20.5T'."
            )
        if len(valeurs) == 2:
            valeurs = [valeurs[0] + "." + valeurs[1]]

        produit += [float(valeurs[0])]

    # Renommage des colonnes et lignes
    # nom colonne
    for i in range(len(data.columns)):
        data = data.rename(columns={data.columns[i]: client[i]})

    # nom ligne
    for i in range(len(data.index)):
        data = data.rename(index={data.index[i]: produit[i]})

    # netoyage des données
    cout = []
    a = []
    for ligne in data.values[:]:
        for element in ligne:
            valeurs = re.findall(r"\d+", element)
            if len(valeurs) > 2:
                raise ValueError(
                    "Les coûts de transport doivent être entiers ou décimaux. Par exemple: '10$/T' ou '20.5$/T'."
                )
            if len(valeurs) == 2:
                valeurs = [valeurs[0] + "." + valeurs[1]]
            a += [float(valeurs[0])]
        cout.append(a)
        a = []
    cout = np.array(cout)
    data.iloc[:, :] = cout

    # vérification
    somme_produits = np.sum(produit)
    somme_clients = np.sum(client)
    if somme_produits < somme_clients:
        raise ValueError(
            "La somme des produits disponible est inférieure à la demande des clients. \n Tous les clients ne peuvent pas être servis."
        )

    # output
    return {"client": client, "cout": cout, "produit": produit, "data": data}


def _a_ub(data: pd.DataFrame) -> list:
    """
    Construit une liste de matrices représentant les contraintes d'inégalité entre les disponibilités des entrepôts et
    la somme des quantités livrées pour chaque client. Chaque matrice a une dimension de "nombre de clients" x
    "nombre d'entrepôts".

    Args:
    - data (pd.DataFrame): Un DataFrame représentant les données de l'instance du problème.

    Returns:
    - list: Une liste de matrices numpy, où chaque matrice représente les contraintes d'inégalité pour un entrepôt.

    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> _a_ub(data)
    [array([1., 1., 0., 0.]), array([0., 0., 1., 1.])]
    """

    a_ub = []
    for i in range(len(data.index)):
        matrix = np.zeros(len(data.index) * len(data.columns))
        matrix[i * len(data.columns) : (i + 1) * len(data.columns)] = 1
        a_ub.append(matrix)
    return a_ub


def _a_eq(data: pd.DataFrame) -> list:
    """
    Construit une matrice de coefficients qui associe chaque client à une colonne de coûts.
    Pour chaque client i, seul les coûts sur la colonne i de la base de données lui sont associés.

    Args:
    - data: un DataFrame représentant la base de données modifiée (conforme aux besoins et disponibilités des clients et entrepôts)

    Returns:
    - list: Une liste de matrices numpy, où chaque matrice représente les contraintes d'égalité pour un client.

    Example:
    >>> data = pd.DataFrame({'8.5T': ['2$/T', '2$/T'], '21.5T': ['2$/T', '2$/T']}, index=['10T', '20T'])
    >>> _a_eq(data)
    [array([1., 0., 1., 0.]), array([0., 1., 0., 1.])]
    """

    a_eq = []
    for i in range(len(data.columns)):
        matrix = np.zeros(len(data.index) * len(data.columns))
        for j in range(0, len(data.index) * len(data.columns), len(data.columns)):
            matrix[i + j] = 1
        a_eq.append(matrix)
    return a_eq


def _resolution(data: pd.DataFrame):
    """
    Résout le problème d'optimisation de minimisation des coûts de production en utilisant la fonction linéaire de la bibliothèque scipy.optimize.

    Args:
    - data (pd.DataFrame) : un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - result (OptimizeResult) : un objet OptimizeResult contenant les informations sur la solution trouvée par l'optimiseur. Cet objet contient les champs suivants :
        * message : un message décrivant le statut de l'optimisation (succès, échec, convergence, etc.)
        * success : un booléen indiquant si l'optimisation s'est terminée avec succès
        * status : un code numérique indiquant le statut de l'optimisation (0 pour succès, valeurs positives pour des erreurs spécifiques, valeurs négatives pour des avertissements)
        * fun : la valeur optimale de la fonction objective (coût total)
        * x : un ndarray contenant les valeurs optimales des variables de décision (quantités de produits à livrer)
        * nit : le nombre d'itérations effectuées
        * residual : un ndarray contenant les résidus de la solution optimale par rapport aux contraintes d'égalité et d'inégalité linéaires
        * marginals : un ndarray contenant les marginaux de la solution optimale
        * mip_node_count : le nombre de noeuds visités dans la résolution de la relaxation linéaire du problème de programmation en nombres entiers
        * mip_dual_bound : la borne supérieure du dual de la relaxation linéaire du problème de programmation en nombres entiers
        * mip_gap : l'écart relatif entre la borne supérieure du dual et la borne inférieure du primal pour le problème de programmation en nombres entiers, si applicable.
    """
    c = _modif_data(data)["cout"].flatten()
    A_ub = _a_ub(data=_modif_data(data)["data"])
    b_ub = np.array(_modif_data(data)["produit"])
    A_eq = _a_eq(data=_modif_data(data)["data"])
    b_eq = np.array(_modif_data(data)["client"])
    x_bounds = (0, None)
    result = linprog(
        c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method="highs"
    )
    return result


def livraison(data: pd.DataFrame) -> pd.DataFrame:
    """
    Résout le problème d'optimisation pour la livraison de produits aux clients et retourne un DataFrame avec les quantités
    à livrer à chaque client pour chaque entrepôts.

    Args:
    - data (pd.DataFrame) : un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - DataFrame: Un DataFrame contenant les quantités à livrer à chaque client pour chaque produit. Les colonnes sont les
        numéros des clients et les index sont les numéros des produits.
    """
    livraison = _resolution(data).x
    livraison = np.reshape(livraison, (len(data.index), len(data.columns)))
    livraison = pd.DataFrame(
        livraison,
        columns=np.array(range(1, len(_modif_data(data)["client"]) + 1)),
        index=np.array(range(1, len(_modif_data(data)["produit"]) + 1)),
    )
    return livraison

def cout(data: pd.DataFrame) -> pd.DataFrame:
    cout = pd.DataFrame(
        livraison(data).values * _modif_data(data)["data"].values,
        columns=np.array(range(1, len(_modif_data(data)["client"]) + 1)),
        index=np.array(range(1, len(_modif_data(data)["produit"]) + 1)),
    )
    return cout
