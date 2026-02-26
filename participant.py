import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk

class ParticipantManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Gérer la table Participant")
        
        # Configuration de la fenêtre principale
        self.root.geometry("900x500")  # Ajustement de la taille de la fenêtre

        # Cadre pour les barres de recherche
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        # Barre de recherche pour l'ID du participant
        tk.Label(search_frame, text="Rechercher par ID Participant:").pack(side=tk.LEFT, padx=5)
        self.entry_search_id_participant = tk.Entry(search_frame)
        self.entry_search_id_participant.pack(side=tk.LEFT, padx=5)
        
        # Barre de recherche pour l'ID de l'athlète
        tk.Label(search_frame, text="Rechercher par ID Athlète:").pack(side=tk.LEFT, padx=5)
        self.entry_search_id_athlete = tk.Entry(search_frame)
        self.entry_search_id_athlete.pack(side=tk.LEFT, padx=5)
        
        # Bouton pour déclencher la recherche
        self.btn_search = tk.Button(search_frame, text="Rechercher", command=self.rechercher_participant)
        self.btn_search.pack(side=tk.LEFT, padx=5)

        # Tableau d'affichage des participants
        self.tree = ttk.Treeview(self.root, columns=("id_participant", "type", "id_athlete", "id_delegation"), show="headings")
        self.tree.heading("id_participant", text="ID Participant")
        self.tree.heading("type", text="Type")
        self.tree.heading("id_athlete", text="ID Athlète")
        self.tree.heading("id_delegation", text="ID Délégation")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Ajout de la barre de défilement verticale
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Boutons de modification et suppression
        self.btn_update = tk.Button(self.root, text="Modifier le participant", command=self.modifier_participant)
        self.btn_update.pack(pady=5)

        self.btn_delete = tk.Button(self.root, text="Supprimer le participant", command=self.supprimer_participant)
        self.btn_delete.pack(pady=5)

        self.load_data()

    def load_data(self):
        participants = self.db_manager.fetch_all_participants()
        for participant in participants:
            self.tree.insert("", "end", values=participant)

    def rechercher_participant(self):
        # Récupérer les valeurs des champs de recherche
        search_id_participant = self.entry_search_id_participant.get().strip()
        search_id_athlete = self.entry_search_id_athlete.get().strip()

        # Construire la requête de recherche en fonction des valeurs fournies
        participants = self.db_manager.fetch_all_participants()

        # Filtrer en fonction des critères de recherche
        filtered_data = []
        for participant in participants:
            if (search_id_participant and str(participant[0]) == search_id_participant) or (search_id_athlete and str(participant[2]) == search_id_athlete):
                filtered_data.append(participant)

        # Réinitialiser l'affichage du tableau
        self.tree.delete(*self.tree.get_children())
        
        # Insérer les résultats filtrés dans le tableau
        for participant in filtered_data:
            self.tree.insert("", "end", values=participant)

    def modifier_participant(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un participant à modifier.")
            return

        # Récupérer les données de la ligne sélectionnée
        participant_data = self.tree.item(selected_item)["values"]
        participant_id = participant_data[0]

        # Fenêtre de modification pour tous les champs d'un coup
        window = tk.Toplevel(self.root)
        window.title("Modifier le participant")

        tk.Label(window, text="Type:").pack(pady=5)
        entry_type = tk.Entry(window)
        entry_type.pack(pady=5)
        entry_type.insert(0, participant_data[1])

        tk.Label(window, text="ID Athlète:").pack(pady=5)
        entry_id_athlete = tk.Entry(window)
        entry_id_athlete.pack(pady=5)
        entry_id_athlete.insert(0, participant_data[2])

        tk.Label(window, text="ID Délégation:").pack(pady=5)
        entry_id_delegation = tk.Entry(window)
        entry_id_delegation.pack(pady=5)
        entry_id_delegation.insert(0, participant_data[3])

        def save_changes():
            new_type = entry_type.get().strip()
            new_id_athlete = entry_id_athlete.get().strip()
            new_id_delegation = entry_id_delegation.get().strip()

            if new_type and new_id_athlete and new_id_delegation:
                self.db_manager.update_participant(participant_id, new_type, new_id_athlete, new_id_delegation)
                messagebox.showinfo("Succès", "Le participant a été modifié avec succès.")
                self.tree.delete(*self.tree.get_children())
                self.load_data()
                window.destroy()
            else:
                messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")

        tk.Button(window, text="Enregistrer", command=save_changes).pack(pady=10)

    def supprimer_participant(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un participant à supprimer.")
            return

        participant_id = self.tree.item(selected_item)["values"][0]
        self.db_manager.delete_participant(participant_id)
        messagebox.showinfo("Succès", "Le participant a été supprimé avec succès.")
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def run(self):
        self.root.mainloop()
