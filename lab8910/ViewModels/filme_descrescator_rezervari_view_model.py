from dataclasses import dataclass

from Domain.film import Film


@dataclass
class FilmeRezervariViewModel:
    film: Film
    numar_rezervari: int

    def __str__(self):
        return f'{self.film} are numarul de rezervari {self.numar_rezervari}.'
