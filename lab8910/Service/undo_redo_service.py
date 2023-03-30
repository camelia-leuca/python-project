
from Domain.undo_redo_operation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.undo_operations = []
        self.redo_operations = []

    def adauga_operatie_undo(self, undo_redo_operation: UndoRedoOperation):
        self.undo_operations.append(undo_redo_operation)
        self.redo_operations.clear()

    def undo(self):
        if self.undo_operations:
            last_undo_operation = self.undo_operations.pop()
            self.redo_operations.append(last_undo_operation)
            last_undo_operation.do_undo()

    def redo(self):
        if self.redo_operations:
            last_redo_operation = self.redo_operations.pop()
            self.undo_operations.append(last_redo_operation)
            last_redo_operation.do_redo()
