from dataclasses import dataclass

@dataclass
class Fermata:
    id_fermata: int
    nome: str
    coordX: int
    coordY: int


    def __hash__(self):
        return self._id_fermata

    def __str__(self):
        return f"{self._nome}"
