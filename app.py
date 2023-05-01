"""Description.

Module contenant l'interface utilisateur de la librairie transport et format.
"""

import typer
from rich import print
from lib.lib_transport import *
import lib.lib_format as lf
from lib.lib_graphe import *
from lib.lib_dataclass import *


def callback():
    """
    Merci d'utiliser notre application !

    Pour lancer l'application vous avez seulement besoin d'écrire dans la console: >>> python app.py

    Après avoir donné le nom de votre fichier.

    Vous pouvez choisir entre 7 commandes différentes. Ces commandes sont disponibles dans l'aide ci-dessous.

    Si vous voulez utilisez une des commandes seule il faut préciser dans la console le fichier que vous voulez utiliser:
    Exemple: >>> python app.py total-cout nom_de_fichier.csv
    """


app = typer.Typer(callback=callback, add_completion=True)


def get_data(chemin: str):
    try:
        data = import_data(chemin)
        Verif_Data(data)
        return data
    except:
        Verif_Data(import_data(chemin))
        print("Erreur lors du chargement des données.")
        raise typer.Abort()


@app.command("total-cout")
def total_cout(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    )
):
    """Renvoie le coût total minimal pour livrer tous les clients"""
    data = get_data(chemin)
    print("Le coût total minimal est de " + str(lf.total_cout(data)) + "$.")


@app.command("total-quantite")
def total_quantite(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    )
):
    """Renvoie les quantités totales livrées lorsque l'on minimise les coûts de transport."""
    data = get_data(chemin)
    print("La quantité livré est " + str(lf.total_res(data)) + ".")


@app.command("resultat-client")
def resultat_client(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    )
):
    """Tableau de résultat donnant le coût par client et le nombre d'entrepôt qui le livre."""
    data = get_data(chemin)
    print(lf.client_res(data))


@app.command("resultat-entrepot")
def resultat_entrepot(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    )
):
    """Tableau de résultat donnant le coût par entrepôt et le nombre de client livré."""
    data = get_data(chemin)
    print(lf.entrepot_res(data))


@app.command("representation")
def representation(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    )
):
    """Renvoie une représentation graphique des différentes livraison entre les entrepots et clients."""
    data = get_data(chemin)
    print(graphe(data))


@app.command("representation-client")
def representation_client(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    ),
    client: str = typer.Option(
        None,
        "--client",
        prompt="Numéro du client",
        help="Choix du client à visualiser.",
    ),
):
    """Renvoie une représentation graphique des différentes livraison entre les entrepots et un client au choix."""
    data = get_data(chemin)
    print(graphe_client(data=data, client=int(client)))


@app.command("representation-entrepot")
def representation_entrepot(
    chemin: str = typer.Option(
        None,
        "--chemin",
        prompt="Entrez le chemin du fichier de données",
        help="Chemin du fichier de travail",
    ),
    entrepot: str = typer.Option(
        None,
        "--entrepot",
        prompt="Numéro de l'entrepot",
        help="Choix de l'entrepôt à visualiser.",
    ),
):
    """Renvoie une représentation graphique des différentes livraison entre un entrepot au choix et les différents clients."""
    data = get_data(chemin)
    print(graphe_entrepot(data=data, entrepot=int(entrepot)))


if __name__ == "__main__":
    typer.run(app())
