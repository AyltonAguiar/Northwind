from pathlib import Path
import mod_terraform as m_tf
import socket



# print(socket.gethostbyname(socket.gethostname()))
# import logging
# def tests(a,b):
#     try:
#         if a > b:
#             print(a)
#         elif a < b:
#             print(b)
#         return b
#     except Exception as e:
#         logging.error(e)
#         return False

# ret = tests(0,0)
# print(ret)

# Caminhos dos arquivos na pasta terraform
# path_s3 = Path().absolute().parent.parent.joinpath('terraform','02_aws_s3_and_files','.terraform','terraform.tfstate')
# path_redshift = Path().absolute().parent.parent.joinpath('terraform','03_aws_redshift','terraform.tfstate')

# path_s3 = Path(r'C:\repositorio_estudos\engdados\northwind-eng\terraform\02_aws_s3_and_files\.terraform\terraform.tfstate')
# m_tf.path_validate(path_s3, "path_s3")
path_s3 = m_tf.get_path_s3()
# path_redshift = m_tf.get_path_redshift()

# print(path_terraform)
print(path_s3)

# if path_s3.is_file() and path_redshift.is_file() is True:
#     print('Caminho terraform correto: ', path_s3, sep='\n')
# elif path_s3.is_file() or path_redshift.is_file() is False:
#     print('Arquivo não existe: ', path_s3, sep='\n')

# Pegando os Outputs do arquivo de backend.hcl
# backend_details = m_tf.read_s3_tfstate_backend(f"{path_s3}")
# backend_bucket, backend_region, backend_key = backend_details

# # Pegando os básicos Outputs do Redshift tfstate
# redshift_details = m_tf.read_redshift_tfstate(f"{path_redshift}")
# redshift_iam_arn, redshift_secrete_name, redshift_region_name = redshift_details
