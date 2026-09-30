"""Service-Klasse fuer alle Berechnungen."""

from .models import Student, Pruefungsstatus


class StudienfortschrittService:
    """Berechnet Notendurchschnitt und ECTS-Fortschritt eines Studierenden."""

    def durchschnittsnote(self, student: Student) -> float:
        """
        Unwarianter Notendurchschnitt ueber alle bestandenen Pruefungsleistungen.

        Alle Module gehen unabhaengig von ihrer ECTS-Zahl gleich gewichtet ein.
        """
        bestandene_noten = [
            pruefungsleistung.note
            for belegung in student.belegungen.values()
            for pruefungsleistung in belegung.pruefungsleistungen
            if pruefungsleistung.status == Pruefungsstatus.BESTANDEN
        ]
        if not bestandene_noten:
            return 0.0
        return sum(bestandene_noten) / len(bestandene_noten)

    def erreichte_ects(self, student: Student) -> int:
        """Summe der ECTS aller Module, die mindestens eine bestandene Pruefungsleistung haben."""
        summe = 0
        for modul, belegung in student.belegungen.items():
            if any(
                pruefungsleistung.status == Pruefungsstatus.BESTANDEN
                for pruefungsleistung in belegung.pruefungsleistungen
            ):
                summe += modul.ects
        return summe

    def ects_prozent(self, student: Student) -> float:
        """Anteil der bereits erreichten ECTS an den insgesamt benoetigten ECTS in Prozent."""
        gesamt_ects = student.studiengang.gesamt_ects
        if gesamt_ects == 0:
            return 0.0
        return self.erreichte_ects(student) / gesamt_ects * 100
