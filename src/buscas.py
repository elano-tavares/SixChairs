# src/buscas.py (MODIFICADO - Correção de Importação)

# Importa Filme para tipagem
from src.filme import Filme # <-- MODIFICADO AQUI: Importa APENAS a classe Filme
# Removido: , TAMANHO_REGISTRO (não é mais importado diretamente)

# Importa as funções de busca de cada tipo de índice
from indices.trie import buscar_titulos_por_prefixo 
from indices.hash import buscar_filmes_por_diretor 
from indices.arvore import buscar_filmes_por_ano_b_tree, buscar_filme_por_id_b_tree 

# Importa a função de leitura de filmes do binary_store
from src.binary_store import ler_filmes_binario 

# Removido: import struct

#--------------------#
#  Busca por Gênero  #
#--------------------#
def buscar_filmes_por_genero(genero: str, caminho_bin="data/filmes.bin") -> list[Filme]:
    genero_lower = genero.lower() 
    resultados = []

    filmes_completos = ler_filmes_binario(caminho_bin)
    
    for filme in filmes_completos:
        if genero_lower in filme.genero.lower().split(','):
            resultados.append(filme)
    return resultados

#---------------------#
#  Busca com Filtros  #
#---------------------#
def buscar_filmes_com_filtros(
    prefixo_titulo: str | None,
    diretor: str | None,
    ano: int | None,
    id_filme: str | None,
    genero: str | None,
    trie_obj, 
    hash_diretor_obj: dict, 
    indice_ano_obj, 
    indice_id_obj,  
    caminho_bin: str = "data/filmes.bin",
    ordenar_por: str = 'titulo', 
    ordem_crescente: bool = True 
) -> list[Filme]:
    """
    Realiza buscas de filmes combinando diferentes filtros usando os índices.
    Aplica a ordenação final aos resultados.
    """

    if id_filme:
        filme = buscar_filme_por_id_b_tree(indice_id_obj, id_filme, caminho_bin)
        if filme:
            return [filme] 
        return [] 

    filmes_candidatos_por_criterio = []

    if prefixo_titulo:
        filmes_candidatos_por_criterio.append(set(buscar_titulos_por_prefixo(trie_obj, prefixo_titulo, caminho_bin)))

    if diretor:
        filmes_candidatos_por_criterio.append(set(buscar_filmes_por_diretor(diretor, hash_diretor_obj, caminho_bin)))

    if ano:
        filmes_candidatos_por_criterio.append(set(buscar_filmes_por_ano_b_tree(indice_ano_obj, ano, caminho_bin)))

    if genero:
        filmes_candidatos_por_criterio.append(set(buscar_filmes_por_genero(genero, caminho_bin)))

    if not filmes_candidatos_por_criterio:
        return []

    filmes_filtrados_set = set.intersection(*filmes_candidatos_por_criterio)
    filmes_filtrados_list = list(filmes_filtrados_set) 

    if ordenar_por == 'titulo':
        filmes_filtrados_list.sort(key=lambda f: f.titulo.lower(), reverse=not ordem_crescente)
    elif ordenar_por == 'ano':
        filmes_filtrados_list.sort(key=lambda f: f.ano, reverse=not ordem_crescente)
    elif ordenar_por == 'diretor':
        filmes_filtrados_list.sort(key=lambda f: f.diretor.lower(), reverse=not ordem_crescente)

    return filmes_filtrados_list