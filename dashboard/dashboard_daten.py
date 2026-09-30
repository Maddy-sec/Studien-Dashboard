
from dataclasses import dataclass


@dataclass
class DashboardDaten:
    """Buendelt die fuer die Anzeige aufbereiteten Kennzahlen eines Studierenden."""
    erreichte_ects: int
    erforderliche_ects: int
    erreichte_ects_prozent: float
    durchschnittsnote: float
    ziel_notendurchschnitt: float
    ziel_erreicht: bool
    studiengang_name: str
