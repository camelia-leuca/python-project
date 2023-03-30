import random
import string
from typing import List

from Domain.add_operation import AddOperation
from Domain.cascade_delete_operation import CascadeDeleteOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.film__validator import FilmValidator
from Domain.modify_operation import ModifyOperation
from Domain.multi_add_operation import MultiAddOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self, film_repository: Repository,
                 film_validator: FilmValidator,
                 rezervare_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.__film_validator = film_validator
        self.__film_repository = film_repository
        self.__undo_redo_service = undo_redo_service
        self.__rezervare_repository_json = rezervare_repository

    def get_all(self) -> List[Film]:
        return self.__film_repository.read()

    def adauga(self,
               id_film: str,
               titlu: str,
               an_aparitie: int,
               pret_bilet: float,
               program: str):
        """
        Adauga un obiect de tip Film.
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, program)
        self.__film_validator.valideaza(film)
        self.__film_repository.adauga(film)
        self.__undo_redo_service.adauga_operatie_undo(AddOperation(
            self.__film_repository,
            film))

    def sterge(self, id_film: str):
        """
        Sterge un obiect de tip Film.
        """
        obiecte_de_sters = []
        film_de_sters = self.__film_repository.read(id_film)
        for rezervare in self.__rezervare_repository_json.read():
            if rezervare.id_film == id_film:
                obiecte_de_sters.append(rezervare)
        for rezervare in obiecte_de_sters:
            self.__rezervare_repository_json.sterge(rezervare.id_entitate)
        if len(obiecte_de_sters):
            obiecte_de_sters += [film_de_sters]
            self.__undo_redo_service.adauga_operatie_undo(
                CascadeDeleteOperation(self.__film_repository,
                                       self.__rezervare_repository_json,
                                       obiecte_de_sters))
        else:
            self.__undo_redo_service.adauga_operatie_undo(DeleteOperation(
                self.__film_repository, film_de_sters))
        self.__film_repository.sterge(id_film)

    def modifica(self,
                 id_film: str,
                 titlu: str,
                 an_aparitie: int,
                 pret_bilet: float,
                 program: str):
        """
        Modifica un obiect de tip Film.
        """
        film_vechi = self.__film_repository.read(id_film)
        film = Film(id_film, titlu, an_aparitie, pret_bilet, program)
        self.__film_validator.valideaza(film)
        self.__film_repository.modifica(film)
        self.__undo_redo_service.adauga_operatie_undo(ModifyOperation(
            self.__film_repository,
            film_vechi,
            film))

    def genereaza_n_filme(self, n: int):
        """
        Genereaza si adauga n obiecte de tip Film.
        """
        filme_generate = []
        for i in range(n):
            id_film = str(random.randrange(1, 1000))
            titlu = ''.join(random.choices(string.ascii_letters, k=10))
            an_aparitie = random.randrange(1000, 9999)
            pret_bilet = random.randrange(10, 100)
            program = random.choice(["da", "nu"])
            film = Film(id_film,
                        titlu,
                        an_aparitie,
                        pret_bilet,
                        program)
            filme_generate.append(film)
            self.__film_repository.adauga(film)
        self.__undo_redo_service.adauga_operatie_undo(MultiAddOperation(
            self.__film_repository,
            filme_generate))

    def cautare_filme(self, text):
        """
        Cauta textul dat in atributele obiectelor de tip Film.
        """
        rezultat = [x for x in self.__film_repository.read() if
                    text in x.titlu or
                    text in str(x.an_aparitie) or
                    text in str(x.pret_bilet) or
                    text in x.program]
        return rezultat
