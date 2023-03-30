from datetime import date, datetime

from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare


def test_film():
    film = Film("1", "titlu", 2002, 50, "da")
    assert film.id_entitate == "1"
    assert film.titlu == "titlu"
    assert film.an_aparitie == 2002
    assert film.pret_bilet == 50
    assert film.program == "da"


def test_card_client():
    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client = CardClient("1",
                             "nume",
                             "prenume",
                             "0123456789012",
                             data_nasterii,
                             data_inregistrarii,
                             30
                             )
    assert card_client.id_entitate == "1"
    assert card_client.nume == "nume"
    assert card_client.prenume == "prenume"
    assert card_client.CNP == "0123456789012"
    assert card_client.data_nasterii == data_nasterii
    assert card_client.data_inregistrarii == data_inregistrarii
    assert card_client.puncte_acumulate == 30


def test_rezervare():
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare = Rezervare("1", "1", "1", data_ora)
    assert rezervare.id_entitate == "1"
    assert rezervare.id_film == "1"
    assert rezervare.id_card_client == "1"
    assert rezervare.data_ora == data_ora


def test_domain():
    test_film()
    test_card_client()
    test_rezervare()
