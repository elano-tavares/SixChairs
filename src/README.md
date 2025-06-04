# Pasta src/

Esta pasta contém os módulos principais da lógica do sistema.

- extrator.py: extrai os dados dos arquivos .tsv do IMDb e monta os objetos Filme.
- filme.py: define a estrutura da classe Filme e os métodos de serialização para binário.
- gravador.py: responsável por salvar e carregar registros do arquivo binário.
- buscador.py: conterá as funções de busca usando os índices.
- estatisticas.py: conterá funções analíticas como médias, contagens e agrupamentos.

Todos os módulos aqui interagem com os dados e arquivos binários da pasta /data.