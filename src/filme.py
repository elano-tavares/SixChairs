# src/filme.py (CORREÇÃO DE ATRIBUTO DE CLASSE)

import struct

class Filme:
    # Atributos de classe para o formato e tamanho do registro
    FORMATO_REGISTRO = "10s100si20s100s"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)

    def __init__(self, id: str, titulo: str, ano: int, genero: str, diretor: str):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.diretor = diretor
    
    def __repr__(self):
        return f"[{self.id}] {self.titulo} ({self.ano}) - {self.genero} | Diretor: {self.diretor}"
    
    def __eq__(self, other):
        if isinstance(other, Filme):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def to_bytes(self) -> bytes:
        """
        Converte o objeto Filme para uma sequência de bytes formatada
        de acordo com FORMATO_REGISTRO (atributo de classe).
        """
        return struct.pack(
            Filme.FORMATO_REGISTRO, # Acessa via Filme.FORMATO_REGISTRO
            self.id.encode("utf-8")[:10].ljust(10, b"\x00"),
            self.titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
            self.ano,
            self.genero.encode("utf-8")[:20].ljust(20, b"\x00"),
            self.diretor.encode("utf-8")[:100].ljust(100, b"\x00"),
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        Cria um objeto Filme a partir de uma sequência de bytes formatada
        de acordo com FORMATO_REGISTRO (atributo de classe).
        """
        id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack(cls.FORMATO_REGISTRO, data) # Acessa via cls.FORMATO_REGISTRO
        return cls(
            id_b.decode("utf-8").rstrip("\x00"),
            titulo_b.decode("utf-8").rstrip("\x00"),
            ano,
            genero_b.decode("utf-8").rstrip("\x00"),
            diretor_b.decode("utf-8").rstrip("\x00")
        )