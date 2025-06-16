# estatisticas.py

import struct
from collections import defaultdict, Counter
from src.filme import Filme
from src.gravador import TAMANHO_REGISTRO

FORMATO_REGISTRO = "10s100si20s100s"

def gerar_estatisticas(caminho_bin="data/filmes.bin"):
    total = 0
    por_ano = defaultdict(int)
    por_genero = defaultdict(int)
    por_diretor = defaultdict(int)

    with open(caminho_bin, "rb") as f:
        while True:
            dados = f.read(TAMANHO_REGISTRO)
            if not dados:
                break

            id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack(FORMATO_REGISTRO, dados)

            ano = int(ano)
            genero = genero_b.decode("utf-8").strip("\x00")
            diretor = diretor_b.decode("utf-8").strip("\x00")

            total += 1
            por_ano[ano] += 1
            por_diretor[diretor] += 1

            for g in genero.split(","):
                por_genero[g.strip()] += 1

    mais_ano = max(por_ano.items(), key=lambda x: x[1]) if por_ano else (None, 0)
    mais_genero = max(por_genero.items(), key=lambda x: x[1]) if por_genero else (None, 0)
    mais_diretor = max(por_diretor.items(), key=lambda x: x[1]) if por_diretor else (None, 0)

    print("\n📊 Estatísticas dos Filmes")
    print("-------------------------")
    print(f"🎞️ Total de filmes: {total}")
    print(f"📅 Ano com mais filmes: {mais_ano[0]} ({mais_ano[1]})")
    print(f"🎭 Gênero mais comum: {mais_genero[0]} ({mais_genero[1]})")
    print(f"🎬 Diretor com mais filmes: {mais_diretor[0]} ({mais_diretor[1]})")

    print("\nTop 5 Gêneros:")
    for genero, qtd in Counter(por_genero).most_common(5):
        print(f" - {genero}: {qtd} filme(s)")

    print("\nTop 5 Diretores:")
    for diretor, qtd in Counter(por_diretor).most_common(5):
        print(f" - {diretor}: {qtd} filme(s)")

    print("\nTop 5 Anos com mais filmes:")
    for ano, qtd in Counter(por_ano).most_common(5):
        print(f" - {ano}: {qtd} filme(s)")
