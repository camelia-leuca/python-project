from abc import ABC


class UndoRedoOperation(ABC):
    def undo(self):
        ...

    def redo(self):
        ...
