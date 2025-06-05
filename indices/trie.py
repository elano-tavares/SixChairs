
import pickle

class TrieNode:
    def __init__(self):
        self.filhos = {}
        self.offsets = []  # lista de posições no arquivo binário
        self.fim_de_palavra = False


class Trie:
    def __init__(self):
        self.raiz = TrieNode()

    def inserir(self, titulo: str, offset: int):
        no = self.raiz
        for char in titulo.lower():
            if char not in no.filhos:
                no.filhos[char] = TrieNode()
            no = no.filhos[char]
        no.fim_de_palavra = True
        no.offsets.append(offset)

    def buscar(self, prefixo: str) -> list[int]:
        no = self.raiz
        for char in prefixo.lower():
            if char not in no.filhos:
                return []
            no = no.filhos[char]
        return self._coletar_offsets(no)

    def _coletar_offsets(self, no: TrieNode) -> list[int]:
        resultados = []
        if no.fim_de_palavra:
            resultados.extend(no.offsets)
        for filho in no.filhos.values():
            resultados.extend(self._coletar_offsets(filho))
        return resultados


def salvar_trie_em_arquivo(trie: Trie, caminho: str):
    with open(caminho, "wb") as f:
        pickle.dump(trie, f)
    print(f"📁 TRIE salva em: {caminho}")

def carregar_trie_de_arquivo(caminho: str) -> Trie:
    with open(caminho, "rb") as f:
        return pickle.load(f)
