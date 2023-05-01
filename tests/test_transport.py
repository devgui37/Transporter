"""Description.

Tests du module lib_transport
"""

import pytest
from scipy.optimize import linprog
import pandas as pd
import numpy as np
from lib.lib_transport import (
    _sup_doublons,
    _modif_data,
    _a_ub,
    _a_eq,
    _resolution,
    livraison,
    import_data,
)

np.random.seed(1234)


def test_import():
    import_data("data_test.csv")


def test_sup_doublons():
    clients = ["21.5T", "21.5T.1", "10T", "5.79458T"]
    cl_attendu = ["21.5T", "21.5T", "10T", "5.79458T"]
    entrepots = ["10.2T", "20T", "25T", "35T"]
    cout = np.random.randint(1, 10, size=(4, 4)).astype(str)
    cout = np.core.defchararray.add(cout, "$/T")
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    sortie = _sup_doublons(data)
    assert np.all(sortie.columns == cl_attendu)


def test_modif_data():
    # test sur client, entrepot et cout
    clients = ["21.5T", "21.5T.1", "10T", "5.79458T"]
    cl_attendu = [21.5, 21.5, 10, 5.79458]
    entrepots = ["10.2T", "20T", "25T", "35T"]
    ent_attendu = [10.2, 20, 25, 35]
    cout_attendu = np.random.uniform(1, 10, size=(4, 4))
    cout = cout_attendu.astype(str)
    cout = np.core.defchararray.add(cout, "$/T")
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    assert _modif_data(data)["client"] == cl_attendu
    assert _modif_data(data)["produit"] == ent_attendu
    assert np.array_equal(_modif_data(data)["cout"], cout_attendu)


def test_modif_data_raise_error():
    # probleme client
    clients = ["21.5T", "21.5T.1"]
    cout = [["2$/T", "1$/T"], ["1$/T", "1$/T"]]
    entrepots = ["10.2T", "20T"]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        data.rename(columns={"21.5T": "20.486.54894T"}, inplace=True)
        _modif_data(data)

    # probleme entrepot
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        data.rename(index={"10.2T": "784.1894.65T"}, inplace=True)
        _modif_data(data)

    # probleme cout
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        data.iloc[0, 0] = "2.2546.251€/T"
        _modif_data(data)

    # Probleme somme client / entrepot
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        data.rename(columns={"21.5T": "10000T"}, inplace=True)
        _modif_data(data)
        # Dans ce cas la somme des demandes clients sont supérieures au stock disponible.


def test_all_resolution():
    clients = ["10T", "15T.1"]
    entrepots = ["100T", "20T"]
    cout = [["2$/T", "1$/T"], ["1.5$/T", "1$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)

    assert np.array_equal(_a_ub(data), [[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]])
    assert np.array_equal(_a_eq(data), [[1, 0, 1, 0], [0, 1, 0, 1]])
    lin = linprog(
        c=[2.0, 1.0, 1.5, 1.0],
        A_eq=[[1, 0, 1, 0], [0, 1, 0, 1]],
        b_eq=[10.0, 15.0],
        A_ub=[[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]],
        b_ub=[100.0, 20.0],
        bounds=(0, None),
        method="highs",
    )
    assert np.array_equal(_resolution(data).x, lin.x)
    assert np.array_equal(_resolution(data).fun, lin.fun)


def test_transport():
    clients = ["10T", "15T.1"]
    entrepots = ["100T", "20T"]
    cout = [["2$/T", "1$/T"], ["1.5$/T", "1$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    np.array_equal(_resolution(data).x, livraison(data).values.flatten())
