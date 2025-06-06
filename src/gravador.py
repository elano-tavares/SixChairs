# gravador.py

import struct
from typing import List
from src.filme import Filme
from indices.trie import Trie

# Caminho padrão do arquivo binário
ARQUIVO_BINARIO = "data/filmes.bin"

# Definição da estrutura binária: id(10s), título(100s), ano(i), gênero(20s), diretor(100s)
FORMATO_REGISTRO = "10s100si20s100s"
TAMANHO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)

#-------------------------#
#  Salvar_filmes_binario  #
#-------------------------#
def salvar_filmes_binario(filmes: List[Filme], caminho: str = ARQUIVO_BINARIO):
    """
    Salva uma lista de filmes no arquivo binário em modo heap (inserção serial).
    """
    with open(caminho, "wb") as f:
        for filme in filmes:
            registro = struct.pack(
                FORMATO_REGISTRO,
                filme.id.encode("utf-8")[:10].ljust(10, b"\x00"),
                filme.titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
                filme.ano,
                filme.genero.encode("utf-8")[:20].ljust(20, b"\x00"),
                filme.diretor.encode("utf-8")[:100].ljust(100, b"\x00"),
            )
            f.write(registro)
    print(f"✅ {len(filmes)} filmes salvos em: {caminho}")

#----------------------#
#  Ler_filmes_binario  #
#----------------------#
def ler_filmes_binario(caminho: str = ARQUIVO_BINARIO) -> List[Filme]:
    """
    Lê todos os filmes do arquivo binário e retorna como lista de objetos Filme.
    """
    filmes = []
    try:
        with open(caminho, "rb") as f:
            while True:
                bytes_lidos = f.read(TAMANHO_REGISTRO)
                if not bytes_lidos:
                    break
                id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack(FORMATO_REGISTRO, bytes_lidos)
                filme = Filme(
                    id_b.decode("utf-8").rstrip("\x00"),
                    titulo_b.decode("utf-8").rstrip("\x00"),
                    ano,
                    genero_b.decode("utf-8").rstrip("\x00"),
                    diretor_b.decode("utf-8").rstrip("\x00")
                )
                filmes.append(filme)
    except FileNotFoundError:
        print(f"⚠️ Arquivo binário não encontrado: {caminho}")
    return filmes

#---------------------------#
#  Salvar_filmes__bin_trie  #
#---------------------------#
def salvar_filmes_binario_com_trie(filmes: List[Filme], caminho: str = ARQUIVO_BINARIO) -> Trie:
    trie = Trie()
    with open(caminho, "wb") as f:
        for i, filme in enumerate(filmes):
            offset = i * TAMANHO_REGISTRO
            registro = struct.pack(
                FORMATO_REGISTRO,
                filme.id.encode("utf-8")[:10].ljust(10, b"\x00"),
                filme.titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
                filme.ano,
                filme.genero.encode("utf-8")[:20].ljust(20, b"\x00"),
                filme.diretor.encode("utf-8")[:100].ljust(100, b"\x00"),
            )
            f.write(registro)
            trie.inserir(filme.titulo, offset)
    print(f"✅ {len(filmes)} filmes salvos no binário e TRIE construída.")
    return trie
