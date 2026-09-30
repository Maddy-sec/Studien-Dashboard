
import json
import os
from typing import List

from .dashboard_repository import DashboardRepository
from .models import Student, Studiengang, Modul, Pruefungsleistung


class JsonDashboardRepository(DashboardRepository):
    """Laedt und speichert Studierendendaten dateibasiert im JSON-Format."""

    def __init__(self, dateipfad: str):
        self._dateipfad = dateipfad

    def lade_studierende(self) -> List[Student]:
        if not os.path.exists(self._dateipfad):
            return []

        with open(self._dateipfad, "r", encoding="utf-8") as datei:
            rohdaten = json.load(datei)

        studierende: List[Student] = []
        for eintrag in rohdaten:
            studiengang = self._studiengang_aus_dict(eintrag["studiengang"])
            student = Student(
                name=eintrag["name"],
                ziel_notendurchschnitt=eintrag["ziel_notendurchschnitt"],
                studiengang=studiengang,
            )
            for belegung_eintrag in eintrag.get("belegungen", []):
                modul = studiengang.modul_nach_name(belegung_eintrag["modul"])
                if modul is None:
                    # Modul ist im Studiengang nicht (mehr) vorhanden - Eintrag ueberspringen.
                    continue
                belegung = student.modul_belegen(modul)
                for pl_eintrag in belegung_eintrag.get("pruefungsleistungen", []):
                    belegung.pruefungsleistung_hinzufuegen(
                        Pruefungsleistung(
                            semester=pl_eintrag["semester"],
                            note=pl_eintrag.get("note"),
                        )
                    )
            studierende.append(student)
        return studierende

    def speichere_studierende(self, studierende: List[Student]) -> None:
        rohdaten = [self._student_zu_dict(student) for student in studierende]
        os.makedirs(os.path.dirname(self._dateipfad) or ".", exist_ok=True)
        with open(self._dateipfad, "w", encoding="utf-8") as datei:
            json.dump(rohdaten, datei, ensure_ascii=False, indent=2)

    # Hilfsmethoden zur Umwandlung zwischen Objektgraph und JSON-Struktur # 

    @staticmethod
    def _studiengang_aus_dict(daten: dict) -> Studiengang:
        studiengang = Studiengang(name=daten["name"], gesamt_ects=daten["gesamt_ects"])
        for modul_eintrag in daten.get("module", []):
            studiengang.modul_hinzufuegen(
                Modul(name=modul_eintrag["name"], ects=modul_eintrag["ects"])
            )
        return studiengang

    @staticmethod
    def _student_zu_dict(student: Student) -> dict:
        studiengang = student.studiengang
        return {
            "name": student.name,
            "ziel_notendurchschnitt": student.ziel_notendurchschnitt,
            "studiengang": {
                "name": studiengang.name,
                "gesamt_ects": studiengang.gesamt_ects,
                "module": [
                    {"name": modul.name, "ects": modul.ects} for modul in studiengang.module
                ],
            },
            "belegungen": [
                {
                    "modul": modul.name,
                    "pruefungsleistungen": [
                        {"semester": pl.semester, "note": pl.note}
                        for pl in belegung.pruefungsleistungen
                    ],
                }
                for modul, belegung in student.belegungen.items()
            ],
        }
