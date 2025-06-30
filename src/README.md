# Pasta src/

Esta pasta contém os módulos principais com a lógica do sistema. Os arquivos `gravador.py` e `menu.py` foram removidos e suas funcionalidades foram incorporadas nos módulos abaixo.

- **`cli.py`**: Implementa a interface de linha de comando (CLI) interativa. Gerencia os menus, a entrada do usuário e a exibição dos resultados.

- **`index_builder.py`**: Módulo central que gerencia o ciclo de vida dos índices. É responsável por construir, carregar, salvar e atualizar (em caso de importação de novos dados) todos os índices (Trie, Hash e Árvore B).

- **`binary_store.py`**: Camada de acesso ao arquivo binário (`filmes.bin`). Contém funções para ler, escrever e adicionar registros de filmes de forma serializada.

- **`filme.py`**: Define a classe `Filme`, que representa a estrutura de dados de um filme, e contém os métodos de serialização (`to_bytes`) e desserialização (`from_bytes`).

- **`buscas.py`**: Contém a lógica de busca que utiliza os índices para filtrar os dados. Permite a busca por múltiplos critérios combinados.

- **`extrator.py`**: Responsável por extrair e processar os dados brutos dos arquivos `.tsv` do IMDb, transformando-os em uma lista de objetos `Filme`.

- **`estatisticas.py`**: Gera e exibe estatísticas sobre o catálogo de filmes, como contagens e rankings de diretores, gêneros e anos.