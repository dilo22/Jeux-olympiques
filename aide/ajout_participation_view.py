import tkinter as tk
from tkinter import messagebox

class AjoutParticipationView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Ajouter une participation")

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

        # Boutons radio pour le type de participant
        self.label_type = tk.Label(self.root, text="Type de participant :")
        self.label_type.pack(pady=5)
        self.participant_type_var = tk.StringVar(value="athlete")
        tk.Radiobutton(self.root, text="Athlète", variable=self.participant_type_var, value="athlete").pack(pady=2)
        tk.Radiobutton(self.root, text="Délégation", variable=self.participant_type_var, value="delegation").pack(pady=2)

        self.label_id_athlete = tk.Label(self.root, text="ID de l'athlète (ou délégation) :")
        self.label_id_athlete.pack(pady=5)
        self.entry_id_athlete = tk.Entry(self.root)
        self.entry_id_athlete.pack(pady=5)

        # Boutons radio pour la médaille
        self.label_medaille = tk.Label(self.root, text="Médaille :")
        self.label_medaille.pack(pady=5)
        self.medaille_var = tk.StringVar(value="aucun")
        tk.Radiobutton(self.root, text="Or", variable=self.medaille_var, value="or").pack(pady=2)
        tk.Radiobutton(self.root, text="Argent", variable=self.medaille_var, value="argent").pack(pady=2)
        tk.Radiobutton(self.root, text="Bronze", variable=self.medaille_var, value="bronze").pack(pady=2)
        tk.Radiobutton(self.root, text="Aucun", variable=self.medaille_var, value="aucun").pack(pady=2)

        # Boutons radio pour le type de résultat
        self.label_type_resultat = tk.Label(self.root, text="Type de résultat :")
        self.label_type_resultat.pack(pady=5)
        self.type_resultat_var = tk.StringVar(value="MAX")
        tk.Radiobutton(self.root, text="MIN", variable=self.type_resultat_var, value="MIN").pack(pady=2)
        tk.Radiobutton(self.root, text="MAX", variable=self.type_resultat_var, value="MAX").pack(pady=2)

        self.label_resultat = tk.Label(self.root, text="Résultat :")
        self.label_resultat.pack(pady=5)
        self.entry_resultat = tk.Entry(self.root)
        self.entry_resultat.pack(pady=5)

        # Bouton pour ajouter la participation
        self.btn_add_participation = tk.Button(self.root, text="Ajouter la participation", command=self.ajouter_participation)
        self.btn_add_participation.pack(pady=10)

    def ajouter_participation(self):
        # Récupérer les données des champs
        id_match = self.entry_id_match.get().strip()
        id_evenement = self.entry_id_evenement.get().strip()
        phase = self.entry_phase.get().strip()
        date = self.entry_date.get().strip()
        participant_type = self.participant_type_var.get().lower()  # Récupère la valeur du bouton radio
        id_athlete = self.entry_id_athlete.get().strip()
        resultat = self.entry_resultat.get().strip()
        medaille = self.medaille_var.get().lower()  # Récupère la valeur du bouton radio
        type_resultat = self.type_resultat_var.get().upper()  # Récupère la valeur du bouton radio

        if id_match and id_evenement and phase and date and participant_type and id_athlete and resultat and medaille and type_resultat:
            try:
                # Vérifier si le match existe déjà
                if not self.db_manager.match_existe(id_match):
                    # Insérer dans la table 'match'
                    self.db_manager.insert_match(id_match, id_evenement, phase, date)
                
                # Insérer dans la table 'participant'
                id_participant = self.db_manager.insert_participant(participant_type, id_athlete)
                
                # Insérer dans la table 'participation'
                self.db_manager.insert_participation(id_match, id_participant, resultat, medaille, type_resultat)

                messagebox.showinfo("Succès", "Participation ajoutée avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter la participation : {e}")
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")

    def run(self):
        self.root.mainloop()
