from abc import ABC, abstractmethod


# Abstrakte Basisklasse als gemeinsame Schnittstelle für alle konkreten Zahlungsmethoden.
class Zahlungsmethode(ABC):

    @abstractmethod
    def bezahlen(self, betrag: float) -> str:
        pass


# Konkrete Unterklassen überschreiben bezahlen() und implementieren jeweils ihr eigenes Verhalten
class Kreditkarte(Zahlungsmethode):

    def bezahlen(self, betrag: float) -> str:
        return f"Kreditkartenzahlung über {betrag:.2f} EUR"

class PayPal(Zahlungsmethode):

    def bezahlen(self, betrag: float) -> str:
        return f"Paypal-Zahlung über {betrag:.2f} EUR"

class Ueberweisung(Zahlungsmethode):

    def bezahlen(self, betrag: float) -> str:
        return f"Überweisung über {betrag:.2f} EUR"