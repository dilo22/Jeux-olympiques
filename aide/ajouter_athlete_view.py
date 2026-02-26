import tkinter as tk
from tkinter import messagebox

class AjouterAthleteView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()  
        self.root.title("Ajouter un Athlète")

        # Labels et champs d'entrée pour les informations de l'athlète
        self.label_nom = tk.Label(self.root, text="Nom de l'athlète :")
        self.label_nom.pack(pady=5)
        self.entry_nom = tk.Entry(self.root)
        self.entry_nom.pack(pady=5)

        self.label_prenom = tk.Label(self.root, text="Prénom de l'athlète :")
        self.label_prenom.pack(pady=5)
        self.entry_prenom = tk.Entry(self.root)
        self.entry_prenom.pack(pady=5)

        self.label_sexe = tk.Label(self.root, text="Sexe de l'athlète :")
        self.label_sexe.pack(pady=5)
        self.entry_sexe = tk.Entry(self.root)
        self.entry_sexe.pack(pady=5)

        self.label_delegation = tk.Label(self.root, text="ID de la délégation :")
        self.label_delegation.pack(pady=5)
        self.entry_delegation = tk.Entry(self.root)
        self.entry_delegation.pack(pady=5)

        self.label_discipline = tk.Label(self.root, text="ID de la discipline :")
        self.label_discipline.pack(pady=5)
        self.entry_discipline = tk.Entry(self.root)
        self.entry_discipline.pack(pady=5)

        self.button_add = tk.Button(self.root, text="Ajouter", command=self.ajouter_athlete)
        self.button_add.pack(pady=10)

    def ajouter_athlete(self):
        # Récupérer les données saisies
        nom = self.entry_nom.get().strip().upper()
        prenom = self.entry_prenom.get().strip().capitalize()
        sexe = self.entry_sexe.get().strip().upper()
        delegation = self.entry_delegation.get().strip()
        discipline = self.entry_discipline.get().strip()

        if nom and prenom and sexe and delegation and discipline:
            try:
                # Insertion dans la base de données
                self.db_manager.insert_athlete(nom, prenom, sexe, delegation, discipline)
                messagebox.showinfo("Succès", "Athlète ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter l'athlète : {e}")
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")

    def run(self):
        self.root.mainloop()
