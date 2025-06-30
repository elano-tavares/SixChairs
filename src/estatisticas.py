# src/estatisticas.py (MODIFICADO - Correção de Importação)

import struct
from collections import defaultdict, Counter
from src.filme import Filme # <-- MODIFICADO AQUI: Importa APENAS a classe Filme
# Removido: , TAMANHO_REGISTRO (não é mais importado diretamente)

# FORMATO_REGISTRO pode ser removido se Filme.FORMATO_REGISTRO for usado,
# mas para manter compatibilidade com o unpack local, deixamos por enquanto.
FORMATO_REGISTRO = "10s100si20s100s"

def gerar_estatisticas(caminho_bin="data/filmes.bin"):
    total = 0
    por_ano = defaultdict(int)
    por_genero = defaultdict(int)
    por_diretor = defaultdict(int)

    try:
        with open(caminho_bin, "rb") as f:
            while True:
                # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
                bytes_lidos = f.read(Filme.TAMANHO_REGISTRO) 
                if not bytes_lidos:
                    break

                id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack(FORMATO_REGISTRO, bytes_lidos)

                ano = int(ano)
                genero = genero_b.decode("utf-8").strip("\x00")
                diretor = diretor_b.decode("utf-8").strip("\x00")

                total += 1
                por_ano[ano] += 1
                por_diretor[diretor] += 1

                for g in genero.split(","):
                    por_genero[g.strip()] += 1
    except FileNotFoundError:
        print(f"⚠️ Arquivo binário não encontrado: {caminho_bin}. Nenhuma estatística gerada.")
        return
    except Exception as e:
        print(f"❌ Erro ao ler dados para estatísticas: {e}")
        return

    if total == 0:
        print("📊 Nenhum dado de filme encontrado para gerar estatísticas.")
        return

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
    if por_genero:
        for genero, qtd in Counter(por_genero).most_common(5):
            print(f" - {genero}: {qtd} filme(s)")
    else:
        print(" - N/A")

    print("\nTop 5 Diretores:")
    if por_diretor:
        for diretor, qtd in Counter(por_diretor).most_common(5):
            print(f" - {diretor}: {qtd} filme(s)")
    else:
        print(" - N/A")

    print("\nTop 5 Anos com mais filmes:")
    if por_ano:
        for ano, qtd in Counter(por_ano).most_common(5):
            print(f" - {ano}: {qtd} filme(s)")
    else:
        print(" - N/A")