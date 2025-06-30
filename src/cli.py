# src/cli.py (antigo menu.py - MODIFICADO)

from pathlib import Path
from src.buscas import buscar_filmes_com_filtros
from src.index_builder import IndexBuilder
from src.estatisticas import gerar_estatisticas
from src.extrator import carregar_nome_diretores, carregar_diretores_por_titulo, extrair_filmes

# ... (função exibir_resultados_paginados permanece a mesma) ...
def exibir_resultados_paginados(filmes: list, itens_por_pagina: int = 10):
    """
    Exibe uma lista de filmes de forma paginada, permitindo ao usuário navegar
    entre as páginas e reordenar os resultados.
    """
    if not filmes:
        print("🔍 Nenhum filme encontrado.")
        return

    total_filmes = len(filmes)
    total_paginas = (total_filmes + itens_por_pagina - 1) // itens_por_pagina
    pagina_atual = 1

    while True:
        print(f"\n🔎 {total_filmes} resultado(s) encontrado(s):")
        print(f"📄 Página {pagina_atual} de {total_paginas}")
        inicio = (pagina_atual - 1) * itens_por_pagina
        fim = min(inicio + itens_por_pagina, total_filmes)

        for i in range(inicio, fim):
            print(f"🔸 {filmes[i]}")

        print("\n📖 Opções de navegação:")
        print("n = próxima página | p = página anterior | r = reordenar | s = sair da visualização")
        
        escolha_paginacao = input("Escolha: ").lower()

        if escolha_paginacao == 'n':
            if pagina_atual < total_paginas:
                pagina_atual += 1
            else:
                print("⚠️ Já está na última página.")
        elif escolha_paginacao == 'p':
            if pagina_atual > 1:
                pagina_atual -= 1
            else:
                print("⚠️ Já está na primeira página.")
        elif escolha_paginacao == 'r':
            print("\nReordenar por:")
            print("1. Título (A-Z)")
            print("2. Título (Z-A)")
            print("3. Ano (Crescente)")
            print("4. Ano (Decrescente)")
            print("5. Diretor (A-Z)")
            print("6. Diretor (Z-A)")
            
            opcao_ordenacao = input("Escolha a opção de ordenação: ")
            
            if opcao_ordenacao == '1':
                filmes.sort(key=lambda f: f.titulo.lower())
            elif opcao_ordenacao == '2':
                filmes.sort(key=lambda f: f.titulo.lower(), reverse=True)
            elif opcao_ordenacao == '3':
                filmes.sort(key=lambda f: f.ano)
            elif opcao_ordenacao == '4':
                filmes.sort(key=lambda f: f.ano, reverse=True)
            elif opcao_ordenacao == '5':
                filmes.sort(key=lambda f: f.diretor.lower())
            elif opcao_ordenacao == '6':
                filmes.sort(key=lambda f: f.diretor.lower(), reverse=True)
            else:
                print("❌ Opção de ordenação inválida.")
            pagina_atual = 1
            
        elif escolha_paginacao == 's':
            break
        else:
            print("❌ Opção inválida. Tente novamente.")


def menu_principal(index_builder: IndexBuilder, caminho_bin: str = "data/filmes.bin"):
    """
    Função principal da interface de linha de comando.
    """
    print("\n📚 Bem-vindo ao sistema de busca SixChairs!")
    
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Buscar filmes")
        print("2. Importar novo lote de filmes (TSV simplificado)")
        print("3. Ver estatísticas")
        print("0. Sair")

        opcao_principal = input("Escolha uma opção: ")

        if opcao_principal == "0":
            print("👋 Saindo do sistema. Até logo!")
            break
        
        # ### O menu de busca (opção 1) não precisa de alterações ###
        elif opcao_principal == "1":
            # ... (código da opção 1 permanece o mesmo) ...
            while True:
                print("\n--- MENU DE BUSCA ---")
                print("1. Buscar por título (prefixo)")
                print("2. Buscar por diretor")
                print("3. Buscar por ano")
                print("4. Buscar por ID")
                print("5. Buscar por gênero")
                print("6. Combinação de filtros")
                print("0. Voltar ao menu principal")

                opcao_busca = input("Escolha uma opção: ")

                if opcao_busca == "0":
                    break

                prefixo = diretor = id_filme = None
                ano = genero = None
                ordenar_por_param = 'titulo' 
                ordem_crescente_param = True 

                if opcao_busca == "1":
                    prefixo = input("Digite o prefixo do título: ")
                elif opcao_busca == "2":
                    diretor = input("Digite o nome do diretor: ")
                elif opcao_busca == "3":
                    try:
                        ano = int(input("Digite o ano: "))
                    except ValueError:
                        print("❌ Ano inválido.")
                        continue
                elif opcao_busca == "4":
                    id_filme = input("Digite o ID do filme (ex: tt0000001): ")
                elif opcao_busca == "5":
                    genero = input("Digite o gênero do filme: ")
                elif opcao_busca == "6":
                    txt = input("Prefixo do título (ou Enter): ")
                    prefixo = txt if txt else None
                    txt = input("Nome do diretor (ou Enter): ")
                    diretor = txt if txt else None
                    txt = input("Ano (ou Enter): ")
                    if txt:
                        try:
                            ano = int(txt)
                        except ValueError:
                            print("❌ Ano inválido.")
                            continue
                    txt = input("ID do filme (ou Enter): ")
                    id_filme = txt if txt else None
                    txt = input("Gênero (ou Enter): ")
                    genero = txt if txt else None
                    
                    print("\nOrdenar resultados inicialmente por:")
                    print("1. Título (Padrão: A-Z)")
                    print("2. Ano (Crescente)")
                    print("3. Diretor (A-Z)")
                    ord_opt = input("Escolha a ordenação inicial (1/2/3 ou Enter para padrão): ")
                    if ord_opt == '2':
                        ordenar_por_param = 'ano'
                    elif ord_opt == '3':
                        ordenar_por_param = 'diretor'
                else:
                    print("❌ Opção inválida.")
                    continue

                resultados = buscar_filmes_com_filtros(
                    prefixo_titulo=prefixo,
                    diretor=diretor,
                    ano=ano,
                    id_filme=id_filme,
                    genero=genero,
                    trie_obj=index_builder.trie,
                    hash_diretor_obj=index_builder.hash_diretor,
                    indice_ano_obj=index_builder.indice_ano,
                    indice_id_obj=index_builder.indice_id,
                    caminho_bin=caminho_bin,
                    ordenar_por=ordenar_por_param,
                    ordem_crescente=ordem_crescente_param
                )
                
                exibir_resultados_paginados(resultados)

        ### SEÇÃO MODIFICADA ###
        elif opcao_principal == "2": # Importar novo lote de filmes
            caminho_tsv = input("Digite o caminho do arquivo .tsv simplificado (ex: data/teste.tsv): ").strip()
            if not Path(caminho_tsv).exists():
                print(f"❌ Arquivo TSV não encontrado: {caminho_tsv}")
                continue

            try:
                # Chama o novo método de importação simplificada
                qtd = index_builder.importar_lote_simplificado(caminho_tsv)
                
                if qtd > 0:
                    print(f"✅ {qtd} filmes importados com sucesso.")
                    # Salva todos os índices após a importação bem-sucedida
                    index_builder.salvar_todos_indices()
                else:
                    print("ℹ️ Nenhum filme novo foi importado.")
            except Exception as e:
                print(f"❌ Erro ao importar lote: {e}")

        elif opcao_principal == "3": # Ver estatísticas
            gerar_estatisticas(caminho_bin)

        else:
            print("❌ Opção inválida.")