# main.py

from pathlib import Path
import sys

from src.extrator import (
    carregar_nome_diretores,
    carregar_diretores_por_titulo,
    extrair_filmes
)

from src.gravador import (
    salvar_filmes_binario_com_trie,
    salvar_filmes_binario, 
    ler_filmes_binario
)

from indices.trie import (
    salvar_trie_em_arquivo,
    carregar_trie_de_arquivo,
    buscar_titulos_por_prefixo    
)

from indices.hash import (
    construir_indice_hash_por_diretor, 
    salvar_hash_em_arquivo, 
    carregar_hash_de_arquivo,
    buscar_filmes_por_diretor
)


def main():
    DATA_DIR = Path("data")
    BIN_FILE = DATA_DIR / "filmes.bin"
    TRIE_FILE = DATA_DIR / "trie.idx"
    HASH_FILE = DATA_DIR / "hash.idx"

    # Se o binário já existe, carregamos os filmes
    if BIN_FILE.exists():
        print("📦 Arquivo binário encontrado. Carregando dados salvos...")
        filmes = ler_filmes_binario(BIN_FILE)

        # TRIE
        if TRIE_FILE.exists():
            trie = carregar_trie_de_arquivo(TRIE_FILE)
            print("✅ TRIE carregada de data/trie.idx")
        else:
            trie = salvar_filmes_binario_com_trie(filmes, str(BIN_FILE))
            salvar_trie_em_arquivo(trie, TRIE_FILE)
            print("📁 TRIE construída e salva em data/trie.idx")

        # HASH
        if HASH_FILE.exists():
            hash_diretor = carregar_hash_de_arquivo(HASH_FILE)
            print("✅ Índice hash por diretor carregado de data/hash.idx")
        else:
            hash_diretor = construir_indice_hash_por_diretor(filmes)
            salvar_hash_em_arquivo(hash_diretor, HASH_FILE)
            print("📁 Índice hash por diretor construído e salvo em data/hash.idx")

    else:
        print("📤 Arquivo binário não encontrado. Preparando extração dos arquivos TSV...")

        # Verifica se os arquivos .tsv existem
        NAMES_FILE = DATA_DIR / "name.basics.tsv"
        CREW_FILE = DATA_DIR / "title.crew.tsv"
        BASICS_FILE = DATA_DIR / "title.basics.tsv"

        REQUIRED_FILES = [NAMES_FILE, CREW_FILE, BASICS_FILE]

        print("📁 Verificando arquivos na pasta /data...")
        arquivos_ok = True
        for file in REQUIRED_FILES:
            if not file.exists():
                print(f"❌ Arquivo ausente: {file}")
                arquivos_ok = False

        if not arquivos_ok:
            print("⚠️  Certifique-se de que todos os arquivos .tsv estejam disponíveis na pasta 'data/'")
            sys.exit(1)

        print("✅ Todos os arquivos foram encontrados. Extraindo e salvando...")

        nomes_diretores = carregar_nome_diretores(NAMES_FILE)
        diretores_por_titulo = carregar_diretores_por_titulo(CREW_FILE)
        filmes = extrair_filmes(BASICS_FILE, diretores_por_titulo, nomes_diretores, limite=1000)

        # Salva binário, TRIE e hash
        trie = salvar_filmes_binario_com_trie(filmes, str(BIN_FILE))
        salvar_trie_em_arquivo(trie, TRIE_FILE)

        hash_diretor = construir_indice_hash_por_diretor(filmes)
        salvar_hash_em_arquivo(hash_diretor, HASH_FILE)

        print("💾 Filmes, TRIE e índice hash salvos com sucesso.")

    #------------------#
    #      TESTES      #
    #------------------#
    print("\n🔍 Teste: buscar por diretor 'Mario Caserini'")
    filmes_encontrados = buscar_filmes_por_diretor("Mario Caserini", hash_diretor)
    for filme in filmes_encontrados[:15]:
        print(filme)
    
    print("\n🔎 Teste: buscar por prefixo 'Hamlet'")
    resultados = buscar_titulos_por_prefixo(trie, "Hamlet")
    print(f"🔍 {len(resultados)} filme(s) encontrados:")
    for f in resultados[:15]:
        print(f)

    print("\n🎬 Exemplos de filmes carregados:")
    for f in filmes[:15]:
        print(f)


# Chama a função principal
if __name__ == "__main__":
    main()