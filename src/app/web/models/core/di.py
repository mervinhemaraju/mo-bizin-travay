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
        di["DB_HOST"] = os.environ["DB_HOST"]

        # * Secrets manager Doppler for database access
        doppler_database_access = DopplerSDK()
        doppler_database_access.set_access_token(di["SECRETS_DATABASE_ACCESS_TOKEN"])

        # * Retrieve the database secrets
        database_secrets = doppler_database_access.secrets.list(
            project=SECRETS_DS_PROJECT_NAME, config=SECRETS_DS_CONFIG
        ).secrets

        # * Database variables
        di["db_host"] = di["DB_HOST"]
        di["db_username"] = database_secrets["MONGO_MAIN_MBT_USERNAME"]["raw"]
        di["db_password"] = database_secrets["MONGO_MAIN_MBT_PASSWORD"]["raw"]
        di["db_ca_file"] = "/Users/mervin.hemaraju/Temp/ca.pem"
        di["db_cert_file"] = "/Users/mervin.hemaraju/Temp/mongod.pem"

        return func(*args, **kwargs)

    return wrapper
