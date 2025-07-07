# src/buscas.py

# Importa Filme para tipagem
from src.filme import Filme 

# Importa as funções de busca de cada tipo de índice
from indices.trie import buscar_titulos_por_prefixo 
from indices.hash import buscar_filmes_por_diretor 
from indices.arvore import buscar_filmes_por_ano_b_tree, buscar_filme_por_id_b_tree 

#--------------------#
#  Busca por Gênero  #
#--------------------#
def buscar_filmes_por_genero(genero: str, caminho_bin="data/filmes.bin") -> list[Filme]:
    """
    Busca filmes por gênero fazendo uma varredura sequencial no arquivo binário,
    sem carregá-lo inteiramente em memória.
    """
    genero_lower = genero.lower() 
    resultados = []

    try:
        with open(caminho_bin, "rb") as f:
            while True:
                # Lê um único registro (o tamanho de um filme) do arquivo
                bytes_lidos = f.read(Filme.TAMANHO_REGISTRO) 
                if not bytes_lidos:
                    # Se não houver mais bytes para ler, chegamos ao fim do arquivo
                    break
                
                # Converte os bytes lidos em um objeto Filme
                filme = Filme.from_bytes(bytes_lidos)
                
                # Compara o gênero do filme com o gênero buscado
                if genero_lower in filme.genero.lower().split(','):
                    resultados.append(filme)
    except FileNotFoundError:
        print(f"⚠️  Arquivo binário não encontrado: {caminho_bin}")
        
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
