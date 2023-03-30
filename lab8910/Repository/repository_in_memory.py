from Domain.Entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Returneaza obiectul de tip Entitate cu id-ul dat din fisier sau toate
         obiectele aflate in acel fisier.
        """
        if id_entitate is None:
            return list(self.entitati.values())
        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga un obiect de tip Entitate in-memory.
        """
        if self.read(entitate.id_entitate) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate: str):
        """
        Sterge un obiect de tip Entitate cu id-ul dat in-memory.
        """
        if self.read(id_entitate) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica un obiect de tip entitate in-memory.
        """
        if self.read(entitate.id_entitate) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate
