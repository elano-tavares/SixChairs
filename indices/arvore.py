# arvore.py

import pickle
from collections import defaultdict
from src.filme import Filme
from src.gravador import TAMANHO_REGISTRO
import struct

#-------------------------------#
#    Construir índice por ano   #
#-------------------------------#
def construir_indice_ano(filmes: list) -> dict[int, list[int]]:
    indice = defaultdict(list)
    for offset, filme in enumerate(filmes):
        posicao = offset * TAMANHO_REGISTRO
        indice[filme.ano].append(posicao)
    return dict(indice)

#-------------------------------#
#    Construir índice por id    #
#-------------------------------#
def construir_indice_id(filmes: list) -> dict[str, int]:
    indice = {}
    for offset, filme in enumerate(filmes):
        posicao = offset * TAMANHO_REGISTRO
        indice[filme.id] = posicao
    return indice

#-------------------------------#
#    Salvar índice em arquivo   #
#-------------------------------#
def salvar_indice_em_arquivo(indice: dict[int, list[int]], caminho: str):
    with open(caminho, "wb") as f:
        pickle.dump(indice, f)

#-------------------------------#
#    Carregar índice do disco   #
#-------------------------------#
def carregar_indice_de_arquivo(caminho: str) -> dict[int, list[int]]:
    with open(caminho, "rb") as f:
        return pickle.load(f)

#-------------------------------#
#    Buscar filmes por ano(s)   #
#-------------------------------#
def buscar_filmes_por_ano(indice: dict[int, list[int]], ano: int | tuple, caminho_bin="data/filmes.bin") -> list[Filme]:
    filmes = []
    anos = []

    if isinstance(ano, tuple):
        anos = [a for a in indice if ano[0] <= a <= ano[1]]
    else:
        anos = [ano] if ano in indice else []

    with open(caminho_bin, "rb") as f:
        for a in sorted(anos):
            for offset in indice[a]:
                f.seek(offset)
                dados = f.read(TAMANHO_REGISTRO)
                if not dados:
                    continue
                id_b, titulo_b, ano_lido, genero_b, diretor_b = struct.unpack("10s100si20s100s", dados)
                filme = Filme(
                    id_b.decode("utf-8").strip("\x00"),
                    titulo_b.decode("utf-8").strip("\x00"),
                    ano_lido,
                    genero_b.decode("utf-8").strip("\x00"),
                    diretor_b.decode("utf-8").strip("\x00")
                )
                filmes.append(filme)
    return filmes

#-------------------------------#
#     Buscar filmes por id      #
#-------------------------------#
def buscar_filme_por_id(indice_id: dict[str, int], filme_id: str, caminho_bin="data/filmes.bin") -> Filme | None:
    if filme_id not in indice_id:
        return None

    offset = indice_id[filme_id]
    with open(caminho_bin, "rb") as f:
        f.seek(offset)
        dados = f.read(TAMANHO_REGISTRO)
        if not dados:
            return None
        id_b, titulo_b, ano_lido, genero_b, diretor_b = struct.unpack("10s100si20s100s", dados)
        return Filme(
            id_b.decode("utf-8").strip("\x00"),
            titulo_b.decode("utf-8").strip("\x00"),
            ano_lido,
            genero_b.decode("utf-8").strip("\x00"),
            diretor_b.decode("utf-8").strip("\x00")
        )
