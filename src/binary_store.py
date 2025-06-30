# src/binary_store.py (MODIFICADO - Correção de Importação)

import csv
from typing import List
from src.filme import Filme # Importa apenas a classe Filme

# Caminho padrão do arquivo binário
ARQUIVO_BINARIO = "data/filmes.bin"

#-------------------------#
#  salvar_filmes_binario  #
#-------------------------#
def salvar_filmes_binario(filmes: List[Filme], caminho: str = ARQUIVO_BINARIO):
    """
    Salva uma lista de filmes no arquivo binário em modo heap (inserção serial).
    Utiliza o método Filme.to_bytes() para serializar cada objeto.
    """
    with open(caminho, "wb") as f:
        for filme in filmes:
            f.write(filme.to_bytes())
    print(f"✅ {len(filmes)} filmes salvos em: {caminho}")

#----------------------#
#  ler_filmes_binario  #
#----------------------#
def ler_filmes_binario(caminho: str = ARQUIVO_BINARIO) -> List[Filme]:
    """
    Lê todos os filmes do arquivo binário e retorna como lista de objetos Filme.
    Utiliza o método Filme.from_bytes() para desserializar cada registro.
    """
    filmes = []
    try:
        with open(caminho, "rb") as f:
            while True:
                # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
                bytes_lidos = f.read(Filme.TAMANHO_REGISTRO) 
                if not bytes_lidos:
                    break
                filme = Filme.from_bytes(bytes_lidos)
                filmes.append(filme)
    except FileNotFoundError:
        print(f"⚠️ Arquivo binário não encontrado: {caminho}")
    return filmes

#-------------------------------#
#  NOVA FUNÇÃO: ler_filme_por_offset  #
#-------------------------------#
def ler_filme_por_offset(offset: int, caminho: str = ARQUIVO_BINARIO) -> Filme | None:
    """
    Lê um único filme do arquivo binário em um dado offset.
    Retorna o objeto Filme ou None se o offset for inválido ou o arquivo não existir.
    """
    try:
        with open(caminho, "rb") as f:
            f.seek(offset)
            # Acessa TAMANHO_REGISTRO via Filme.TAMANHO_REGISTRO
            bytes_lidos = f.read(Filme.TAMANHO_REGISTRO)
            if not bytes_lidos:
                return None
            return Filme.from_bytes(bytes_lidos)
    except FileNotFoundError:
        print(f"⚠️ Arquivo binário não encontrado: {caminho}")
        return None
    except Exception as e:
        print(f"❌ Erro ao ler filme no offset {offset}: {e}")
        return None

#---------------------------------------#
#  Função: adicionar_filme_ao_binario   #
#---------------------------------------#
def adicionar_filme_ao_binario(filme: Filme, caminho: str = ARQUIVO_BINARIO) -> int:
    """
    Adiciona um único filme ao final do arquivo binário e retorna seu offset.
    Abre o arquivo em modo 'ab' (append binary).
    """
    with open(caminho, "ab") as f:
        offset = f.tell()
        f.write(filme.to_bytes())
    return offset