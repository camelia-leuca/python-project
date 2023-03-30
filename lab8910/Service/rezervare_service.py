import random
from datetime import datetime, date
from typing import List

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.multi_add_operation import MultiAddOperation
from Domain.multi_delete_operation import MultiDeleteOperation
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.filme_descrescator_rezervari_view_model \
    import FilmeRezervariViewModel


class RezervareService:
    def __init__(self,
                 film_repository: Repository,
                 card_client_repository: Repository,
                 rezervare_repository: Repository,
                 rezervare_validator: RezervareValidator,
                 undo_redo_service: UndoRedoService):

        self.__film_repository = film_repository
        self.__card_client_repository = card_client_repository
        self.__rezervare_repository = rezervare_repository
        self.__rezervare_validator = rezervare_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self) -> List[Rezervare]:
        return self.__rezervare_repository.read()

    def adauga(self,
               id_rezervare: str,
               id_film: str,
               id_card_client: str,
               data_ora: datetime):
        """
        Adauga un obiect de tip Rezervare.
        Daca exista un card client, se adauga 10% din pretul biletului
         la puncte.
        """
        if self.__film_repository.read(id_film) is None:
            raise KeyError("Nu exista niciun film cu id-ul dat!")
        if self.__card_client_repository.read(id_card_client) is None:
            raise KeyError("Nu exista niciun card cu id-ul dat!")
        if self.__film_repository.read(id_film).program == "nu":
            raise ValueError("Filmul nu este in program!")
        rezervare = Rezervare(id_rezervare,
                              id_film,
                              id_card_client,
                              data_ora)
        self.__rezervare_validator.valideaza(rezervare)
        self.__rezervare_repository.adauga(rezervare)
        if id_card_client:
            card_client = self.adauga_puncte(id_film, id_card_client)
            self.__card_client_repository.modifica(card_client)
        self.__undo_redo_service.adauga_operatie_undo(AddOperation(
            self.__rezervare_repository,
            rezervare))

    def sterge(self, id_rezervare: str):
        """
        Sterge un obiect de tip Rezervare
        """
        rezervare_stearsa = self.__rezervare_repository.read(id_rezervare)
        self.__rezervare_repository.sterge(id_rezervare)
        self.__undo_redo_service.adauga_operatie_undo(DeleteOperation(
            self.__rezervare_repository,
            rezervare_stearsa))

    def modifica(self,
                 id_rezervare: str,
                 id_film: str,
                 id_card_client: str,
                 data_ora: datetime):
        """
        Modifica un obiect de tip Rezervare.
        Daca exista un card client, se adauga 10% din noul pret
         al biletului la puncte.
        """
        if self.__film_repository.read(id_film) is None:
            raise KeyError("Nu exista niciun film cu id-ul dat!")
        if self.__card_client_repository.read(id_card_client) is None:
            raise KeyError("Nu exista niciun card cu id-ul dat!")
        if self.__film_repository.read(id_film).program == "nu":
            raise ValueError("Filmul nu este in program!")

        id_card_client_initial = self.__rezervare_repository. \
            read(id_rezervare).id_card_client
        id_film_initial = self.__rezervare_repository. \
            read(id_rezervare).id_film
        if id_card_client != id_card_client_initial or id_film:
            if id_card_client_initial is not None:
                card_client = self.sterge_puncte(id_film_initial,
                                                 id_card_client_initial)
                self.__card_client_repository.modifica(card_client)
            if id_card_client is not None:
                card_client = self.adauga_puncte(id_film, id_card_client)
                self.__card_client_repository.modifica(card_client)
        rezervare_veche = self.__rezervare_repository.read(id_rezervare)
        rezervare = Rezervare(id_rezervare,
                              id_film,
                              id_card_client,
                              data_ora)
        self.__rezervare_validator.valideaza(rezervare)
        self.__rezervare_repository.modifica(rezervare)
        self.__undo_redo_service.adauga_operatie_undo(ModifyOperation(
            self.__rezervare_repository,
            rezervare_veche,
            rezervare))

    def adauga_puncte(self, id_film: str, id_card_client: str) -> CardClient:
        """
        Adauga puncte pe cardul client.
        Folosita la adaugarea/ modificarea rezervarilor.
        """
        pret = int(self.__film_repository.read(id_film).pret_bilet)
        nume = self.__card_client_repository.read(id_card_client).nume
        prenume = self.__card_client_repository.read(id_card_client).prenume
        CNP = self.__card_client_repository.read(id_card_client).CNP
        data_nasterii = self.__card_client_repository. \
            read(id_card_client).data_nasterii
        data_inregistrarii = self.__card_client_repository. \
            read(id_card_client).data_inregistrarii
        puncte = self.__card_client_repository. \
            read(id_card_client).puncte_acumulate
        puncte = int(puncte + float(pret) * 10 / 100)

        card_client = CardClient(id_card_client,
                                 nume,
                                 prenume,
                                 CNP,
                                 data_nasterii,
                                 data_inregistrarii,
                                 puncte)
        return card_client

    def sterge_puncte(self, id_film: str, id_card_client: str) -> CardClient:
        """
        Sterge puncte de pe cardul client.
        Folosita la modificarea rezervarilor.
        """
        if id_card_client:
            pret_film_intial = self.__film_repository. \
                read(id_film).pret_bilet
            puncte_initial = self.__card_client_repository. \
                read(id_card_client).puncte_acumulate
            puncte = int(puncte_initial - float(pret_film_intial) * 10 / 100)
            nume = self.__card_client_repository.read(id_card_client).nume
            prenume = self.__card_client_repository. \
                read(id_card_client).prenume
            CNP = self.__card_client_repository.read(id_card_client).CNP
            data_nasterii = self.__card_client_repository. \
                read(id_card_client).data_nasterii
            data_inregistrarii = self.__card_client_repository. \
                read(id_card_client).data_inregistrarii
            card_client = CardClient(id_card_client,
                                     nume,
                                     prenume,
                                     CNP,
                                     data_nasterii,
                                     data_inregistrarii,
                                     puncte)
            return card_client

    def puncte(self, id_card_client: str) -> int:
        """
        Returneaza punctele acumulate pe card.
        """
        return self.__card_client_repository.read(id_card_client). \
            puncte_acumulate

    def genereaza_n_rezervari(self, n: int):
        """
        Genereaza si adauga n obiecte de tip Rezervare.
        """
        rezervari_generate = []
        for i in range(n):
            id_rezervare = str(random.randrange(1, 1000))

            id_film_in_program = []
            for film in self.__film_repository.read():
                if film.program == "da":
                    id_film_in_program.append(film.id_entitate)
            id_carduri_client = []
            for card_client in self.__card_client_repository.read():
                id_carduri_client.append(card_client.id_entitate)
            id_carduri_client.append(None)

            id_film = random.choice(id_film_in_program)
            id_card_client = random.choice(id_carduri_client)

            an = random.randrange(1900, 2021)
            luna = random.randrange(1, 12)
            zi = random.randrange(1, 28)
            ora = random.randrange(0, 23)
            minut = random.randrange(0, 59)
            date_time = f"{zi}/{luna}/{an} {ora}:{minut}"
            data_ora = datetime.strptime(date_time, "%d/%m/%Y %H:%M")

            rezervare = Rezervare(id_rezervare,
                                  id_film,
                                  id_card_client,
                                  data_ora)
            rezervari_generate.append(rezervare)
            self.__rezervare_repository.adauga(rezervare)
        self.__undo_redo_service.adauga_operatie_undo(MultiAddOperation(
            self.__rezervare_repository,
            rezervari_generate))

    def rezervare_in_interval(self, interval: str) -> List[Rezervare]:
        """
        Returneaza rezervarile dintr-un interval de timp(ore) dat.
        """
        try:
            ora1, ora2 = interval.split("-")
            ora1 = datetime.strptime(ora1, "%H:%M").time()
            ora2 = datetime.strptime(ora2, "%H:%M").time()
            rezultat = list(filter(lambda x:
                                   ora1 <= x.data_ora.time() <= ora2,
                                   self.__rezervare_repository.read()))
            return rezultat
        except ValueError as ve:
            print(ve)

    def filme_descrescator_dupa_rezervari(self) -> \
            List[FilmeRezervariViewModel]:
        """
        Returneaza filmele ordonate descrescator dupa numarul de rezervari.
        """
        rezultat = []
        numar_rezervari_per_film = {}
        for film in self.__film_repository.read():
            numar_rezervari_per_film[film.id_entitate] = 0
        for rezervare in self.__rezervare_repository.read():
            numar_rezervari_per_film[rezervare.id_film] += 1

        for id_film in numar_rezervari_per_film:
            rezultat.append(FilmeRezervariViewModel(
                self.__film_repository.read(id_film),
                numar_rezervari_per_film[id_film]
            ))
        return sorted(rezultat,
                      key=lambda rezervari: rezervari.numar_rezervari,
                      reverse=True)

    def sterge_rezervari_in_interval(self, data1: date, data2: date,):
        """
        Sterge rezervarile dintr-un interval de zile dat.
        """
        rezervari = self.__rezervare_repository.read()

        def rezervari_de_sters(n: int, de_sters: List):
            """
            Determina rezervarile ce trebuie sterse.
            """
            if n < 0:
                return de_sters
            if data1 <= rezervari[n].data_ora.date() <= data2:
                de_sters.append(rezervari[n])
            return rezervari_de_sters(n-1, de_sters)

        de_sters = rezervari_de_sters(len(rezervari)-1, [])
        for rezervare in de_sters:
            self.sterge(str(rezervare.id_entitate))
        self.__undo_redo_service.adauga_operatie_undo(
            MultiDeleteOperation(self.__rezervare_repository,
                                 de_sters))
