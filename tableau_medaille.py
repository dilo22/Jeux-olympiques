import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import unicodedata


class TableauMedaille:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager

        self.flag_images = {}

        self.COL_FLAG_W = 44
        self.COL_NUM_W = 90

        self.BG = "white"
        self.CARD_BG = "#F6F7FB"
        self.CARD_BORDER = "#E3E6EF"
        self.HEADER_FG = "#111827"

        self._build_ui()
        self._load_flags()

    # ---------------- UI ----------------
    def _build_ui(self):

        self.canvas = tk.Canvas(self.root, bg=self.BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.container = tk.Frame(self.canvas, bg=self.BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        self.container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        title = tk.Label(
            self.container,
            text="Tableau des Médailles",
            font=("Helvetica", 16, "bold"),
            bg=self.BG,
            fg=self.HEADER_FG
        )
        title.grid(row=0, column=0, columnspan=6, pady=(5, 12), sticky="w", padx=20)

        # Header
        self.header_bar = tk.Frame(self.container, bg=self.BG)
        self.header_bar.grid(row=1, column=0, columnspan=6, sticky="ew", padx=20)

        self.header_bar.grid_columnconfigure(0, minsize=self.COL_FLAG_W)
        self.header_bar.grid_columnconfigure(1, weight=1)
        self.header_bar.grid_columnconfigure(2, minsize=self.COL_NUM_W)
        self.header_bar.grid_columnconfigure(3, minsize=self.COL_NUM_W)
        self.header_bar.grid_columnconfigure(4, minsize=self.COL_NUM_W)
        self.header_bar.grid_columnconfigure(5, minsize=self.COL_NUM_W)

        headers = ["", "Pays", "Or", "Argent", "Bronze", "Total"]

        for col, text in enumerate(headers):
            tk.Label(
                self.header_bar,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg=self.BG,
                fg=self.HEADER_FG,
                anchor="w" if col == 1 else "center"
            ).grid(row=0, column=col, padx=6, pady=8, sticky="ew")

        self.list_frame = tk.Frame(self.container, bg=self.BG)
        self.list_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=20)

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
            print("Dossier drapeaux introuvable :", flags_dir)
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

    # ---------------- Render ----------------
    def afficher_donnees(self):

        for w in self.list_frame.winfo_children():
            w.destroy()

        delegations = self.db_manager.fetch_delegations_sorted_by_medals()

        for idx, d in enumerate(delegations):

            _id, nom, _continent, or_, argent, bronze = d
            total = int(or_) + int(argent) + int(bronze)

            card = tk.Frame(
                self.list_frame,
                bg=self.CARD_BG,
                highlightthickness=1,
                highlightbackground=self.CARD_BORDER
            )

            card.grid(row=idx, column=0, columnspan=6, sticky="ew", pady=6)

            card.grid_columnconfigure(0, minsize=self.COL_FLAG_W)
            card.grid_columnconfigure(1, weight=1)
            card.grid_columnconfigure(2, minsize=self.COL_NUM_W)
            card.grid_columnconfigure(3, minsize=self.COL_NUM_W)
            card.grid_columnconfigure(4, minsize=self.COL_NUM_W)
            card.grid_columnconfigure(5, minsize=self.COL_NUM_W)

            # Flag
            flag = self._get_flag(nom)

            if flag:
                lbl_flag = tk.Label(card, image=flag, bg=self.CARD_BG)
                lbl_flag.image = flag
                lbl_flag.grid(row=0, column=0, padx=(12, 6), pady=10, sticky="w")
            else:
                tk.Label(card, bg=self.CARD_BG).grid(row=0, column=0)

            # Pays
            tk.Label(
                card,
                text=nom,
                font=("Helvetica", 11, "bold"),
                bg=self.CARD_BG,
                fg="#111827"
            ).grid(row=0, column=1, padx=6, pady=10, sticky="w")

            # Fonction cellule fixe
            def fixed_cell(col, value, bold=False):

                cell = tk.Frame(card, width=self.COL_NUM_W, bg=self.CARD_BG)
                cell.grid(row=0, column=col)
                cell.grid_propagate(False)

                tk.Label(
                    cell,
                    text=value,
                    font=("Helvetica", 11, "bold") if bold else ("Helvetica", 11),
                    bg=self.CARD_BG,
                    fg="#111827"
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