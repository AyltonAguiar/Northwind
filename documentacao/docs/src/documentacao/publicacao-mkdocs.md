# Publicando Mkdocs


## __Mkdocs github manual__

No diretório da documentação utilize o comando `mkdocs build` para gerar o diretório `\site` com a estrutura. Após gerar o diretório `\site` utilize o comando `mkdocs gh-deploy --force`.

```
mkdocs build
mkdocs gh-deploy --force
```


## __Mkdocs github automático__ 

O Modelo automático é realizado pela criação de um workflow no github. O CI é configurado no arquivo `.github/workflows/ci.yml`

```yml title="mkdocs-ci.yml"
name: ci 
on:
  push:
    branches:
      - master 
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - uses: actions/cache@v2
        with:
          key: ${{ github.ref }}
          path: .cache
      - run: pip install -r requirements.txt
      - run: pip install \
               mkdocs-material \
               mkdocs-table-reader-plugin
      - run: mkdocs gh-deploy --force

```

!!! Attention "Atenção"
    Se a página do GitHub não aparecer após alguns minutos, vá para as configurações do seu repositório e certifique-se de que a [ramificação da fonte](https://docs.github.com/pt/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) de publicação da sua página do GitHub esteja definida como gh-pages.



*Aguarde uns alguns instantes para verificar a publicação do site estático.*
