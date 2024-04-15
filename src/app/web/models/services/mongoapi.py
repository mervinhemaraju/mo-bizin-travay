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

    def get_paginated_data(self, query, page=1):
        # Create the query
        regex = {"$regex": query, "$options": "i"}  # case-insensitive
        query_filter = {"$or": [{"title": regex}, {"opening_source": regex}]}

        # Get the data
        response = requests.get(
            url=f"{self.base_url}/fetch/all",
            headers=self.headers,
            data=json.dumps(
                {
                    "query": query_filter,
                    "page": page,
                }
            ),
            auth=self.auth,
        ).json()

        # Return the details
        return response["data"], response["total_pages"], response["total_documents"]
