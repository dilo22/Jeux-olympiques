import tkinter as tk
from tkinter import messagebox

class RechercheParticipationView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Rechercher des participations")

        # Définir une taille de fenêtre plus grande (par exemple : largeur=1000, hauteur=600)
        self.root.geometry("1000x600")

        # Champs pour l'ID du match
        self.label_id_match = tk.Label(self.root, text="ID du match :")
        self.label_id_match.pack(pady=10)
        self.entry_id_match = tk.Entry(self.root)
        self.entry_id_match.pack(pady=10)

        # Bouton pour effectuer la recherche
        self.btn_rechercher = tk.Button(self.root, text="Rechercher", command=self.rechercher_participations)
        self.btn_rechercher.pack(pady=10)

        # Frame pour ajouter des barres de défilement
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Ajout des barres de défilement (horizontale et verticale)
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Zone de texte pour afficher les résultats, avec retour à la ligne désactivé (wrap='none')
        self.result_box = tk.Text(frame, wrap='none', width=120, height=25, 
                                  xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        self.result_box.pack(fill=tk.BOTH, expand=True)

        # Configurer les barres de défilement pour la zone de texte
        scrollbar_y.config(command=self.result_box.yview)
        scrollbar_x.config(command=self.result_box.xview)

    def rechercher_participations(self):
        # Récupérer l'ID du match
        id_match = self.entry_id_match.get().strip()

        if not id_match:
            messagebox.showwarning("Champ manquant", "Veuillez entrer un ID de match.")
            return

        try:
            # Requête pour récupérer les participations
            participations = self.db_manager.fetch_participations_by_match(id_match)

            # Effacer la zone de texte avant d'afficher les résultats
            self.result_box.delete(1.0, tk.END)

            if participations:
                for participation in participations:
                    participant_name, nom_evenement, resultat, medaille, type_resultat = participation
                    self.result_box.insert(tk.END, f"Participant : {participant_name}, Événement : {nom_evenement}, "
                                                   f"Résultat : {resultat}, Médaille : {medaille}, Type Résultat : {type_resultat}\n")
            else:
                self.result_box.insert(tk.END, "Aucune participation trouvée pour ce match.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche des participations : {e}")

    def run(self):
        self.root.mainloop()
