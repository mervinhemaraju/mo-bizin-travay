import os
from kink import di
from functools import wraps
from boto3 import Session
from botocore.config import Config


def main_injection(func):
    def __build_boto_client(client_name, config):
        return Session().client(service_name=client_name, config=config)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # * DI for os variables
        di["MAIN_URL"] = os.environ["MAIN_URL"]
        di["CAREERS_URL"] = os.environ["CAREERS_URL"]
        di["DELAY"] = os.environ["DELAY"]
        di["WRAPPER_FILTER"] = os.environ["WRAPPER_FILTER"]
        di["OPENINGS_FILTER"] = os.environ["OPENINGS_FILTER"]
        di["FILTERS_NAME"] = os.environ["FILTER_NAME"]
        di["FILTER_POSTED_DATE"] = os.environ["FILTER_POSTED_DATE"]
        di["FILTER_LINK"] = os.environ["FILTER_LINK"]
        di["FILTER_PAGINATION_BUTTON"] = os.environ["FILTER_PAGINATION_BUTTON"]
        di["RECRUITER"] = os.environ["RECRUITER"]
        di["AWS_REGION"] = os.environ["AWS_REGION"]
        di["dynamodb_table"] = os.environ["DB_TABLE_NAME"]

        # * Boto3 variables
        di["boto_config"] = Config(region_name=di["AWS_REGION"], signature_version="v4")

        di["boto_dynamodb"] = __build_boto_client(
            client_name="dynamodb", config=di["boto_config"]
        )

        return func(*args, **kwargs)

    return wrapper
