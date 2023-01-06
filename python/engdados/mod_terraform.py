import json
import logging
from pathlib import Path
import sys

def path_validate(path, name):
    # Validação do arquivo informado no path, se existe ou não(True or False)
    if path.is_file() is True:
        print(f'Arquivo válido do "{name}": ', path)
    elif path.is_file() is False:
        sys.exit('Arquivo não válido: não identificado, verificar o caminho descrito ou se o arquivo existe')

def get_path_s3():
    # captura do arquivo terraform.state
    path_s3_tfstate = Path().absolute().parent.parent.joinpath('terraform','02_aws_s3_and_files','.terraform','terraform.tfstate')
    # validação do path
    path_validate(path_s3_tfstate, get_path_s3.__name__)
    return path_s3_tfstate

def get_path_redshift():
    # captura do arquivo terraform.state
    path_redshift_tfstate = Path().absolute().parent.parent.joinpath('terraform','03_aws_redshift','terraform.tfstate')
    # validação do path
    path_validate(path_redshift_tfstate, get_path_redshift.__name__)
    return path_redshift_tfstate

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
