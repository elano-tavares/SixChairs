# indices/arvore.py

import pickle
from src.filme import Filme 

class BTreeNode:
    def __init__(self, t, is_leaf):
        """
        Inicializa um nó da Árvore B.
        t: Grau mínimo da árvore (define o número mínimo e máximo de chaves).
        is_leaf: Booleano, True se for um nó folha.
        """
        self.t = t  # Grau mínimo
        self.keys = []  # Lista de tuplas (chave, offset). Mantida ordenada.
        self.children = [] # Lista de BTreeNode (filhos do nó)
        self.is_leaf = is_leaf

    def is_full(self) -> bool:
        """Verifica se o nó está cheio."""
        return len(self.keys) == (2 * self.t - 1)

    def __repr__(self):
        """Representação para depuração do nó."""
        return f"BTreeNode(keys={[k[0] for k in self.keys]}, is_leaf={self.is_leaf})"

class BTree:
    def __init__(self, t: int = 3):
        """
        Inicializa uma Árvore B.
        t: Grau mínimo da árvore.
        """
        self.t = t 
        self.root = BTreeNode(t, True) # A raiz inicial é uma folha

    def inserir(self, key, offset: int):
        """
        Insere uma nova chave e seu offset associado na Árvore B.
        """
        root = self.root
        if root.is_full():
            # Se a raiz está cheia, a árvore cresce em altura
            s = BTreeNode(self.t, False) # Nova raiz não é folha
            s.children.append(root) # A antiga raiz se torna o primeiro filho da nova raiz
            self._split_child(s, 0, root) # Divide a antiga raiz
            self.root = s # Atualiza a raiz da árvore
            self._insert_non_full(s, key, offset) # Insere na nova estrutura
        else:
            self._insert_non_full(root, key, offset)

    def _insert_non_full(self, node: BTreeNode, key, offset: int):
        """
        Método auxiliar para inserir uma chave em um nó que não está cheio.
        """
        i = len(node.keys) - 1 # Começa do final para encontrar a posição de inserção
        
        if node.is_leaf:
            # Encontra a posição para inserir e insere a tupla (chave, offset)
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            node.keys.insert(i + 1, (key, offset)) # Insere a tupla (chave, offset)
        else:
            # Encontra o filho correto para descer
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            
            # Se o filho para onde vamos descer está cheio, o dividimos
            if node.children[i].is_full():
                self._split_child(node, i, node.children[i])
                # Após a divisão, a chave promovida pode alterar o caminho.
                # Se a chave a ser inserida for maior que a chave que subiu,
                # ela deve ir para o filho à direita da chave promovida.
                if key > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], key, offset) # Insere recursivamente no filho

    def _split_child(self, parent_node: BTreeNode, i: int, full_child: BTreeNode):
        """
        Divide um nó filho cheio em dois, promovendo uma chave para o pai.
        parent_node: O nó pai do full_child.
        i: Índice do full_child no array de filhos do parent_node.
        full_child: O nó filho que está cheio e será dividido.
        """
        new_child = BTreeNode(self.t, full_child.is_leaf)
        
        # A chave mediana do full_child é promovida para o parent_node
        # Pega a tupla (chave, offset) completa
        promoted_key_pair = full_child.keys[self.t - 1] 
        
        # Divide as chaves e filhos
        # O new_child pega a parte direita (da mediana em diante)
        new_child.keys = full_child.keys[self.t:]
        # O full_child original mantém a parte esquerda (antes da mediana)
        full_child.keys = full_child.keys[:self.t - 1] # Remove a chave promovida e o restante

        if not full_child.is_leaf:
            new_child.children = full_child.children[self.t:]
            full_child.children = full_child.children[:self.t]

        # Insere o novo filho ao lado do filho original no nó pai
        parent_node.children.insert(i + 1, new_child)
        # Insere a chave promovida no nó pai na posição correta
        parent_node.keys.insert(i, promoted_key_pair)

    def buscar(self, key) -> list[int]:
        """
        Busca uma chave na Árvore B e retorna uma lista de offsets associados.
        Como anos podem não ser únicos, retorna todos os offsets para a chave.
        """
        return self._buscar_recursivo(self.root, key)

    def _buscar_recursivo(self, node: BTreeNode, key) -> list[int]:
        """
        Método auxiliar recursivo para buscar uma chave.
        """
        i = 0
        # Encontra a primeira chave maior ou igual à chave buscada
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        
        offsets_encontrados = []
        
        # Verifica se a chave foi encontrada neste nó
        if i < len(node.keys) and key == node.keys[i][0]:
            # Coleta todos os offsets para essa chave neste nó (útil para chaves duplicadas como anos)
            offsets_encontrados.extend([k[1] for k in node.keys if k[0] == key])
            
            # Se não for uma folha, continua buscando nos filhos, pois a chave pode estar em múltiplos locais
            # ou ser um separador para um intervalo de chaves que contém a chave buscada.
            if not node.is_leaf:
                # Busca no filho à esquerda da chave encontrada
                offsets_encontrados.extend(self._buscar_recursivo(node.children[i], key))
                # Busca no filho à direita da chave encontrada (se houver, e se a chave for a última no nó)
                if i + 1 < len(node.children):
                    offsets_encontrados.extend(self._buscar_recursivo(node.children[i + 1], key))
            
            return offsets_encontrados
        
        # Se não encontrou no nó atual e é folha, a chave não existe na árvore
        elif node.is_leaf:
            return []
        
        # Se não encontrou no nó atual e não é folha, desce para o filho apropriado
        else:
            return self._buscar_recursivo(node.children[i], key)

    def buscar_intervalo(self, min_key, max_key) -> list[int]:
        """
        Busca todas as chaves dentro de um intervalo [min_key, max_key] e retorna seus offsets.
        """
        offsets = []
        self._coletar_offsets_em_intervalo(self.root, min_key, max_key, offsets)
        return list(set(offsets)) # Remove duplicatas, se houver, pois uma chave pode aparecer em múltiplos caminhos na busca

    def _coletar_offsets_em_intervalo(self, node: BTreeNode, min_key, max_key, offsets_list: list[int]):
        """
        Método auxiliar recursivo para coletar offsets dentro de um intervalo.
        """
        i = 0
        # Encontra o primeiro filho ou chave que pode estar no intervalo
        while i < len(node.keys) and min_key > node.keys[i][0]:
            i += 1
        
        # Percorre os filhos e chaves
        
        # Visita o filho antes da primeira chave no intervalo (se houver)
        if not node.is_leaf and i < len(node.children):
            self._coletar_offsets_em_intervalo(node.children[i], min_key, max_key, offsets_list)

        # Percorre as chaves do nó atual
        current_key_idx = i
        while current_key_idx < len(node.keys):
            key_val, offset_val = node.keys[current_key_idx]
            if min_key <= key_val <= max_key:
                offsets_list.append(offset_val)
            elif key_val > max_key: # Se já passou do max_key na folha, podemos parar de verificar chaves neste nó
                break
            
            # Se não é folha, visita o filho à direita da chave atual
            if not node.is_leaf and current_key_idx + 1 < len(node.children):
                self._coletar_offsets_em_intervalo(node.children[current_key_idx + 1], min_key, max_key, offsets_list)
            
            current_key_idx += 1
            
        # Garante que o último filho (se houver e não foi visitado) seja visitado
        if not node.is_leaf and current_key_idx < len(node.children): # Se ainda restam filhos para visitar
            self._coletar_offsets_em_intervalo(node.children[current_key_idx], min_key, max_key, offsets_list)


    def salvar_para_arquivo(self, caminho: str):
        """Salva a B-Tree completa em um arquivo usando pickle."""
        with open(caminho, "wb") as f:
            pickle.dump(self, f)
        print(f"📁 B-Tree salva em: {caminho}")

    @staticmethod
    def carregar_de_arquivo(caminho: str):
        """Carrega a B-Tree de um arquivo usando pickle."""
        with open(caminho, "rb") as f:
            return pickle.load(f)

