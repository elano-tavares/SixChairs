# 🎬 SixChairs — Catálogo Local de Filmes

SixChairs é um sistema de linha de comando simples e eficiente para organizar, buscar e analisar um catálogo de filmes offline, utilizando os dados públicos do IMDb.

Este projeto foi desenvolvido como trabalho da disciplina de Classificação e Pesquisa de Dados (CPD), com foco em estruturas de arquivos, indexação e algoritmos de busca.

---

## 🚀 Como Executar

1.  **Prepare os Dados:**
    * Baixe os arquivos de dados do IMDb (`name.basics.tsv`, `title.crew.tsv`, `title.basics.tsv`).
    * Coloque-os dentro da pasta `/data`.

2.  **Execute o Programa:**
    * A partir da raiz do projeto, execute o comando:
        ```bash
        python main.py
        ```
    * Na primeira execução, o sistema irá processar os arquivos `.tsv`, gerar o arquivo binário `filmes.bin` e construir todos os índices necessários. Em execuções futuras, ele carregará os arquivos de índice existentes.

---

## 🧩 Objetivos

- Armazenar filmes em um arquivo binário único (`filmes.bin`).
- Criar e persistir índices para otimizar buscas:
  - **Trie:** para buscas por prefixo de título.
  - **Hash:** para buscas por nome de diretor.
  - **Árvore B:** para buscas por ID e por ano (incluindo intervalos).
- Realizar filtragens e ordenações eficientes.
- Operar localmente, sem dependência de bancos de dados externos.

---

## 📂 Estrutura do Projeto

| Pasta    | Conteúdo                                                                                                  |
|----------|-----------------------------------------------------------------------------------------------------------|
| **/src** | Contém os módulos principais com a lógica do sistema (CLI, construção de índices, buscas, etc.).          |
| **/indices** | Implementação das estruturas de dados usadas como índices (Trie, Hash, Árvore B).                     |
| **/data**| Armazena os arquivos de entrada (`.tsv`), o arquivo de dados binário (`.bin`) e os arquivos de índice (`.idx`). |

---

## ✨ Funcionalidades

- Importação e processamento inicial de dados do IMDb.
- Armazenamento binário eficiente dos registros de filmes.
- Busca combinada por título, diretor, ano, gênero ou ID.
- Importação incremental de novos filmes em lote a partir de um arquivo `.tsv`.
- Geração de estatísticas sobre os dados.
- Interface de linha de comando (CLI) interativa com paginação e reordenação de resultados.