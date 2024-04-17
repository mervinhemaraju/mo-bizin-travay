import requests
import json
from kink import inject
from requests.auth import HTTPBasicAuth


@inject
class MongoAPI:
    def __init__(self, api_base_url, api_username, api_password):
        self.base_url = api_base_url
        self.headers = {"Content-Type": "application/json"}
        self.auth = HTTPBasicAuth(api_username, api_password)

    def save_all(self, documents: list[dict]):
        # Post the data
        return requests.post(
            url=f"{self.base_url}/save",
            headers=self.headers,
            data=json.dumps(
                {
                    "documents": documents,
                }
            ),
            auth=self.auth,
        ).json()

    def delete_by_source(self, opening_source):
        # Post the data
        response = requests.delete(
            url=f"{self.base_url}/delete",
            headers=self.headers,
            data=json.dumps(
                {
                    "query": {"opening_source": opening_source},
                }
            ),
            auth=self.auth,
        ).json()

        # return the deleted count
        return response["count"]
