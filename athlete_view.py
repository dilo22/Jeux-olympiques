import tkinter as tk
from tkinter import messagebox

class AthleteView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Recherche Athlète")

        # Labels et champs d'entrée
        self.label_nom = tk.Label(self.root, text="Nom de l'athlète :")
        self.label_nom.pack(pady=5)
        self.entry_nom = tk.Entry(self.root)
        self.entry_nom.pack(pady=5)

        self.label_prenom = tk.Label(self.root, text="Prénom de l'athlète :")
        self.label_prenom.pack(pady=5)
        self.entry_prenom = tk.Entry(self.root)
        self.entry_prenom.pack(pady=5)

        # Bouton de recherche
        self.button_search = tk.Button(self.root, text="Rechercher", command=self.rechercher_athlete)
        self.button_search.pack(pady=10)

    def rechercher_athlete(self):
        nom = self.entry_nom.get().strip().upper()  # Nom en majuscules
        prenom = self.entry_prenom.get().strip().capitalize()  # Prénom avec première lettre majuscule

        athletes = self.db_manager.fetch_athletes(nom=nom, prenom=prenom)
        
        if athletes:
            result_window = tk.Toplevel(self.root)
            result_window.title("Résultats de la recherche")

            # Création d'une scrollbar
            scrollbar = tk.Scrollbar(result_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Création d'une listbox pour afficher les résultats
            listbox = tk.Listbox(result_window, yscrollcommand=scrollbar.set, width=100)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH)

            # Ajouter les résultats dans la listbox
            for athlete in athletes:
                info = (f"Id : {athlete[0]} | "
                        f"Nom : {athlete[1]} | "
                        f"Prénom : {athlete[2]} | "
                        f"Sexe : {athlete[3]} | "
                        f"Délégation : {athlete[4]} | "
                        f"Médailles d'or : {athlete[5]} | "
                        f"Médailles d'argent : {athlete[6]} | "
                        f"Médailles de bronze : {athlete[7]} | "
                        f"Discipline : {athlete[8] if athlete[8] else 'Non spécifiée'}")
                listbox.insert(tk.END, info)

            # Configurer la scrollbar pour la listbox
            scrollbar.config(command=listbox.yview)

        else:
            messagebox.showwarning("Aucun résultat", "Aucun athlète trouvé avec ce nom ou prénom.")






    def run(self):
        self.root.mainloop()
