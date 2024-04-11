from pymongo import MongoClient
from kink import inject
from datetime import datetime


@inject
class Dao:
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

    def save_all(self, documents: list[dict]):
        self.collection.insert_many(documents)

    def delete_by_source(self, opening_source):
        # Delete documents for the specified source
        result = self.collection.delete_many({"opening_source": opening_source})

        return result.deleted_count

    def fetch_by_recruiter(self, recruiter_name):
        # Retrieve documents for the specified recruiter
        documents = self.collection.find({"recruiter": recruiter_name})

        # Return the list
        return list(documents)

    def fetch_by_source(self, opening_source):
        # Retrieve documents for the specified source
        documents = self.collection.find({"opening_source": opening_source})

        # Return the list
        return list(documents)
