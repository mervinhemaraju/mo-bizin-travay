import os
from kink import di
from functools import wraps
from dopplersdk import DopplerSDK
from app.web.models.utils.constants import SECRETS_DS_CONFIG, SECRETS_DS_PROJECT_NAME


def main_injection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # * DI for os variables
        di["SECRETS_DATABASE_ACCESS_TOKEN"] = os.environ[
            "SECRETS_DATABASE_ACCESS_TOKEN"
        ]
        di["MONGO_API_BASE_URL"] = os.environ["MONGO_API_BASE_URL"]

        # * Secrets manager Doppler for database access
        doppler_database_access = DopplerSDK()
        doppler_database_access.set_access_token(di["SECRETS_DATABASE_ACCESS_TOKEN"])

        # * Retrieve the database secrets
        database_secrets = doppler_database_access.secrets.list(
            project=SECRETS_DS_PROJECT_NAME, config=SECRETS_DS_CONFIG
        ).secrets

        # * Database variables
        di["api_base_url"] = di["MONGO_API_BASE_URL"]
        di["api_username"] = database_secrets["MONGO_MAIN_MBT_USERNAME"]["raw"]
        di["api_password"] = database_secrets["MONGO_MAIN_MBT_PASSWORD"]["raw"]

        return func(*args, **kwargs)

    return wrapper
