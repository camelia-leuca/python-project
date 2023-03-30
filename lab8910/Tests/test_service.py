from datetime import datetime

from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.film import Film
from Domain.film__validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.repository_json import RepositoryJson
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.test_repository import clear_file


def test_film_service():
    clear_file("test_film.json")
    rezervare_repository_json = RepositoryJson("rezervari.json")
    undo_redo_service = UndoRedoService()
    film_repository_json = RepositoryJson("test_film.json")
    film_validator = FilmValidator()
    film_service = FilmService(film_repository_json,
                               film_validator,
                               rezervare_repository_json,
                               undo_redo_service)

    film_service.adauga("1", "titlu", 2002, 50, "da")
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read("1").id_entitate == "1"
    assert film_repository_json.read("1").titlu == "titlu"
    assert film_repository_json.read("1").an_aparitie == 2002
    assert film_repository_json.read("1").pret_bilet == 50
    assert film_repository_json.read("1").program == "da"

    film_service.modifica("1", "Titlu", 2021, 100, "da")
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read("1").id_entitate == "1"
    assert film_repository_json.read("1").titlu == "Titlu"
    assert film_repository_json.read("1").an_aparitie == 2021
    assert film_repository_json.read("1").pret_bilet == 100
    assert film_repository_json.read("1").program == "da"

    film_service.sterge("1")
    assert len(film_repository_json.read()) == 0

    film_service.adauga("1", "titlu", 2002, 50, "da")
    film_service.adauga("2", "Titlu", 2002, 100, "nu")
    film_service.adauga("3", "Titlu", 2002, 70, "da")

    assert film_service.cautare_filme("da") == \
           [Film("1", "titlu", 2002, 50, "da"),
            Film("3", "Titlu", 2002, 70, "da")]


