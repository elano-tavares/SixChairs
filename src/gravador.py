# gravador.py

import csv
import struct
from typing import List
from src.filme import Filme
from indices.trie import Trie

# Caminho padrão do arquivo binário
ARQUIVO_BINARIO = "data/filmes.bin"

# Definição da estrutura binária: id(10s), título(100s), ano(i), gênero(20s), diretor(100s)
FORMATO_REGISTRO = "10s100si20s100s"
TAMANHO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)

#-------------------------#
#  Salvar_filmes_binario  #
#-------------------------#
def salvar_filmes_binario(filmes: List[Filme], caminho: str = ARQUIVO_BINARIO):
    """
    Salva uma lista de filmes no arquivo binário em modo heap (inserção serial).
    """
    with open(caminho, "wb") as f:
        for filme in filmes:
            registro = struct.pack(
                FORMATO_REGISTRO,
                filme.id.encode("utf-8")[:10].ljust(10, b"\x00"),
                filme.titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
                filme.ano,
                filme.genero.encode("utf-8")[:20].ljust(20, b"\x00"),
                filme.diretor.encode("utf-8")[:100].ljust(100, b"\x00"),
            )
            f.write(registro)
    print(f"✅ {len(filmes)} filmes salvos em: {caminho}")

#----------------------#
#  Ler_filmes_binario  #
#----------------------#
def ler_filmes_binario(caminho: str = ARQUIVO_BINARIO) -> List[Filme]:
    """
    Lê todos os filmes do arquivo binário e retorna como lista de objetos Filme.
    """
    filmes = []
    try:
        with open(caminho, "rb") as f:
            while True:
                bytes_lidos = f.read(TAMANHO_REGISTRO)
                if not bytes_lidos:
                    break
                id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack(FORMATO_REGISTRO, bytes_lidos)
                filme = Filme(
                    id_b.decode("utf-8").rstrip("\x00"),
                    titulo_b.decode("utf-8").rstrip("\x00"),
                    ano,
                    genero_b.decode("utf-8").rstrip("\x00"),
                    diretor_b.decode("utf-8").rstrip("\x00")
                )
                filmes.append(filme)
    except FileNotFoundError:
        print(f"⚠️ Arquivo binário não encontrado: {caminho}")
    return filmes

#---------------------------#
#  Salvar_filmes__bin_trie  #
#---------------------------#
def salvar_filmes_binario_com_trie(filmes: List[Filme], caminho: str = ARQUIVO_BINARIO) -> Trie:
    trie = Trie()
    with open(caminho, "wb") as f:
        for i, filme in enumerate(filmes):
            offset = i * TAMANHO_REGISTRO
            registro = struct.pack(
                FORMATO_REGISTRO,
                filme.id.encode("utf-8")[:10].ljust(10, b"\x00"),
                filme.titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
                filme.ano,
                filme.genero.encode("utf-8")[:20].ljust(20, b"\x00"),
                filme.diretor.encode("utf-8")[:100].ljust(100, b"\x00"),
            )
            f.write(registro)
            trie.inserir(filme.titulo, offset)
    print(f"✅ {len(filmes)} filmes salvos no binário e TRIE construída.")
    return trie

#---------------------------#
#    Importar_novo_lote     #
#---------------------------#
def importar_filmes_em_lote(caminho_tsv: str,
                            caminho_bin: str,
                            trie=None,
                            hash_diretor=None,
                            indice_ano=None,
                            indice_id=None,
                            limite: int = 1000) -> int:
    adicionados = 0

    with open(caminho_tsv, encoding="utf-8") as f_tsv, open(caminho_bin, "ab") as f_bin:
        leitor = csv.reader(f_tsv, delimiter="\t")
        for linha in leitor:
            if len(linha) < 5:
                continue
            idf, titulo, ano, genero, diretor = linha
            try:
                ano = int(ano)
            except:
                continue

            dados = struct.pack(
                FORMATO_REGISTRO,
                idf.encode("utf-8")[:10].ljust(10, b"\x00"),
                titulo.encode("utf-8")[:100].ljust(100, b"\x00"),
                ano,
                genero.encode("utf-8")[:20].ljust(20, b"\x00"),
                diretor.encode("utf-8")[:100].ljust(100, b"\x00")
            )

            pos = f_bin.tell()
            f_bin.write(dados)

            if trie:
                trie.inserir(titulo.lower(), pos)
            if hash_diretor:
                hash_diretor.setdefault(diretor, []).append(pos)
            if indice_ano:
                indice_ano.setdefault(ano, []).append(pos)
            if indice_id:
                indice_id[idf] = pos

            adicionados += 1
            if adicionados >= limite:
                break

    return adicionados