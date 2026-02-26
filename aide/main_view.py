import tkinter as tk
from athlete_view import AthleteView
from country_view import CountryView
from athlete_view import AthleteView
from ajouter_athlete_view import AjouterAthleteView  
from modifier_athlete import ModifierAthleteView
from supprimer_athlete import SupprimerAthleteView
class MainView:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.root.title("Interface Principale")

        # Bouton pour afficher toutes les délégations
        self.btn_delegation = tk.Button(root, text="Tous les délégations", command=self.open_country_view)
        self.btn_delegation.pack(pady=10)

        # Bouton pour rechercher un athlète
        self.btn_athlete = tk.Button(root, text="Rechercher un athlète", command=self.open_athlete_view)
        self.btn_athlete.pack(pady=10)

        # Bouton pour ajouter un athlète
        self.btn_add_athlete = tk.Button(root, text="Ajouter un athlète", command=self.open_add_athlete_view)
        self.btn_add_athlete.pack(pady=10)

        # Bouton pour Modifier un athlète
        self.btn_update_athlete = tk.Button(root, text="Modifier un athlète", command=self.open_update_athlete_view)
        self.btn_update_athlete.pack(pady=10)

        # Bouton pour Supprimer un athlète
        self.btn_delete_athlete = tk.Button(root, text="Supprimer un athlète", command=self.open_delete_athlete_view)
        self.btn_delete_athlete.pack(pady=10)

        # Bouton pour ajouter une participation
        self.btn_add_participation = tk.Button(root, text="Ajouter une participation", command=self.open_add_participation_view)
        self.btn_add_participation.pack(pady=10)

        # Bouton pour ajouter un match
        self.btn_add_match = tk.Button(root, text="Ajouter un match", command=self.open_add_match_view)
        self.btn_add_match.pack(pady=10)

        # Bouton pour ajouter une participation
        self.btn_research = tk.Button(root, text="Effectuer une recherche", command=self.open_research_view)
        self.btn_research.pack(pady=10)

        # Bouton pour modifier un match
        self.btn_match = tk.Button(root, text="Modifier un match", command=self.open_match)
        self.btn_match.pack(pady=10)

        # Bouton pour modifier un participant
        self.btn_participant = tk.Button(root, text="Modifier un participant", command=self.open_participant)
        self.btn_participant.pack(pady=10)

        # Bouton pour modifier une participation
        self.btn_participation = tk.Button(root, text="Modifier une participation", command=self.open_participation)
        self.btn_participation.pack(pady=10)

    def open_match (self):
        from match import MatchManager
        match_view = MatchManager(self.db_manager)
        match_view.run()

    def open_participant (self):
        from participant import ParticipantManager
        match_view = ParticipantManager(self.db_manager)
        match_view.run()

    def open_participation (self):
        from participation import ParticipationManager
        match_view = ParticipationManager(self.db_manager)
        match_view.run()
    
    def open_add_match_view (self):
        from ajout_match_view import AjoutMatchView
        match_view = AjoutMatchView(self.db_manager)
        match_view.run()
    
    def open_research_view (self):
        from recherche_participation_view import RechercheParticipationView
        search_view = RechercheParticipationView(self.db_manager)
        search_view.run()

    def open_add_participation_view(self):
        from ajout_participation_view import AjoutParticipationView
        add_participation_view = AjoutParticipationView(self.db_manager)
        add_participation_view.run()
    def open_delete_athlete_view(self):
        delete_view = SupprimerAthleteView(self.db_manager)
        delete_view.run()
    def open_update_athlete_view(self):
        update_view = ModifierAthleteView(self.db_manager)
        update_view.run()
    # Ouvre la vue CountryView
    def open_country_view(self):
        country_view = CountryView(self.db_manager)
        country_view.run()

    # Ouvre la vue AthleteView
    def open_athlete_view(self):
        athlete_view = AthleteView(self.db_manager)
        athlete_view.run()

    # Ouvre la vue AjouterAthleteView
    def open_add_athlete_view(self):
        add_athlete_view = AjouterAthleteView(self.db_manager)
        add_athlete_view.run()

"""def main(db_manager):
    root = tk.Tk()
    app = MainView(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    from db_manager import DBManager  

    # Initialiser la gestion de la base de données
    db_manager = DBManager()
    db_manager.connect_db()


    main(db_manager)

    # Fermer la connexion à la base de données
    db_manager.close()"""







 
