import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from lib.lib_graphe import graphe, graphe_client, graphe_entrepot
import pytest


def test_graphe():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    graphe(data)
    plt.close()
    
    assert True

def test_graphe_client():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    graphe_client(data,1)
    plt.close()
    
    assert True
    
def test_graphe_client_2():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        graphe_client(data,-1)
        
def test_graphe_client_3():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        graphe_client(data,1000)
    
    
def test_graphe_entrepot():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    graphe_entrepot(data,1)
    plt.close()
    
    assert True
    
def test_graphe_entrepot_2():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        graphe_entrepot(data,-1)

def test_graphe_entrepot_3():
    clients = ["8.5T", "21.5T"]
    entrepots = ["10.2T", "20T"]
    cout = [["2$/T", "2$/T"], ["2$/T", "2$/T"]]
    data = pd.DataFrame(data=cout, index=entrepots, columns=clients)
    with pytest.raises(ValueError):
        graphe_entrepot(data,1000)
    