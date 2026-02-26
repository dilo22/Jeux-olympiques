import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk

class MatchManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Gérer la table Match")

        # Cadre pour la recherche
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        # Barre de recherche pour l'ID du match
        tk.Label(search_frame, text="Rechercher par ID Match:").pack(side=tk.LEFT, padx=5)
        self.entry_search_id_match = tk.Entry(search_frame)
        self.entry_search_id_match.pack(side=tk.LEFT, padx=5)

        # Bouton pour déclencher la recherche
        self.btn_search = tk.Button(search_frame, text="Rechercher", command=self.rechercher_match)
        self.btn_search.pack(side=tk.LEFT, padx=5)

        # Tableau d'affichage des matchs
        self.tree = ttk.Treeview(self.root, columns=("id_match", "id_evenement", "phase", "date"), show="headings")
        self.tree.heading("id_match", text="ID Match")
        self.tree.heading("id_evenement", text="ID Événement")
        self.tree.heading("phase", text="Phase")
        self.tree.heading("date", text="Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Ajout de la barre de défilement (scrollbar) à droite
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Boutons de modification et suppression
        self.btn_update = tk.Button(self.root, text="Modifier le match", command=self.modifier_match)
        self.btn_update.pack(pady=5)

        self.btn_delete = tk.Button(self.root, text="Supprimer le match", command=self.supprimer_match)
        self.btn_delete.pack(pady=5)

        self.load_data()

    def load_data(self):
        matches = self.db_manager.fetch_all_matches()
        for match in matches:
            self.tree.insert("", "end", values=match)

    def rechercher_match(self):
        # Récupérer l'ID du match recherché
        search_id_match = self.entry_search_id_match.get().strip()

        # Réinitialiser le tableau d'affichage
        self.tree.delete(*self.tree.get_children())

        if search_id_match:
            # Filtrer les matchs selon l'ID recherché
            matches = self.db_manager.fetch_match_by_id(search_id_match)
            for match in matches:
                self.tree.insert("", "end", values=match)
        else:
            # Recharger tous les matchs si aucun critère n'est défini
            self.load_data()

    def modifier_match(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un match à modifier.")
            return

        match_id = self.tree.item(selected_item)["values"][0]
        new_id_evenement = simpledialog.askstring("Modifier l'événement", "Nouvel ID Événement:")
        new_phase = simpledialog.askstring("Modifier la phase", "Nouvelle phase:")
        new_date = simpledialog.askstring("Modifier la date", "Nouvelle date (AAAA-MM-JJ):")

        if new_id_evenement and new_phase and new_date:
            self.db_manager.update_match(match_id, new_id_evenement, new_phase, new_date)
            messagebox.showinfo("Succès", "Le match a été modifié avec succès.")
            self.tree.delete(*self.tree.get_children())
            self.load_data()

    def supprimer_match(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un match à supprimer.")
            return

        match_id = self.tree.item(selected_item)["values"][0]
        self.db_manager.delete_match(match_id)
        messagebox.showinfo("Succès", "Le match a été supprimé avec succès.")
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def run(self):
        self.root.mainloop()
