# indices/hash.py (MODIFICADO - Correção de Importação)

import pickle
from collections import defaultdict
from src.filme import Filme # <-- MODIFICADO AQUI: Importa APENAS a classe Filme
from src.binary_store import ler_filme_por_offset

#--------------------------------#
#      Construir índice hash     #
#--------------------------------#
def construir_indice_hash_por_diretor(filmes: list[Filme]) -> dict[str, list[int]]:
    """
    Constrói um índice hash que mapeia nomes de diretores para
    listas de offsets de filmes no arquivo binário.
    """
    hash_diretor = defaultdict(list)
    for i, filme in enumerate(filmes): 
        # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
        posicao = i * Filme.TAMANHO_REGISTRO 
        hash_diretor[filme.diretor].append(posicao)
    return hash_diretor

#----------------------------------#
#      Salvar hash em arquivo      #
#----------------------------------#
def salvar_hash_em_arquivo(hash_diretor: dict[str, list[int]], caminho: str) -> None:
    """
    Salva o índice hash (dicionário) em um arquivo binário usando pickle.
    """
    with open(caminho, "wb") as f:
        pickle.dump(hash_diretor, f)
    print(f"📁 Índice Hash salvo em: {caminho}")

#----------------------------------#
#      Carregar hash do arquivo    #
#----------------------------------#
def carregar_hash_de_arquivo(caminho: str) -> dict[str, list[int]]:
    """
    Carrega o índice hash (dicionário) de um arquivo binário usando pickle.
    """
    with open(caminho, "rb") as f:
        return pickle.load(f)

#----------------------------------#
#      Buscar por diretor          #
#----------------------------------#
def buscar_filmes_por_diretor(nome_diretor: str, hash_diretor: dict[str, list[int]], caminho_bin: str = "data/filmes.bin") -> list[Filme]:
    """
    Busca filmes pelo nome do diretor usando o índice hash.
    Retorna uma lista de objetos Filme.
    """
    if nome_diretor not in hash_diretor:
        return []

    filmes = []
    for offset in hash_diretor[nome_diretor]:
        filme = ler_filme_por_offset(offset, caminho_bin)
        if filme:
            filmes.append(filme)
    return filmes