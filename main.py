# main.py

from pathlib import Path
import sys

from src.extrator import (
    carregar_nome_diretores,
    carregar_diretores_por_titulo,
    extrair_filmes
)

from src.gravador import (
    salvar_filmes_binario, 
    ler_filmes_binario
)

def main():
    DATA_DIR = Path("data")
    NAMES_FILE = DATA_DIR / "name.basics.tsv"
    CREW_FILE = DATA_DIR / "title.crew.tsv"
    BASICS_FILE = DATA_DIR / "title.basics.tsv"

    REQUIRED_FILES = [NAMES_FILE, CREW_FILE, BASICS_FILE]

    # Verifica se todos os arquivos existem
    print("📦 Verificando arquivos na pasta /data...")
    arquivos_ok = True
    for file in REQUIRED_FILES:
        if not file.exists():
            print(f"❌ Arquivo ausente: {file}")
            arquivos_ok = False

    if not arquivos_ok:
        print("⚠️  Certifique-se de que todos os arquivos .tsv estejam disponíveis na pasta 'data/'")
        sys.exit(1)

    # Continua normalmente se os arquivos existirem
    print("✅ Todos os arquivos foram encontrados.\n")

    nomes_diretores = carregar_nome_diretores(NAMES_FILE)
    diretores_por_titulo = carregar_diretores_por_titulo(CREW_FILE)

    filmes = extrair_filmes(BASICS_FILE, diretores_por_titulo, nomes_diretores, limite=1000)

    # Após extrair os filmes, salvar
    salvar_filmes_binario(filmes)

    filmes_lidos = ler_filmes_binario()
    print("\n📂 Filmes lidos do arquivo binário:")
    for f in filmes_lidos[:5]:
        print(f)

if __name__ == "__main__":
    main()