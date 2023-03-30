from dataclasses import dataclass
from datetime import date

from Domain.Entitate import Entitate


@dataclass
class CardClient(Entitate):
    """
    Descrie cardul unui client.
    """
    nume: str
    prenume: str
    CNP: str
    data_nasterii: date
    data_inregistrarii: date
    puncte_acumulate: int
