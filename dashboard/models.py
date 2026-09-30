
from enum import Enum
from typing import Optional, List, Dict


class Pruefungsstatus(Enum):
    """Enumeration der drei zulaessigen Zustaende einer Pruefungsleistung."""
    BESTANDEN = "bestanden"
    NICHT_BESTANDEN = "nicht bestanden"
    NOCH_NICHT_ABGELEGT = "noch nicht abgelegt"


class Pruefungsleistung:
    """Ein einzelner Pruefungsversuch innerhalb einer Belegung."""

    def __init__(self, semester: int, note: Optional[float] = None):
        self.semester = semester
        self.note = note

    @property
    def status(self) -> Pruefungsstatus:
        if self.note is None:
            return Pruefungsstatus.NOCH_NICHT_ABGELEGT
        if self.note <= 4.0:
            return Pruefungsstatus.BESTANDEN
        return Pruefungsstatus.NICHT_BESTANDEN

    def __repr__(self) -> str:
        return f"Pruefungsleistung(semester={self.semester}, note={self.note}, status={self.status.value})"


class Belegung:
    """Assoziationsklasse zwischen Student und Modul."""

    MAX_PRUEFUNGSVERSUCHE = 3

    def __init__(self):
        self._pruefungsleistungen: List[Pruefungsleistung] = []

    def pruefungsleistung_hinzufuegen(self, pruefungsleistung: Pruefungsleistung) -> None:
        if len(self._pruefungsleistungen) >= self.MAX_PRUEFUNGSVERSUCHE:
            raise ValueError(
                f"Maximal {self.MAX_PRUEFUNGSVERSUCHE} Pruefungsleistungen je Belegung erlaubt."
            )
        self._pruefungsleistungen.append(pruefungsleistung)

    @property
    def pruefungsleistungen(self) -> List[Pruefungsleistung]:
        return list(self._pruefungsleistungen)


class Modul:
    """Ein einzelnes Modul eines Studiengangs."""

    def __init__(self, name: str, ects: int):
        self.name = name
        self.ects = ects

    def __repr__(self) -> str:
        return f"Modul({self.name!r}, ects={self.ects})"

    def __hash__(self):
        # Module werden als dict-Schluessel in Student._belegungen verwendet.
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Modul) and self.name == other.name


class Studiengang:
    
    def __init__(self, name: str, gesamt_ects: int):
        self.name = name
        self.gesamt_ects = gesamt_ects
        self._module: List[Modul] = []

    def modul_hinzufuegen(self, modul: Modul) -> None:
        self._module.append(modul)

    @property
    def module(self) -> List[Modul]:
        return list(self._module)

    def modul_nach_name(self, name: str) -> Optional[Modul]:
        for modul in self._module:
            if modul.name == name:
                return modul
        return None


class Student:
    """Ein Studierender mit Zielnotendurchschnitt und einem Studiengang."""

    def __init__(self, name: str, ziel_notendurchschnitt: float, studiengang: Studiengang):
        self._name = name
        self._ziel_notendurchschnitt = ziel_notendurchschnitt
        self.studiengang = studiengang
        self._belegungen: Dict[Modul, Belegung] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def ziel_notendurchschnitt(self) -> float:
        return self._ziel_notendurchschnitt

    def modul_belegen(self, modul: Modul) -> Belegung:
        """Legt bei Bedarf eine neue Belegung fuer das Modul an und gibt sie zurueck."""
        if modul not in self._belegungen:
            self._belegungen[modul] = Belegung()
        return self._belegungen[modul]

    @property
    def belegungen(self) -> Dict[Modul, Belegung]:
        return dict(self._belegungen)

    def __repr__(self) -> str:
        return f"Student({self._name!r})"
