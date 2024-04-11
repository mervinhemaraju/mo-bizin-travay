import os
from kink import di
from functools import wraps
from boto3 import Session
from botocore.config import Config
from dopplersdk import DopplerSDK
from slack_sdk import WebClient
from utils.constants import (
    SECRETS_CIM_CONFIG,
    SECRETS_CIM_PROJECT_NAME,
    SECRETS_CIM_SLACK_BOT_MAIN_TOKEN,
    SECRETS_DS_CONFIG,
    SECRETS_DS_PROJECT_NAME,
    FILE_PATH_CERT_MONGOD,
    FILE_PATH_CERT_CA,
)


def main_injection(func):
    def __build_boto_client(client_name, config):
        return Session().client(service_name=client_name, config=config)

    def create_certificate_file(content, file_location):
        with open(file_location, "w") as file:
            file.write(content)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # * Statics
        # * DI for os variables
        di["DELAY"] = os.environ["DELAY"]
        di["AWS_REGION"] = os.environ["AWS_REGION"]
        di["SECRETS_CLOUD_IAC_TOKEN"] = os.environ["SECRETS_CLOUD_IAC_TOKEN"]
        di["SECRETS_DATABASE_ACCESS_TOKEN"] = os.environ[
            "SECRETS_DATABASE_ACCESS_TOKEN"
        ]
        di["DB_HOST"] = os.environ["DB_HOST"]
        di["SLACK_CHANNEL"] = os.environ["SLACK_CHANNEL"]
        di["SOURCE"] = os.environ["SOURCE"]
        di["SOURCE_URL"] = os.environ["SOURCE_URL"]
        di["STARTUP_URL"] = os.environ["STARTUP_URL"]
        di["DOMAIN"] = os.environ["DOMAIN"]

        # * Boto3 variables
        di["boto_config"] = Config(region_name=di["AWS_REGION"], signature_version="v4")

        di["boto_dynamodb"] = __build_boto_client(
            client_name="dynamodb", config=di["boto_config"]
        )

        # * Secrets manager Doppler for cloud IAC
        doppler_cloud_iac = DopplerSDK()
        doppler_cloud_iac.set_access_token(di["SECRETS_CLOUD_IAC_TOKEN"])

        # * Secrets manager Doppler for database access
        doppler_database_access = DopplerSDK()
        doppler_database_access.set_access_token(di["SECRETS_DATABASE_ACCESS_TOKEN"])

        # * Retrieve the database secrets
        database_secrets = doppler_database_access.secrets.list(
            project=SECRETS_DS_PROJECT_NAME, config=SECRETS_DS_CONFIG
        ).secrets

        # * Slack Sdk
        di["slack_wc"] = WebClient(
            token=doppler_cloud_iac.secrets.get(
                project=SECRETS_CIM_PROJECT_NAME,
                config=SECRETS_CIM_CONFIG,
                name=SECRETS_CIM_SLACK_BOT_MAIN_TOKEN,
            ).value["raw"]
        )

        # * Create the ca file
        create_certificate_file(
            content=database_secrets["MONGO_CERT_CA"]["raw"],
            file_location=FILE_PATH_CERT_CA,
        )

        # * Create the mongod file
        create_certificate_file(
            content=database_secrets["MONGO_CERT_MONGOD"]["raw"],
            file_location=FILE_PATH_CERT_MONGOD,
        )

        # * Database variables
        di["db_host"] = di["DB_HOST"]
        di["db_username"] = database_secrets["MONGO_MAIN_MBT_USERNAME"]["raw"]
        di["db_password"] = database_secrets["MONGO_MAIN_MBT_PASSWORD"]["raw"]
        di["db_ca_file"] = FILE_PATH_CERT_CA
        di["db_cert_file"] = FILE_PATH_CERT_MONGOD

        return func(*args, **kwargs)

    return wrapper
