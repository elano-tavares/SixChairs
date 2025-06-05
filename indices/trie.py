
import pickle
import struct
from src.filme import Filme

#constantes
TAMANHO_REGISTRO = 236

class TrieNode:
    def __init__(self):
        self.filhos = {}
        self.offsets = []  # lista de posições no arquivo binário
        self.fim_de_palavra = False


class Trie:
    def __init__(self):
        self.raiz = TrieNode()
        
    #------------------#
    #      Insere      #
    #------------------#

    def inserir(self, titulo: str, offset: int):
        no = self.raiz
        for char in titulo.lower():
            if char not in no.filhos:
                no.filhos[char] = TrieNode()
            no = no.filhos[char]
        no.fim_de_palavra = True
        no.offsets.append(offset)

    #------------------#
    #      Busca      #
    #------------------#

    def buscar(self, prefixo: str) -> list[int]:
        no = self.raiz
        for char in prefixo.lower():
            if char not in no.filhos:
                return []
            no = no.filhos[char]
        return self._coletar_offsets(no)


    #-------------------#
    #      OffSets      #
    #-------------------#
    def _coletar_offsets(self, no: TrieNode) -> list[int]:
        resultados = []
        if no.fim_de_palavra:
            resultados.extend(no.offsets)
        for filho in no.filhos.values():
            resultados.extend(self._coletar_offsets(filho))
        return resultados



 #-----------------------------#
 #      Salva Trie em bin      #
 #-----------------------------#

def salvar_trie_em_arquivo(trie: Trie, caminho: str):
    with open(caminho, "wb") as f:
        pickle.dump(trie, f)
    print(f"📁 TRIE salva em: {caminho}")

def carregar_trie_de_arquivo(caminho: str) -> Trie:
    with open(caminho, "rb") as f:
        return pickle.load(f)
    


 #-----------------------------#
 #      Busca Por Prefixo      #
 #-----------------------------#

def buscar_titulos_por_prefixo(trie: Trie, prefixo: str, bin_path: str = "data/filmes.bin") -> list[Filme]:
    offsets = trie.buscar(prefixo)
    filmes = []

    with open(bin_path, "rb") as f:
        for offset in offsets:
            f.seek(offset)
            bytes_lidos = f.read(TAMANHO_REGISTRO)
            if not bytes_lidos:
                continue
            id_b, titulo_b, ano, genero_b, diretor_b = struct.unpack("10s100si20s100s", bytes_lidos)
            filme = Filme(
                id_b.decode("utf-8").rstrip("\x00"),
                titulo_b.decode("utf-8").rstrip("\x00"),
                ano,
                genero_b.decode("utf-8").rstrip("\x00"),
                diretor_b.decode("utf-8").rstrip("\x00")
            )
            filmes.append(filme)
    return filmes


