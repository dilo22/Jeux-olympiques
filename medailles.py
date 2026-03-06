import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import math
import unicodedata


class Medailles:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager

        self.flag_images = {}
        self.athletes_cache = []

        self.page_size = 100
        self.page_index = 0

        # Largeurs fixes
        self.COL_FLAG_W = 80
        self.COL_ATHLETE_W = 260
        self.COL_NUM_W = 95

        self.BG = "white"
        self.FG = "#111827"

        self._build_ui()
        self._load_flags()

    # ---------------- UI ----------------
    def _build_ui(self):
        self.root.configure(bg=self.BG)

        # Barre pagination
        self.topbar = tk.Frame(self.root, bg=self.BG)
        self.topbar.pack(fill=tk.X, pady=(10, 5))

        self.nav_frame = tk.Frame(self.topbar, bg=self.BG)
        self.nav_frame.pack(anchor="center")

        self.btn_prev = tk.Button(
            self.nav_frame,
            text="◀ Précédent",
            command=self.prev_page,
            cursor="hand2"
        )
        self.btn_prev.grid(row=0, column=0, padx=10)

        self.page_label = tk.Label(
            self.nav_frame,
            text="Page 0/0",
            bg=self.BG,
            fg=self.FG,
            font=("Helvetica", 11, "bold")
        )
        self.page_label.grid(row=0, column=1, padx=10)

        self.btn_next = tk.Button(
            self.nav_frame,
            text="Suivant ▶",
            command=self.next_page,
            cursor="hand2"
        )
        self.btn_next.grid(row=0, column=2, padx=10)

        # Zone scrollable
        self.main_frame = tk.Frame(self.root, bg=self.BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(self.main_frame, bg=self.BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.scrollbar = tk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.container = tk.Frame(self.canvas, bg=self.BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        self.container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Conteneur centré
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=0)
        self.container.grid_columnconfigure(2, weight=1)

        self.content_frame = tk.Frame(self.container, bg=self.BG)
        self.content_frame.grid(row=0, column=1, pady=5)

        # Header puis liste, sur deux lignes différentes
        self.header_frame = tk.Frame(self.content_frame, bg=self.BG)
        self.header_frame.grid(row=0, column=0, sticky="w")

        self.list_frame = tk.Frame(self.content_frame, bg=self.BG)
        self.list_frame.grid(row=1, column=0, sticky="w")

        self._draw_header()

    # ---------------- Header ----------------
    def _draw_header(self):
        headers = ["Drapeau", "Athlète", "OR", "ARGENT", "BRONZE", "Total"]

        for col, text in enumerate(headers):
            width = self._col_width(col)

            cell = tk.Frame(self.header_frame, width=width, bg=self.BG)
            cell.grid(row=0, column=col)
            cell.grid_propagate(False)

            anchor = "w" if col in (0, 1) else "center"

            """tk.Label(
                cell,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg=self.BG,
                fg=self.FG,
                anchor=anchor
            ).pack(fill="both", expand=True, padx=6, pady=8)"""

    # ---------------- Outils cellules fixes ----------------
    def _col_width(self, col):
        if col == 0:
            return self.COL_FLAG_W
        if col == 1:
            return self.COL_ATHLETE_W
        return self.COL_NUM_W

    # ---------------- Flags ----------------
    def _normalize(self, text: str) -> str:
        s = str(text).strip().lower()
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

        for ch in [" ", "-", "_", "'", "’", ".", ","]:
            s = s.replace(ch, "")

        return s

    def _load_flags(self):
        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        flags_dir = os.path.join(project_dir, "images", "drapeau")

        if not os.path.exists(flags_dir):
            return

        for file in os.listdir(flags_dir):
            if not file.lower().endswith(".png"):
                continue

            path = os.path.join(flags_dir, file)
            filename = os.path.splitext(file)[0]
            key = self._normalize(filename)

            try:
                im = Image.open(path).resize((30, 20), Image.Resampling.LANCZOS)
                self.flag_images[key] = ImageTk.PhotoImage(im)
            except Exception as e:
                print("Erreur image:", path, e)

    def _get_flag(self, nom):
        return self.flag_images.get(self._normalize(nom))

    # ---------------- Data ----------------
    def afficher_donnees(self):
        self.athletes_cache = self.db_manager.fetch_athletes2()
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

    # ---------------- Render ----------------
    def render_page(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        total_pages = self.total_pages()

        if total_pages == 0:
            self.page_label.config(text="Page 0/0")
            self.btn_prev.config(state="disabled")
            self.btn_next.config(state="disabled")
            self.container.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        self.page_label.config(text=f"Page {self.page_index + 1}/{total_pages}")

        self.btn_prev.config(state="normal" if self.page_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.page_index + 1 < total_pages else "disabled")

        start = self.page_index * self.page_size
        end = min(start + self.page_size, len(self.athletes_cache))
        page_rows = self.athletes_cache[start:end]

        # Header dans la liste
        header = tk.Frame(self.list_frame, bg=self.BG)
        header.grid(row=0, column=0, pady=(0, 6), sticky="w")

        header.grid_columnconfigure(0, minsize=self.COL_FLAG_W)
        header.grid_columnconfigure(1, minsize=self.COL_ATHLETE_W)
        header.grid_columnconfigure(2, minsize=self.COL_NUM_W)
        header.grid_columnconfigure(3, minsize=self.COL_NUM_W)
        header.grid_columnconfigure(4, minsize=self.COL_NUM_W)
        header.grid_columnconfigure(5, minsize=self.COL_NUM_W)

        # Drapeau
        cell = tk.Frame(header, width=self.COL_FLAG_W, bg=self.BG)
        cell.grid(row=0, column=0)
        cell.grid_propagate(False)
        tk.Label(
            cell,
            text="Drapeau",
            font=("Helvetica", 12, "bold"),
            bg=self.BG,
            fg=self.FG
        ).pack(expand=True)

        # Athlète
        cell = tk.Frame(header, width=self.COL_ATHLETE_W, bg=self.BG)
        cell.grid(row=0, column=1)
        cell.grid_propagate(False)
        tk.Label(
            cell,
            text="Athlète",
            font=("Helvetica", 12, "bold"),
            bg=self.BG,
            fg=self.FG,
            anchor="w"
        ).pack(fill="both", expand=True, padx=(6, 0))

        # Colonnes numériques du header
        def fixed_header(col, text):
            cell = tk.Frame(header, width=self.COL_NUM_W, bg=self.BG)
            cell.grid(row=0, column=col)
            cell.grid_propagate(False)

            tk.Label(
                cell,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg=self.BG,
                fg=self.FG
            ).pack(expand=True)

        fixed_header(2, "O")
        fixed_header(3, "A")
        fixed_header(4, "B")
        fixed_header(5, "Total")

        for idx, athlete in enumerate(page_rows, start=1):
            nom, prenom, sexe, nom_delegation, id_athlete, or_, argent, bronze, id_discipline = athlete

            nom_complet = f"{nom} {prenom}"
            total = int(or_) + int(argent) + int(bronze)

            row = tk.Frame(self.list_frame, bg=self.BG)
            row.grid(row=idx, column=0, pady=4, sticky="w")

            row.grid_columnconfigure(0, minsize=self.COL_FLAG_W)
            row.grid_columnconfigure(1, minsize=self.COL_ATHLETE_W)
            row.grid_columnconfigure(2, minsize=self.COL_NUM_W)
            row.grid_columnconfigure(3, minsize=self.COL_NUM_W)
            row.grid_columnconfigure(4, minsize=self.COL_NUM_W)
            row.grid_columnconfigure(5, minsize=self.COL_NUM_W)

            # Drapeau
            flag = self._get_flag(nom_delegation)
            if flag:
                lbl = tk.Label(row, image=flag, bg=self.BG)
                lbl.image = flag
                lbl.grid(row=0, column=0, padx=(6, 6), pady=6)
            else:
                tk.Label(row, text="", bg=self.BG).grid(row=0, column=0)

            # Athlète
            athlete_cell = tk.Frame(row, width=self.COL_ATHLETE_W, bg=self.BG)
            athlete_cell.grid(row=0, column=1, sticky="w")
            athlete_cell.grid_propagate(False)

            tk.Label(
                athlete_cell,
                text=nom_complet,
                font=("Helvetica", 11),
                bg=self.BG,
                fg=self.FG,
                anchor="w"
            ).pack(fill="both", expand=True, padx=(6, 0))

            # Colonnes numériques fixes
            def fixed_cell(col, value, bold=False):
                cell = tk.Frame(row, width=self.COL_NUM_W, bg=self.BG)
                cell.grid(row=0, column=col)
                cell.grid_propagate(False)

                tk.Label(
                    cell,
                    text=str(value),
                    font=("Helvetica", 11, "bold") if bold else ("Helvetica", 11),
                    bg=self.BG,
                    fg=self.FG
                ).pack(expand=True)

            fixed_cell(2, or_)
            fixed_cell(3, argent)
            fixed_cell(4, bronze)
            fixed_cell(5, total, True)

        self.container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)

    # ---------------- Canvas events ----------------
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    # ---------------- Scroll ----------------
    def _bind_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.delta:
            step = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(step, "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")