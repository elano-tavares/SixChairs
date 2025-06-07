from src.filme import Filme
from indices.trie import buscar_titulos_por_prefixo
from indices.hash import buscar_filmes_por_diretor
from indices.arvore import buscar_filmes_por_ano, buscar_filme_por_id

def buscar_filmes_com_filtros(
    prefixo_titulo: str | None,
    diretor: str | None,
    ano: int | None,
    id_filme: str | None,
    trie: dict,
    hash_diretor: dict,
    indice_ano: dict,
    indice_id: dict,
    caminho_bin: str = "data/filmes.bin"
) -> list[Filme]:

    # Conjuntos para intersecção
    resultados = []

    if id_filme:
        filme = buscar_filme_por_id(indice_id, id_filme, caminho_bin)
        return [filme] if filme else []

    if prefixo_titulo:
        resultados.append(set(buscar_titulos_por_prefixo(trie, prefixo_titulo)))

    if diretor:
        resultados.append(set(buscar_filmes_por_diretor(diretor, hash_diretor, caminho_bin)))

    if ano:
        resultados.append(set(buscar_filmes_por_ano(indice_ano, ano, caminho_bin)))

    if not resultados:
        return []

    # Interseção dos conjuntos
    filmes_filtrados = set.intersection(*resultados)
    return list(filmes_filtrados)
