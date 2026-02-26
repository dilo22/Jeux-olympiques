import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk

class ParticipationManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Gérer la table Participation")
        
        # Configuration de la fenêtre principale
        self.root.geometry("900x500")  # Ajustement de la taille de la fenêtre

        # Cadre pour les barres de recherche
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        # Barre de recherche pour l'ID du match
        tk.Label(search_frame, text="Rechercher par ID Match:").pack(side=tk.LEFT, padx=5)
        self.entry_search_id_match = tk.Entry(search_frame)
        self.entry_search_id_match.pack(side=tk.LEFT, padx=5)
        
        # Barre de recherche pour l'ID du participant
        tk.Label(search_frame, text="Rechercher par ID Participant:").pack(side=tk.LEFT, padx=5)
        self.entry_search_id_participant = tk.Entry(search_frame)
        self.entry_search_id_participant.pack(side=tk.LEFT, padx=5)
        
        
        # Bouton pour déclencher la recherche
        self.btn_search = tk.Button(search_frame, text="Rechercher", command=self.rechercher_participation)
        self.btn_search.pack(side=tk.LEFT, padx=5)

        # Tableau d'affichage des participations
        self.tree = ttk.Treeview(self.root, columns=("id_match", "id_participant", "resultat", "medaille", "type_resultat"), show="headings")
        self.tree.heading("id_match", text="ID Match")
        self.tree.heading("id_participant", text="ID Participant")
        self.tree.heading("resultat", text="Résultat")
        self.tree.heading("medaille", text="Médaille")
        self.tree.heading("type_resultat", text="Type de résultat")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Ajout de la barre de défilement verticale
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Boutons de modification et suppression
        self.btn_update = tk.Button(self.root, text="Modifier la participation", command=self.modifier_participation)
        self.btn_update.pack(pady=5)

        self.btn_delete = tk.Button(self.root, text="Supprimer la participation", command=self.supprimer_participation)
        self.btn_delete.pack(pady=5)

        self.load_data()

    def load_data(self):
        participations = self.db_manager.fetch_all_participations()
        for participation in participations:
            self.tree.insert("", "end", values=participation)

    def rechercher_participation(self):
        # Récupérer les valeurs des champs de recherche
        search_id_match = self.entry_search_id_match.get().strip()
        search_id_participant = self.entry_search_id_participant.get().strip()

        # Construire la requête de recherche en fonction des valeurs fournies
        participations = self.db_manager.fetch_all_participations()

        # Filtrer en fonction des critères de recherche
        filtered_data = []
        for participation in participations:
            if (search_id_match and str(participation[0]) == search_id_match) or (search_id_participant and str(participation[1]) == search_id_participant):
                filtered_data.append(participation)

        # Réinitialiser l'affichage du tableau
        self.tree.delete(*self.tree.get_children())
        
        # Insérer les résultats filtrés dans le tableau
        for participation in filtered_data:
            self.tree.insert("", "end", values=participation)

    def modifier_participation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une participation à modifier.")
            return

        # Récupérer les données de la ligne sélectionnée
        participation_data = self.tree.item(selected_item)["values"]
        id_match = participation_data[0]
        id_participant = participation_data[1]

        # Fenêtre de modification pour tous les champs d'un coup
        window = tk.Toplevel(self.root)
        window.title("Modifier la participation")

        tk.Label(window, text="Résultat:").pack(pady=5)
        entry_resultat = tk.Entry(window)
        entry_resultat.pack(pady=5)
        entry_resultat.insert(0, participation_data[2])

        tk.Label(window, text="Médaille (or, argent, bronze, aucun):").pack(pady=5)
        entry_medaille = tk.Entry(window)
        entry_medaille.pack(pady=5)
        entry_medaille.insert(0, participation_data[3])

        tk.Label(window, text="Type de résultat (MIN ou MAX):").pack(pady=5)
        entry_type_resultat = tk.Entry(window)
        entry_type_resultat.pack(pady=5)
        entry_type_resultat.insert(0, participation_data[4])

        def save_changes():
            new_resultat = entry_resultat.get().strip()
            new_medaille = entry_medaille.get().strip().lower()
            new_type_resultat = entry_type_resultat.get().strip().upper()

            if new_resultat and new_medaille and new_type_resultat:
                self.db_manager.update_participation(id_match, id_participant, new_resultat, new_medaille, new_type_resultat)
                messagebox.showinfo("Succès", "La participation a été modifiée avec succès.")
                self.tree.delete(*self.tree.get_children())
                self.load_data()
                window.destroy()
            else:
                messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")

        tk.Button(window, text="Enregistrer", command=save_changes).pack(pady=10)

    def supprimer_participation(self):
        # Obtenir la sélection dans l'interface
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une participation à supprimer.")
            return

        # Récupérer les valeurs sélectionnées dans l'interface (id_match et id_participant)
        participation_data = self.tree.item(selected_item)["values"]
        if len(participation_data) < 2:
            messagebox.showwarning("Données manquantes", "Impossible de récupérer les informations de la participation.")
            return

        # Extraire id_match et id_participant
        id_match = participation_data[0]
        id_participant = participation_data[1]

        try:
            # Appeler la méthode delete_participation avec les bons arguments
            self.db_manager.delete_participation(id_match, id_participant)
            messagebox.showinfo("Succès", "La participation a été supprimée avec succès.")
            
            # Rafraîchir l'interface après suppression
            self.tree.delete(*self.tree.get_children())
            self.load_data()  # Recharger les données dans l'interface
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression de la participation : {e}")

    def run(self):
        self.root.mainloop()
