"""Grafische Darstellungsschicht (Tkinter)."""

import tkinter as tk
from tkinter import messagebox
from datetime import date

from .dashboard_controller import DashboardController
from .dashboard_daten import DashboardDaten

FARBE_ZIEL_ERREICHT = "#2e7d32"
FARBE_ZIEL_NICHT_ERREICHT = "#c62828"
FARBE_RING_HINTERGRUND = "#e0e0e0"
FARBE_RING_FORTSCHRITT = "#1565c0"


class DashboardView:
    """Zeigt ECTS-Fortschritt, Notendurchschnitt und die belegten Module eines Studierenden an."""

    def __init__(self, controller: DashboardController):
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Studien-Dashboard")
        self._student = None

    def starte(self) -> None:
        """Baut das Hauptfenster auf und startet die Tkinter-Ereignisschleife."""
        studierende = self._controller.lade_studierende()
        if not studierende:
            messagebox.showerror("Studien-Dashboard", "Es wurden keine Studierendendaten gefunden.")
            self._root.destroy()
            return

        # Prototyp: Es wird der erste gespeicherte Studierende angezeigt.
        self._student = studierende[0]
        daten = self._controller.ermittle_dashboard_daten(self._student)

        heute = date.today().strftime("%d.%m.%Y")
        tk.Label(self._root, text=f"Hallo {self._student.name}!", font=("Arial", 16, "bold")).pack(pady=(15, 0))
        tk.Label(self._root, text=f"{daten.studiengang_name} - Stand {heute}").pack(pady=(0, 5))
        tk.Label(self._root, text="Mein Studienfortschritt", font=("Arial", 13, "bold")).pack(pady=(5, 15))

        kachelbereich = tk.Frame(self._root)
        kachelbereich.pack(padx=15, pady=5)

        self._baue_ects_kachel(kachelbereich, daten).grid(row=0, column=0, padx=10)
        self._baue_noten_kachel(kachelbereich, daten).grid(row=0, column=1, padx=10)

        tk.Button(
            self._root, text="ECTS-Fortschritt (Detailansicht)", command=self._zeige_modulliste
        ).pack(pady=15)

        self._root.mainloop()

    def _baue_ects_kachel(self, parent: tk.Widget, daten: DashboardDaten) -> tk.LabelFrame:
        """Baut die Kachel mit Fortschrittsring fuer den ECTS-Fortschritt."""
        kachel = tk.LabelFrame(parent, text="ECTS-Fortschritt", padx=10, pady=10)

        durchmesser = 120
        rand = 12
        canvas = tk.Canvas(kachel, width=durchmesser, height=durchmesser, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(
            rand, rand, durchmesser - rand, durchmesser - rand,
            outline=FARBE_RING_HINTERGRUND, width=10,
        )
        winkel = min(daten.erreichte_ects_prozent, 100) / 100 * 360
        if winkel > 0:
            canvas.create_arc(
                rand, rand, durchmesser - rand, durchmesser - rand,
                start=90, extent=-winkel, style="arc",
                outline=FARBE_RING_FORTSCHRITT, width=10,
            )
        canvas.create_text(
            durchmesser / 2, durchmesser / 2,
            text=f"{daten.erreichte_ects_prozent:.0f}%", font=("Arial", 14, "bold"),
        )

        tk.Label(kachel, text=f"{daten.erreichte_ects} von {daten.erforderliche_ects} ECTS").pack(pady=(8, 0))
        return kachel

    def _baue_noten_kachel(self, parent: tk.Widget, daten: DashboardDaten) -> tk.LabelFrame:
        """Baut die Kachel mit Notendurchschnitt und Zielerreichung."""
        kachel = tk.LabelFrame(
            parent, text=f"Notendurchschnitt - Ziel <= {daten.ziel_notendurchschnitt:.1f}",
            padx=15, pady=15,
        )

        farbe = FARBE_ZIEL_ERREICHT if daten.ziel_erreicht else FARBE_ZIEL_NICHT_ERREICHT
        tk.Label(kachel, text=f"{daten.durchschnittsnote:.1f}", font=("Arial", 22, "bold"), fg=farbe).pack(
            pady=(5, 10)
        )

        text = "Ziel aktuell erreicht" if daten.ziel_erreicht else "Ziel aktuell nicht erreicht"
        tk.Label(kachel, text=text, font=("Arial", 10, "bold"), fg=farbe).pack()
        return kachel

    def _zeige_modulliste(self) -> None:
        """Oeffnet ein separates Fenster mit der Detailansicht der belegten Module."""
        module = self._controller.ermittle_belegte_module(self._student)

        fenster = tk.Toplevel(self._root)
        fenster.title("ECTS-Fortschritt (Detailansicht)")

        spaltentitel = ("Semester", "Modul", "Note", "Status")
        for spalte, titel in enumerate(spaltentitel):
            tk.Label(
                fenster, text=titel, font=("Arial", 10, "bold"),
                borderwidth=1, relief="solid", padx=8, pady=4,
            ).grid(row=0, column=spalte, sticky="nsew")

        if not module:
            tk.Label(fenster, text="Es sind noch keine Module belegt.").grid(
                row=1, column=0, columnspan=4, padx=10, pady=10
            )
            return

        for zeile, (semester, name, note, status) in enumerate(module, start=1):
            werte = (
                str(semester) if semester is not None else "-",
                name,
                f"{note:.1f}" if note is not None else "-",
                status,
            )
            for spalte, wert in enumerate(werte):
                tk.Label(fenster, text=wert, borderwidth=1, relief="solid", padx=8, pady=4).grid(
                    row=zeile, column=spalte, sticky="nsew"
                )
