import os
import tkinter as tk
from PIL import Image, ImageTk

class TableauMedaille:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.flag_images = []  

     
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_table()

        #self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def create_table(self):
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_v = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar_v.set)

        self.container = tk.Frame(self.canvas)
        self.container.bind("<Configure>", self.onFrameConfigure)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="n")

        self.container.bind("<Configure>", self.onFrameConfigure)

        self.canvas.bind("<Configure>", self.onCanvasConfigure)

    def afficher_donnees(self):
        delegations = self.db_manager.fetch_delegations_sorted_by_medals()

        headers = ["", "Délégation", "O", "A", "B", "Total"]
        for col, header in enumerate(headers):
            label = tk.Label(self.container, text=header, font=("Helvetica", 12, "bold"), padx=10, pady=5)
            label.grid(row=0, column=col, padx=10, pady=5)

        for i, delegation in enumerate(delegations, start=1):
            id_delegation, nom_delegation, continent, nb_medaille_or, nb_medaille_argent, nb_medaille_bronze = delegation

            flag_path = f"C:/Users/hibah/Desktop/L3/BD/TP2/images/drapeau/{nom_delegation}.png"

            if os.path.exists(flag_path):
                flag_image = Image.open(flag_path)
                flag_image = flag_image.resize((30, 20), Image.Resampling.LANCZOS)
                flag_photo = ImageTk.PhotoImage(flag_image)

                self.flag_images.append(flag_photo)

                flag_label = tk.Label(self.container, image=flag_photo)
                flag_label.grid(row=i, column=0, padx=10, pady=5)
                flag_label.image = flag_photo
            else:
                flag_label = tk.Label(self.container, text=" ", padx=10, pady=5)
                flag_label.grid(row=i, column=0, padx=10, pady=5)

            tk.Label(self.container, text=nom_delegation, padx=10, pady=5).grid(row=i, column=1)
            tk.Label(self.container, text=str(nb_medaille_or), padx=10, pady=5).grid(row=i, column=2)
            tk.Label(self.container, text=str(nb_medaille_argent), padx=10, pady=5).grid(row=i, column=3)
            tk.Label(self.container, text=str(nb_medaille_bronze), padx=10, pady=5).grid(row=i, column=4)
            total_medals = nb_medaille_or + nb_medaille_argent + nb_medaille_bronze
            tk.Label(self.container, text=str(total_medals), padx=10, pady=5).grid(row=i, column=5)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        container_width = self.container.winfo_reqwidth()
        x_offset = max((canvas_width - container_width) // 2, 0)
        self.canvas.coords(self.canvas_window, x_offset, 0)

    def on_mouse_wheel(self, event):
        # Sécurité : vérifier que le canvas existe encore
        if not hasattr(self, "canvas") or not self.canvas.winfo_exists():
            return

        # Windows / Mac
        if event.delta:
            if event.delta < 0:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(-1, "units")

        # Linux
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
