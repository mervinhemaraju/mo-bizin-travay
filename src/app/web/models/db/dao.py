from pymongo import MongoClient


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

    def get_paginated_data(self, page):
        skip = (page - 1) * self.PER_PAGE
        data = self.collection.find().skip(skip).limit(self.PER_PAGE)
        return list(data)
