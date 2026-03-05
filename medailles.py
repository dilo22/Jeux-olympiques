import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import math


class Medailles:

    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager

        self.flag_images = {}
        self.athletes_cache = []

        self.page_size = 100
        self.page_index = 0

        self._build_ui()
        self._load_flags()

    # ---------------- UI ----------------

    def _build_ui(self):

        # barre pagination
        self.topbar = tk.Frame(self.root, bg="white")
        self.topbar.pack(fill=tk.X, pady=(10, 0))

        self.btn_prev = tk.Button(
            self.topbar,
            text="◀ Précédent",
            command=self.prev_page,
            cursor="hand2"
        )
        self.btn_prev.pack(side=tk.LEFT, padx=10)

        self.page_label = tk.Label(
            self.topbar,
            text="Page 0/0",
            bg="white",
            font=("Helvetica", 11, "bold")
        )
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.btn_next = tk.Button(
            self.topbar,
            text="Suivant ▶",
            command=self.next_page,
            cursor="hand2"
        )
        self.btn_next.pack(side=tk.LEFT)

        # canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.container = tk.Frame(self.canvas, bg="white")

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.container,
            anchor="n"
        )

        self.container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    # ---------------- Flags ----------------

    def _normalize(self, text):
        return str(text).lower().replace("-", "").replace(" ", "").strip()

    def _load_flags(self):

        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        flags_dir = os.path.join(project_dir, "images", "drapeau")

        print("flags_dir =", flags_dir)

        if not os.path.exists(flags_dir):
            print("Dossier drapeaux introuvable")
            return

        count = 0

        for file in os.listdir(flags_dir):

            if not file.lower().endswith(".png"):
                continue

            path = os.path.join(flags_dir, file)
            filename = os.path.splitext(file)[0]

            key = self._normalize(filename)

            try:
                im = Image.open(path)
                im = im.resize((30, 20), Image.Resampling.LANCZOS)

                self.flag_images[key] = ImageTk.PhotoImage(im)

                count += 1

            except Exception as e:
                print("Erreur image:", path, e)

        print("Drapeaux chargés =", count)

    # ---------------- Data ----------------

    def afficher_donnees(self):

        self.athletes_cache = self.db_manager.fetch_athletes2()

        print("lignes athletes =", len(self.athletes_cache))

        self.page_index = 0

        self.render_page()

    def total_pages(self):

        if not self.athletes_cache:
            return 0

        return math.ceil(len(self.athletes_cache) / self.page_size)

    def prev_page(self):

        if self.page_index > 0:

            self.page_index -= 1

            self.render_page()

    def next_page(self):

        if self.page_index + 1 < self.total_pages():

            self.page_index += 1

            self.render_page()

    # ---------------- Render table ----------------

    def render_page(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        total_pages = self.total_pages()

        if total_pages == 0:

            self.page_label.config(text="Page 0/0")

            return

        self.page_label.config(text=f"Page {self.page_index + 1}/{total_pages}")

        headers = ["Drapeau", "Athlète", "O", "A", "B", "Total"]

        # headers
        for col, header in enumerate(headers):

            tk.Label(
                self.container,
                text=header,
                font=("Helvetica", 12, "bold"),
                bg="white",
                padx=15,
                pady=8
            ).grid(row=0, column=col, sticky="n")

        # centrer les colonnes
        for col in range(len(headers)):
            self.container.grid_columnconfigure(col, weight=1)

        start = self.page_index * self.page_size
        end = min(start + self.page_size, len(self.athletes_cache))

        page_rows = self.athletes_cache[start:end]

        for i, athlete in enumerate(page_rows, start=1):

            nom, prenom, sexe, nom_delegation, id_athlete, or_, argent, bronze, id_discipline = athlete

            nom_complet = f"{nom} {prenom}"

            total = or_ + argent + bronze

            key = self._normalize(nom_delegation)

            flag = self.flag_images.get(key)

            # drapeau
            if flag:

                lbl = tk.Label(self.container, image=flag, bg="white")
                lbl.image = flag
                lbl.grid(row=i, column=0, pady=4)

            else:

                tk.Label(self.container, text="", bg="white").grid(row=i, column=0)

            # athlète
            tk.Label(
                self.container,
                text=nom_complet,
                bg="white",
                font=("Helvetica", 10)
            ).grid(row=i, column=1, pady=4)

            # médailles
            tk.Label(self.container, text=str(or_), bg="white").grid(row=i, column=2)
            tk.Label(self.container, text=str(argent), bg="white").grid(row=i, column=3)
            tk.Label(self.container, text=str(bronze), bg="white").grid(row=i, column=4)
            tk.Label(self.container, text=str(total), bg="white").grid(row=i, column=5)

        self.container.update_idletasks()

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.yview_moveto(0)

    # ---------------- Canvas events ----------------

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):

        if event.delta:

            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")