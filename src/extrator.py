# extrator.py

import csv
from typing import List, Dict
from src.filme import Filme

#---------------------------#
#  Carregar_nome_diretores  #
#---------------------------#
def carregar_nome_diretores(nome_tsv: str) -> Dict[str, str]:
    """Lê name.basics.tsv e retorna um dicionário nconst → primaryName"""
    nomes = {}
    with open(nome_tsv, encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f, delimiter='\t')
        for linha in leitor:
            nconst = linha['nconst']
            nome = linha['primaryName']
            nomes[nconst] = nome
    return nomes

#---------------------------------#
#  Carregar_diretores_por_titulo  #
#---------------------------------#
def carregar_diretores_por_titulo(crew_tsv: str) -> Dict[str, str]:
    """Lê title.crew.tsv e retorna um dicionário tconst → primeiro nconst do diretor"""
    diretores = {}
    with open(crew_tsv, encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f, delimiter='\t')
        for linha in leitor:
            tconst = linha['tconst']
            diretores_ids = linha['directors']
            if diretores_ids and diretores_ids != r'\N':
                primeiro = diretores_ids.split(',')[0]
                diretores[tconst] = primeiro
    return diretores

#------------------#
#  Extrair_filmes  #
#------------------#
def extrair_filmes(basics_tsv: str,
                   diretores_por_titulo: Dict[str, str],
                   nomes_diretores: Dict[str, str],
                   limite: int = 1000) -> List[Filme]:
    filmes = []
    with open(basics_tsv, encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f, delimiter='\t')
        for linha in leitor:
            if linha['titleType'] != 'movie':
                continue
            if linha['tconst'] not in diretores_por_titulo:
                continue
            if linha['startYear'] in [r'\N', ''] or linha['genres'] in [r'\N', '']:
                continue

            try:
                ano = int(linha['startYear'])
            except ValueError:
                continue

            tconst = linha['tconst']
            titulo = linha['primaryTitle']
            genero = linha['genres'].split(',')[0]
            diretor_id = diretores_por_titulo[tconst]
            diretor_nome = nomes_diretores.get(diretor_id, "Desconhecido")

            filme = Filme(tconst, titulo, ano, genero, diretor_nome)
            filmes.append(filme)

            if len(filmes) >= limite:
                break

    return filmes