# src/index_builder.py (NOVO ARQUIVO)

import csv # Para a função importar_lote_e_atualizar_indices
from collections import defaultdict # Para inicializar hash_diretor
from typing import List, Dict

from src.filme import Filme # Importa a classe Filme
from src.binary_store import adicionar_filme_ao_binario, ler_filmes_binario # Funções para interagir com o binário

# Importa as classes e funções relevantes dos índices
from indices.trie import Trie, salvar_trie_em_arquivo, carregar_trie_de_arquivo
from indices.hash import salvar_hash_em_arquivo, carregar_hash_de_arquivo # construir_indice_hash_por_diretor não é necessário aqui, pois a lógica de construção é in-line
from indices.arvore import BTree # A classe BTree para instanciar


class IndexBuilder:
    def __init__(self, bin_path: str = "data/filmes.bin"):
        """
        Inicializa o IndexBuilder e as instâncias dos índices.
        bin_path: Caminho para o arquivo binário principal de filmes.
        """
        self.bin_path = bin_path
        self.trie = Trie()
        self.hash_diretor = defaultdict(list) # Inicializa como defaultdict para facilitar append
        self.indice_ano = BTree(t=3) # Instância da sua B-Tree para ano (t=3 é um valor comum)
        self.indice_id = BTree(t=3)  # Instância da sua B-Tree para ID (t=3 é um valor comum)

    def construir_todos_indices(self, filmes: List[Filme]):
        """
        Constrói todos os índices do zero a partir de uma lista completa de filmes.
        Isso é usado na inicialização do sistema quando o binário é criado.
        """
        print("🛠️ Construindo todos os índices...")
        
        # Reinicia os índices para garantir uma construção limpa
        self.trie = Trie()
        self.hash_diretor = defaultdict(list)
        self.indice_ano = BTree(t=3)
        self.indice_id = BTree(t=3)

        for i, filme in enumerate(filmes):
            # O offset é calculado com base na posição serial no arquivo binário
            offset = i * Filme.TAMANHO_REGISTRO 
            
            self.trie.inserir(filme.titulo, offset)
            self.hash_diretor[filme.diretor].append(offset)
            self.indice_ano.inserir(filme.ano, offset)
            self.indice_id.inserir(filme.id, offset)
        print("✅ Índices construídos.")

    def atualizar_indices_com_novo_filme(self, filme: Filme):
        """
        Adiciona um único filme ao arquivo binário e atualiza todos os índices
        com o offset correspondente.
        """
        offset = adicionar_filme_ao_binario(filme, self.bin_path)
        self.trie.inserir(filme.titulo, offset)
        self.hash_diretor.setdefault(filme.diretor, []).append(offset) # Usa setdefault para garantir a lista
        self.indice_ano.inserir(filme.ano, offset)
        self.indice_id.inserir(filme.id, offset)
        return offset

    def importar_lote_e_atualizar_indices(self, caminho_tsv: str, extrator_funcoes: dict, limite: int = 1000) -> int:
        """
        Extrai filmes de um arquivo TSV (similar ao extrair_filmes, mas incrementalmente)
        e os adiciona ao binário e atualiza todos os índices.
        extrator_funcoes: Dicionário contendo as funções de extração e caminhos de arquivos TSV.
                          Ex: {'carregar_nomes': func, 'carregar_diretores': func, 'basics_file': path, ...}
        """
        adicionados = 0
        print(f"🔄 Importando até {limite} filmes do TSV e atualizando índices...")

        # Carregar mapeamentos necessários para extração (se o TSV de lote não for autocontido)
        # Assumindo que você passa estas funções e caminhos do extrator para cá.
        # Isso evita duplicação da lógica de extração complexa.
        nomes_diretores = extrator_funcoes['carregar_nomes'](extrator_funcoes['nomes_file'])
        diretores_por_titulo = extrator_funcoes['carregar_diretores'](extrator_funcoes['crew_file'])
        
        try:
            with open(caminho_tsv, encoding='utf-8-sig') as f_tsv:
                leitor = csv.DictReader(f_tsv, delimiter='\t')
                # Assumindo que o TSV importado é title.basics.tsv ou similar.
                # Você pode precisar ajustar a leitura das colunas se o TSV de lote for diferente.
                
                for linha in leitor:
                    if adicionados >= limite:
                        break

                    # Filtros e parse de dados similares ao extrator.py
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
                    
                    # Adiciona ao binário e atualiza todos os índices
                    self.atualizar_indices_com_novo_filme(filme)
                    adicionados += 1
                    
        except FileNotFoundError:
            print(f"❌ Arquivo TSV de lote não encontrado: {caminho_tsv}")
            return 0
        except Exception as e:
            print(f"❌ Erro ao processar arquivo TSV de lote: {e}")
            return 0
                
        print(f"✅ {adicionados} filmes importados e índices atualizados.")
        return adicionados
    
    def salvar_todos_indices(self):
        """Salva todas as instâncias dos índices em seus respectivos arquivos."""
        print("💾 Salvando índices...")
        salvar_trie_em_arquivo(self.trie, "data/trie.idx")
        salvar_hash_em_arquivo(self.hash_diretor, "data/hash.idx")
        self.indice_ano.salvar_para_arquivo("data/b_ano.idx") # Chama o método da instância BTree
        self.indice_id.salvar_para_arquivo("data/b_id.idx")   # Chama o método da instância BTree
        print("✅ Todos os índices foram salvos com sucesso.")

    def carregar_todos_indices(self) -> bool:
        """
        Tenta carregar todas as instâncias dos índices de seus arquivos.
        Retorna True se todos os índices foram carregados com sucesso, False caso contrário.
        """
        print("🔄 Carregando índices existentes...")
        try:
            self.trie = carregar_trie_de_arquivo("data/trie.idx")
            self.hash_diretor = carregar_hash_de_arquivo("data/hash.idx")
            self.indice_ano = BTree.carregar_de_arquivo("data/b_ano.idx") # Chama o método estático da classe BTree
            self.indice_id = BTree.carregar_de_arquivo("data/b_id.idx")   # Chama o método estático da classe BTree
            print("✅ Índices carregados.")
            return True
        except FileNotFoundError:
            print("⚠️ Um ou mais arquivos de índice não encontrados. Será necessário reconstruir.")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar índices: {e}. Será necessário reconstruir.")
            return False