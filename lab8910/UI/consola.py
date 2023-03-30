
from datetime import datetime
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


class Consola:
    def __init__(self,
                 film_service: FilmService,
                 card_client_service: CardClientService,
                 rezervare_service: RezervareService,
                 undo_redo_service: UndoRedoService):
        self.__film_service = film_service
        self.__card_client_service = card_client_service
        self.__rezervare_service = rezervare_service
        self.__undo_redo_service = undo_redo_service

    def run_menu(self):
        while True:
            print("1. CRUD filme.")
            print("2. CRUD carduri client.")
            print("3. CRUD Rezervari.")
            print("4. Cautare full text in filme si clienti.")
            print("5. Afiseaza rezervarile intr-un interval de timp dat.")
            print("6. Afiseaza filmele ordonate descrescator dupa "
                  "numarul de rezervari.")
            print("7. Afiseaza cardurile client ordonate descrescator dupa "
                  "punctele acumulate.")
            print("8. Sterge rezervarile dintr-un interval dat.")
            print("9. Incrementeaza cu o valoare data punctele de pe toate"
                  " cardurile a caror zi de nastere se afla intr-un"
                  " interval dat.")
            print("u. Undo.")
            print("r. Redo.")
            print("x. Iesire")

            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.run_filme_menu()
            elif optiune == "2":
                self.run_carduri_client_menu()
            elif optiune == "3":
                self.run_rezervari_menu()
            elif optiune == "4":
                self.ui_cautare_full_text()
            elif optiune == "5":
                self.ui_rezervari_in_interval()
            elif optiune == "6":
                self.ui_filme_descrescator_dupa_rezervari()
            elif optiune == "7":
                self.ui_carduri_descrescator_dupa_puncte()
            elif optiune == "8":
                self.ui_sterge_rezervari_in_interval()
            elif optiune == "9":
                self.ui_incrementeaza_puncte()
            elif optiune == "u":
                self.__undo_redo_service.undo()
            elif optiune == "r":
                self.__undo_redo_service.redo()
            elif optiune == "x":
                break
            else:
                print("Optiune invalida!")

    def run_filme_menu(self):
        while True:
            print("1. Adauga film.")
            print("2. Sterge film.")
            print("3. Modifica film.")
            print("a. Afiseaza toate filmele.")
            print("n. Genereaza n filme.")
            print("x. Iesire.")

            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_film()
            elif optiune == "2":
                self.ui_sterge_film()
            elif optiune == "3":
                self.ui_modifica_film()
            elif optiune == "n":
                self.ui_genereaza_filme()
            elif optiune == "x":
                break
            elif optiune == "a":
                self.showall_filme()
            else:
                print("Optiune invalida!")

    def run_carduri_client_menu(self):
        while True:
            print("1. Adauga cardul client.")
            print("2. Sterge cardul client.")
            print("3. Modifica cardul client.")
            print("n. Genereaza n carduri client.")
            print("a. Afiseaza cardurile client.")
            print("x. Iesire.")

            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_card_client()
            elif optiune == "2":
                self.ui_sterge_card_client()
            elif optiune == "3":
                self.ui_modifica_card_client()
            elif optiune == "n":
                self.ui_genereaza_carduri_client()
            elif optiune == "x":
                break
            elif optiune == "a":
                self.showall_card_client()
            else:
                print("Optiune invalida!")

    def run_rezervari_menu(self):
        while True:
            print("1. Adauga rezervarea.")
            print("2. Sterge rezervarea.")
            print("3. Modifica rezervarea.")
            print("n. Genereaza n rezervari.")
            print("a. Afiseaza toate rezervarile.")
            print("x. Iesire.")

            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_rezervare()
            elif optiune == "2":
                self.ui_sterge_rezervare()
            elif optiune == "3":
                self.ui_modifica_rezervare()
            elif optiune == "n":
                self.ui_genereaza_rezervari()
            elif optiune == "x":
                break
            elif optiune == "a":
                self.showall_rezervare()
            else:
                print("Optiune invalida!")

    def ui_adauga_film(self):
        try:
            id_film = input("Dati id- ul filmului: ")
            titlu = input("Dati titlul filmului: ")
            an_aparitie = int(input("Dati anul aparitiei filmului: "))
            pret_bilet = float(input("Dati pretul biletului: "))
            program = input("Dati prgramul filmului (da/nu): ")

            self.__film_service.adauga(id_film,
                                       titlu,
                                       an_aparitie,
                                       pret_bilet,
                                       program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_adauga_card_client(self):
        try:
            id_card_client = input("Dati id- ul cardului client: ")
            nume = input("Dati numele clientului: ")
            prenume = input("Dati prenumele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            data_nasterii = datetime.strptime(
                input("Dati data nasterii clientului (dd/mm/yyyy): "),
                "%d/%m/%Y").date()
            data_inregistrarii = datetime.strptime(
                input("Dati data inregistrarii clientului (dd/mm/yyyy): "),
                "%d/%m/%Y").date()
            puncte_acumulate = int(input("Dati punctele acumulate: "))

            self.__card_client_service.adauga(
                id_card_client,
                nume,
                prenume,
                CNP,
                data_nasterii,
                data_inregistrarii,
                puncte_acumulate
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_adauga_rezervare(self):
        try:
            id_rezervare = input("Dati id- ul rezervarii: ")
            id_film = input("Dati id- ul filmului: ")
            id_card_client = input("Dati id- ul cardului client: ")
            data_ora = datetime.strptime(
                input("Dati data si ora rezervarii (dd/mm/yyyy/ hh:mm): "),
                "%d/%m/%Y %H:%M")

            self.__rezervare_service.adauga(id_rezervare,
                                            id_film,
                                            id_card_client,
                                            data_ora)
            if id_card_client:
                print(f'Numarul de puncte acumulate este '
                      f'{self.__rezervare_service.puncte(id_card_client)}')

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_film(self):
        try:
            id_film = input("Dati id-ul filmului de sters: ")
            self.__film_service.sterge(id_film)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_card_client(self):
        try:
            id_card_client = input("Dati id-ul cardului client de sters: ")
            self.__card_client_service.sterge(id_card_client)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_rezervare(self):
        try:
            id_rezervare = input("Dati id-ul rezervarii de sters: ")
            self.__rezervare_service.sterge(id_rezervare)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_film(self):
        try:
            id_film = input("Dati id- ul filmului de modificat: ")
            titlu = input("Dati noul titlu al filmului: ")
            an_aparitie = int(input("Dati noul an al aparitiei filmului: "))
            pret_bilet = float(input("Dati noul pret al biletului: "))
            program = input("Dati noul prgram al filmului (da/nu): ")

            self.__film_service.modifica(id_film,
                                         titlu,
                                         an_aparitie,
                                         pret_bilet,
                                         program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_card_client(self):
        try:
            id_card_client = input("Dati id- ul cardului client"
                                   " de modificat: ")
            nume = input("Dati noul nume al clientului: ")
            prenume = input("Dati noul prenume al clientului: ")
            CNP = input("Dati noul CNP al clientului: ")
            data_nasterii = datetime.strptime(
                input("Dati noua data a nasterii clientului (dd/mm/yyyy): "),
                "%d/%m/%Y").date()
            data_inregistrarii = datetime.strptime(
                input("Dati noua data a inregistrarii clientului "
                      "(dd/mm/yyyy): "), "%d/%m/%Y").date()
            puncte_acumulate = int(input("Dati noua valoare a "
                                         "punctelor acumulate: "))

            self.__card_client_service.modifica(
                id_card_client,
                nume,
                prenume,
                CNP,
                data_nasterii,
                data_inregistrarii,
                puncte_acumulate
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_rezervare(self):
        try:
            id_rezervare = input("Dati id- ul rezervarii de modificat: ")
            id_film = input("Dati noul id al filmului: ")
            id_card_client = input("Dati noul id al cardului client: ")
            data_ora = datetime.strptime(
                input("Dati noua data si ora a rezervarii "
                      "(dd/mm/yyyy/ hh:mm): "), "%d/%m/%Y %H:%M")

            self.__rezervare_service.modifica(id_rezervare,
                                              id_film,
                                              id_card_client,
                                              data_ora)
            if id_card_client:
                print(f'Numarul de puncte acumulate este '
                      f'{self.__rezervare_service.puncte(id_card_client)}')

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_genereaza_filme(self):
        try:
            n = int(input("Dati numarul n: "))
            self.__film_service.genereaza_n_filme(n)
        except Exception as e:
            print(e)

    def ui_genereaza_carduri_client(self):
        try:
            n = int(input("Dati numarul n: "))
            self.__card_client_service.genereaza_n_carduri_client(n)
        except Exception as e:
            print(e)

    def ui_genereaza_rezervari(self):
        try:
            n = int(input("Dati numarul n: "))
            self.__rezervare_service.genereaza_n_rezervari(n)
        except Exception as e:
            print(e)

    def showall_filme(self):
        for film in self.__film_service.get_all():
            print(film)

    def showall_card_client(self):
        for card_client in self.__card_client_service.get_all():
            print(card_client)

    def showall_rezervare(self):
        for rezervare in self.__rezervare_service.get_all():
            print(rezervare)

    def ui_cautare_full_text(self):
        text = input("Dati textul: ")
        if self.__film_service.cautare_filme(text):
            print(self.__film_service.cautare_filme(text))
        if self.__card_client_service.cautare_clienti(text):
            print(self.__card_client_service.cautare_clienti(text))

    def ui_rezervari_in_interval(self):
        interval = input("Dati intervalul orelor (hh:mm-HH:MM): ")
        print(self.__rezervare_service.rezervare_in_interval(interval))

    def ui_filme_descrescator_dupa_rezervari(self):
        for element in self.__rezervare_service.\
                filme_descrescator_dupa_rezervari():
            print(element)

    def ui_carduri_descrescator_dupa_puncte(self):
        for element in self.__card_client_service.\
                carduri_descrescator_dupa_puncte():
            print(element)

    def ui_sterge_rezervari_in_interval(self):
        try:
            interval = input("Dati intervalul zilelor (dd/mm/yy-DD/MM/YY): ")
            data1, data2 = interval.split("-")
            data1 = datetime.strptime(data1, "%d/%m/%Y").date()
            data2 = datetime.strptime(data2, "%d/%m/%Y").date()
            if data1 > data2:
                data1, data2 = data2, data1
            self.__rezervare_service.\
                sterge_rezervari_in_interval(data1, data2)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_incrementeaza_puncte(self):
        try:
            interval = input("Dati intervalul zilelor (dd/mm/yy-DD/MM/YY): ")
            puncte = int(input("Dati valoarea cu care se "
                               "incrementeaza punctele acumulate: "))
            data1, data2 = interval.split("-")
            data1 = datetime.strptime(data1, "%d/%m/%Y").date()
            data2 = datetime.strptime(data2, "%d/%m/%Y").date()
            if data1 > data2:
                data1, data2 = data2, data1

            self.__card_client_service.\
                incrementeaza_puncte_in_interval(puncte,
                                                 data1,
                                                 data2)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
