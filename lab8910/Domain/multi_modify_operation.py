from typing import List

from Domain.Entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiModifyOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiecte_vechi: List[Entitate],
                 obiecte_noi: List[Entitate]):
        self.__repository = repository
        self.__obiecte_vechi = obiecte_vechi
        self.__obiecte_noi = obiecte_noi

    def do_undo(self):
        for obiect_vechi in self.__obiecte_vechi:
            self.__repository.modifica(obiect_vechi)

    def do_redo(self):
        for obiect_nou in self.__obiecte_noi:
            self.__repository.modifica(obiect_nou)
