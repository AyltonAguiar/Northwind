#  __Python__

[python desenvolvimento]: #python-desenvolvimento


## __Introdução__

Pensando em aumentar a legibilidade, manutenção e organização do código. O código em python está separado em 3 partes:

1.  `python\engdados\s3_redshift_load_files.py`: Script main, contendo de forma resumida o código sem detalhes das funções.
2.  `python\engdados\mod_terraform.py`: módulo contendo algumas poucas funções para auxiliar com os arquivos do terraform.
3.  `python\engdados\mod_aws.py`: módulo contendo algumas funções para auxiliar nos recursos da AWS.

### Módulos
Nos trechos abaixo, as funções vão apresentar os módulos na frente, por exemplo: `m_tf.get_path_s3()`.

| módulo        | abreviação |
| ------------- | ---------- |
| mod_terraform | `m_tf`     |
| mod_aws       | `m_aws`    |

### Imports

Imports utilizados no desenvolvimento. Sobre a instalação dos imports, favor verificar o tópico [requirements](#requirements).
Caso tenha dificuldades em ler conteúdos em inglês, sugiro utilizar o navegador google chrome para visualização das documentações.

| Imports  | descrição                                                                                                                                                    | documentação                                                                                                       |
| :------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| boto3    | AWS SDK for Python (Boto3) para criar, configurar e gerenciar serviços da AWS                                                                                | [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html){:target='_blank'} |
| pandas   | Ferramenta de análise e manipulação de dados de código aberto rápida, poderosa, flexível e fácil de usar, construída sobre a linguagem de programação Python | [Guia do usuário](https://pandas.pydata.org/docs/user_guide/index.html){:target='_blank'}                          |
| io       | O módulo fornece as principais facilidades do Python para lidar com vários tipos de E/S                                                                      | [io Python](https://docs.python.org/3/library/io.html){:target='_blank'}                                           |
| json     | A biblioteca json nos permite poder analisar JSON                                                                                                            | [json Python](https://docs.python.org/pt-br/3/library/json.html){:target='_blank'}                                 |
| psycopg2 | Adaptador de banco de dados PostgreSQL                                                                                                                       | [Official Psycopg](https://www.psycopg.org/docs/){:target='_blank'}                                                |
| logging  | Este módulo define funções e classes que implementam um sistema flexível de registro de eventos para aplicativos e bibliotecas.                              | [logging Python](https://docs.python.org/3/library/logging.html){:target='_blank'}                                 |

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

??? info "code function get_path_s3()"
    === ":octicons-file-code-16: `python\engdados\mod_terraform.py`"

    ``` python linenums="13"
    def get_path_s3():
        # captura do arquivo terraform.state
        path_s3_tfstate = Path().absolute().parent.parent.joinpath('terraform','02_aws_s3_and_files','.terraform','terraform.tfstate')
        # validação do path
        path_validate(path_s3_tfstate, get_path_s3.__name__)
        return path_s3_tfstate
    ```

??? info "code function get_path_redshift()"
    === ":octicons-file-code-16: `python\engdados\mod_terraform.py`"

    ``` python linenums="20"
    def get_path_redshift():
        # captura do arquivo terraform.state
        path_redshift_tfstate = Path().absolute().parent.parent.joinpath('terraform','03_aws_redshift','terraform.tfstate')
        # validação do path
        path_validate(path_redshift_tfstate, get_path_redshift.__name__)
        return path_redshift_tfstate
    ```

??? info "code function read_s3_tfstate_backend()"
    === ":octicons-file-code-16: `python\engdados\mod_terraform.py`"

    ``` python linenums="27"
    def read_s3_tfstate_backend(path):
        try:
            # Captura as informações pelo backend do tfstate
            with open(path) as file_name:
                s3_details_backend = json.load(file_name)

                backend_bucket = s3_details_backend['backend']['config'].get('bucket')
                backend_region = s3_details_backend['backend']['config'].get('region')
                backend_key = s3_details_backend['backend']['config'].get('key')
                print('', "############ S3 Backend ##########", s3_details_backend['backend']['config'], sep='\n')
                return [backend_bucket, backend_region, backend_key]
        except Exception as e:
            logging.error(e)
            return False
    ```

??? info "code function read_redshift_tfstate()"
    === ":octicons-file-code-16: `python\engdados\mod_terraform.py`"

    ``` python linenums="42"
    def read_redshift_tfstate(path):
    # Captura dos outputs criados no arquivo terraform.tfstate da pasta aws_redshift
        try:
            with open(path) as rd_terraform:
                rd_terraform_json = json.load(rd_terraform)

                redshift_iam_arn = rd_terraform_json['outputs'].get('iam_role_arn').get('value')
                redshift_secrete_name = rd_terraform_json['outputs'].get('secrete_name').get('value')
                redshift_region_name = rd_terraform_json['outputs'].get('region_name').get('value')
                print('', "####### Outputs redshift.tfstate ##########",redshift_iam_arn, redshift_secrete_name, redshift_region_name, sep='\n')
                return [redshift_iam_arn, redshift_secrete_name, redshift_region_name]
        except Exception as e:
                logging.error(e)
                return False
    ```


##  __Pegar arquivos armazenados no bucket S3__ {#pegar-arquivos-armazenados-no-bucket-S3}

Para identificar objetos no S3, precisamos do nome do bucket e dos arquivos a serem lidos. Para facilitar esse processo, foi criada a função `m_aws.get_bucket()`. Essa função precisa de informações como o nome do bucket compartilhado, a chave do bucket backend e a conexão do cliente s3. Ela retornará o nome do bucket que armazena os objetos.

A função `m_aws.get_csv_s3()` verifica e lista os objetos com extensão '.csv' ou '.CSV', retornando a lista de objetos.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 2- seleciona o objeto do bucket/key fornecido e pega o valor do output 'bucket-name'
    bucket_name = m_aws.get_bucket(s3_client, backend_bucket, backend_key)

    # 3- Listagem de objetos do bucket fornecido
    list_objects = m_aws.get_csv_s3(s3_client, bucket_name)
    ```

??? info "code function get_bucket()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="8"
    def get_bucket(s3_client, backend_bucket, backend_key):
        # Identificar bucket  remote state
        try:
            s3_object = s3_client.get_object(Bucket=backend_bucket, Key=backend_key)
            object_file = s3_object["Body"].read().decode()
            parsed_object = json.loads(object_file)
            bucket_name = parsed_object['outputs'].get('bucket-name').get('value')
            print('',"####### Bucket Name Object S3 ##########",bucket_name, sep='\n')

        except Exception as e:
            logging.error(e)
            return False
        return bucket_name
    ```

??? info "code function get_csv_s3()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="23"
    def get_csv_s3(s3_client, bucket_name):
        # Lista os Objetos do bucket setado e armazena na variável s3_objects
        try:
            s3_list_obj = s3_client.list_objects(Bucket=bucket_name)
            s3_objects = []
            
            for obj in s3_list_obj['Contents']:
                if obj['Key'].endswith('csv') or obj['Key'].endswith('CSV'):
                    s3_objects.append(obj['Key'])
            print('',"####### Objects S3 ##########",s3_objects[0:10], sep='\n')

        except Exception as e:
            logging.error(e)
            return False
        return s3_objects
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

??? info "code function get_secrets_redshift()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="40"
    def get_secrets_redshift(client_secret, redshift_secrete_name):
        try:
            # Captura dos segredos do redshift na AWS Secrets
            get_secret_value_response = client_secret.get_secret_value(SecretId = redshift_secrete_name)
            secret_json = json.loads(get_secret_value_response['SecretString'])
            
        except Exception as e:
            logging.error(e)
            return False
        return secret_json
    ```
    [Pegar dados armazenados no Secrets Manager]: #pegar-dados-armazenados-no-secrets-manager


### Criação de usuários, grupos e vinculos {#criar-usuarios-grupos-vinculos-python}

A função `m_aws.create_users_redshift()` tem como objetivo criar os usuários, grupos e realizar vinculos entre as partes.
Por último a limpeza do arquivo com dados do secrets manager.


=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    ## 5.1 Criando os usuários dos grupos loaders, transformers e reporters
    m_aws.create_users_redshift(cur, secrets_manager_json)
    ## 5.2 Apagando as informações do secrets
    del secrets_manager_json
    ```


??? info "code function create_users_redshift()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="69"
    def create_users_redshift(cur, secret_json):
        try:
            # Usuários dos grupos - Falta melhorar essa parte bem hardcode e.e Deus me perdoe, mas é isso aí.
            loaders = []
            reporters = []
            transformers = []

            # Pegando usuários e senhas dos loaders, transformers e reporters
            for key, value in secret_json.items():
                if 'loaders' in key:
                    loaders.append(value)
                elif 'reporters' in key:
                    reporters.append(value)
                elif 'transformers' in key:
                    transformers.append(value)

            # Gerando novas listas a cada 2 items na lista original
            loaders = [loaders[i:i+2] for i in range(0, len(loaders), 2)]
            reporters = [reporters[i:i+2] for i in range(0, len(reporters), 2)]
            transformers = [transformers[i:i+2] for i in range(0, len(transformers), 2)]

            groups = loaders, reporters, transformers
            group_names = ["loaders", "reporters", "transformers"]

            # Criação dos grupos
            for group in group_names:
                cur.execute(f"CREATE GROUP {group};")
        
            # Criando Usuários com senhas (0=nome do usuário, 1=senha)
            for group in groups:
                for user in group:
                    cur.execute(f"create user {user[0]} with password '{user[1]}';")
                    
            # Adição dos usuários aos grupos
            for idx, group in enumerate(groups):
                for idx2, user in enumerate(group):
                    cur.execute(f"alter group {group_names[idx]} add user {user[0]};")
        except Exception as e:
            logging.error(e)
            return False
    ```
    [Criar usuários, grupos e vinculos]: #criar-usuarios-grupos-vinculos-python

##  __Permissões aos grupos e listagem de pastas__ {#permissões-e-listagem-de-pastas}

Lembra que criamos os usuários e grupos de usuários? Então, estaremos realizando a primeira parte das permissões para os usuários criados, após essa etapa será realizado a preparação para os nomes das pastas.

Para adição de permissões, a função `m_aws.give_permissions_database()` receberá a conexão, o nome do banco de dados e nome do grupo.
A função `m_aws.get_folder()` pega a primeira parte do diretório da lista de objetos e armazena em `SCHEMAS_REDSHIFT`.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 6- Permissão Create para loaders, select para transformers no banco de dados
    m_aws.give_permissions_database(cur,redshift_db_name, groups_redshift)

    # 7- pegar o primeiro diretório e adiciona-lo a uma lista de schema.
    schemas_redshift = []
    schemas_redshift = m_aws.get_folder(list_objects)
    ```

??? info "code function give_permissions_database()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="111"
    def give_permissions_database(cur, redshift_db_name, groups):
        try:
            group_exception = ['reporters']
            groups_count = group_exception

            # Executando permissão por grupo não presente em 'groups_count'
            for group in groups.keys():
                if group not in groups_count:
                    cur.execute(f'''
                    grant create on database {redshift_db_name} to group {group};
                    grant select on all tables in schema information_schema to group {group};
                    grant select on all tables in schema pg_catalog to group {group};
                    ''')
                    groups_count.append(group)
        except Exception as e:
            logging.error(e)
            return False
    ```

??? info "code function get_folder()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="149"
    def get_folder(list_objects):
        # Criação da primeira parte do diretório como schema no banco de dados redshift
        try:       
            folders = []
            for folder in list_objects:
                folder = folder.split('/',1)[0]
                if (folder not in folders):
                    # Adiciona apenas as pastas diferentes
                    folders.append(folder.split('/',1)[0])
            return folders
        except Exception as e:
            logging.error(e)
            return False
        #print(folders)
    ```
    [Permissões e listagem de pastas]: #permissões-e-listagem-de-pastas


##  __Criação e Permissões para Schemas__ {#criação-e-permissões-para-schemas}

Nessa etapa criaremos os schemas e adicionaremos as permissões para os usuários do grupo 'transformers'.

A função `m_aws.create_schema_redshift()` cria os schemas com base nos diretórios armazenados em `schemas_redshift`.

Os Tranformadores precisam de acesso aos schemas criados, pois vão trabalhar com todas as tabelas existentes. A função `m_aws.give_permission_schemas()` visa permitir ao grupo selecionado tenha permissões, além de fazer com que o `redshift_db_user`
ganhe privilégios para as novas tabelas criadas.

=== ":octicons-file-code-16: `python\engdados\s3_redshift_load_files.py`"

    ``` python
    # 8- Criação dos schemas caso não exista
    m_aws.create_schema_redshift(cur, schemas_redshift, redshift_db_user)

    # 9- Permissão para o grupo transformers sobre os schemas criados
    m_aws.give_permission_schemas(cur, schemas_redshift, redshift_db_user, group_transformers)
    ```

??? info "code function create_schema_redshift()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="165"
    def create_schema_redshift(cur, folders, redshift_db_user):
        # Criação da primeira parte do diretório como schema no banco de dados redshift
        try:       
            for schema in folders:
                print('', "####### Comando executado: ##########", sep='\n')
                print(f'CREATE SCHEMA IF NOT EXISTS "{schema}" AUTHORIZATION {redshift_db_user};')
                cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}" AUTHORIZATION {redshift_db_user};') # vai criar a pasta entre "", exemplo: "c&a"
        except Exception as e:
            logging.error(e)
            return False
        return True
    ```

??? info "code function give_permission_schemas()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="130"
    def give_permission_schemas(cur, folders, redshift_db_user, group):
        try:
            for key, value in group.items():
                if value == 2:  # 'loaders':1, 'transformers':2, 'reporters':3

                    # Adicionando permissões apenas usuários do grupo 'transformers' e privilégios para um determinado user
                    for schema in folders:
                        cur.execute(f'''
                        grant usage on schema "{schema}" to group {key};
                        grant select on all tables in schema "{schema}" to group {key};
                        alter default privileges for user {redshift_db_user} in schema "{schema}"
                        grant select on tables to group {key};
                        ''')
            return True
        except Exception as e:
            logging.error(e)
            return False
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

??? info "code function csv_to_redshift()"
    === ":octicons-file-code-16: `python\engdados\mod_aws.py`"

    ``` python linenums="239"
    def csv_to_redshift(cur, s3, bucket_name, list_objects, redshift_details, redshift_db_name):
    # Reading the individual files from the AWS S3 buckets and putting them in dataframes
        redshift_iam_arn, redshift_secrete_name, redshift_region_name = redshift_details
        
        for file in list_objects:
            obj = s3.Object(bucket_name,file)
            data = obj.get()['Body'].read()
            # Identificando o delimitador
            delimiter_csv = csv_identify_delimiter(data.decode('utf-8'))

            # Leitura de csv
            csv_df = pd.read_csv(io.BytesIO(data), header = 0, delimiter = delimiter_csv, low_memory = False)
            columns_df = csv_df.columns
            print('', '####### Iniciando tratamento csv ... ##########', sep='\n')

            # resevando nomes dos schemas, tabelas e colunas
            schema = '"'+file.split('/')[0]+'"'
            table = file.split('/')[-1].lower()
            table = table.replace('.csv','').replace('.CSV','')
            print('','Tratamento de schema e tabela finalizado.', sep = '\n')
            print('', "Pasta para schema: ", schema,'',"Arquivo para tabela: ", table, sep = '\n')

            # Tratamento das colunas, identificação de datatype e length
            columns, columns_names = csv_column_dtype(csv_df, columns_df)

            # Criação das tabelas e colunas
            cur.execute(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{columns};")
            print('', "####### Comando executado: ##########", sep = '\n')
            print(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{columns};")

            # Copy CSV do S3 para o Redshift
            cur.execute(f"""
            copy {schema}.{table} {columns_names}
            from 's3://{bucket_name}/{file}' 
            iam_role '{redshift_iam_arn}'
            delimiter '{delimiter_csv}' 
            region '{redshift_region_name}'
            IGNOREHEADER 1
            DATEFORMAT AS 'YYYY-MM-DD HH:MI:SS'
            removequotes
            maxerror 3;
            """)

            print('',"Copy do Objeto Finalizado", sep='\n')
    ```

    [Criação das tabelas e copy]: #criação-e-permissões-para-schemas


## :material-format-list-checks: Check Objetivos

Os ícones :octicons-check-circle-fill-24:{ style="color: #00e676" } são os finalizados e os :octicons-check-circle-fill-24:{ style="color: var(--md-default-fg-color--lightest)" } são os em abertos.

- [x] [Pegar dados dos arquivos terraform.tfstate](#pegando-os-arquivos-tfstate)
- [x] [Pegar os arquivos csv's armazenados na amazom S3](#pegar-arquivos-armazenados-no-bucket-S3)
- [x] [Pegar dados armazenados no Secrets Manager](#pegar-dados-armazenados-no-secrets-manager)
- [x] [Criar usuários, grupos e vínculos](#criar-usuarios-grupos-vinculos-python)
- [x] [Permissões aos grupos e listagem de pastas](#permissões-e-listagem-de-pastas)
- [x] [Permissões e criação de schemas](#criação-e-permissões-para-schemas)
- [x] [Criação das tabelas e copy](#criação-de-tabelas-e-copys)
- [ ] Refatorar os módulos mod_aws e mod_terraform

