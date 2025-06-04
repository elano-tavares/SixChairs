import csv
from typing import List, Dict

class Filme:
    def __init__(self, id: str, titulo: str, ano: int, genero: str, diretor: str):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.diretor = diretor

    def __repr__(self):
        return f"[{self.id}] {self.titulo} ({self.ano}) - {self.genero} | Dir: {self.diretor}"


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


def main():
    NAMES_FILE = "name.basics.tsv"
    CREW_FILE = "title.crew.tsv"
    BASICS_FILE = "title.basics.tsv"

    nomes_diretores = carregar_nome_diretores(NAMES_FILE)
    diretores_por_titulo = carregar_diretores_por_titulo(CREW_FILE)
    filmes = extrair_filmes(BASICS_FILE, diretores_por_titulo, nomes_diretores, limite=1000)

    print("\nExemplos de filmes extraídos:")
    for f in filmes[:10]:
        print(f)

if __name__ == "__main__":
    main()
