from Domain.film import Film
from Domain.film_error import FilmError


class FilmValidator:
    @staticmethod
    def valideaza(film: Film):
        erori = []
        if film.id_entitate is None:
            erori.append("Id-ul trebuie completat!")
        if film.titlu is None:
            erori.append("Titlul trebuie completat!")
        if film.an_aparitie is None:
            erori.append("Anul aparitiei trebuie completat!")
        if film.pret_bilet is None:
            erori.append("Pretul biletului trebuie completat!")
        if film.program is None:
            erori.append("Programul trebuie completat!")
        if film.id_entitate.isdigit() is False:
            erori.append("Id-ul trebuie sa contina numai cifre!")
        if film.an_aparitie <= 0:
            erori.append("Anul aparitiei trbuie sa fie un numar natural!")
        if film.pret_bilet <= 0:
            erori.append("Pretul biletului trebuie sa fie un numar "
                         "strict pozitiv!")
        if film.program not in ["da", "nu"]:
            erori.append("Program trebuie sa fie 'da' sau 'nu''!")
        if len(erori) > 0:
            raise FilmError(erori)
