from typing import List

from Domain.Entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class CascadeDeleteOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 repository_cascade: Repository,
                 obiecte_sterse: List[Entitate]):
        self.__repository = repository
        self.__repository_cascade = repository_cascade
        self.__obiecte_sterse = obiecte_sterse

    def do_undo(self):
        for i in range(len(self.__obiecte_sterse)-1):
            self.__repository_cascade.adauga(self.__obiecte_sterse[i])
        self.__repository.adauga(self.__obiecte_sterse
                                 [len(self.__obiecte_sterse)-1])

    def do_redo(self):
        for i in range(len(self.__obiecte_sterse)-1):
            self.__repository_cascade.sterge(self.__obiecte_sterse[i]
                                             .id_entitate)
        self.__repository.sterge(self.__obiecte_sterse
                                 [len(self.__obiecte_sterse)-1].id_entitate)
