"""Start der Anwendung ."""

import os

from .json_dashboard_repository import JsonDashboardRepository
from .studienfortschritt_service import StudienfortschrittService
from .dashboard_controller import DashboardController
from .dashboard_view import DashboardView

DATENPFAD = os.path.join(os.path.dirname(__file__), "..", "data", "studierende.json")


class DashboardApp:
    """Erzeugt alle benoetigten Objekte und verdrahtet sie miteinander."""

    def start(self) -> None:
        repository = JsonDashboardRepository(DATENPFAD)
        service = StudienfortschrittService()
        controller = DashboardController(repository, service)
        view = DashboardView(controller)
        view.starte()


if __name__ == "__main__":
    DashboardApp().start()
