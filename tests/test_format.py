"""Description.

Tests du module lib_format
"""

import pandas as pd
from rich.table import Table
from rich.columns import Columns
from lib.lib_format import client_res, entrepot_res, total_res, total_cout
import pandas as pd

clients = ["8.5T", "21.5T"]
entrepots = ["10.2T", "20T"]
cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
data = pd.DataFrame(data=cout, index=entrepots, columns=clients)


def test_client_res():
    table = client_res(data)
    # test sur les colonnes
    assert table.columns[0].header == "Client"
    assert table.columns[1].header == "Quantités"
    assert table.columns[2].header == "Coûts"
    assert table.columns[3].header == "Nombre d'entrepôt solicité"
    assert table.columns[4].header == "Numéros des entrepôts solicités"

    # test sur les lignes
    assert table.columns[0]._cells == ["Client 1", "Client 2"]
    assert table.columns[1]._cells == ["8.5", "21.5"]
    assert table.columns[2]._cells == ["17.0", "43.0"]
    assert table.columns[3]._cells == ["1", "2"]
    assert table.columns[4]._cells == ["[1]", "[1, 2]"]


def test_entrepot_res():
    table = entrepot_res(data)
    # test sur les colonnes
    assert table.columns[0].header == "Entrepôt"
    assert table.columns[1].header == "Quantités"
    assert table.columns[2].header == "Coûts"
    assert table.columns[3].header == "Nombre de client livré"
    assert table.columns[4].header == "Numéros des clients livrés"

    # test sur les lignes
    assert table.columns[0]._cells == ["Entrepôt 1", "Entrepôt 2"]
    assert table.columns[1]._cells == ["10.2", "19.8"]
    assert table.columns[2]._cells == ["20.4", "39.6"]
    assert table.columns[3]._cells == ["2", "1"]
    assert table.columns[4]._cells == ["[1, 2]", "[2]"]

def test_total_res():
     assert total_res(data) == 30.0

def test_total_cout():
     assert total_cout(data) == 60.0
