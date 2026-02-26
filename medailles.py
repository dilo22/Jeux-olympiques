import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os

class Medailles():
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.flag_images = {}  
        self.create_widgets()

    def create_widgets(self):
        # Configuration du tableau pour afficher les athlètes
        colonnes = ("Drapeau", "Athlète", "O", "A", "B", "Total")
        self.tree = ttk.Treeview(self.root, columns=colonnes, show="headings", height=10)
        self.tree.pack(pady=20, padx=20, fill="x", expand=True)

        # En-têtes des colonnes
        self.tree.heading("Drapeau", text="Drapeau", anchor=tk.CENTER)
        self.tree.heading("Athlète", text="Athlète", anchor=tk.CENTER)
        self.tree.heading("O", text="O", anchor=tk.CENTER)
        self.tree.heading("A", text="A", anchor=tk.CENTER)
        self.tree.heading("B", text="B", anchor=tk.CENTER)
        self.tree.heading("Total", text="Total", anchor=tk.CENTER)

        # Largeur des colonnes
        self.tree.column("Drapeau", width=50, anchor=tk.CENTER) 
        self.tree.column("Athlète", width=250, anchor=tk.CENTER)
        self.tree.column("O", width=70, anchor=tk.CENTER)
        self.tree.column("A", width=70, anchor=tk.CENTER)
        self.tree.column("B", width=70, anchor=tk.CENTER)
        self.tree.column("Total", width=100, anchor=tk.CENTER)

    def afficher_donnees(self):
        athletes = self.db_manager.fetch_athletes2()

        for athlete in athletes:
            nom, prenom, sexe, id_delegation, id_athlete, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, id_discipline = athlete

            # Combiner nom et prénom 
            nom_complet = f"{nom} {prenom}"

            total_medals = nb_medaille_or + nb_medaille_argent + nb_medaille_bronze

            flag_image = self.get_flag_image(id_delegation)

            self.tree.insert("", "end", values=(flag_image, nom_complet, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze, total_medals))

    def get_flag_image(self, id_delegation):
        """Charge l'image du drapeau associée à la délégation."""
        if id_delegation in self.flag_images:
            return self.flag_images[id_delegation]  

        flag_path = f"C:/Users/hibah/Desktop/L3/BD/TP2/images/{id_delegation}.png"
        if os.path.exists(flag_path):
            image = Image.open(flag_path)
            image = image.resize((30, 20), Image.ANTIALIAS)  
            photo = ImageTk.PhotoImage(image)
            self.flag_images[id_delegation] = photo 
            return photo
        else:
            # Si l'image n'existe pas
            return None