import sys
import boto3
import json
import yaml
import click
import base64


@click.command()
@click.argument('environment')
@click.argument('secret_name')
def get_secret(environment, secret_name):
    """Provide the secret name"""
    #AWS Client Config
    endpoint_url = "https://secretsmanager.eu-west-1.amazonaws.com"
    region_name = "eu-west-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )
    
    #Retrive the secretDictionry 
    get_value = client.get_secret_value(
        SecretId=environment + "-" + secret_name
    )
    
    b = json.loads(get_value['SecretString'])
    c = {}
    for i, j in b.items():
        c[i.strip()] = j.strip()
        print(c)
    kube_file_data = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": secret_name}, 'data': c}
    with open(f"{secret_name}.yml", 'w') as yamlfile:
        yaml.dump(kube_file_data, yamlfile)


if __name__ == "__main__":
    # display help when no arguments passed.
    if len(sys.argv) == 1:
        get_secret.main(['--help'])
    else:
        get_secret()