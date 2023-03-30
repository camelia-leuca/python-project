from datetime import datetime

from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Repository.repository_json import RepositoryJson


def clear_file(filename):
    with open(filename, "w") as f:
        pass


def test_film_repository():
    clear_file("test_film.json")
    film_repository_json = RepositoryJson("test_film.json")

    film = Film("1", "titlu", 2002, 50, "da")
    film_repository_json.adauga(film)
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read("1").id_entitate == "1"
    assert film_repository_json.read("1").titlu == "titlu"
    assert film_repository_json.read("1").an_aparitie == 2002
    assert film_repository_json.read("1").pret_bilet == 50
    assert film_repository_json.read("1").program == "da"

    film_repository_json.modifica(Film("1", "Titlu", 2021, 100, "da"))
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read("1").id_entitate == "1"
    assert film_repository_json.read("1").titlu == "Titlu"
    assert film_repository_json.read("1").an_aparitie == 2021
    assert film_repository_json.read("1").pret_bilet == 100
    assert film_repository_json.read("1").program == "da"

    film_repository_json.sterge("1")
    assert len(film_repository_json.read()) == 0


def test_card_client_repository():
    clear_file("test_card_client.json")
    card_client_repository_json = RepositoryJson("test_card_client.json")
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
    card_client_repository_json.adauga(card_client)
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read("1").id_entitate == "1"
    assert card_client_repository_json.read("1").nume == "nume"
    assert card_client_repository_json.read("1").prenume == "prenume"
    assert card_client_repository_json.read("1").CNP == "0123456789012"
    assert card_client_repository_json.read("1").data_nasterii == \
           data_nasterii
    assert card_client_repository_json.read("1").data_inregistrarii == \
           data_inregistrarii
    assert card_client_repository_json.read("1").puncte_acumulate == 30

    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client = CardClient("1",
                             "Nume",
                             "Prenume",
                             "1234567890123",
                             data_nasterii,
                             data_inregistrarii,
                             60
                             )
    card_client_repository_json.modifica(card_client)
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read("1").id_entitate == "1"
    assert card_client_repository_json.read("1").nume == "Nume"
    assert card_client_repository_json.read("1").prenume == "Prenume"
    assert card_client_repository_json.read("1").CNP == "1234567890123"
    assert card_client_repository_json.read("1").data_nasterii == \
           data_nasterii
    assert card_client_repository_json.read("1").data_inregistrarii == \
           data_inregistrarii
    assert card_client_repository_json.read("1").puncte_acumulate == 60

    card_client_repository_json.sterge("1")
    assert len(card_client_repository_json.read()) == 0


def test_rezervare_repository():
    clear_file("test_rezervare.json")
    rezervare_repository_json = RepositoryJson("test_rezervare.json")
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")

    rezervare = Rezervare("1", "1", "1", data_ora)
    rezervare_repository_json.adauga(rezervare)
    assert rezervare_repository_json.read("1").id_entitate == "1"
    assert rezervare_repository_json.read("1").id_film == "1"
    assert rezervare_repository_json.read("1").id_card_client == "1"
    assert rezervare_repository_json.read("1").data_ora == data_ora

    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare = Rezervare("1", "1", "1", data_ora)
    rezervare_repository_json.modifica(rezervare)
    assert rezervare_repository_json.read("1").id_entitate == "1"
    assert rezervare_repository_json.read("1").id_film == "1"
    assert rezervare_repository_json.read("1").id_card_client == "1"
    assert rezervare_repository_json.read("1").data_ora == \
           data_ora

    rezervare_repository_json.sterge("1")
    assert len(rezervare_repository_json.read()) == 0


def test_repository():
    test_film_repository()
    test_card_client_repository()
    test_rezervare_repository()
