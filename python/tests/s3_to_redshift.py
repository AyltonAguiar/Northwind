import boto3
import pandas as pd
import io
import json
import psycopg2
import logging

# Conexão ao Redshift
"""Accessing the S3 buckets using boto3 client"""
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')


# Variáveis para o Copy
delimiter = "';'"
iam_role = []
ignoreheader = '1'
dateformat = "'YYYY-MM-DD HH:MI:SS'"
region = 'us-east-1'


#######################
######  Funções  ######
#######################

def read_s3_backendHcl(patch):
# Capturar detalhes a partir do backend-engdados.hcl
    file_name = open(patch)
    s3_details_backend = json.load(file_name)

    global backend_bucket, backend_region, backend_key
    backend_bucket = s3_details_backend['backend']['config'].get('bucket')
    backend_region = s3_details_backend['backend']['config'].get('region')
    backend_key = s3_details_backend['backend']['config'].get('key')

    print('', "############ S3 Backend.Hcl ##########", s3_details_backend['backend']['config'], sep='\n')


def read_redshift_tfstate(patch):
    # Captura dos outputs criados no arquivo terraform.tfstate da pasta aws_redshift
    rd_terraform = open(patch)
    rd_terraform_json = json.load(rd_terraform)

    global redshift_iam_arn, redshift_secrete_name, redshift_region_name
    redshift_iam_arn = rd_terraform_json['outputs'].get('iam_role_arn').get('value')
    redshift_secrete_name = rd_terraform_json['outputs'].get('secrete_name').get('value')
    redshift_region_name = rd_terraform_json['outputs'].get('region_name').get('value')
    
    print('',"####### Outputs redshift.tfstate ##########",
          redshift_iam_arn, redshift_secrete_name, redshift_region_name, sep='\n')


def get_bucket():
    # Identificar bucket  remote state
    try:
        s3_object = s3_client.get_object(Bucket=backend_bucket, Key=backend_key)
        object_file = s3_object["Body"].read().decode()
        parsed_object = json.loads(object_file)
        global bucket_name
        bucket_name = parsed_object['outputs'].get('bucket-name').get('value')
        print('',"####### Bucket Name Object S3 ##########",bucket_name, sep='\n')

    except Exception as e:
        logging.error(e)
        return False
    return True


def s3_list_obj():
    # Lista os Objetos do bucket setado e armazena na variável s3_objects
    try:
        s3_list_obj = s3_client.list_objects(Bucket=bucket_name)
        
        global s3_objects
        s3_objects = []
        
        for obj in s3_list_obj['Contents']:
            if obj['Key'].endswith('csv') or obj['Key'].endswith('CSV'):
                s3_objects.append(obj['Key'])
        print('',"####### Objects S3 ##########",s3_objects[0:10], sep='\n')

    except Exception as e:
        logging.error(e)
        return False
    return True

def get_secrets_redshift():
    # Captura dos segredos do redshift na AWS Secrets
    client_secret = boto3.client('secretsmanager', region_name=redshift_region_name)
    get_secret_value_response = client_secret.get_secret_value(SecretId = redshift_secrete_name)
    secret_json = json.loads(get_secret_value_response['SecretString'])

    global redshift_db_name, redshift_db_user, redshift_db_password, redshift_db_port, redshift_db_host

    redshift_db_name= secret_json.get('data_base')
    redshift_db_user = secret_json.get('username')
    redshift_db_password = secret_json.get('password')
    redshift_db_port = secret_json.get('port')
    redshift_db_host = secret_json.get('host').split(':')[0] # acontece de ter ':5439' junto, então precisa tratar.

    print('',"####### Outputs Secrets Manager ##########",
          redshift_db_host, redshift_db_port, sep='\n')


def folder_to_schema():
    # Criação da primeira parte do diretório como schema no banco de dados redshift
    rd_con = psycopg2.connect(host=redshift_db_host, database=redshift_db_name,
                              user=redshift_db_user, password=redshift_db_password, port=redshift_db_port)
    rd_con.autocommit = True
    cur = rd_con.cursor()
    
    folders = []
    for folder in s3_objects:
        folder = folder.split('/',1)[0]
        if (folder not in folders):
            # Adiciona apenas as pastas diferentes
            folders.append(folder.split('/',1)[0])
            # Executa o script de create table
            print('', "####### Comando executado: ##########", sep='\n')
            print(f'CREATE SCHEMA IF NOT EXISTS "{folder}" AUTHORIZATION aylton;')
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{folder}" AUTHORIZATION aylton;') # vai criar a pasta entre "", exemplo: "c&a"
    rd_con.close()
    print(folders)


def object_to_redshift():
#Reading the individual files from the AWS S3 buckets and putting them in dataframes """
    rd_con = psycopg2.connect(host=redshift_db_host, database=redshift_db_name,
                              user=redshift_db_user, password=redshift_db_password, port=redshift_db_port)
    rd_con.autocommit = True
    cur = rd_con.cursor()

    for file in s3_objects[0:5]:
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
        for column_csv in csv_header:
            column.append(column_csv+' varchar(256)')   # ATENÇÃO: PODEMOS ADICIONAR COLUNAS ENTRE ASPAS CASO SEJA NECESSÁRIO
        column="("+', '.join(column)+")"
        print('','Tratamento de colunas finalizado.', sep='\n')
        print('', "Header_csv para Colunas:", column, sep='\n')

        # Criação das tabelas com colunas em text
        cur.execute(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{column};")
        print('', "####### Comando executado: ##########", sep='\n')
        print(f"CREATE TABLE IF NOT EXISTS {redshift_db_name}.{schema}.{table}{column};")

        # Copy CSV do S3 para o Redshift
        cur.execute(f"""
        copy {schema}.{table}
        from 's3://{bucket_name}/{file}' 
        iam_role '{redshift_iam_arn}'
        delimiter {delimiter} 
        region '{region}'
        IGNOREHEADER {ignoreheader}
        DATEFORMAT AS {dateformat}
        removequotes
        maxerror 10
        TRUNCATECOLUMNS;
        """)

        print('',"Copy do Objeto Finalizado", sep='\n')
        # O truncatecolumns é muito importante para truncar valores até o tamanho do varchar(256)
        # caso os dados na coluna excedam o varchar(256) e não estiver com o truncatecolumns o excute copy dará erro.
    rd_con.close()


#######################
######   Start   ######
#######################
# vou deixar 2 quebras de linha para eliminar confusões sobre comentário/código

## Lendo e capturando as informações de bucket, region, key
read_s3_backendHcl("C:/repositorio_estudos/engdados/northwind-eng/terraform/02_aws_s3_and_files/.terraform/terraform.tfstate")

## Lendo e capturando as informações de alguns outputs no arquivo do terraform.tfstate
read_redshift_tfstate("C:/repositorio_estudos/engdados/northwind-eng/terraform/03_aws_redshift/terraform.tfstate")

## Capturando nome do bucket com base no backend criado
get_bucket()

## Aqui vamos capturar os objetos(csv) com base no bucket identificado
s3_list_obj()

## Captura dos segredos do redshift na AWS Secrete (Criados lá no terraform)
get_secrets_redshift()

## Cria as pastas(primeira parte do diretório) como schemas no redshift
folder_to_schema()

## Nessa função vamos capturar todos o arquivos do bucket que estejam armazenados na variável S3_objects
object_to_redshift()
