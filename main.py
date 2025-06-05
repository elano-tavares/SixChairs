from pathlib import Path
from src.filme import Filme
import sys
import os
import struct

from src.extrator import (
    carregar_nome_diretores,
    carregar_diretores_por_titulo,
    extrair_filmes
)

from src.gravador import (
    TAMANHO_REGISTRO,
    salvar_filmes_binario_com_trie,
    salvar_filmes_binario, 
    ler_filmes_binario
)

from indices.trie import(
    Trie,
    salvar_trie_em_arquivo,
    carregar_trie_de_arquivo,
    buscar_titulos_por_prefixo    
)

def main():
    DATA_DIR = Path("data")
    BIN_FILE = DATA_DIR / "filmes.bin"

    # Se o arquivo binário já existe, lê diretamente
    if BIN_FILE.exists():
        print("📦 Arquivo binário encontrado. Carregando dados salvos...")
        filmes = ler_filmes_binario(BIN_FILE)
        
        trie = salvar_filmes_binario_com_trie(filmes, str(BIN_FILE))
        salvar_trie_em_arquivo(trie, "data/trie.idx")
        print("💾 Filmes extraídos, TRIE construída e ambos salvos com sucesso.")

        
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

        salvar_filmes_binario(filmes, str(BIN_FILE))
        print("💾 Filmes extraídos e salvos com sucesso.")

        filmes = ler_filmes_binario(BIN_FILE)
        trie = carregar_trie_de_arquivo("data/trie.idx")



    #------------------#
    #      TESTES      #
    #------------------#
    
    #Mostra os títulos encontrados na Trie com o prefixo 
    print("\n🔎 Teste: buscar por prefixo 'The '")
    resultados = buscar_titulos_por_prefixo(trie, "The ")
    print(f"🔍 {len(resultados)} filme(s) encontrados:")

    for f in resultados[:5]:
        print(f)

    #Mostra os primeiros filmes carregados
    print("\n🎬 Exemplos de filmes carregados:")
    for f in filmes[:15]:
        print(f)
   


if __name__ == "__main__":
    main()
