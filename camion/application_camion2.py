"""Description.

Module contenant l'interface utilisateur de la librairie transport et format.
"""

import typer
from rich import print
import lib_transport_camion2 as lt
import lib_format_camion2 as lf


def callback():
    """
    Merci d'utiliser notre application !

    Pour lancer l'application vous avez seulement besoin d'écrire dans la console: >>> python application.py start

    Après avoir donné le nom de votre fichier.

    Vous pouvez choisir entre 8 commandes différentes. Ces commandes sont disponibles dans l'aide ci-dessous.

    Si vous voulez utilisez une des commandes seule il faut préciser dans la console le fichier que vous voulez utiliser:
    Exemple: >>> python application.py total-cout nom_de_fichier.csv
    """


app = typer.Typer(callback=callback)


def get_data(chemin: str):
    try:
        data = lt.import_data(chemin)
        lt.Verif_Data(data)
        return data
    except:
        lt.Verif_Data(lt.import_data(chemin))
        print("Erreur lors du chargement des données.")
        raise typer.Abort()


def capacite():
    input


@app.command()
def total_cout(chemin: str,capacite : int, CF:int):
    """Renvoie le coût total minimal pour livrer tous les clients"""
    data = get_data(chemin)
    print("Le coût total minimal est de " + str(lf.total_cout(data,capacite,CF)) + "$.")


@app.command()
def total_quantite(chemin: str):
    """Renvoie les quantités totales livrées lorsque l'on minimise les coûts de transport."""
    data = get_data(chemin)
    print("La quantité livré est " + str(lf.total_res(data)) + ".")


@app.command()
def resultat_client(chemin: str,capacite : int, CF:int):
    """\033[32mTableau de résultat donnant le coût par client et le nombre d'entrepôt qui le livre."""
    data = get_data(chemin)
    print(lf.client_res(data,capacite,CF))


@app.command()
def resultat_entrepot(chemin: str,capacite : int, CF:int):
    """\033[34mTableau de résultat donnant le coût par entrepôt et le nombre de client livré."""
    data = get_data(chemin)
    print(lf.entrepot_res(data,capacite,CF))


@app.command()
def representation(chemin: str):
    """Renvoie une représentation graphique des différentes livraison entre les entrepots et clients."""
    data = get_data(chemin)
    print(lt.graphe(data))


@app.command()
def representation_client(chemin: str):
    """\033[32mRenvoie une représentation graphique des différentes livraison entre les entrepots et un client au choix."""
    data = get_data(chemin)
    client_i = input("Numéro du client : ")
    client = int(client_i)
    print(lt.graphe_client(data=data, client=client))


@app.command()
def representation_entrepot(chemin: str):
    """\033[34mRenvoie une représentation graphique des différentes livraison entre un entrepot au choix et les différents clients."""
    data = get_data(chemin)
    entrepot_i = input("Numéro de l'entrepot : ")
    entrepot = int(entrepot_i)
    print(lt.graphe_entrepot(data=data, entrepot=entrepot))


@app.command()
def start(
    chemin: str = typer.Option(
        None, "--chemin", prompt="Entrez le chemin du fichier de données"
    ),
    capacite: int = typer.Option(None, "--capacite", prompt="Capacité d'un camion (en T)"),
    CF: int = typer.Option(None, "--CF", prompt="Valeur du CF pour l'utilisation d'un camion"),
    choix: str = typer.Option(
        "Les différentes commandes sont disponible dans l'aide",
        "--choix",
        prompt="Quelle commande souhaitez-vous lancer ?",
    ),
):
    """\033[31mCommande qui regroupe toute les autres et qui permet de les utiliser à la suite avec la même base de données."""
    lt.Verif_Chemin(chemin)
    while True:
        if choix == "total-cout":
            total_cout(chemin,capacite,CF)
        elif choix == "total-quantite":
            total_quantite(chemin)
        elif choix == "resultat-client":
            resultat_client(chemin,capacite,CF)
        elif choix == "resultat-entrepot":
            resultat_entrepot(chemin,capacite,CF)
        elif choix == "representation":
            representation(chemin)
        elif choix == "representation-client":
            representation_client(chemin)
        elif choix == "representation-entrepot":
            representation_entrepot(chemin)
        else:
            print("Commande invalide.")

        relancer = input("Voulez-vous relancer une commande ? (oui/non): ")
        if relancer.lower() == "oui":
            choix = typer.prompt("Quelle commande souhaitez-vous lancer ?")
        else:
            break


if __name__ == "__main__":
    app()
