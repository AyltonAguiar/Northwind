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

        redshift_db_name= secret_json.get('data_base')
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


def give_permissions_database(cur,redshift_db_name, group_loaders, group_transformers):
    # Permissão para loaders e transformers
    cur.execute(f'''
    grant create on database {redshift_db_name} to group {group_loaders};
    grant create on database {redshift_db_name} to group {group_transformers};
    grant select on all tables in schema information_schema to group {group_loaders};
    grant select on all tables in schema pg_catalog to group {group_loaders};
    grant select on all tables in schema information_schema to group {group_transformers};
    grant select on all tables in schema pg_catalog to group {group_transformers};
    ''')

def give_permission_schemas(cur, folders, redshift_db_user, group):
    try:
    # permissão para as tabelas criadas
    # Adicionando as permissões USAGE, SELECT
        for schema in folders:
            cur.execute(f'''
            grant usage on schema "{schema}" to group {group};
            grant select on all tables in schema "{schema}" to group {group};
            alter default privileges for user {redshift_db_user} in schema "{schema}"
            grant select on tables to group {group};
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
            # Executa o script de create table
            print('', "####### Comando executado: ##########", sep='\n')
            print(f'CREATE SCHEMA IF NOT EXISTS "{schema}" AUTHORIZATION {redshift_db_user};')
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}" AUTHORIZATION {redshift_db_user};') # vai criar a pasta entre "", exemplo: "c&a"
    except Exception as e:
        logging.error(e)
        return False
    return True

def csv_to_redshift(cur, s3, bucket_name, list_objects, redshift_details, redshift_db_name):
#Reading the individual files from the AWS S3 buckets and putting them in dataframes """
    # 
    redshift_iam_arn, redshift_secrete_name, redshift_region_name = redshift_details

    for file in list_objects:
        obj = s3.Object(bucket_name,file)
        data=obj.get()['Body'].read()
        csv_file = pd.read_csv(io.BytesIO(data), header=0, delimiter=";", low_memory=False)
        csv_header = list(csv_file.columns)
        
        print('', '####### Iniciando tratamento csv ... ##########', sep='\n')
    
        # criação do schema, tabela e colunas em text
        schema = '"'+file.split('/')[0]+'"'
        table = file.split('/')[-1].lower()
        table = table.replace('.csv','').replace('.CSV','')
        print('','Tratamento de schema e tabela finalizado.', sep='\n')
        print('', "Pasta para schema: ", schema,'',"Arquivo para tabela: ", table, sep='\n')

        # Criação das colunas com data type varchar(256)
        column = []
        column_origin = [] #Somente as colunas sem datatype
        for column_csv in csv_header:
            # podemos usar varchar(max)
            # ATENÇÃO: PODEMOS ADICIONAR COLUNAS ENTRE ASPAS CASO SEJA NECESSÁRIO
            column.append(column_csv+' varchar(max)')
            column_origin.append(column_csv)

        column="("+', '.join(column)+""",
         created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
          updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        
        column_origin="("+', '.join(column_origin)+")"
        print('','Tratamento de colunas finalizado.', sep='\n')
        print('', "Header_csv para Colunas:", column, sep='\n')

        # Criação das tabelas com colunas em text
        cur.execute(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{column};")
        print('', "####### Comando executado: ##########", sep='\n')
        print(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{column};")

        # Copy CSV do S3 para o Redshift
        cur.execute(f"""
        copy {schema}.{table} {column_origin}
        from 's3://{bucket_name}/{file}' 
        iam_role '{redshift_iam_arn}'
        delimiter ';' 
        region '{redshift_region_name}'
        IGNOREHEADER 1
        DATEFORMAT AS 'YYYY-MM-DD HH:MI:SS'
        removequotes
        maxerror 3;
        """)

        print('',"Copy do Objeto Finalizado", sep='\n')
        # O truncatecolumns é muito importante para truncar valores até o tamanho do varchar(256)
        # caso os dados na coluna excedam o varchar(256) e não estiver com o truncatecolumns o excute copy dará erro.
