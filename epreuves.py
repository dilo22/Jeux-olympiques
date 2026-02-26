import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

class Epreuves():
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.create_widgets()

    def create_widgets(self):
        self.create_filters()

        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        colonnes = ("Nom Événement", "Phase")
        self.tree = ttk.Treeview(container, columns=colonnes, show="headings", height=10, yscrollcommand=scrollbar.set)
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.tree.yview)  

        # En-têtes des colonnes
        self.tree.heading("Nom Événement", text="Nom Événement", anchor=tk.CENTER)
        self.tree.heading("Phase", text="Phase", anchor=tk.CENTER)

        # Largeur des colonnes
        self.tree.column("Nom Événement", width=200, anchor=tk.CENTER)
        self.tree.column("Phase", width=150, anchor=tk.CENTER)

        # Associer l'événement de double-clic à une fonction
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.tree.selection()[0]
        nom_evenement = self.tree.item(selected_item, "values")[0]

        # Récupérer l'id_match associé à cet événement
        id_match = self.db_manager.get_id_match_from_evenement(nom_evenement)

        if id_match:
            # Ouvrir une nouvelle fenêtre pour afficher les participants
            self.open_participant_window(id_match)
        else:
            tk.messagebox.showerror("Erreur", "ID du match introuvable pour cet événement.")


    def open_participant_window(self, id_match):
        # Créer une nouvelle fenêtre
        participant_window = tk.Toplevel(self.root)
        participant_window.title(f"Participants pour le match {id_match}")

        # Ajouter un Treeview pour afficher les participants
        participant_tree = ttk.Treeview(participant_window, columns=("Participant", "Phase", "Résultat", "Médaille"), show="headings", height=10)
        participant_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Définir les en-têtes
        participant_tree.heading("Participant", text="Participant")
        participant_tree.heading("Phase", text="Phase")
        participant_tree.heading("Résultat", text="Résultat")
        participant_tree.heading("Médaille", text="Médaille")

        # Appeler la fonction pour récupérer les participants
        participants = self.db_manager.fetch_participations_by_match(id_match)

        # Insérer les participants dans le Treeview
        for participant in participants:
            participant_tree.insert("", "end", values=participant)



    def create_filters(self):
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10, padx=20, fill="x")

        date_label = tk.Label(filter_frame, text="Date :")
        date_label.grid(row=0, column=0, padx=5)

        # Générer les dates dans le format "YYYY-MM-DD"
        dates = [f"2024-07-{day:02d}" for day in range(24, 32)] + [f"2024-08-{day:02d}" for day in range(1, 12)]
        self.date_combobox = ttk.Combobox(filter_frame, values=dates, state="readonly")
        self.date_combobox.set("2024-07-24")  # Valeur par défaut

        self.date_combobox.grid(row=0, column=1, padx=5)

        # Liste déroulante "Toutes les équipes"
        equipe_label = tk.Label(filter_frame, text="Toutes les équipes :")
        equipe_label.grid(row=0, column=2, padx=5)
        delegations = self.db_manager.fetch_delegations2()
        self.equipe_combobox = ttk.Combobox(filter_frame, values=["Toutes les équipes"] + delegations, state="readonly")
        self.equipe_combobox.set("Toutes les équipes")
        self.equipe_combobox.grid(row=0, column=3, padx=5)

        # Liste déroulante "Tous les sports"
        sport_label = tk.Label(filter_frame, text="Tous les sports :")
        sport_label.grid(row=0, column=4, padx=5)
        disciplines = self.db_manager.fetch_all_disciplines()
        self.sport_combobox = ttk.Combobox(filter_frame, values=["Tous les sports"] + disciplines, state="readonly")
        self.sport_combobox.set("Tous les sports")
        self.sport_combobox.grid(row=0, column=5, padx=5)

        # Liste déroulante "Genres"
        genre_label = tk.Label(filter_frame, text="Genres :")
        genre_label.grid(row=1, column=0, padx=5)
        genres = ["Toutes genres", "Homme", "Femme", "Mixte"]
        self.genre_combobox = ttk.Combobox(filter_frame, values=genres, state="readonly")
        self.genre_combobox.set("Toutes genres")  # Valeur par défaut
        self.genre_combobox.grid(row=1, column=1, padx=5)

        # Liste déroulante "Phase"
        phase_label = tk.Label(filter_frame, text="Phase :")
        phase_label.grid(row=1, column=2, padx=5)
        phases = ["Toutes les phases", "Médaille"]
        self.phase_combobox = ttk.Combobox(filter_frame, values=phases, state="readonly")
        self.phase_combobox.set("Toutes les phases")  # Valeur par défaut
        self.phase_combobox.grid(row=1, column=3, padx=5)

        # Bouton pour appliquer les filtres
        filter_button = tk.Button(filter_frame, text="Rechercher", command=self.filtrer_donnees)
        filter_button.grid(row=2, column=4, padx=5)

    def afficher_donnees(self):
        # Récupérer la date sélectionnée
        date_selectionnee = self.date_combobox.get()
        #print(f"Date sélectionnée: {date_selectionnee}")  

        # Vider l'arbre pour insérer de nouvelles données
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Récupérer les épreuves filtrées en fonction des filtres sélectionnés
        epreuves = self.db_manager.fetch_epreuves_filtrees(date_selectionnee)

        # Remplir l'arbre avec les données récupérées
        for epreuve in epreuves:
            nom_evenement, phase = epreuve
            self.tree.insert("", "end", values=(nom_evenement, phase))

    def filtrer_donnees(self):
        # Récupérer les valeurs sélectionnées dans les filtres
        date = self.date_combobox.get()
        equipe = self.equipe_combobox.get()
        sport = self.sport_combobox.get()
        genre = self.genre_combobox.get()
        phase = self.phase_combobox.get()

        # Vider l'arbre pour insérer de nouvelles données
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Appliquer les filtres via la base de données
        epreuves_filtrees = self.db_manager.fetch_epreuves_filtrees(date, equipe, sport, genre, phase)

        # Insérer les données dans l'arbre
        for epreuve in epreuves_filtrees:
            nom_evenement, phase = epreuve
            self.tree.insert("", "end", values=(nom_evenement, phase))

