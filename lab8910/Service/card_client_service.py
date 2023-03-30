import copy
import random
import string
from datetime import datetime, date
from typing import List

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.multi_add_operation import MultiAddOperation
from Domain.multi_modify_operation import MultiModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from my_sort import my_sort


class CardClientService:
    def __init__(self,
                 card_client_repository: Repository,
                 card_client_validator: CardClientValidator,
                 undo_redo_service: UndoRedoService):
        self.__card_client_repository = card_client_repository
        self.__card_client_validator = card_client_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self) -> List[CardClient]:
        return self.__card_client_repository.read()

    def adauga(self,
               id_card_client: str,
               nume: str,
               prenume: str,
               CNP: str,
               data_nasterii: date,
               data_inregistrarii: date,
               puncte_acumulate: int
               ):
        """
        Adauga un obiect de tip CardClient.
        """
        for card_client in self.__card_client_repository.read():
            if card_client.CNP == CNP:
                raise KeyError("Exista deja un card cu CNP-ul dat!")
        card_client = CardClient(
            id_card_client,
            nume,
            prenume,
            CNP,
            data_nasterii,
            data_inregistrarii,
            puncte_acumulate
        )
        self.__card_client_validator.valideaza(card_client)
        self.__card_client_repository.adauga(card_client)
        self.__undo_redo_service.adauga_operatie_undo(AddOperation(
            self.__card_client_repository,
            card_client))

    def sterge(self, id_card_client: str):
        """
        Sterge un obiect de tip CardClient.
        """
        card_client_sters = self.__card_client_repository. \
            read(id_card_client)
        self.__card_client_repository.sterge(id_card_client)
        self.__undo_redo_service.adauga_operatie_undo(DeleteOperation(
            self.__card_client_repository,
            card_client_sters))

    def modifica(self,
                 id_card_client: str,
                 nume: str,
                 prenume: str,
                 CNP: str,
                 data_nasterii: date,
                 data_inregistrarii: date,
                 puncte_acumulate: int
                 ):
        """
        Modifica un obiect de tip CardClient.
        """
        card_client_vechi = self.__card_client_repository. \
            read(id_card_client)
        for card_client in self.__card_client_repository.read():
            if card_client.CNP == CNP and card_client.id_entitate \
                    != id_card_client:
                raise KeyError("Exista deja un card cu CNP-ul dat!")
        card_client = CardClient(
            id_card_client,
            nume,
            prenume,
            CNP,
            data_nasterii,
            data_inregistrarii,
            puncte_acumulate
        )
        self.__card_client_validator.valideaza(card_client)
        self.__card_client_repository.modifica(card_client)
        self.__undo_redo_service.adauga_operatie_undo((ModifyOperation(
            self.__card_client_repository,
            card_client_vechi,
            card_client)))

    @staticmethod
    def genereaza_data():
        """
        Genereaza o data dd/mm/yyyy.
        """
        an = random.randrange(1900, 2021)
        luna = random.randrange(1, 12)
        zi = random.randrange(1, 28)
        data = f"{zi}/{luna}/{an}"
        return datetime.strptime(data, "%d/%m/%Y").date()

    def genereaza_n_carduri_client(self, n: int):
        """
        Genereaza si adauga n obiecte de tip Card Client.
        """
        carduri_client_generate = []
        for i in range(n):
            id_card_client = str(random.randrange(1, 1000))
            nume = ''.join(random.choices(string.ascii_letters, k=10))
            prenume = ''.join(random.choices(string.ascii_letters, k=10))
            CNP = ''.join(random.choices(string.digits, k=13))
            data_nasterii = self.genereaza_data()
            data_inregistrarii = self.genereaza_data()
            puncte_acumulate = random.randrange(0, 500)

            card_client = CardClient(id_card_client,
                                     nume,
                                     prenume,
                                     CNP,
                                     data_nasterii,
                                     data_inregistrarii,
                                     puncte_acumulate)

            carduri_client_generate.append(card_client)
            self.__card_client_repository.adauga(card_client)
        self.__undo_redo_service.adauga_operatie_undo(MultiAddOperation(
            self.__card_client_repository,
            carduri_client_generate))

    def cautare_clienti(self, text) -> List[CardClient]:
        """
        Cauta textul dat in atributele obiectelor CardClient.
        """
        rezultat = list(filter(lambda x:
                               text in x.nume or
                               text in x.prenume or
                               text in x.CNP or
                               text in str(x.data_nasterii) or
                               text in str(x.data_inregistrarii) or
                               text in str(x.puncte_acumulate),
                               self.__card_client_repository.read()))
        return rezultat

    def carduri_descrescator_dupa_puncte(self) -> List[CardClient]:
        """
        Sorteaza descrescator cardurile client dupa numarul de puncte
        acumulte.
        """
        return my_sort(self.__card_client_repository.read(),
                       key=lambda card_client: card_client.puncte_acumulate,
                       reverse=True)

    @staticmethod
    def incrementeaza_puncte(card_client: CardClient, puncte: int):
        """
        Incrementeaza punctele acumulate pe un card client.
        """
        card_client.puncte_acumulate += puncte
        return card_client

    def incrementeaza_puncte_in_interval(self,
                                         puncte: int,
                                         data1: date,
                                         data2: date):
        """
        Incrementeaza puncte acumulate cu o valoare data pe toate cardurile
        a caror zi de nastere este in intervalul dat.
        """
        carduri_client_de_modificat = []
        for card_client in self.__card_client_repository.read():
            if data1 <= card_client.data_nasterii <= data2:
                carduri_client_de_modificat.append(card_client)

        carduri_client_modificate = copy. \
            deepcopy(carduri_client_de_modificat)
        carduri_client_modificate = list(
            map(lambda card_client: self.incrementeaza_puncte(
                card_client,
                puncte),
                carduri_client_modificate))
        for card_client_nou in carduri_client_modificate:
            self.__card_client_repository.modifica(card_client_nou)
        self.__undo_redo_service.adauga_operatie_undo(
            MultiModifyOperation(
                self.__card_client_repository,
                carduri_client_de_modificat,
                carduri_client_modificate))
