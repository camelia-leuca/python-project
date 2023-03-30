import jsonpickle

from Domain.Entitate import Entitate
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __read_file(self):
        """
        Citeste un fisier.
        """
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self):
        """
        Scrie in fisier.
        """
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        """
        Returneaza continutul din fisier.
        """
        self.entitati = self.__read_file()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate):
        """
        Adauga un obiect in fisier.
        """
        self.entitati = self.__read_file()
        super().adauga(entitate)
        self.__write_file()

    def sterge(self, id_entitate: str):
        """
        Sterge un obiect cu id-ul dat din fisier.
        """
        self.entitati = self.__read_file()
        super().sterge(id_entitate)
        self.__write_file()

    def modifica(self, entitate: Entitate):
        """
        Modifica un obiect din fisier.
        """
        self.entitati = self.__read_file()
        super().modifica(entitate)
        self.__write_file()
