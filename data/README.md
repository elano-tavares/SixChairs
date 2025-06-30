# Pasta data/

Esta pasta armazena os arquivos de entrada e saída do sistema.

Ela é usada pelos módulos da pasta `/src` para:

- Receber os arquivos de entrada extraídos do IMDb (ex: `name.basics.tsv`, `title.basics.tsv`, `title.crew.tsv`).
- Salvar os registros processados no formato binário (ex: `filmes.bin`).
- Armazenar os arquivos de índice persistidos (ex: `trie.idx`, `hash.idx`, `b_ano.idx`, `b_id.idx`).

⚠️ **Observação:**
Por padrão, os arquivos `.tsv` originais do IMDb são ignorados pelo controle de versão (veja o arquivo `.gitignore`).
Cada colaborador deve obter os arquivos manualmente e colocá-los nesta pasta antes de executar o sistema.

Esta pasta não contém código-fonte, apenas dados de entrada e saída.