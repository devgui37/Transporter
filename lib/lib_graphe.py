import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from lib.lib_transport import livraison

def graphe(data: pd.DataFrame):
    """
    Génère et affiche un graphe représentant les liens entre les clients et les entrepôts,
    ainsi que les quantités de produit livrée à chaque client par chaque entrepôts.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.

    Returns:
    - None: La fonction affiche le graphe, mais ne renvoie rien.

    Example:
    >>> graphe(data)
    """
    data = livraison(data)

    # nom pour les nodes
    for i in range(len(data.columns)):
        new_name = "C" + str(data.columns[i])
        data = data.rename(columns={data.columns[i]: new_name})

    for i in range(len(data.index)):
        new_name = "E" + str(data.index[i])
        data = data.rename(index={data.index[i]: new_name})

    G = nx.Graph()

    # ajout noeuds
    for i in range(0, len(data)):
        G.add_node(data.columns[i])
        G.add_node(data.index[i])

    # ajout arrêtes
    for i in range(0, len(data.columns)):
        for j in range(0, len(data.index)):
            if data.iloc[j, i] > 0:
                G.add_edge(
                    data.columns[i], data.index[j], weight=float(data.iloc[j, i])
                )

    # couleurs noeuds
    for node in G.nodes():
        if node[0] == "C":
            color = "green"
        else:
            color = "blue"
        G.add_node(node, node_color=color)

    # représentation du graphe
    pos = nx.circular_layout(G)

    node_colors = [G.nodes[node]["node_color"] for node in G.nodes()]

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, alpha=0.6, node_color=node_colors)
    nx.draw_networkx_labels(G, pos)

    # labels
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # edges
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="black")

    plt.axis("off")
    plt.show()


def graphe_client(data: pd.DataFrame, client: int):
    """
    Génère et affiche un graphe représentant les liens entre un client choisi et les entrepôts,
    ainsi que les quantités de produit livrée à ce client par chaque entrepôts.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.
    - client (int): un entier représentant le numéro du client à visualiser dans le graphe.

    Returns:
    - None: La fonction affiche le graphe, mais ne renvoie rien.

    Example:
    >>> graphe_clients(data, 1)
    """
    data = livraison(data)

    if client > len(data.columns):
        raise ValueError("Numéro de client non existant")
    if client < 0:
        raise ValueError("Le numéro du client ne peut-être négatif")

    for i in range(len(data.index)):
        new_name = "E" + str(data.index[i])
        data = data.rename(index={data.index[i]: new_name})

    data = data.iloc[:, client - 1]
    G = nx.Graph()
    for i in range(0, len(data)):
        G.add_node("Client " + str(client))
        G.add_node(data.index[i])

    for j in range(0, len(data.index)):
        if data.iloc[j] > 0:
            G.add_edge(
                "Client " + str(client), data.index[j], weight=float(data.iloc[j])
            )

    # couleurs noeuds
    for node in G.nodes():
        if node[0] == "C":
            color = "green"
        else:
            color = "blue"
        G.add_node(node, node_color=color)

    # représentation du graphe
    pos = nx.circular_layout(G)

    node_colors = [G.nodes[node]["node_color"] for node in G.nodes()]

    pos = nx.circular_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, alpha=0.6, node_color=node_colors)
    nx.draw_networkx_labels(G, pos)

    # labels
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # edges
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="black")

    plt.axis("off")
    plt.show()


def graphe_entrepot(data: pd.DataFrame, entrepot: int):
    """
    Génère et affiche un graphe représentant les liens entre les clients et un entrepôt choisi,
    ainsi que les quantités de produit livrée aux clients par cet entrepôt.

    Args:
    - data (pd.DataFrame): un DataFrame contenant les informations sur les coûts de livraison, la quantité de produits disponibles et la demande des clients.
    - entrepot (int): un entier représentant le numéro de l'entrepot à visualiser dans le graphe.

    Returns:
    - None: La fonction affiche le graphe, mais ne renvoie rien.

    Example:
    >>> graphe_entrepot(data, 1)
    """

    data = livraison(data)
    
    if entrepot > len(data.columns):
        raise ValueError("Numéro d'entrepot non existant")
    if entrepot < 0:
        raise ValueError("Le numéro de l'entrepot ne peut-être négatif")
    
    #nom pour les nodes
    for i in range(len(data.columns)):
        new_name = "C" + str(data.columns[i])
        data = data.rename(columns={data.columns[i]: new_name})
        
    data = data.iloc[entrepot-1,:]
    G = nx.Graph()
    for i in range(0, len(data)):
        G.add_node("Entrepot " + str(entrepot))
        G.add_node(data.index[i])
            
    #ajout arrêtes   
    for j in range(0, len(data.index)):
        if data.iloc[j] > 0:
            G.add_edge("Entrepot " + str(entrepot), data.index[j], weight=float(data.iloc[j]))
        
    #couleurs noeuds 
    for node in G.nodes():
        if node[0] == 'C':
            color = 'green'
        else:
            color = 'blue'
        G.add_node(node, node_color=color)
        
    #représentation du graphe        
    pos = nx.circular_layout(G)

    node_colors = [G.nodes[node]['node_color'] for node in G.nodes()]

    #nodes
    nx.draw_networkx_nodes(G,pos,node_size=800, alpha=0.6,node_color=node_colors)
    nx.draw_networkx_labels(G, pos)

    #labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    #edges
    nx.draw_networkx_edges(G,pos,width=1)
    nx.draw_networkx_edge_labels(G,pos, edge_labels = labels, font_color= 'black')

    plt.axis("off")
    plt.show()