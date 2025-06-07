from src.buscas import buscar_filmes_com_filtros

def menu_busca_interativa(trie, hash_diretor, indice_ano, indice_id, caminho_bin="data/filmes.bin"):
    print("\n📚 Bem-vindo ao sistema de busca SixChairs!")
    while True:
        print("\n--- MENU DE BUSCA ---")
        print("1. Buscar por título (prefixo)")
        print("2. Buscar por diretor")
        print("3. Buscar por ano")
        print("4. Buscar por ID")
        print("5. Buscar por gênero")
        print("6. Combinação de filtros")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("👋 Saindo do sistema. Até logo!")
            break

        prefixo = diretor = id_filme = None
        ano = None

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
        else:
            print("❌ Opção inválida.")
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
            for f in resultados[:100]:
                print("🔸", f)
