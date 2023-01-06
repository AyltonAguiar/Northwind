import mod_terraform as m_tf
import mod_aws as m_aws
import boto3
import psycopg2

# Conexão ao Redshift
"""Accessing the S3 buckets using boto3 client"""
session = boto3.Session(profile_name='ayltonaguiar')
s3_client = session.client('s3')
s3 = session.resource('s3')

# Nome dos grupos
group_loaders = str('loaders_users')         # Os carregadores, pode ser Airbyte, Fivetran, stitch
group_transformers = str('dbt_users')         # Os transformadores
# group_reporters = str('bi_users')            # Os espectadores

# Variáveis Globais
SCHEMAS_REDSHIFT = []

# 1- Pega o caminho dos arquivos, valida e guarda as informações básicas em novas variáveis
path_s3 = m_tf.get_path_s3()
path_redshift = m_tf.get_path_redshift()
## 1.1- s3
backend_details = m_tf.read_s3_tfstate_backend(f"{path_s3}")
backend_bucket, backend_region, backend_key = backend_details
## 1.2- redshift
redshift_details = m_tf.read_redshift_tfstate(f"{path_redshift}")
redshift_iam_arn, redshift_secrete_name, redshift_region_name = redshift_details

# 2- seleciona o objeto do bucket/key fornecido e pega o valor do output 'bucket-name'
bucket_name = m_aws.get_bucket(s3_client, backend_bucket, backend_key)

# 3- Listagem de objetos do bucket fornecido
list_objects = m_aws.get_csv_s3(s3_client, bucket_name)

# 4- Acessando e pegando os valores guardados do Redshift no Secrets Manager
client_secret = session.client('secretsmanager', region_name=redshift_region_name)
secrets_manager_details= m_aws.get_secrets_redshift(client_secret, redshift_secrete_name)
redshift_db_name, redshift_db_user, redshift_db_password, redshift_db_port, redshift_db_host = secrets_manager_details

# 5- conexão ao banco
rd_con = psycopg2.connect(host=redshift_db_host, database=redshift_db_name,
                          user=redshift_db_user, password=redshift_db_password, port=redshift_db_port)
rd_con.autocommit = True
cur = rd_con.cursor()

# 6- Permissão Create para loaders, select para transformers no banco de dados
m_aws.give_permissions_database(cur,redshift_db_name, group_loaders, group_transformers)

# 7- pegar o primeiro diretório e adiciona-lo a uma lista de schema.
SCHEMAS_REDSHIFT = m_aws.get_folder(list_objects)
#print(SCHEMAS_REDSHIFT)

# 8- Criação dos schemas caso não exista
m_aws.create_schema_redshift(cur, SCHEMAS_REDSHIFT, redshift_db_user)

# 9- Permissão para os schemas criados
m_aws.give_permission_schemas(cur, SCHEMAS_REDSHIFT, redshift_db_user, group_transformers)

# 10- Criação das tabelas, colunas e copy
m_aws.csv_to_redshift(cur, s3, bucket_name, list_objects, redshift_details, redshift_db_name)

# 11- fechando conexão
rd_con.close()
