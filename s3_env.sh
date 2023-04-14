#! /bin/bash
AWS_ACCESS_KEY_ID=`vault kv get -field=AWS_ACCESS_KEY_ID onyxia-kv/projet-formiable/s3` && export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=`vault kv get -field=AWS_SECRET_ACCESS_KEY onyxia-kv/projet-formiable/s3` && export AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
export MLFLOW_S3_ENDPOINT_URL='https://minio.lab.sspcloud.fr'
