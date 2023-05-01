import sys
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, DirectoryTree, Label, Input, Footer
from textual.containers import  VerticalScroll, Horizontal, Grid
from textual.reactive import var, reactive
from lib.lib_graphe import *
from lib.lib_transport import *
from lib.lib_format import *


class QuitScreen(Screen):
    """Ecran qui nous permet de quitter l'application."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Voulez vous vraiment quitter l'application ?", id="question"),
            Button("Quitter", variant="error", id="quit"),
            Button("Annuler", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class ErrorScreen(Screen):
    """Ecran qui apparait lors d'une erreur et qui affiche celle-ci."""
    ...
    #en developpement



class ResultScreen(Screen):
    """Ecran qui donne le résultat de la commande choisie."""
    def __init__(self, content: str):
        self.content = content
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            VerticalScroll(Label(self.content), id="left"),
            VerticalScroll(
                Grid(
                    Label("Voulez-vous continuer ?", id="question"),
                    Button("Oui", variant="success", id="cancel"),
                    Button("Non", variant="error", id="quit"),
                    id="dialog"), 
            id="right"
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()



class MyApp(App):

    CSS_PATH = "aes.css"

    chemin = var(str)
    sortie = var(str)
    show_tree = var(True)
    num_c = reactive(1)
    num_e = reactive(1)


    BINDINGS = [
        ("q", "request_quit", "Quitter l'application")
    ]


    def compose(self) -> ComposeResult:
        path = "./" if len(sys.argv) < 2 else sys.argv[1] 
        yield Horizontal(
            VerticalScroll(DirectoryTree(path, id="tree-view")),
            VerticalScroll(Static("Les commandes:", classes="header"),
                           Button("Total coût", id="total_c"),
                           Button("Total quantité", id = "total_q"),
                           Button("Représentation", id = "rep")
                           ),
            VerticalScroll(Static("Client", classes="header"),
                           Button.success("Résultat client", id="res_client"),
                           Button.success("Représentation client", id = "rep_client"),
                           Input(placeholder="Numéro du Client", id="num_client")
                           ),
            VerticalScroll(Static("Entrepôt", classes="header"),
                           Button("Résultat entrepot", variant="primary", id="res_entrepot"),
                           Button("Représentation entrepot", variant="primary", id = "rep_entrepot"),
                           Input(placeholder="Numéro de l'entrepot", id="num_entrepot")
                           ),
                           )
        yield Footer()


    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        self.chemin = event.path

    def on_input_changed(self, event: Input.Changed) -> None:  
        """Lorsque la valeur des inputbox change, change le graphe demandé."""
        input_id = event.input.id
        if input_id == "num_client":
            self.num_c = int(event.value or "1")
        if input_id == "num_entrepot":
            self.num_e = int(event.value or "1")
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Lorsque l'on appuie sur l'un des boutons de l'accueil, lance la commande en question."""
        button_id = event.button.id
        assert button_id is not None

        if button_id == "total_c":
            content = "Le coût total minimal est de " + str(total_cout(lt.import_data(self.chemin))) + "$."
            self.push_screen(ResultScreen(content))
        elif button_id == "total_q":
            content = "La quantité livré est " + str(total_res(lt.import_data(self.chemin))) + "."
            self.push_screen(ResultScreen(content))
        elif button_id == "rep":
            self.sortie = graphe(lt.import_data(self.chemin))
        elif button_id == "res_client":
            content = client_res(lt.import_data(self.chemin))
            self.push_screen(ResultScreen(content))
        elif button_id == "res_entrepot":
            content = entrepot_res(lt.import_data(self.chemin))
            self.push_screen(ResultScreen(content))
        elif button_id == "rep_client":
            self.sortie = graphe_client(lt.import_data(self.chemin), client=self.num_c)
        elif button_id == "rep_entrepot":
            self.sortie = graphe_entrepot(lt.import_data(self.chemin), entrepot=self.num_e)
        #rajouter le fait que si il y a une erreur, erreur = msg.erreur

    
    def action_request_quit(self) -> None:
        """Lorsque l'utilisateur appuie sur la touche Q, lance l'écran qui permet de quitter l'application."""
        self.push_screen(QuitScreen())


if __name__ == "__main__":
    app = MyApp()
    app.run()
