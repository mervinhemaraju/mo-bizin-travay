import os
from kink import di
from functools import wraps
from dopplersdk import DopplerSDK
from app.web.models.utils.constants import SECRETS_DS_CONFIG, SECRETS_DS_PROJECT_NAME
from slack_sdk import WebClient
from app.web.models.utils.constants import (
    SECRETS_CIM_CONFIG,
    SECRETS_CIM_PROJECT_NAME,
    SECRETS_CIM_SLACK_BOT_MAIN_TOKEN,
)


def main_injection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # * DI for os variables
        di["SECRETS_DATABASE_ACCESS_TOKEN"] = os.environ[
            "SECRETS_DATABASE_ACCESS_TOKEN"
        ]
        di["SECRETS_CLOUD_IAC_MAIN_TOKEN"] = os.environ["SECRETS_CLOUD_IAC_MAIN_TOKEN"]
        di["MONGO_API_BASE_URL"] = os.environ["MONGO_API_BASE_URL"]
        di["SLACK_CHANNEL_MAIN"] = os.environ["SLACK_CHANNEL_MAIN"]
        di["APP_SECRET_KEY"] = os.environ["APP_SECRET_KEY"]

        # * Secrets manager Doppler for database access
        doppler_database_access = DopplerSDK()
        doppler_database_access.set_access_token(di["SECRETS_DATABASE_ACCESS_TOKEN"])

        # * Secrets manager Doppler for database access
        doppler_cloud_iac = DopplerSDK()
        doppler_cloud_iac.set_access_token(di["SECRETS_CLOUD_IAC_MAIN_TOKEN"])

        # * Retrieve the database secrets
        database_secrets = doppler_database_access.secrets.list(
            project=SECRETS_DS_PROJECT_NAME, config=SECRETS_DS_CONFIG
        ).secrets

        # * Database variables
        di["api_base_url"] = di["MONGO_API_BASE_URL"]
        di["api_username"] = database_secrets["MONGO_MAIN_MBT_USERNAME"]["raw"]
        di["api_password"] = database_secrets["MONGO_MAIN_MBT_PASSWORD"]["raw"]

        # * Slack Sdk
        di["slack_wc"] = WebClient(
            token=doppler_cloud_iac.secrets.get(
                project=SECRETS_CIM_PROJECT_NAME,
                config=SECRETS_CIM_CONFIG,
                name=SECRETS_CIM_SLACK_BOT_MAIN_TOKEN,
            ).value["raw"]
        )

        return func(*args, **kwargs)

    return wrapper
