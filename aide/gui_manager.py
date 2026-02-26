import tkinter as tk
from tkinter import ttk
from db_manager import DBManager

class GUIManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Filtrer les athlètes des JO Paris 2024")
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.setup_ui()
    
    def setup_ui(self):
        # Label pour délégation
        ttk.Label(self.frame, text="Délégation :").grid(row=0, column=0, sticky=tk.W)
        
        # Combobox pour choisir la délégation
        self.delegation_var = tk.StringVar()
        self.delegation_cb = ttk.Combobox(self.frame, textvariable=self.delegation_var)
        self.delegation_cb.grid(row=0, column=1)
        
        # Charger les délégations
        self.load_delegations()

        # Label pour sexe
        ttk.Label(self.frame, text="Sexe :").grid(row=1, column=0, sticky=tk.W)

        # Combobox pour le sexe
        self.sexe_var = tk.StringVar()
        self.sexe_cb = ttk.Combobox(self.frame, textvariable=self.sexe_var, values=["H", "F"])
        self.sexe_cb.grid(row=1, column=1)

        # Label pour la medaille
        ttk.Label(self.frame, text="Médaille :").grid(row=2, column=0, sticky=tk.W)

        # Case à cocher pour filtrer par médaille
        self.medal_var = tk.StringVar()  # Variable pour stocker le type de médaille
        self.medal_cb = ttk.Combobox(self.frame, textvariable=self.medal_var, values=["","OR", "ARGENT", "BRONZE"])
        self.medal_cb.grid(row=2, column=1)

        # Bouton pour filtrer
        filter_button = ttk.Button(self.frame, text="Filtrer", command=self.filter_athletes)
        filter_button.grid(row=4, column=1, sticky=tk.W)

        # Listbox pour afficher les athlètes
        self.athletes_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.athletes_listbox.grid(row=5, column=0, columnspan=2)

        # Bouton pour quitter
        quit_button = ttk.Button(self.frame, text="Quitter", command=self.root.destroy)
        quit_button.grid(row=6, column=1, sticky=tk.W)


    def load_delegations(self):
        delegations = self.db_manager.fetch_delegations()
        # Stocker un mapping entre le nom de la délégation et son ID
        self.delegation_map = {d[1]: d[0] for d in delegations}  # d[1] = nom, d[0] = ID
        self.delegation_cb['values'] = list(self.delegation_map.keys())  # Affiche les noms des délégations

    def filter_athletes(self):
        # Obtenir les valeurs des filtres
        delegation_name = self.delegation_var.get()
        delegation_id = self.delegation_map.get(delegation_name, None)  # Récupérer l'ID de la délégation

        sexe = self.sexe_var.get()
        medal = self.medal_var.get() if self.medal_var.get() != "" else None   # Récupérer le type de médaille

        # Récupérer les athlètes filtrés
        athletes = self.db_manager.fetch_athletes(delegation=delegation_id, sexe=sexe if sexe else None,  medal=medal if medal else None)
        
        # Mettre à jour la liste des athlètes
        self.athletes_listbox.delete(0, tk.END)
        for athlete in athletes:
            self.athletes_listbox.insert(tk.END, f"{athlete[0]} {athlete[1]} ")


    
   
    def run(self):
        self.root.mainloop()
