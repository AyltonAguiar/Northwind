
## __Apresentação__

O intuito é auxiliar na reprodução da documentação realizada no projeto.

## __Pré-requisitos__

A máquina deve conter `python`(preferência acima da versão 3.8) e `pip`.

??? question "Não tenho o pip, como baixar?"

    Atalho para o site: [Pypi-pip](https://pypi.org/project/pip/) 

??? question "Como faço para instalar o Python?"

    Aqui nesse tópico passo alguns links: [tutorial](../engdados/prerequisitos.md#tutorial-python)


## __Começando__

Para iniciar a documentação apresentada, pode-se utilizar uma `venv` e o arquivo `requirements.txt`. Assim você possui um projeto reservado utilizando dos prós do ambiente virtual.


```{.py title="criar ambiente virtual"}
python -m venv .venv
```

```{.py title="ativar ambiente virtual"}
.\.venv\Scripts\Activate
```

```{.py title="Instalação dos requirements"}
pip install -r requirements.txt
```

??? question "Como usar o ambiente virtual?"

    criar:
    ``` py
    python -m venv .venv
    ```
    ativar:
    ``` py
    .\.venv\Scripts\Activate
    ```
    desativar:
    ``` py
    deactivate
    ```

### Iniciando Mkdocs

Após a execução do comando `mkdocs serve`, o servidor será iniciado e poderá ser acessado em [`http://127.0.0.1:8000`](http://127.0.0.1:8000).

```py title="Iniciando servidor local"
mkdocs serve
```