def test_card_client_service():
    clear_file("test_card_client.json")
    undo_redo_service = UndoRedoService()
    card_client_repository_json = RepositoryJson("test_card_client.json")
    card_client_validator = CardClientValidator()
    card_client_service = CardClientService(card_client_repository_json,
                                            card_client_validator,
                                            undo_redo_service)

    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("1",
                               "nume",
                               "prenume",
                               "0123456789012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )
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
    card_client_service.modifica("1",
                                 "Nume",
                                 "Prenume",
                                 "1234567890123",
                                 data_nasterii,
                                 data_inregistrarii,
                                 60
                                 )
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

    card_client_service.sterge("1")
    assert len(card_client_repository_json.read()) == 0

    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("1",
                               "nume",
                               "prenume",
                               "0123456789012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )
    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client_service.adauga("2",
                               "Nume",
                               "Prenume",
                               "1234567890123",
                               data_nasterii,
                               data_inregistrarii,
                               60
                               )

    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    data_nasterii2 = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii2 = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    assert card_client_service.cautare_clienti("nume") == \
           [CardClient("1",
                       "nume",
                       "prenume",
                       "0123456789012",
                       data_nasterii,
                       data_inregistrarii,
                       30),
            CardClient("2",
                       "Nume",
                       "Prenume",
                       "1234567890123",
                       data_nasterii2,
                       data_inregistrarii2,
                       60)]

    card1 = card_client_repository_json.read("1")
    card2 = card_client_repository_json.read("2")
    assert card_client_service.carduri_descrescator_dupa_puncte() == \
           [card2, card1]

    data1 = datetime.strptime("12/12/2000", "%d/%m/%Y").date()
    data2 = datetime.strptime("12/12/2004", "%d/%m/%Y").date()
    card_client_service.\
        incrementeaza_puncte_in_interval(10, data1, data2)
    assert card_client_repository_json.read("1").puncte_acumulate == 40
    assert card_client_repository_json.read("2").puncte_acumulate == 60


def test_rezervare_service():
    clear_file("test_rezervare.json")
    undo_redo_service = UndoRedoService()
    rezervare_repository_json = RepositoryJson("test_rezervare.json")
    rezervare_validator = RezervareValidator()
    film_repository_json = RepositoryJson("test_film.json")
    card_client_repository_json = RepositoryJson("test_card_client.json")
    rezervare_service = RezervareService(
        film_repository_json,
        card_client_repository_json,
        rezervare_repository_json,
        rezervare_validator,
        undo_redo_service)

    # pret1 = 50
    # pret3 = 70
    # puncte1 = 40
    # puncte2 = 60
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    assert rezervare_repository_json.read("1").id_entitate == "1"
    assert rezervare_repository_json.read("1").id_film == "1"
    assert rezervare_repository_json.read("1").id_card_client == "1"
    assert rezervare_repository_json.read("1").data_ora == data_ora
    assert card_client_repository_json.read("1").puncte_acumulate == 45
    assert card_client_repository_json.read("2").puncte_acumulate == 60

    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.modifica("1", "3", "2", data_ora)
    assert rezervare_repository_json.read("1").id_entitate == "1"
    assert rezervare_repository_json.read("1").id_film == "3"
    assert rezervare_repository_json.read("1").id_card_client == "2"
    assert rezervare_repository_json.read("1").data_ora == \
           data_ora
    assert card_client_repository_json.read("1").puncte_acumulate == 40
    assert card_client_repository_json.read("2").puncte_acumulate == 67

    rezervare_service.sterge("1")
    assert len(rezervare_repository_json.read()) == 0

    film_repository_json.sterge("3")

    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("2", "1", "1", data_ora)
    rezervare1 = rezervare_repository_json.read("1")
    rezervare2 = rezervare_repository_json.read("2")

    assert rezervare_service.rezervare_in_interval("15:00-17:00") == \
           [rezervare1]

    interval = "1/1/2010-1/1/2012"
    data1, data2 = interval.split("-")
    data1 = datetime.strptime(data1, "%d/%m/%Y").date()
    data2 = datetime.strptime(data2, "%d/%m/%Y").date()
    rezervare_service.sterge_rezervari_in_interval(data1, data2)

    assert rezervare_repository_json.read() == [rezervare2]


def test_undo_redo():
    clear_file("test_film.json")
    clear_file("test_card_client.json")
    clear_file("test_rezervare.json")

    undo_redo_service = UndoRedoService()

    film_repository_json = RepositoryJson("test_film.json")
    card_client_repository_json = RepositoryJson("test_card_client.json")
    rezervare_repository_json = RepositoryJson("test_rezervare.json")

    film_validator = FilmValidator()
    film_service = FilmService(film_repository_json,
                               film_validator,
                               rezervare_repository_json,
                               undo_redo_service)

    card_client_validator = CardClientValidator()
    card_client_service = CardClientService(card_client_repository_json,
                                            card_client_validator,
                                            undo_redo_service)

    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(
        film_repository_json,
        card_client_repository_json,
        rezervare_repository_json,
        rezervare_validator,
        undo_redo_service)

    # [] -> [1, 2, 3]
    film_service.adauga("1", "titlu", 2002, 50, "da")
    film_service.adauga("2", "Titlu", 2002, 100, "nu")
    film_service.adauga("3", "Titlu", 2002, 70, "da")

    # [1, 2, 3] -> [1, 2]
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1]
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 0

    # [] -> []
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 0

    # [] -> [1, 2, 3]
    film_service.adauga("1", "titlu", 2002, 50, "da")
    film_service.adauga("2", "Titlu", 2002, 100, "nu")
    film_service.adauga("3", "Titlu", 2002, 70, "da")

    # [1, 2, 3] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 3
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "2"
    assert film_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 2]
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 3
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "2"
    assert film_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 4]
    film_service.adauga("4", "Titlu", 2002, 70, "da")

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1]
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 1
    assert film_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 0

    # [] -> [1, 4]
    undo_redo_service.redo()
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "1"
    assert film_repository_json.read()[1].id_entitate == "4"

    # [] -> [1, 2, 3]
    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("1",
                               "nume",
                               "prenume",
                               "0123456789012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client_service.adauga("2",
                               "Nume",
                               "Prenume",
                               "1234567890123",
                               data_nasterii,
                               data_inregistrarii,
                               60
                               )

    data_nasterii = datetime.strptime("20/12/2021", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("3",
                               "nume",
                               "prenume",
                               "0123456780012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    # [1, 2, 3] -> [1, 2]
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 2
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1]
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 0

    # [] -> []
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 0

    # [] -> [1, 2, 3]
    data_nasterii = datetime.strptime("20/12/2002", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("1",
                               "nume",
                               "prenume",
                               "0123456789012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client_service.adauga("2",
                               "Nume",
                               "Prenume",
                               "1234567890123",
                               data_nasterii,
                               data_inregistrarii,
                               60
                               )

    data_nasterii = datetime.strptime("20/12/2021", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("3",
                               "nume",
                               "prenume",
                               "0123456780012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    # [1, 2, 3] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 3
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "2"
    assert card_client_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 2]
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 2
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 3
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "2"
    assert card_client_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 4]
    data_nasterii = datetime.strptime("20/12/2021", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("4",
                               "nume",
                               "prenume",
                               "0123456780002",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 2
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1]
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 1
    assert card_client_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(card_client_repository_json.read()) == 0

    # [] -> [1, 4]
    undo_redo_service.redo()
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 2
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(card_client_repository_json.read()) == 2
    assert card_client_repository_json.read()[0].id_entitate == "1"
    assert card_client_repository_json.read()[1].id_entitate == "4"

    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client_service.adauga("2",
                               "Nume",
                               "Prenume",
                               "1234567890123",
                               data_nasterii,
                               data_inregistrarii,
                               60
                               )

    data_nasterii = datetime.strptime("20/12/2021", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("3/3/2003", "%d/%m/%Y").date()
    card_client_service.adauga("3",
                               "nume",
                               "prenume",
                               "0123456780012",
                               data_nasterii,
                               data_inregistrarii,
                               30
                               )

    data1 = datetime.strptime("12/12/2000", "%d/%m/%Y").date()
    data2 = datetime.strptime("12/12/2004", "%d/%m/%Y").date()
    card_client_service.\
        incrementeaza_puncte_in_interval(10, data1, data2)
    assert card_client_repository_json.read("1").puncte_acumulate == 40
    assert card_client_repository_json.read("2").puncte_acumulate == 60

    undo_redo_service.undo()
    assert card_client_repository_json.read("1").puncte_acumulate == 30
    assert card_client_repository_json.read("2").puncte_acumulate == 60

    # [] -> [1, 2, 3]
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("2", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2017 9:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("3", "1", "1", data_ora)

    # [1, 2, 3] -> [1, 2]
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1]
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 0

    # [] -> []
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 0

    # [] -> [1, 2, 3]
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("2", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2017 9:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("3", "1", "1", data_ora)

    # [1, 2, 3] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 3
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "2"
    assert rezervare_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 2]
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "2"

    # [1, 2] -> [1, 2, 3]
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 3
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "2"
    assert rezervare_repository_json.read()[2].id_entitate == "3"

    # [1, 2, 3] -> [1]
    undo_redo_service.undo()
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "1"

    # [1] -> [1, 4]
    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("4", "1", "1", data_ora)

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1]
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "1"

    # [1] -> []
    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 0

    # [] -> [1, 4]
    undo_redo_service.redo()
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "4"

    # [1, 4] -> [1, 4]
    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "1"
    assert rezervare_repository_json.read()[1].id_entitate == "4"

    clear_file("test_rezervare.json")

    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("2", "1", "1", data_ora)
    rezervare2 = rezervare_repository_json.read("2")

    interval = "1/1/2010-1/1/2012"
    data1, data2 = interval.split("-")
    data1 = datetime.strptime(data1, "%d/%m/%Y").date()
    data2 = datetime.strptime(data2, "%d/%m/%Y").date()
    rezervare_service.sterge_rezervari_in_interval(data1, data2)

    assert rezervare_repository_json.read() == [rezervare2]

    undo_redo_service.undo()
    assert len(rezervare_repository_json.read()) == 2
    assert rezervare_repository_json.read()[0].id_entitate == "2"
    assert rezervare_repository_json.read()[1].id_entitate == "1"

    undo_redo_service.redo()
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "2"

    # Cascade test
    clear_file("test_film.json")
    clear_file("test_card_client.json")
    clear_file("test_rezervare.json")

    film_service.adauga("1", "titlu", 2002, 50, "da")
    film_service.adauga("2", "Titlu", 2002, 100, "da")

    data_nasterii = datetime.strptime("20/12/2005", "%d/%m/%Y").date()
    data_inregistrarii = datetime.strptime("4/3/2006", "%d/%m/%Y").date()
    card_client_service.adauga("1",
                               "Nume",
                               "Prenume",
                               "1234567890123",
                               data_nasterii,
                               data_inregistrarii,
                               60
                               )

    data_ora = datetime.strptime("5/7/2010 16:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("1", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2013 20:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("2", "1", "1", data_ora)
    data_ora = datetime.strptime("5/7/2017 9:00", "%d/%m/%Y %H:%M")
    rezervare_service.adauga("3", "2", "1", data_ora)

    film_service.sterge("1")
    assert len(film_repository_json.read()) == 1
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "3"

    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "2"
    assert film_repository_json.read()[1].id_entitate == "1"
    assert len(rezervare_repository_json.read()) == 3
    assert rezervare_repository_json.read()[0].id_entitate == "3"
    assert rezervare_repository_json.read()[1].id_entitate == "1"
    assert rezervare_repository_json.read()[2].id_entitate == "2"

    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 1
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "3"

    undo_redo_service.redo()
    assert len(film_repository_json.read()) == 1
    assert len(rezervare_repository_json.read()) == 1
    assert rezervare_repository_json.read()[0].id_entitate == "3"

    undo_redo_service.undo()
    assert len(film_repository_json.read()) == 2
    assert film_repository_json.read()[0].id_entitate == "2"
    assert film_repository_json.read()[1].id_entitate == "1"
    assert len(rezervare_repository_json.read()) == 3
    assert rezervare_repository_json.read()[0].id_entitate == "3"
    assert rezervare_repository_json.read()[1].id_entitate == "1"
    assert rezervare_repository_json.read()[2].id_entitate == "2"


def test_service():
    test_film_service()
    test_card_client_service()
    test_rezervare_service()
    test_undo_redo()
