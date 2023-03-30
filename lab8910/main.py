from Domain.card_client_validator import CardClientValidator
from Domain.film__validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.repository_json import RepositoryJson
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.test_all import test_all
from UI.consola import Consola


def main():
    test_all()
    undo_redo_service = UndoRedoService()
    film_repository_json = RepositoryJson("filme.json")
    rezervare_repository_json = RepositoryJson("rezervari.json")

    film_validator = FilmValidator()
    film_service = FilmService(film_repository_json,
                               film_validator,
                               rezervare_repository_json,
                               undo_redo_service)

    card_client_repository_json = RepositoryJson("carduri_client.json")
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

    consola = Consola(film_service,
                      card_client_service,
                      rezervare_service,
                      undo_redo_service)
    consola.run_menu()


main()
