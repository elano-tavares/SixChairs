# main.py

from pathlib import Path
import sys

# Importa funções do extrator que são usadas para a extração inicial dos TSVs
from src.extrator import (
    carregar_nome_diretores,
    carregar_diretores_por_titulo,
    extrair_filmes
)

# Importa funções do binary_store para salvar o binário inicial
from src.binary_store import salvar_filmes_binario, ler_filmes_binario # ler_filmes_binario pode ser útil aqui

# Importa o novo IndexBuilder, que gerencia todos os índices
from src.index_builder import IndexBuilder

# Importa a nova interface de linha de comando
from src.cli import menu_principal

def main():
    DATA_DIR = Path("data")
    BIN_FILE = DATA_DIR / "filmes.bin"
    
    # Instancia o IndexBuilder, passando o caminho do arquivo binário principal
    index_builder = IndexBuilder(str(BIN_FILE))

    # Tenta carregar os índices existentes e o arquivo binário
    # Se o BIN_FILE não existe OU os índices não puderam ser carregados, reconstruir
    if not BIN_FILE.exists() or not index_builder.carregar_todos_indices():
        print("📤 Arquivo binário ou um ou mais índices não encontrados/válidos. Preparando extração dos arquivos TSV...")

        # Verifica se os arquivos .tsv necessários existem na pasta data/
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
            sys.exit(1) # Sai do programa se os arquivos TSV não estiverem presentes

        print("✅ Todos os arquivos foram encontrados. Extraindo e salvando filmes...")

        # Carrega os dados brutos e extrai os objetos Filme
        nomes_diretores = carregar_nome_diretores(str(NAMES_FILE))
        diretores_por_titulo = carregar_diretores_por_titulo(str(CREW_FILE))
        filmes_extraidos = extrair_filmes(str(BASICS_FILE), diretores_por_titulo, nomes_diretores, limite=1000)

        # Salva a lista de filmes extraídos no arquivo binário
        salvar_filmes_binario(filmes_extraidos, str(BIN_FILE))
        print(f"✅ {len(filmes_extraidos)} filmes salvos inicialmente em: {BIN_FILE}")

        # Constrói todos os índices a partir dos filmes recém-salvos
        index_builder.construir_todos_indices(filmes_extraidos)
        
        # Salva os índices recém-construídos para persistência
        index_builder.salvar_todos_indices()
        print("💾 Filmes e todos os índices (TRIE, Hash, B-Tree) salvos com sucesso.")

    else:
        print("✅ Dados e índices carregados com sucesso de arquivos existentes.")

    # Inicia a interface de linha de comando, passando o index_builder
    menu_principal(index_builder, str(BIN_FILE))

if __name__ == "__main__":
    main()
