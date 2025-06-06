# hash.py

import pickle
import struct
from collections import defaultdict
from src.filme import Filme
from src.gravador import TAMANHO_REGISTRO

#--------------------------------#
#      Construir índice hash     #
#--------------------------------#
def construir_indice_hash_por_diretor(filmes: list) -> dict[str, list[int]]:
    hash_diretor = defaultdict(list)
    for offset, filme in enumerate(filmes):
        posicao = offset * TAMANHO_REGISTRO  # 234 bytes fixos
        hash_diretor[filme.diretor].append(posicao)
    return hash_diretor

#----------------------------------#
#      Salvar hash em arquivo      #
#----------------------------------#
def salvar_hash_em_arquivo(hash_diretor: dict[str, list[int]], caminho: str) -> None:
    with open(caminho, "wb") as f:
        pickle.dump(hash_diretor, f)

#----------------------------------#
#      Carregar hash do arquivo    #
#----------------------------------#
def carregar_hash_de_arquivo(caminho: str) -> dict[str, list[int]]:
    with open(caminho, "rb") as f:
        return pickle.load(f)

#----------------------------------#
#      Buscar por diretor          #
#----------------------------------#
def buscar_filmes_por_diretor(nome_diretor: str, hash_diretor: dict[str, list[int]], caminho_bin: str = "data/filmes.bin") -> list[Filme]:
    if nome_diretor not in hash_diretor:
        return []

    filmes = []
    with open(caminho_bin, "rb") as f:
        for offset in hash_diretor[nome_diretor]:
            f.seek(offset)
            dados = f.read(TAMANHO_REGISTRO)
            if not dados:
                continue
            id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack("10s100si20s100s", dados)
            filme = Filme(
                id_b.decode("utf-8").rstrip("\x00"),
                titulo_b.decode("utf-8").rstrip("\x00"),
                ano,
                genero_b.decode("utf-8").rstrip("\x00"),
                diretor_b.decode("utf-8").rstrip("\x00")
            )
            filmes.append(filme)
    return filmes