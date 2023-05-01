"""Description.

Test d'intégration de l'application.
"""

import pandas as pd
from subprocess import run


def test_commande_total_cout():
    resultat = run(
        ["python", "app.py", "total-cout", "--chemin", "data_test.csv"],
        capture_output=True,
    )
    assert (
        resultat.stdout.decode("ISO-8859-1")
        == "Le coût total minimal est de 60.0$.\r\n"
    )


def test_commande_total_quantite():
    resultat = run(
        ["python", "app.py", "total-quantite", "--chemin", "data_test.csv"],
        capture_output=True,
    )
    assert resultat.stdout.decode("ISO-8859-1") == "La quantité livré est 30.0.\r\n"


def test_commande_resultat_client():
    resultat = run(
        ["python", "app.py", "resultat-client", "--chemin", "data_test.csv"],
        capture_output=True,
    )
    assert resultat.stdout.decode("latin") == (
        "                                   Résultat                                    \r\n"
        "+-----------------------------------------------------------------------------+\r\n"
        "|          |           |       | Nombre d'entrepôt    | Numéros des entrepôts |\r\n"
        "| Client   | Quantités | Coûts | solicité             | solicités             |\r\n"
        "|----------+-----------+-------+----------------------+-----------------------|\r\n"
        "| Client 1 | 8.5       | 17.0  | 1                    | [1]                   |\r\n"
        "| Client 2 | 21.5      | 43.0  | 2                    | [1, 2]                |\r\n"
        "+-----------------------------------------------------------------------------+\r\n"
    )


def test_commande_resultat_entrepot():
    resultat = run(
        ["python", "app.py", "resultat-entrepot", "--chemin", "data_test.csv"],
        capture_output=True,
    )
    assert resultat.stdout.decode("latin") == (
        "                                   Résultat                                    \r\n"
        "+-----------------------------------------------------------------------------+\r\n"
        "|            |           |       | Nombre de client     | Numéros des clients |\r\n"
        "| Entrepôt   | Quantités | Coûts | livré                | livrés              |\r\n"
        "|------------+-----------+-------+----------------------+---------------------|\r\n"
        "| Entrepôt 1 | 10.2      | 20.4  | 2                    | [1, 2]              |\r\n"
        "| Entrepôt 2 | 19.8      | 39.6  | 1                    | [2]                 |\r\n"
        "+-----------------------------------------------------------------------------+\r\n"
    )


def test_graphe1():
    run(
        ["python", "app.py", "representation", "--chemin", "data_test.csv"],
        capture_output=True,
    )

    assert True


def test_graphe2():
    resultat = run(
        ["python", "app.py", "representation-entrepot", "--chemin", "data_test.csv"],
        capture_output=True,
    )

    assert resultat.stdout.decode("latin") == ("Numéro de l'entrepot: ")
