from pymongo import MongoClient
from kink import inject


@inject
class Dao:
    # Pagination
    PER_PAGE = 10

    def __init__(
        self, db_host, db_username, db_password, db_ca_file, db_cert_file
    ) -> None:
        # Create a mongodb connection
        mongo = MongoClient(
            host=db_host,
            tls=True,
            tlsAllowInvalidCertificates=False,
            tlsCAFile=db_ca_file,
            tlsCertificateKeyFile=db_cert_file,
            username=db_username,
            password=db_password,
        )

        # Retrieve the mbt db
        db = mongo["mo-bizin-travay"]

        # Retrieve the collection openings
        self.collection = db["openings"]

        # Create a text index on the title and opening source fields
        self.collection.create_index([("title", "text"), ("opening_source", "text")])

    def get_paginated_data(self, page, query):
        skip = (page - 1) * self.PER_PAGE
        regex = {"$regex": query, "$options": "i"}  # case-insensitive
        data = (
            # self.collection.find({"$text": {"$search": f"/.*{query}/"}})
            # self.collection.find({"title": {"$regex": query}})
            self.collection.find({"$or": [{"title": regex}, {"opening_source": regex}]})
            .skip(skip)
            .limit(self.PER_PAGE)
        )
        return list(data)
