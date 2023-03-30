from dataclasses import dataclass
from datetime import datetime

from Domain.Entitate import Entitate


@dataclass
class Rezervare(Entitate):
    """
    Descrie o rezervare.
    """
    id_film: str
    id_card_client: str
    data_ora: datetime
