
from typing import List, Optional, Tuple

from .models import Student
from .dashboard_repository import DashboardRepository
from .studienfortschritt_service import StudienfortschrittService
from .dashboard_daten import DashboardDaten


class DashboardController:
   
    def __init__(self, repository: DashboardRepository, service: StudienfortschrittService):
        self._repository = repository
        self._service = service

    def lade_studierende(self) -> List[Student]:
        """Ruft die vorhandenen Studierenden ueber das Repository ab."""
        return self._repository.lade_studierende()

    def ermittle_dashboard_daten(self, student: Student) -> DashboardDaten:
        """Laesst den Service die relevanten Kennzahlen berechnen und buendelt sie."""
        durchschnittsnote = self._service.durchschnittsnote(student)
        erreichte_ects = self._service.erreichte_ects(student)
        # Ohne bestandene Pruefungsleistung liegt noch kein aussagekraeftiger
        # Notendurchschnitt vor - in diesem Fall gilt das Ziel nicht als erreicht.
        ziel_erreicht = erreichte_ects > 0 and durchschnittsnote <= student.ziel_notendurchschnitt
        return DashboardDaten(
            erreichte_ects=erreichte_ects,
            erforderliche_ects=student.studiengang.gesamt_ects,
            erreichte_ects_prozent=self._service.ects_prozent(student),
            durchschnittsnote=durchschnittsnote,
            ziel_notendurchschnitt=student.ziel_notendurchschnitt,
            ziel_erreicht=ziel_erreicht,
            studiengang_name=student.studiengang.name,
        )

    def ermittle_belegte_module(
        self, student: Student
    ) -> List[Tuple[Optional[int], str, Optional[float], str]]:
        """Zeigt die Detailansicht der belegten Module als einfache Anzeige-Tupel"""
        ergebnis = []
        for modul, belegung in student.belegungen.items():
            neueste_leistung = belegung.pruefungsleistungen[-1] if belegung.pruefungsleistungen else None
            semester = neueste_leistung.semester if neueste_leistung else None
            note = neueste_leistung.note if neueste_leistung else None
            status_text = neueste_leistung.status.value if neueste_leistung else "keine Pruefung erfasst"
            ergebnis.append((semester, modul.name, note, status_text))
        return ergebnis
