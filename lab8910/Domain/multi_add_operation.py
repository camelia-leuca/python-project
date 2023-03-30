from typing import List

from Domain.Entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiAddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiecte_adaugate: List[Entitate]):
        self.__repository = repository
        self.__obiecte_adaugate = obiecte_adaugate

    def do_undo(self):
        for entitate in self.__obiecte_adaugate:
            self.__repository.sterge(entitate.id_entitate)

    def do_redo(self):
        for entitate in self.__obiecte_adaugate:
            self.__repository.adauga(entitate)
