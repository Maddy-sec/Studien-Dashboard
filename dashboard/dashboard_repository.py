"""Legt die Speicherschnittstelle fest, ohne sie vorzugeben."""

from abc import ABC, abstractmethod
from typing import List

from .models import Student


class DashboardRepository(ABC):
  
    @abstractmethod
    def lade_studierende(self) -> List[Student]:
        """Laedt alle gespeicherten Studierenden inklusive ihres vollstaendigen Objektgraphen."""
        raise NotImplementedError

    @abstractmethod
    def speichere_studierende(self, studierende: List[Student]) -> None:
        """Speichert alle uebergebenen Studierenden inklusive ihres vollstaendigen Objektgraphen."""
        raise NotImplementedError
