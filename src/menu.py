from src.buscas import buscar_filmes_com_filtros
from src.gravador import importar_filmes_em_lote
from indices.trie import salvar_trie_em_arquivo
from indices.hash import salvar_hash_em_arquivo
from indices.arvore import salvar_indice_em_arquivo

def menu_busca_interativa(trie, hash_diretor, indice_ano, indice_id, caminho_bin="data/filmes.bin"):
    print("\n📚 Bem-vindo ao sistema de busca SixChairs!")
    mostrar_menu = True

    while True:
        if mostrar_menu:
            print("\n--- MENU DE BUSCA ---")
            print("1. Buscar por título (prefixo)")
            print("2. Buscar por diretor")
            print("3. Buscar por ano")
            print("4. Buscar por ID")
            print("5. Buscar por gênero")
            print("6. Combinação de filtros")
            print("7. Importar novo lote de filmes (TSV)")
            print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("👋 Saindo do sistema. Até logo!")
            break

        prefixo = diretor = id_filme = None
        ano = None
        genero = None
        resultados = []

        if opcao == "1":
            prefixo = input("Digite o prefixo do título: ")
        elif opcao == "2":
            diretor = input("Digite o nome do diretor: ")
        elif opcao == "3":
            try:
                ano = int(input("Digite o ano: "))
            except:
                print("❌ Ano inválido.")
                continue
        elif opcao == "4":
            id_filme = input("Digite o ID do filme (ex: tt0000001): ")
        elif opcao == "5":
            genero = input("Digite o gênero do filme: ")
        elif opcao == "6":
            txt = input("Prefixo do título (ou Enter): ")
            prefixo = txt if txt else None

            txt = input("Nome do diretor (ou Enter): ")
            diretor = txt if txt else None

            txt = input("Ano (ou Enter): ")
            if txt:
                try:
                    ano = int(txt)
                except:
                    print("❌ Ano inválido.")
                    continue

            txt = input("ID do filme (ou Enter): ")
            id_filme = txt if txt else None

            txt = input("Gênero (ou Enter): ")
            genero = txt if txt else None

        elif opcao == "7":
            caminho = input("Digite o caminho do novo arquivo .tsv (ex: data/novos.tsv): ").strip()
            try:
                qtd = importar_filmes_em_lote(
                    caminho_tsv=caminho,
                    caminho_bin=caminho_bin,
                    trie=trie,
                    hash_diretor=hash_diretor,
                    indice_ano=indice_ano,
                    indice_id=indice_id
                )
                print(f"✅ {qtd} filmes importados com sucesso.")

                salvar_trie_em_arquivo(trie, "data/trie.idx")
                salvar_hash_em_arquivo(hash_diretor, "data/hash.idx")
                salvar_indice_em_arquivo(indice_ano, "data/b_ano.idx")
                salvar_indice_em_arquivo(indice_id, "data/b_id.idx")
                print("💾 Índices atualizados foram salvos com sucesso.")

            except Exception as e:
                print("❌ Erro ao importar lote:", e)

            mostrar_menu = True
            continue
        else:
            print("❌ Opção inválida.")
            mostrar_menu = True
            continue

        resultados = buscar_filmes_com_filtros(
            prefixo_titulo=prefixo,
            diretor=diretor,
            ano=ano,
            id_filme=id_filme,
            genero=genero,
            trie=trie,
            hash_diretor=hash_diretor,
            indice_ano=indice_ano,
            indice_id=indice_id,
            caminho_bin=caminho_bin
        )

        if not resultados:
            print("🔍 Nenhum filme encontrado com os filtros informados.")
        else:
            print(f"🔎 {len(resultados)} resultado(s) encontrado(s):")
            for f in resultados[:10]:
                print("🔸", f)

        # Novo menu após resultado
        print("\n📋 O que você deseja fazer agora?")
        print("1. Voltar ao menu principal")
        print("0. Sair")
        subopcao = input("Escolha uma opção: ")
        if subopcao == "0":
            print("👋 Saindo do sistema. Até logo!")
            break
        elif subopcao == "1":
            mostrar_menu = True
        else:
            print("❌ Opção inválida. Voltando ao menu principal.")
            mostrar_menu = True
