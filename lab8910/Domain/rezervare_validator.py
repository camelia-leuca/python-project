from Domain.rezervare import Rezervare


class RezervareValidator:
    @staticmethod
    def valideaza(rezervare: Rezervare):
        erori = []
        if rezervare.id_entitate is None:
            erori.append("Id-ul trebuie completat!")
        if rezervare.id_film is None:
            erori.append("Id-ul filmului trebuie completat!")
        if rezervare.data_ora is None:
            erori.append("Data trebuie completata!")
            erori.append("Id-ul rezervarii trebuie sa contina numai cifre!")
        if rezervare.id_film.isdigit() is False:
            erori.append("Id-ul filmului trebuie sa contina numai cifre!")
        if rezervare.id_card_client is not None:
            if rezervare.id_card_client.isdigit() is False:
                erori.append("Id-ul cardului client trebuie sa contina"
                             " numai cifre!")
        if len(erori) > 0:
            raise ValueError(erori)
