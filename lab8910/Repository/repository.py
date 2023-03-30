from typing import Protocol

from Domain.Entitate import Entitate


class Repository(Protocol):
    def read(self, id_entitate=None):
        ...

    def adauga(self, entitate: Entitate):
        ...

    def sterge(self, id_entitate: str):
        ...

    def modifica(self, entitate: Entitate):
        ...
