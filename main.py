import os

import tkinter as tk
from tkinter import Menu
from db_manager import DBManager  
from tableau_medaille import TableauMedaille  
from medailles import Medailles  
from epreuves import Epreuves  
from PIL import Image, ImageTk
from aide.main_view import MainView


from aide.athlete_view import AthleteView
from aide.country_view import CountryView
from aide.athlete_view import AthleteView
from aide.ajouter_athlete_view import AjouterAthleteView  
from aide.modifier_athlete import ModifierAthleteView
from aide.supprimer_athlete import SupprimerAthleteView

class MainApp:
    def __init__(self, root):
        self.root = root
        self.db_manager = DBManager()
        self.db_manager.connect_db()

        # Création du menu principal
        self.create_menu()

        self.header_frame = tk.Frame(self.root, bg="white")
        self.header_frame.pack(pady=10)

        self.create_header()

        self.create_buttons()

        self.display_frame = tk.Frame(self.root, bg="white")
        self.display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.afficher_tableau()

    def create_menu(self):
        
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Menu "Fichier"
        fichier_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=fichier_menu)
        fichier_menu.add_command(label="Administration", command=self.open_main_view)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Quitter", command=self.root.quit)


    def open_main_view(self):
        main_window = tk.Toplevel(self.root)
        main_window.title("Interface Principale")
        MainView(main_window, self.db_manager)

    def create_header(self):
        base_dir = os.path.dirname(__file__)
        image_path = os.path.join(base_dir, "images", "logo.jpg")
        image = Image.open(image_path)
        image = image.resize((200, 150), Image.Resampling.LANCZOS)  
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self.header_frame, image=self.photo, bg="white")
        self.image_label.pack(side=tk.TOP, pady=10)

        self.title_label = tk.Label(self.header_frame, text="JEUX OLYMPIQUES 2024 PARIS", font=("Helvetica", 16, "bold"), bg="white")
        self.title_label.pack(side=tk.BOTTOM, pady=10)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.pack(pady=10)

        # Boutons pour basculer entre les vues avec changement de curseur
        btn_tableau = tk.Button(self.button_frame, text="Tableau des Médailles", command=self.afficher_tableau, bg="lightblue", width=16, height=1, cursor="hand2")
        btn_tableau.grid(row=0, column=0, padx=10)

        btn_medailles = tk.Button(self.button_frame, text="Médaillé(e)s", command=self.afficher_medailles, bg="lightblue", width=16, height=1, cursor="hand2")
        btn_medailles.grid(row=0, column=1, padx=10)

        btn_epreuves = tk.Button(self.button_frame, text="Tous les épreuves", command=self.afficher_epreuves, bg="lightblue", width=16, height=1, cursor="hand2")
        btn_epreuves.grid(row=0, column=2, padx=10)


    def afficher_tableau(self):
        self.clear_display()
        tableau = TableauMedaille(self.display_frame, self.db_manager)
        tableau.afficher_donnees()

    def afficher_medailles(self):
        self.clear_display()
        medailles = Medailles(self.display_frame, self.db_manager)
        medailles.afficher_donnees()

    def afficher_epreuves(self):
        self.clear_display()
        epreuves = Epreuves(self.display_frame, self.db_manager)
        epreuves.afficher_donnees()

    def clear_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    # Fonction pour ouvrir la fenêtre d'aide
    def open_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Aide")
        help_window.geometry("300x200")
        label = tk.Label(help_window, text="Ceci est une fenêtre d'aide.\nVous pouvez naviguer dans l'application en utilisant les boutons ci-dessus.", font=("Helvetica", 12))
        label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("JEUX OLYMPIQUES 2024 PARIS")
    root.configure(bg="white")

    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "images", "icone.ico")

    root.iconbitmap(icon_path)

    root.geometry("880x700") 
    app = MainApp(root)
    root.mainloop()
