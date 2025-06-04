# filme.py

#----------------#
#  Classe_Filme  #
#----------------#
class Filme:
    def __init__(self, id: str, titulo: str, ano: int, genero: str, diretor: str):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.diretor = diretor
    
    def __repr__(self):
        return f"[{self.id}] {self.titulo} ({self.ano}) - {self.genero} | Diretor: {self.diretor}"