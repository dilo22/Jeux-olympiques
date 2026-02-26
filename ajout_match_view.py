import tkinter as tk
from tkinter import messagebox

class AjoutMatchView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Ajouter un match")

        # Champs pour la table 'match'
        self.label_id_match = tk.Label(self.root, text="ID du match :")
        self.label_id_match.pack(pady=5)
        self.entry_id_match = tk.Entry(self.root)
        self.entry_id_match.pack(pady=5)

        self.label_id_evenement = tk.Label(self.root, text="ID de l'événement :")
        self.label_id_evenement.pack(pady=5)
        self.entry_id_evenement = tk.Entry(self.root)
        self.entry_id_evenement.pack(pady=5)

        self.label_phase = tk.Label(self.root, text="Phase :")
        self.label_phase.pack(pady=5)
        self.entry_phase = tk.Entry(self.root)
        self.entry_phase.pack(pady=5)

        self.label_date = tk.Label(self.root, text="Date (AAAA-MM-JJ) :")
        self.label_date.pack(pady=5)
        self.entry_date = tk.Entry(self.root)
        self.entry_date.pack(pady=5)

        # Bouton pour ajouter le match
        self.btn_add_match = tk.Button(self.root, text="Ajouter le match", command=self.ajouter_match)
        self.btn_add_match.pack(pady=10)

    def ajouter_match(self):
        # Récupérer les données des champs
        id_match = self.entry_id_match.get().strip()
        id_evenement = self.entry_id_evenement.get().strip()
        phase = self.entry_phase.get().strip()
        date = self.entry_date.get().strip()

        # Vérifier si tous les champs sont remplis
        if id_match and id_evenement and phase and date:
            try:
                # Vérifier si le match existe déjà
                if not self.db_manager.match_existe(id_match):
                    # Insérer dans la table 'match'
                    self.db_manager.insert_match(id_match, id_evenement, phase, date)
                    messagebox.showinfo("Succès", "Match ajouté avec succès.")
                else:
                    messagebox.showwarning("Erreur", "Un match avec cet ID existe déjà.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le match : {e}")
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")

    def run(self):
        self.root.mainloop()
