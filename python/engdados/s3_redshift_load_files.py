import mod_terraform as m_tf
import mod_aws as m_aws
import boto3
import psycopg2
import sys

# Conexão ao Redshift
session = boto3.Session(profile_name='ayltonaguiar')
s3_client = session.client('s3')
s3 = session.resource('s3')

# Nome dos grupos
groups_redshift = {'loaders':1, 'transformers':2, 'reporters':3}

# 1- Pega o diretório dos arquivos, valida e guarda as informações básicas em novas variáveis
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

# 4- Acessando Secrets Manager
client_secret = session.client('secretsmanager', region_name=redshift_region_name)
# 4.1 Pegando os valores guardados do Redshift no Secrets Manager
secrets_manager_json = m_aws.get_secrets_redshift(client_secret, redshift_secrete_name)
redshift_db_name, redshift_db_user, redshift_db_password, redshift_db_port, redshift_db_host = m_aws.get_credentials_redshift(secrets_manager_json)

# 5- conexão ao banco
rd_con = psycopg2.connect(host=redshift_db_host, database=redshift_db_name,
                          user=redshift_db_user, password=redshift_db_password, port=redshift_db_port)
rd_con.autocommit = True
cur = rd_con.cursor()
## 5.1 Criando os usuários dos grupos loaders, transformers e reporters
m_aws.create_users_redshift(cur, secrets_manager_json)
## 5.2 Apagando as informações do secrets
del secrets_manager_json

# 6- Permissão Create para loaders, select para transformers no banco de dados
m_aws.give_permissions_database(cur,redshift_db_name, groups_redshift)

# 7- pegar o primeiro diretório e adiciona-lo a uma lista de schema.
schemas_redshift = []
schemas_redshift = m_aws.get_folder(list_objects)

# 8- Criação dos schemas caso não exista
m_aws.create_schema_redshift(cur, schemas_redshift, redshift_db_user)

# 9- Permissão para o grupo transformers sobre os schemas criados
m_aws.give_permission_schemas(cur, schemas_redshift, redshift_db_user, groups_redshift)

# 10- Criação das tabelas, colunas e copy
m_aws.csv_to_redshift(cur, s3, bucket_name, list_objects, redshift_details, redshift_db_name)

# 11- fechando conexão
rd_con.close()
