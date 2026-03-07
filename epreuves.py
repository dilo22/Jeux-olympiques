import tkinter as tk
from tkinter import ttk, messagebox


class Epreuves:
    """
    Vue "Tous les épreuves" SANS Treeview :
    - Filtres compacts en haut
    - Liste scrollable en cartes
    - Clic carte => participants
    """

    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager

        # Palette
        self.BG = "#F5F7FB"
        self.PANEL_BG = "#FFFFFF"
        self.CARD_BG = "#FFFFFF"
        self.CARD_BORDER = "#E5E7EB"
        self.TITLE_FG = "#111827"
        self.SUB_FG = "#6B7280"
        self.ACCENT = "#2563EB"
        self.ACCENT_HOVER = "#1D4ED8"

        self._setup_styles()
        self._build_ui()
        self._build_filters()
        self._build_list()

        self.filtrer_donnees()

    # ---------------- Styles ttk ----------------
    def _setup_styles(self):
        style = ttk.Style()

        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.root.configure(bg=self.BG)

        style.configure(
            "Modern.TCombobox",
            fieldbackground="#F9FAFB",
            background="#F9FAFB",
            foreground="#111827",
            bordercolor="#D1D5DB",
            darkcolor="#D1D5DB",
            lightcolor="#D1D5DB",
            arrowsize=14,
            padding=6,
            relief="flat"
        )

        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", "#F9FAFB")],
            selectbackground=[("readonly", "#F9FAFB")],
            selectforeground=[("readonly", "#111827")],
            bordercolor=[("focus", self.ACCENT), ("readonly", "#D1D5DB")],
            lightcolor=[("focus", self.ACCENT)],
            darkcolor=[("focus", self.ACCENT)]
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 8),
            foreground="white",
            background=self.ACCENT,
            borderwidth=0,
            focuscolor="none"
        )

        style.map(
            "Primary.TButton",
            background=[("active", self.ACCENT_HOVER), ("pressed", self.ACCENT_HOVER)],
            foreground=[("disabled", "#D1D5DB")]
        )

    # ---------------- UI ----------------
    def _build_ui(self):
        self.root.configure(bg=self.BG)

        self.title = tk.Label(
            self.root,
            text="Tous les épreuves",
            font=("Segoe UI", 18, "bold"),
            bg=self.BG,
            fg=self.TITLE_FG
        )
        self.title.pack(anchor="w", padx=20, pady=(10, 6))

        self.filter_card = tk.Frame(
            self.root,
            bg=self.PANEL_BG,
            highlightthickness=1,
            highlightbackground=self.CARD_BORDER,
            bd=0
        )
        self.filter_card.pack(fill="x", padx=20, pady=(0, 8))

        self.filter_frame = tk.Frame(self.filter_card, bg=self.PANEL_BG)
        self.filter_frame.pack(fill="x", padx=12, pady=10)

    # ---------------- Filters ----------------
    def _build_filters(self):
        dates = [f"2024-07-{day:02d}" for day in range(24, 32)] + \
                [f"2024-08-{day:02d}" for day in range(1, 12)]

        delegations = self.db_manager.fetch_delegations2()
        disciplines = self.db_manager.fetch_all_disciplines()
        genres = ["Tous genres", "Homme", "Femme", "Mixte"]
        phases = ["Toutes les phases", "Médaille"]

        # Reset colonnes
        for c in range(6):
            self.filter_frame.grid_columnconfigure(c, weight=0)
        self.filter_frame.grid_columnconfigure(5, weight=1)

        # -------- Ligne 1 --------
        tk.Label(
            self.filter_frame, text="Date",
            bg=self.PANEL_BG, fg=self.SUB_FG, font=("Segoe UI", 10)
        ).grid(row=0, column=0, padx=(0, 6), pady=4, sticky="w")

        self.date_combobox = ttk.Combobox(
            self.filter_frame,
            values=dates,
            state="readonly",
            width=12,
            style="Modern.TCombobox"
        )
        self.date_combobox.set(dates[0] if dates else "")
        self.date_combobox.grid(row=0, column=1, padx=(0, 14), pady=4, sticky="w")

        tk.Label(
            self.filter_frame, text="Équipe",
            bg=self.PANEL_BG, fg=self.SUB_FG, font=("Segoe UI", 10)
        ).grid(row=0, column=2, padx=(0, 6), pady=4, sticky="w")

        self.equipe_combobox = ttk.Combobox(
            self.filter_frame,
            values=["Toutes les équipes"] + delegations,
            state="readonly",
            width=18,
            style="Modern.TCombobox"
        )
        self.equipe_combobox.set("Toutes les équipes")
        self.equipe_combobox.grid(row=0, column=3, padx=(0, 14), pady=4, sticky="w")

        tk.Label(
            self.filter_frame, text="Sport",
            bg=self.PANEL_BG, fg=self.SUB_FG, font=("Segoe UI", 10)
        ).grid(row=0, column=4, padx=(0, 6), pady=4, sticky="w")

        self.sport_combobox = ttk.Combobox(
            self.filter_frame,
            values=["Tous les sports"] + disciplines,
            state="readonly",
            width=16,
            style="Modern.TCombobox"
        )
        self.sport_combobox.set("Tous les sports")
        self.sport_combobox.grid(row=0, column=5, padx=(0, 0), pady=4, sticky="w")

        # -------- Ligne 2 --------
        tk.Label(
            self.filter_frame, text="Genre",
            bg=self.PANEL_BG, fg=self.SUB_FG, font=("Segoe UI", 10)
        ).grid(row=1, column=0, padx=(0, 6), pady=4, sticky="w")

        self.genre_combobox = ttk.Combobox(
            self.filter_frame,
            values=genres,
            state="readonly",
            width=12,
            style="Modern.TCombobox"
        )
        self.genre_combobox.set("Tous genres")
        self.genre_combobox.grid(row=1, column=1, padx=(0, 14), pady=4, sticky="w")

        tk.Label(
            self.filter_frame, text="Phase",
            bg=self.PANEL_BG, fg=self.SUB_FG, font=("Segoe UI", 10)
        ).grid(row=1, column=2, padx=(0, 6), pady=4, sticky="w")

        self.phase_combobox = ttk.Combobox(
            self.filter_frame,
            values=phases,
            state="readonly",
            width=18,
            style="Modern.TCombobox"
        )
        self.phase_combobox.set("Toutes les phases")
        self.phase_combobox.grid(row=1, column=3, padx=(0, 14), pady=4, sticky="w")

        self.search_btn = ttk.Button(
            self.filter_frame,
            text="Rechercher",
            command=self.filtrer_donnees,
            style="Primary.TButton"
        )
        self.search_btn.grid(row=1, column=5, padx=(10, 0), pady=4, sticky="e")

        # Auto-refresh
        for cb in [
            self.date_combobox,
            self.equipe_combobox,
            self.sport_combobox,
            self.genre_combobox,
            self.phase_combobox
        ]:
            cb.bind("<<ComboboxSelected>>", lambda _e: self.filtrer_donnees())

    # ---------------- Scrollable list ----------------
    def _build_list(self):
        self.canvas = tk.Canvas(self.root, bg=self.BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=(0, 8))

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 8), padx=(0, 20))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.list_container = tk.Frame(self.canvas, bg=self.BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_container, anchor="nw")

        self.list_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _clear_list(self):
        for w in self.list_container.winfo_children():
            w.destroy()

    def _render_empty(self, text):
        tk.Label(
            self.list_container,
            text=text,
            bg=self.BG,
            fg=self.SUB_FG,
            font=("Segoe UI", 11)
        ).pack(anchor="center", pady=30)

    def _add_event_card(self, nom_evenement: str, phase: str):
        card = tk.Frame(
            self.list_container,
            bg=self.CARD_BG,
            highlightthickness=1,
            highlightbackground=self.CARD_BORDER,
            bd=0
        )
        card.pack(fill="x", pady=5)

        def on_click(_e=None):
            self._open_event(nom_evenement)

        card.configure(cursor="hand2")
        card.bind("<Button-1>", on_click)
        card.bind("<Enter>", lambda _e: card.configure(highlightbackground="#BFDBFE"))
        card.bind("<Leave>", lambda _e: card.configure(highlightbackground=self.CARD_BORDER))

        top = tk.Frame(card, bg=self.CARD_BG)
        top.pack(fill="x", padx=12, pady=(8, 2))

        name_lbl = tk.Label(
            top,
            text=nom_evenement,
            bg=self.CARD_BG,
            fg=self.TITLE_FG,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify="left",
            wraplength=900
        )
        name_lbl.pack(side="left", fill="x", expand=True)
        name_lbl.bind("<Button-1>", on_click)

        badge = tk.Label(
            top,
            text=phase if phase else "—",
            bg="#DBEAFE",
            fg="#1D4ED8",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3
        )
        badge.pack(side="right")
        badge.bind("<Button-1>", on_click)

        bottom = tk.Frame(card, bg=self.CARD_BG)
        bottom.pack(fill="x", padx=12, pady=(0, 8))

        hint = tk.Label(
            bottom,
            text="Clique pour voir les participants",
            bg=self.CARD_BG,
            fg=self.SUB_FG,
            font=("Segoe UI", 9)
        )
        hint.pack(anchor="w")
        hint.bind("<Button-1>", on_click)

    # ---------------- DB adapter ----------------
    def _to_db_value(self, s: str):
        if s is None:
            return None
        v = str(s).strip()
        if not v:
            return None

        low = v.lower()
        if low.startswith("tous ") or low.startswith("toutes ") or low in ("tous", "toutes"):
            return None

        if low in (
            "tous genres",
            "toutes genres",
            "toutes les phases",
            "tous les sports",
            "toutes les équipes"
        ):
            return None

        return v

    def _fetch_epreuves(self, date, equipe, sport, genre, phase):
        fn = self.db_manager.fetch_epreuves_filtrees

        for args in [
            (date, equipe, sport, genre, phase),
            (date, equipe, sport, genre),
            (date, equipe, sport),
            (date, equipe),
            (date,),
        ]:
            try:
                return fn(*args)
            except TypeError:
                continue

        raise TypeError("Signature inconnue pour fetch_epreuves_filtrees")

    # ---------------- Public API ----------------
    def afficher_donnees(self):
        self.filtrer_donnees()

    def filtrer_donnees(self):
        date = self._to_db_value(self.date_combobox.get())
        equipe = self._to_db_value(self.equipe_combobox.get())
        sport = self._to_db_value(self.sport_combobox.get())
        genre = self._to_db_value(self.genre_combobox.get())
        phase = self._to_db_value(self.phase_combobox.get())

        self._clear_list()

        try:
            epreuves = self._fetch_epreuves(date, equipe, sport, genre, phase)
        except Exception as e:
            self._render_empty("Erreur lors du chargement des épreuves.")
            messagebox.showerror("Erreur", f"Impossible de charger les épreuves.\n\n{e}")
            self._refresh_scroll()
            return

        if not epreuves:
            self._render_empty("Aucune épreuve trouvée avec ces filtres.")
            self._refresh_scroll()
            return

        for item in epreuves:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                nom_evenement, ph = item[0], item[1]
            elif isinstance(item, (list, tuple)) and len(item) == 1:
                nom_evenement, ph = item[0], ""
            else:
                nom_evenement, ph = str(item), ""

            self._add_event_card(str(nom_evenement), str(ph) if ph is not None else "")

        self._refresh_scroll()

    def _open_event(self, nom_evenement: str):
        try:
            id_match = self.db_manager.get_id_match_from_evenement(nom_evenement)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer l'ID du match.\n\n{e}")
            return

        if not id_match:
            messagebox.showerror("Erreur", "ID du match introuvable pour cet événement.")
            return

        self.open_participant_window(id_match)

    # ---------------- Participants ----------------
    def open_participant_window(self, id_match):
        win = tk.Toplevel(self.root)
        win.title(f"Participants - match {id_match}")
        win.configure(bg=self.BG)
        win.geometry("780x520")

        tk.Label(
            win,
            text=f"Participants (match {id_match})",
            font=("Segoe UI", 14, "bold"),
            bg=self.BG,
            fg=self.TITLE_FG
        ).pack(anchor="w", padx=16, pady=(14, 10))

        canvas = tk.Canvas(win, bg=self.BG, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 0), pady=(0, 16))

        sb = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 16))

        canvas.configure(yscrollcommand=sb.set)

        frame = tk.Frame(canvas, bg=self.BG)
        window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        try:
            participants = self.db_manager.fetch_participations_by_match(id_match)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les participants.\n\n{e}")
            win.destroy()
            return

        if not participants:
            tk.Label(frame, text="Aucun participant trouvé.", bg=self.BG, fg=self.SUB_FG).pack(pady=20)
            return

        header = tk.Frame(frame, bg=self.BG)
        header.pack(fill="x", pady=(0, 8))

        labels = ["Participant", "Phase", "Résultat", "Médaille"]
        for i, t in enumerate(labels):
            tk.Label(
                header,
                text=t,
                bg=self.BG,
                fg=self.TITLE_FG,
                font=("Segoe UI", 11, "bold")
            ).grid(row=0, column=i, sticky="w", padx=6)

        header.grid_columnconfigure(0, weight=52)
        header.grid_columnconfigure(1, weight=16)
        header.grid_columnconfigure(2, weight=16)
        header.grid_columnconfigure(3, weight=16)

        for p in participants:
            participant = p[0] if len(p) > 0 else ""
            ph = p[1] if len(p) > 1 else ""
            res = p[2] if len(p) > 2 else ""
            med = p[3] if len(p) > 3 else ""

            row = tk.Frame(
                frame,
                bg="#FFFFFF",
                highlightthickness=1,
                highlightbackground=self.CARD_BORDER
            )
            row.pack(fill="x", pady=5)

            row.grid_columnconfigure(0, weight=52)
            row.grid_columnconfigure(1, weight=16)
            row.grid_columnconfigure(2, weight=16)
            row.grid_columnconfigure(3, weight=16)

            tk.Label(row, text=str(participant),bg="#FFFFFF", fg=self.TITLE_FG,font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=0, sticky="w", padx=10, pady=8)

            tk.Label(
                row, text=str(ph),
                bg="#FFFFFF", fg=self.SUB_FG,
                font=("Segoe UI", 10)
            ).grid(row=0, column=1, sticky="w", padx=6)

            tk.Label(
                row, text=str(res),
                bg="#FFFFFF", fg=self.SUB_FG,
                font=("Segoe UI", 10)
            ).grid(row=0, column=2, sticky="w", padx=6)

            tk.Label(
                row, text=str(med),
                bg="#FFFFFF", fg=self.SUB_FG,
                font=("Segoe UI", 10)
            ).grid(row=0, column=3, sticky="w", padx=6)

    # ---------------- Scroll helpers ----------------
    def _refresh_scroll(self):
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)

    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")