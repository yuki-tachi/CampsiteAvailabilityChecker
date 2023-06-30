from typing import Protocol
from datetime import date

class SiteAvailability(Protocol):
    def check_availability(self, date: date) -> bool:
        ...