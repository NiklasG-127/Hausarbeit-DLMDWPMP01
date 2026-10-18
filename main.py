from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from bestellung import Bestellung
from zahlungsmethoden import Kreditkarte, PayPal, Ueberweisung

app = FastAPI(
    title="Kleine Bestellungs-API",
    version="1.0.0"
)

# Temporäre Speicherung der Bestellungen im Arbeitsspeicher
# (wird bei Neustart der Anwendung zurückgesetzt)
bestellungen = {}


class BestellungErstellen(BaseModel):
    betrag: float = Field(gt=0, le=10000)

class ZahlungAnfrage(BaseModel):
    zahlungsmethode: str

@app.get("/")
def root():
    return {"Title": app.title,
            "Version": app.version
        }

# Erstellt eine Bestellung und speichert sie unter ihrer eindeutigen ID.
@app.post("/orders")
def bestellung_erstellen(anfrage: BestellungErstellen):

    bestellung = Bestellung(anfrage.betrag)
    bestellungen[bestellung.bestell_id] = bestellung

    return {
        "bestell_id": bestellung.bestell_id,
        "betrag": bestellung.betrag,
        "status": bestellung.status.value
    }



# Übergibt die Zahlung an die Bestellung und behandelt fachliche Fehler
@app.post("/orders/{bestell_id}/pay")
def bestellung_bezahlen(
    bestell_id: str,
    anfrage: ZahlungAnfrage
):
    bestellung = bestellungen.get(bestell_id)

    if bestellung is None:
        raise HTTPException(
            status_code=404,
            detail="Bestellung nicht gefunden"
        )

    zahlungsmethoden = {
        "kreditkarte": Kreditkarte(),
        "paypal": PayPal(),
        "ueberweisung": Ueberweisung()
    }

    zahlungsmethode = zahlungsmethoden.get(anfrage.zahlungsmethode.lower())

    if zahlungsmethode is None:
        raise HTTPException(
            status_code=400,
            detail="Unbekannte Zahlungsmethode"
        )

    try:
        ergebnis = bestellung.bezahlen(zahlungsmethode)
    except ValueError as fehler:
        raise HTTPException(
            status_code=409,
            detail=str(fehler)
        )

    return {
        "bestell_id": bestellung.bestell_id,
        "status": bestellung.status.value,
        "zahlung": ergebnis
    }