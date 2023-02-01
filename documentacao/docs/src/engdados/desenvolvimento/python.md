#  __Python__

[python desenvolvimento]: #python-desenvolvimento


## __Introdução__

Pensando em aumentar a legibilidade, manutenção e organização do código. O código em python está separado em 3 partes:

1.  `python\engdados\s3_redshift_load_files.py`: Script main, contendo de forma resumida o código sem detalhes das funções.
2.  `python\engdados\mod_terraform.py`: módulo contendo algumas poucas funções para auxiliar com os arquivos do terraform.
3.  `python\engdados\mod_aws.py`: módulo contendo algumas funções para auxiliar nos recursos da AWS.

### Módulos
Nos trechos abaixo, as funções vão apresentar os módulos na frente, por exemplo: `m_tf.get_path_s3()`.

| módulo| abreviação|
| ---| ---|
| mod_terraform| `m_tf`|
| mod_aws| `m_aws`|

### Imports

Imports utilizados no desenvolvimento. Sobre a instalação dos imports, favor verificar o tópico [requirements](#requirements).
Caso tenha dificuldades em ler conteúdos em inglês, sugiro utilizar o navegador google chrome para visualização das documentações.

| Imports | descrição | documentação |
| :------------- |-------------|-------------|
|boto3 | AWS SDK for Python (Boto3) para criar, configurar e gerenciar serviços da AWS | [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html){:target='_blank'} |
|pandas | Ferramenta de análise e manipulação de dados de código aberto rápida, poderosa, flexível e fácil de usar, construída sobre a linguagem de programação Python | [Guia do usuário](https://pandas.pydata.org/docs/user_guide/index.html){:target='_blank'} |
|io | O módulo fornece as principais facilidades do Python para lidar com vários tipos de E/S | [io Python](https://docs.python.org/3/library/io.html){:target='_blank'} |
|json | A biblioteca json nos permite poder analisar JSON | [json Python](https://docs.python.org/pt-br/3/library/json.html){:target='_blank'} |
|psycopg2 | Adaptador de banco de dados PostgreSQL | [Official Psycopg](https://www.psycopg.org/docs/){:target='_blank'} |
|logging | Este módulo define funções e classes que implementam um sistema flexível de registro de eventos para aplicativos e bibliotecas. | [logging Python](https://docs.python.org/3/library/logging.html){:target='_blank'} |

### Requirements {#requirements}

Requerimentos utilizados e que necessitam de instalação.

=== ":octicons-file-code-16: `python\requirements.txt`"

    ``` t
    # Requerimentos

    # Bibliotecas de desenvolvimento
    pandas      # Manipulação e análise de dados
    boto3       # Integração aos serviços AWS
    psycopg2    # Adaptador do Banco de dados PostgreSQL

    # Sem pacotes com versões específicas
    ```

??? question "Como faço para instalar os requerimentos?"

    Para instalação de requirements utilize o seguinte comando:

    ```
    pip install -r requirements.txt
    ```


### Ambiente virtual {#ambiente-virtual}

Sobre comandos de criação, ativação e desativação de ambiente virtual.
Caso já tenha conhecimento, basta pular para o [conexão aws](#conexão-aws).

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


##  __Conexão AWS__ {#conexão-aws}

Para a conexão estarei utilizando o [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
Estarei utilizando o `profile_name` para realizar a sessão e posteriomente o cliente.

<mark> Necessita da [CLI AWS](../prerequisitos.md#requisito-aws-cli){:target='_blank'}</mark>

=== ":octicons-file-code-16: `s3_redshift_load_files.py`"

    ``` py
    # Conexão ao Redshift
    """Accessing the S3 buckets using boto3 client"""
    session = boto3.Session(profile_name='ayltonaguiar')
    s3_client = session.client('s3')
    s3 = session.resource('s3')
    ```

##  __Pegando os arquivos terraform.tfstate__ {#pegando-os-arquivos-tfstate}

Fiz a leitura buscando em 2 lugares diferentes. A primeira parte é identificação válida dos arquivos (verificar se existem), então foram criadas 2 funções com buscas de caminhos específicos: `m_tf.get_path_s3()` e `m_tf.get_path_redshift()` . Ambas retornam os caminhos (path) dos arquivos.

A segunda parte é a leitura dos arquivos identificados. Foram criadas outras 2 funções com parâmetros específicos para cada uma: `m_tf.read_s3_tfstate_backend()` e `m_tf.read_redshift_tfstate()`. Ambas retornam informações, por exemplo: região do redshift, região do bucket backend (remote state), etc.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 1- Pega o diretório dos arquivos, valida e guarda as informações básicas em novas variáveis
    path_s3 = m_tf.get_path_s3()
    path_redshift = m_tf.get_path_redshift()
    ## 1.1- s3
    backend_details = m_tf.read_s3_tfstate_backend(f"{path_s3}")
    backend_bucket, backend_region, backend_key = backend_details
    ## 1.2- redshift
    redshift_details = m_tf.read_redshift_tfstate(f"{path_redshift}")
    redshift_iam_arn, redshift_secrete_name, redshift_region_name = redshift_details
    ```

    [Pegando os arquivos tfstate]: #pegando-os-arquivos-tfstate


##  __Pegar arquivos armazenados no bucket S3__ {#pegar-arquivos-armazenados-no-bucket-S3}

Para realizarmos a identificação dos objetos no S3, precisamos saber o nome do bucket e quais arquivos devemos realizar leitura.

Por isso criei a função `m_aws.get_bucket()`, ela necessita de algumas informações, por exemplo: o nome do bucket backend que está compartilhando, o bucket backend key e a conexão cliente s3. Ao final estará retornando o nome do bucket que armazena os objetos (nosso querido bucket com os csv's).

A função `m_aws.get_csv_s3()` estará verificando e listando os objetos que terminam com '.csv' ou '.CSV'. Ela retorna `list_objects`.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 2- seleciona o objeto do bucket/key fornecido e pega o valor do output 'bucket-name'
    bucket_name = m_aws.get_bucket(s3_client, backend_bucket, backend_key)

    # 3- Listagem de objetos do bucket fornecido
    list_objects = m_aws.get_csv_s3(s3_client, bucket_name)
    ```

    [Pegar arquivos armazenados no bucket S3]: #pegar-arquivos-armazenados-no-bucket-S3


##  __Pegar dados armazenados no Secrets Manager__ {#pegar-dados-armazenados-no-secrets-manager}

Para dar prosseguimento precisamos recuperar alguns dados sensíveis adicionados no secrets manager, então foi criado a função `m_aws.get_secrets_redshift()` com objetivo de recuperar essas informações e armazená-las para o próximo passo.

A conexão com banco do redshift é feita, nesse projeto, pelo uso do psycopg2. Utilizando as informações recuperadas pela função `m_aws.get_secrets_redshift()`.


=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 4- Acessando e pegando os valores guardados do Redshift no Secrets Manager
    client_secret = session.client('secretsmanager', region_name=redshift_region_name)
    secrets_manager_details = m_aws.get_secrets_redshift(client_secret, redshift_secrete_name)
    redshift_db_name, redshift_db_user, redshift_db_password, redshift_db_port, redshift_db_host = secrets_manager_details

    # 5- conexão ao banco
    rd_con = psycopg2.connect(host=redshift_db_host, database=redshift_db_name,
                            user=redshift_db_user, password=redshift_db_password, port=redshift_db_port)
    rd_con.autocommit = True
    cur = rd_con.cursor()
    ```

    [Pegar dados armazenados no Secrets Manager]: #pegar-dados-armazenados-no-secrets-manager


##  __Permissões aos grupos e listagem de pastas__ {#permissões-e-listagem-de-pastas}

Lembra que criamos os usuários e grupos de usuários? Então, estaremos realizando a primeira parte das permissões para os usuários criados, após essa etapa será realizado a preparação para os nomes das pastas.

Para adição de permissões, a função `m_aws.give_permissions_database()` receberá a conexão, o nome do banco de dados e nome do grupo.
A função `m_aws.get_folder()` pega a primeira parte do diretório da lista de objetos e armazena em `SCHEMAS_REDSHIFT`.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 6- Permissão Create para loaders, select para transformers no banco de dados
    m_aws.give_permissions_database(cur,redshift_db_name, group_loaders, group_transformers)

    # 7- pegar o primeiro diretório e adiciona-lo a uma lista de schema.
    SCHEMAS_REDSHIFT = m_aws.get_folder(list_objects)
    #print(SCHEMAS_REDSHIFT)
    ```

    [Permissões e listagem de pastas]: #permissões-e-listagem-de-pastas


##  __Criação e Permissões para Schemas__ {#criação-e-permissões-para-schemas}

Nessa etapa criaremos os schemas e adicionaremos as permissões para os usuários do grupo 'transformers'.

A função `m_aws.create_schema_redshift()` cria os schemas com base nos diretórios armazenados em `SCHEMAS_REDSHIFT`.

Os Tranformadores precisam de acesso aos schemas criados, pois vão trabalhar com todas as tabelas existentes. A função `m_aws.give_permission_schemas()` visa permitir ao grupo selecionado tenha permissões, além de fazer com que o `redshift_db_user`
ganhe privilégios para as novas tabelas criadas.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 8- Criação dos schemas caso não exista
    m_aws.create_schema_redshift(cur, SCHEMAS_REDSHIFT, redshift_db_user)

    # 9- Permissão para o grupo transformers sobre os schemas criados
    m_aws.give_permission_schemas(cur, SCHEMAS_REDSHIFT, redshift_db_user, group_transformers)
    ```

    [Criação e Permissões para Schemas]: #criação-e-permissões-para-schemas


##  __Criação das tabelas e copy__ {#criação-de-tabelas-e-copys}

A função `m_aws.csv_to_redshift()` é um pouco maior, ela contém outras funções em seu corpo. Em resumo ela pega o objeto, faz a leitura utilizando o `io.BytesIO()`, verifica quais são os delimitadores dos objetos `.csv`, qual o tipo de dado da coluna, qual o tamanho máximo nos registros da coluna e realiza o copy dos dados para o Redshift.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 10- Criação das tabelas, colunas e copy
    m_aws.csv_to_redshift(cur, s3, bucket_name, list_objects, redshift_details, redshift_db_name)

    # 11- fechando conexão
    rd_con.close()
    ```

    [Criação das tabelas e copy]: #criação-e-permissões-para-schemas


## :material-format-list-checks: Check Objetivos

Os ícones :octicons-check-circle-fill-24:{ style="color: #00e676" } são os finalizados e os :octicons-check-circle-fill-24:{ style="color: var(--md-default-fg-color--lightest)" } são os em abertos.

- [x] [Pegar dados dos arquivos terraform.tfstate](#pegando-os-arquivos-tfstate)
- [x] [Pegar os arquivos csv's armazenados na amazom S3](#pegar-arquivos-armazenados-no-bucket-S3)
- [x] [Pegar dados armazenados no Secrets Manager](#pegar-dados-armazenados-no-secrets-manager)
- [x] [Permissões aos grupos e listagem de pastas](#permissões-e-listagem-de-pastas)
- [x] [Permissões e criação de schemas](#criação-e-permissões-para-schemas)
- [x] [Criação das tabelas e copy](#criação-de-tabelas-e-copys)
- [ ] Refatorar os módulos mod_aws e mod_terraform

