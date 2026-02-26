import tkinter as tk
from tkinter import messagebox

class ModifierAthleteView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Modifier un Athlète")

        # Champ pour rechercher l'athlète
        self.label_id = tk.Label(self.root, text="ID de l'athlète :")
        self.label_id.pack(pady=5)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.pack(pady=5)

        self.button_search = tk.Button(self.root, text="Rechercher", command=self.rechercher_athlete)
        self.button_search.pack(pady=10)

        # Champs pour les informations à modifier
        self.label_nom = tk.Label(self.root, text="Nom de l'athlète :")
        self.entry_nom = tk.Entry(self.root)
        self.label_nom.pack(pady=5)
        self.entry_nom.pack(pady=5)

        self.label_prenom = tk.Label(self.root, text="Prénom de l'athlète :")
        self.entry_prenom = tk.Entry(self.root)
        self.label_prenom.pack(pady=5)
        self.entry_prenom.pack(pady=5)

        self.label_sexe = tk.Label(self.root, text="Sexe de l'athlète :")
        self.entry_sexe = tk.Entry(self.root)
        self.label_sexe.pack(pady=5)
        self.entry_sexe.pack(pady=5)

        self.label_delegation = tk.Label(self.root, text="ID de la délégation :")
        self.entry_delegation = tk.Entry(self.root)
        self.label_delegation.pack(pady=5)
        self.entry_delegation.pack(pady=5)

        self.label_medaille_or = tk.Label(self.root, text="Médailles d'or :")
        self.entry_medaille_or = tk.Entry(self.root)
        self.label_medaille_or.pack(pady=5)
        self.entry_medaille_or.pack(pady=5)

        self.label_medaille_argent = tk.Label(self.root, text="Médailles d'argent :")
        self.entry_medaille_argent = tk.Entry(self.root)
        self.label_medaille_argent.pack(pady=5)
        self.entry_medaille_argent.pack(pady=5)

        self.label_medaille_bronze = tk.Label(self.root, text="Médailles de bronze :")
        self.entry_medaille_bronze = tk.Entry(self.root)
        self.label_medaille_bronze.pack(pady=5)
        self.entry_medaille_bronze.pack(pady=5)

        self.label_discipline = tk.Label(self.root, text="ID de la discipline :")
        self.entry_discipline = tk.Entry(self.root)
        self.label_discipline.pack(pady=5)
        self.entry_discipline.pack(pady=5)

        self.button_update = tk.Button(self.root, text="Modifier", command=self.modifier_athlete)
        self.button_update.pack(pady=10)

    def rechercher_athlete(self):
        # Rechercher l'athlète par ID et pré-remplir les champs
        id_athlete = self.entry_id.get().strip()
        athlete = self.db_manager.fetch_athlete_by_id(id_athlete)

        if athlete:
            self.entry_nom.delete(0, tk.END)
            self.entry_prenom.delete(0, tk.END)
            self.entry_sexe.delete(0, tk.END)
            self.entry_delegation.delete(0, tk.END)
            self.entry_medaille_or.delete(0, tk.END)
            self.entry_medaille_argent.delete(0, tk.END)
            self.entry_medaille_bronze.delete(0, tk.END)
            self.entry_discipline.delete(0, tk.END)

            # Insertion des valeurs dans les champs
            self.entry_nom.insert(0, athlete[0] if athlete[0] else "")
            self.entry_prenom.insert(0, athlete[1] if athlete[1] else "")
            self.entry_sexe.insert(0, athlete[2] if athlete[2] else "")
            self.entry_delegation.insert(0, athlete[3] if athlete[3] else "")
            self.entry_medaille_or.insert(0, athlete[4] if athlete[4] else "")
            self.entry_medaille_argent.insert(0, athlete[5] if athlete[5] else "")
            self.entry_medaille_bronze.insert(0, athlete[6] if athlete[6] else "")
            self.entry_discipline.insert(0, athlete[7] if athlete[7] else "")
        else:
            messagebox.showerror("Erreur", "Athlète introuvable.")


    def modifier_athlete(self):
        # Récupérer les données saisies
        id_athlete = self.entry_id.get().strip()
        nom = self.entry_nom.get().strip().upper()
        prenom = self.entry_prenom.get().strip().capitalize()
        sexe = self.entry_sexe.get().strip().upper()
        delegation = self.entry_delegation.get().strip()

        # Si les médailles sont vides, on les remplace par zéro ou None
        medaille_or = self.entry_medaille_or.get().strip()
        medaille_argent = self.entry_medaille_argent.get().strip()
        medaille_bronze = self.entry_medaille_bronze.get().strip()
        discipline = self.entry_discipline.get().strip()

        # Convertir les médailles en entier ou None
        medaille_or = int(medaille_or) if medaille_or.isdigit() else 0
        medaille_argent = int(medaille_argent) if medaille_argent.isdigit() else 0
        medaille_bronze = int(medaille_bronze) if medaille_bronze.isdigit() else 0

        # Mettre à jour l'athlète
        try:
            self.db_manager.update_athlete(id_athlete, nom, prenom, sexe, delegation, medaille_or, medaille_argent, medaille_bronze, discipline)
            messagebox.showinfo("Succès", "Athlète modifié avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de modifier l'athlète : {e}")


    def run(self):
        self.root.mainloop()
