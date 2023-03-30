from Domain.card_client import CardClient
from Domain.card_client_error import CardClientError


class CardClientValidator:
    @staticmethod
    def valideaza(card_client: CardClient):
        erori = []
        if card_client.id_entitate is None:
            erori.append("Id-ul trebuie completat!")
        if card_client.nume is None:
            erori.append("Numele trebuie completat!")
        if card_client.prenume is None:
            erori.append("Prenumele trebuie completat!")
        if card_client.CNP is None:
            erori.append("CNP-ul trebuie completat!")
        if card_client.data_nasterii is None:
            erori.append("Data nasterii trebuie completata!")
        if card_client.data_inregistrarii is None:
            erori.append("Data inregistrarii trebuie completata!")
        if card_client.puncte_acumulate is None:
            erori.append("Punctele acumulate trebuie completate!")
        if card_client.id_entitate.isdigit() is False:
            erori.append("Id-ul trebuie sa contina numai cifre!")
        if card_client.CNP.isdigit() is False or len(card_client.CNP) != 13:
            erori.append("CNP-ul trebuie sa contina 13 cifre!")
        if card_client.puncte_acumulate < 0:
            erori.append("Punctele acumulate trebuie sa fie "
                         "un numar natural!")
        if len(erori) > 0:
            raise CardClientError(erori)
