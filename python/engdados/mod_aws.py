import json
import logging
import pandas as pd
import io
import logging


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


def get_secrets_redshift(client_secret, redshift_secrete_name):
    try:
        # Captura dos segredos do redshift na AWS Secrets
        get_secret_value_response = client_secret.get_secret_value(SecretId = redshift_secrete_name)
        secret_json = json.loads(get_secret_value_response['SecretString'])
      
    except Exception as e:
        logging.error(e)
        return False
    return secret_json


def get_credentials_redshift(secret_json):
    try:
        # Credenciais do Redshift
        redshift_db_name = secret_json.get('data_base')
        redshift_db_user = secret_json.get('username')
        redshift_db_password = secret_json.get('password')
        redshift_db_port = secret_json.get('port')
        redshift_db_host = secret_json.get('host').split(':')[0] # acontece de ter ':5439' junto, então precisa tratar.

        print('',"####### Outputs Secrets Manager ##########",
            redshift_db_host, redshift_db_port, sep='\n')
    except Exception as e:
        logging.error(e)
        return False
    return [redshift_db_name, redshift_db_user, redshift_db_password, redshift_db_port, redshift_db_host]


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


def csv_column_dtype(csv_dataframe, columns_dataframe):
    # Identify dtypes, length of columns
    # List of columns names
    try:
        columns = []
        columns_names = []

        for column_name in columns_dataframe:

            # tratamento dos nomes das colunas com espaço para '_'
            column_tratament = str(column_name).replace(' ', '_').lower()
            # reservando column type
            column_type = csv_dataframe[column_name].dtype
            # reservando apenas os nomes das colunas
            columns_names.append(column_tratament)

            if column_type == 'object':
                # reservando tamanho mãximo da coluna
                column_len = int(csv_dataframe[column_name].str.len().max())
                
                if column_len <= 255:
                    columns.append(f"{column_tratament} varchar({column_len})")
                elif column_len > 255:
                    columns.append(f"{column_tratament} varchar(max)")
            elif "int" in str(column_type):
                columns.append(f"{column_tratament} integer")
            elif "float" in str(column_type):
                columns.append(f"{column_tratament} float")
            else:
                columns.append(f"{column_tratament} varchar(255)")
        
        # junção das colunas reservadas
        columns = "("+', '.join(columns)+""",
            created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        columns_names = "("+', '.join(columns_names)+")"

        print('','Tratamento de colunas finalizado.', sep='\n')
        print('', "Header_csv para Colunas:", columns, sep='\n')
        #print('',columns_names, sep='\n')

        return columns, columns_names

    except Exception as e:
        logging.error(e)
        return False


def csv_identify_delimiter(csv_content):
    # Identificador de delimitador
    try:
        delimiters = [',', '|', '\t', ';']
        counts = {d: csv_content.count(d) for d in delimiters}
        delimiter = max(counts, key=counts.get)
        return delimiter

    except Exception as e:
        logging.error(e)
        return False


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
 