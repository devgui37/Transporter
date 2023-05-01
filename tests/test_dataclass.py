from lib.lib_dataclass import Verif_Chemin, Verif_Data
import pytest
import pandas as pd

def test_VF_class():
    chemin_csv = Verif_Chemin("/chemin/vers/mon_fichier.csv")
    assert isinstance(chemin_csv, Verif_Chemin)

    with pytest.raises(ValueError):
        Verif_Chemin("/chemin/vers/mon_fichier.txt")

    with pytest.raises(ValueError):
        Verif_Chemin(" /chemin/vers/mon_fichier.csv")

    with pytest.raises(ValueError):
        Verif_Chemin("/chemin/vers/mon_fichier_csv")
        


def test_VD_class():
    clients = ["21.5T", "21.5T.1"]
    cout = [["2$/T", "1$/T"], ["1$/T", "1$/T"]]
    entrepots = ["10.2T", "20T"]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    data_class = Verif_Data(data)
    assert isinstance(data_class, Verif_Data)

    clients = ["21.5", "21.5T.1"]
    cout = [["2$/T", "1$/T"], ["1$/T", "1$/T"]]
    entrepots = ["10.2T", "20T"]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        Verif_Data(data)

    clients = ["21.5T", "21.5T.1"]
    cout = [["2", "1$/T"], ["1$/T", "1$/T"]]
    entrepots = ["10.2T", "20T"]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        Verif_Data(data)

    clients = ["21.5T", "21.5T.1"]
    cout = [["2$/T", "1$/T"], ["1$/T", "1$/T"]]
    entrepots = ["10.2T", "20"]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        Verif_Data(data)