from dataclasses import dataclass

from Domain.Entitate import Entitate


@dataclass
class Film(Entitate):
    """
    Descrie un film.
    """
    titlu: str
    an_aparitie: int
    pret_bilet: float
    program: str
