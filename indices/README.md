# Pasta indices/

Esta pasta contém a implementação das estruturas de dados utilizadas como índices para otimizar as buscas no sistema.

- **`trie.py`**: Índice baseado em árvore TRIE, usado para busca por prefixo de títulos.
- **`hash.py`**: Índice baseado em tabela hash para acesso rápido por nome de diretor.
- **`arvore.py`**: Índice baseado em Árvore B, usado para ordenação e buscas por valor exato ou intervalo (ano, ID).

Os índices aqui são criados e atualizados a partir dos dados do arquivo binário localizado em `/data`.