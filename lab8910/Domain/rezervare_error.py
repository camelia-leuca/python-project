from dataclasses import dataclass


@dataclass
class RezervareError(Exception):
    mesaj: list[str]

    def __str__(self):
        return f'RezervareError: {self.mesaj}'
