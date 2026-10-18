from enum import Enum
from uuid import uuid4

from zahlungsmethoden import Zahlungsmethode

# Enum für möglichen Status einer Bestellung
class Bestellstatus(Enum):
    OFFEN = "offen"
    BEZAHLT = "bezahlt"

class Bestellung:

    def __init__(self, betrag: float):
        self.__bestell_id = str(uuid4())
        self.__betrag = betrag
        self.__status = Bestellstatus.OFFEN

    # Properties ermöglichen lesenden Zugriff auf interne Attribute
    @property
    def bestell_id(self) -> str:
        return self.__bestell_id

    @property
    def betrag(self) -> float:
        return self.__betrag

    @property
    def status(self) -> Bestellstatus:
        return self.__status


    def bezahlen(self, zahlungsmethode: Zahlungsmethode) -> str:

        if self.__status == Bestellstatus.BEZAHLT:
            raise ValueError("Die Bestellung wurde bereits bezahlt")

        # Polymorpher Aufruf der konkreten Zahlungsmethode
        ergebnis = zahlungsmethode.bezahlen(self.__betrag)
        self.__status = Bestellstatus.BEZAHLT

        return ergebnis