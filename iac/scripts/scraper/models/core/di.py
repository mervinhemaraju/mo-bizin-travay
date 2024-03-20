import os
from kink import di
from functools import wraps
from boto3 import Session
from botocore.config import Config
from dopplersdk import DopplerSDK
from slack_sdk import WebClient
from utils.constants import (
    SECRETS_MAIN_PROJECT_NAME,
    SECRETS_MAIN_CONFIG,
    SECRETS_MAIN_SLACK_BOT_MAIN_TOKEN,
)


def main_injection(func):
    def __build_boto_client(client_name, config):
        return Session().client(service_name=client_name, config=config)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # * DI for os variables
        di["DELAY"] = os.environ["DELAY"]
        di["AWS_REGION"] = os.environ["AWS_REGION"]
        di["SECRETS_MAIN_TOKEN"] = os.environ["SECRETS_MAIN_TOKEN"]
        di["SLACK_CHANNEL"] = os.environ["SLACK_CHANNEL"]
        di["dynamodb_table"] = os.environ["DB_TABLE_NAME"]
        di["SOURCE"] = os.environ["SOURCE"]
        di["SOURCE_URL"] = os.environ["SOURCE_URL"]

        # * Boto3 variables
        di["boto_config"] = Config(region_name=di["AWS_REGION"], signature_version="v4")

        di["boto_dynamodb"] = __build_boto_client(
            client_name="dynamodb", config=di["boto_config"]
        )

        # * Secrets manager Doppler
        doppler = DopplerSDK()
        doppler.set_access_token(di["SECRETS_MAIN_TOKEN"])

        # * Get secrets
        secrets = doppler.secrets.get(
            project=SECRETS_MAIN_PROJECT_NAME,
            config=SECRETS_MAIN_CONFIG,
            name=SECRETS_MAIN_SLACK_BOT_MAIN_TOKEN,
        )

        # * Slack Sdk
        di["slack_wc"] = WebClient(token=secrets.value["raw"])

        return func(*args, **kwargs)

    return wrapper
