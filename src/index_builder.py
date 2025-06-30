# src/index_builder.py

import csv
from collections import defaultdict
from typing import List, Dict

from src.filme import Filme
from src.binary_store import adicionar_filme_ao_binario, ler_filmes_binario

from indices.trie import Trie, salvar_trie_em_arquivo, carregar_trie_de_arquivo
from indices.hash import salvar_hash_em_arquivo, carregar_hash_de_arquivo
from indices.arvore import BTree


class IndexBuilder:
    def __init__(self, bin_path: str = "data/filmes.bin"):
        """
        Inicializa o IndexBuilder e as instâncias dos índices.
        bin_path: Caminho para o arquivo binário principal de filmes.
        """
        self.bin_path = bin_path
        self.trie = Trie()
        self.hash_diretor = defaultdict(list)
        self.indice_ano = BTree(t=3)
        self.indice_id = BTree(t=3)

    def construir_todos_indices(self, filmes: List[Filme]):
        """
        Constrói todos os índices do zero a partir de uma lista completa de filmes.
        """
        print("🛠️ Construindo todos os índices...")
        
        self.trie = Trie()
        self.hash_diretor = defaultdict(list)
        self.indice_ano = BTree(t=3)
        self.indice_id = BTree(t=3)

        for i, filme in enumerate(filmes):
            offset = i * Filme.TAMANHO_REGISTRO 
            
            self.trie.inserir(filme.titulo, offset)
            self.hash_diretor[filme.diretor].append(offset)
            self.indice_ano.inserir(filme.ano, offset)
            self.indice_id.inserir(filme.id, offset)
        print("✅ Índices construídos.")

    def atualizar_indices_com_novo_filme(self, filme: Filme):
        """
        Adiciona um único filme ao arquivo binário e atualiza todos os índices.
        """
        offset = adicionar_filme_ao_binario(filme, self.bin_path)
        self.trie.inserir(filme.titulo, offset)
        self.hash_diretor.setdefault(filme.diretor, []).append(offset)
        self.indice_ano.inserir(filme.ano, offset)
        self.indice_id.inserir(filme.id, offset)
        return offset

    ### NOVO MÉTODO ADICIONADO ###
    def importar_lote_simplificado(self, caminho_tsv: str) -> int:
        """
        Importa filmes de um arquivo TSV com formato simplificado:
        id\ttitulo\tano\tgenero\tdiretor
        E os adiciona ao binário, atualizando todos os índices.
        """
        adicionados = 0
        print(f"🔄 Importando filmes do TSV simplificado: {caminho_tsv}")
        
        try:
            with open(caminho_tsv, mode='r', encoding='utf-8') as f_tsv:
                leitor = csv.reader(f_tsv, delimiter='\t')
                for linha in leitor:
                    # Pula linhas malformadas ou vazias
                    if len(linha) != 5:
                        continue
                    
                    id_filme, titulo, ano_str, genero, diretor = linha

                    try:
                        ano = int(ano_str)
                    except ValueError:
                        print(f"⚠️ Linha ignorada: ano inválido ('{ano_str}') para o filme '{titulo}'")
                        continue

                    # Cria o objeto Filme
                    filme = Filme(id_filme, titulo, ano, genero, diretor)
                    
                    # Adiciona ao binário e atualiza todos os índices
                    self.atualizar_indices_com_novo_filme(filme)
                    adicionados += 1
                    
        except FileNotFoundError:
            print(f"❌ Arquivo TSV não encontrado: {caminho_tsv}")
            return 0
        except Exception as e:
            print(f"❌ Erro ao processar o arquivo TSV: {e}")
            return 0
                
        print(f"✅ {adicionados} filmes importados e índices atualizados.")
        return adicionados

    def salvar_todos_indices(self):
        """Salva todas as instâncias dos índices em seus respectivos arquivos."""
        print("💾 Salvando índices...")
        salvar_trie_em_arquivo(self.trie, "data/trie.idx")
        salvar_hash_em_arquivo(self.hash_diretor, "data/hash.idx")
        self.indice_ano.salvar_para_arquivo("data/b_ano.idx")
        self.indice_id.salvar_para_arquivo("data/b_id.idx")
        print("✅ Todos os índices foram salvos com sucesso.")

    def carregar_todos_indices(self) -> bool:
        """
        Tenta carregar todas as instâncias dos índices de seus arquivos.
        """
        print("🔄 Carregando índices existentes...")
        try:
            self.trie = carregar_trie_de_arquivo("data/trie.idx")
            self.hash_diretor = carregar_hash_de_arquivo("data/hash.idx")
            self.indice_ano = BTree.carregar_de_arquivo("data/b_ano.idx")
            self.indice_id = BTree.carregar_de_arquivo("data/b_id.idx")
            print("✅ Índices carregados.")
            return True
        except FileNotFoundError:
            print("⚠️ Um ou mais arquivos de índice não encontrados. Será necessário reconstruir.")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar índices: {e}. Será necessário reconstruir.")
            return False