# 🎬 SixChairs — Catálogo Local de Filmes  

SixChairs é um sistema desktop simples e eficiente para organizar, buscar e analisar um catálogo de filmes offline com base nos dados públicos do IMDb.

Este projeto foi desenvolvido como trabalho final da disciplina de Classificação e Pesquisa de Dados (CPD), com foco em estruturas de arquivos, indexação e algoritmos de busca.

---

## 🧩 Objetivos

- Armazenar filmes em arquivos binários organizados como heap (serial).
- Criar índices personalizados para otimizar buscas:
  - TRIE (título)
  - Hash (diretor)
  - Árvore B/B+ (ano ou ID)
- Realizar filtragens e ordenações eficientes diretamente sobre os dados em disco.
- Operar localmente, sem necessidade de banco de dados externo.

---

## 📂 Estrutura do Projeto

| Pasta        | Conteúdo                                                                 |
|--------------|--------------------------------------------------------------------------|
| /src         | Módulos principais (extração de dados, escrita/leitura, estatísticas)   |
| /indices     | Estruturas de índice (TRIE, Hash, B/B+)                                  |
| /data        | Arquivos de entrada (TSV), registros binários e arquivos de índice       |

---

## 🚀 Funcionalidades

- Importação incremental de dados do IMDb (.tsv)
- Armazenamento binário eficiente dos registros
- Busca por título, diretor, ano ou ID
- Filtro combinado (ex: diretor + gênero)
- Estatísticas e ordenações (ex: média de ano por gênero)
- Paginação de resultados
- Indexação offline e permanente

---