# --- Funções auxiliares que usarão a BTree (serão importadas por outros módulos) ---

# Construtor do índice de ano
def construir_indice_ano_b_tree(filmes: list[Filme], t: int = 3) -> BTree:
    """
    Constrói um índice B-Tree para o ano dos filmes.
    t: Grau mínimo da B-Tree.
    """
    b_tree = BTree(t)
    for i, filme in enumerate(filmes):
        # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
        posicao = i * Filme.TAMANHO_REGISTRO 
        b_tree.inserir(filme.ano, posicao)
    return b_tree

# Construtor do índice de ID
def construir_indice_id_b_tree(filmes: list[Filme], t: int = 3) -> BTree:
    """
    Constrói um índice B-Tree para o ID dos filmes.
    t: Grau mínimo da B-Tree.
    """
    b_tree = BTree(t)
    for i, filme in enumerate(filmes):
        # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
        posicao = i * Filme.TAMANHO_REGISTRO
        b_tree.inserir(filme.id, posicao)
    return b_tree

# Funções de busca que usam a BTree e o binary_store
from src.binary_store import ler_filme_por_offset # Importa para ler filmes

def buscar_filmes_por_ano_b_tree(b_tree: BTree, ano: int | tuple, caminho_bin: str = "data/filmes.bin") -> list[Filme]:
    """
    Busca filmes por ano(s) usando a B-Tree.
    Suporta busca por ano único ou intervalo de anos (tupla).
    Retorna uma lista de objetos Filme.
    """
    offsets = []
    if isinstance(ano, tuple):
        offsets = b_tree.buscar_intervalo(ano[0], ano[1])
    else:
        offsets = b_tree.buscar(ano)
    
    filmes = []
    for offset in offsets:
        filme = ler_filme_por_offset(offset, caminho_bin)
        if filme: # Adiciona apenas se o filme foi lido com sucesso
            filmes.append(filme)
    return filmes

def buscar_filme_por_id_b_tree(b_tree_id: BTree, filme_id: str, caminho_bin: str = "data/filmes.bin") -> Filme | None:
    """
    Busca um único filme por ID usando a B-Tree.
    Retorna o objeto Filme ou None.
    """
    offsets = b_tree_id.buscar(filme_id)
    if not offsets:
        return None
    
    # Para ID, esperamos apenas um offset único. Pega o primeiro válido.
    return ler_filme_por_offset(offsets[0], caminho_bin)
