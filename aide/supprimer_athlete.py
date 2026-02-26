import tkinter as tk
from tkinter import messagebox

class SupprimerAthleteView:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = tk.Toplevel()
        self.root.title("Supprimer un Athlète")

        # Label et champ pour entrer l'ID de l'athlète
        self.label_id = tk.Label(self.root, text="ID de l'athlète à supprimer :")
        self.label_id.pack(pady=5)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.pack(pady=5)

        # Bouton pour confirmer la suppression
        self.btn_delete = tk.Button(self.root, text="Supprimer", command=self.supprimer_athlete)
        self.btn_delete.pack(pady=10)

    # Méthode pour supprimer un athlète
    def supprimer_athlete(self):
        id_athlete = self.entry_id.get().strip()
        if id_athlete:
            try:
                self.db_manager.delete_athlete(id_athlete)
                messagebox.showinfo("Succès", f"Athlète avec l'ID {id_athlete} supprimé avec succès.")
                self.root.destroy()  # Ferme la fenêtre après suppression
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer l'athlète : {e}")
        else:
            messagebox.showwarning("Champs manquants", "Veuillez entrer l'ID de l'athlète à supprimer.")

    def run(self):
        self.root.mainloop()
