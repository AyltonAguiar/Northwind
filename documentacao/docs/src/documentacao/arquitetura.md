## __Objetivo__

O objetivo do documento é exibir a arquitetura utilizada no desenvolvimento da documentação utilizando o gerador de páginas estático [MKDocs](https://www.mkdocs.org/).

## __Organização__

Existe duas propostas de padrões utilizados nesse projeto: 

<center>

| **Ambiente** | **Descrição** |
|:-:|:-:|
| Desenvolvimento | Padrão para documentar o desenvolvimento da aplicação, onde há a descrição das funcionalidades e implementações de comandos e códigos |
| Arquitetura | Descrever a arquitetura ou a funcionalidade de forma mais conceitual, sem muitos detalhes de implementação |

</center>

## __Arquitetura do Projeto__

A documentação é composta de vários arquivos, aqui darei foco em `docs\assets` e `docs\src`.

* `docs\assets`: Contém arquivos que <mark> não são </mark> `.md`. Focado em imagens e outros arquivos secundários para anexar à documentação.
* `docs\src`: Concentra a documentação em markdown.


Com isso em mente, teremos a seguinte estrutura:

```bash hl_lines="3 4 7 8 9 11 12"
📦REPOSITÓRIO
┣ 📂docs
┃ ┣ 📂assets
┃ ┃ ┣ 📂projeto1
┃ ┃ ┃ ┗ 📂bagdes
┃ ┃ ┃ ┃ ┗ 📷image.png
┃ ┣ 📂src
┃ ┃ ┣ 📂projeto1
┃ ┃ ┃ ┣ 📂desenvolvimento
┃ ┃ ┃ ┃ ┗ 📜index.md
┃ ┃ ┃ ┣ 📂arquitetura
┃ ┃ ┃ ┃ ┗ 📜arquitetura.md
┣ 📜mkdocs.yml # (1)
┗ 📜requirements.txt 
```

1. Arquivo de configuração do Mkdocks: thema, navegação, plugins, repositório, etc.

