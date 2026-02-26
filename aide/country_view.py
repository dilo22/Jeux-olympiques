import tkinter as tk
from tkinter import ttk

class CountryView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title("Les 204 délégations participantes aux Jeux de 2024")

        # Créer le titre en haut
        title_label = tk.Label(self.root, text="Les 204 délégations participantes aux Jeux de 2024", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Créer le tableau (Treeview)
        self.create_table()

        # Charger les pays depuis la base de données
        self.load_countries()

    def create_table(self):
        # Créer un frame pour le tableau
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Définir le tableau avec des colonnes pour chaque continent
        self.tree = ttk.Treeview(frame, columns=("Afrique", "Amériques", "Asie", "Europe", "Océanie"), show="headings")
        self.tree.heading("Afrique", text="Afrique")
        self.tree.heading("Amériques", text="Amériques")
        self.tree.heading("Asie", text="Asie")
        self.tree.heading("Europe", text="Europe")
        self.tree.heading("Océanie", text="Océanie")

        # Appliquer une couleur à l'en-tête de colonne
        style = ttk.Style()
        style.configure("Treeview.Heading", background="lightblue", font=("Arial", 12, "bold"))

        # Configurer la largeur des colonnes
        self.tree.column("Afrique", width=150)
        self.tree.column("Amériques", width=150)
        self.tree.column("Asie", width=150)
        self.tree.column("Europe", width=150)
        self.tree.column("Océanie", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_countries(self):
        continents = {
            "Afrique": [],
            "Ameriques": [],
            "Asie": [],
            "Europe": [],
            "Oceanie": []
        }

        # Récupérer les pays depuis la base de données
        countries = self.db_manager.fetch_countries_by_continent()
        
        # Organiser les pays par continent
        for country, continent in countries:
            if continent in continents:
                continents[continent].append(country)
            #else:
                #print(f"Continent non trouvé : {continent}")

        # Calculer le nombre maximum de lignes à afficher
        max_length = max([len(continents[continent]) for continent in continents])

        # Ajouter les pays dans le tableau
        for i in range(max_length):
            row = []
            for continent in ["Afrique", "Ameriques", "Asie", "Europe", "Oceanie"]:
                if i < len(continents[continent]):
                    row.append(continents[continent][i])
                else:
                    row.append("")  # Ajouter une cellule vide si aucun pays
            self.tree.insert("", "end", values=row)

        # Afficher le total des pays par continent en bas du tableau
        totals_row = []
        for continent in ["Afrique", "Ameriques", "Asie", "Europe", "Oceanie"]:
            total_pays = len(continents[continent])
            totals_row.append(f"Total: {total_pays}")
        
        self.tree.insert("", "end", values=totals_row, tags=('total_row',))

        # Appliquer une couleur différente pour la ligne des totaux
        self.tree.tag_configure('total_row', background="lightgrey", font=("Arial", 10, "bold"))

    def run(self):
        self.root.mainloop()
