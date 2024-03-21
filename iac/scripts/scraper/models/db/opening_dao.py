from time import sleep
from kink import inject
from dynamodb_json import json_util as json
from models.db.opening import Opening


# * This is the DAO class for the Opening Table
@inject
class ItemDao:
    def __init__(self, boto_dynamodb, dynamodb_table) -> None:
        # * DB Connection
        self.db = boto_dynamodb

        # * Sets the table name the DB will operate on
        self.table = dynamodb_table

    def save_all(self, openings: list[Opening]):
        # Break the opening list into smaller chunks
        # to avoid exceeding the write limit
        chunks = [openings[i : i + 200] for i in range(0, len(openings), 200)]

        for chunk in chunks:
            with Opening.batch_write() as batch:
                for opening in chunk:
                    batch.save(opening)

            sleep(2)

    def delete_all(self, openings: list[Opening]):
        # Break the opening list into smaller chunks
        # to avoid exceeding the write limit
        chunks = [openings[i : i + 200] for i in range(0, len(openings), 200)]

        for chunk in chunks:
            with Opening.batch_write() as batch:
                for opening in chunk:
                    batch.delete(opening)

            sleep(2)

    def get_items_by_recruiter(self, recruiter) -> list[Opening]:
        # Queries the recruiter from GSI
        data = self.db.query(
            IndexName="recruiter_index",
            TableName=self.table,
            KeyConditionExpression="recruiter = :attr",
            ExpressionAttributeValues={":attr": {"S": recruiter}},
        )

        # Loads and format the items
        items = json.loads(data["Items"])

        # Converts the json to python objects
        return [Opening(**item) for item in items]

    def get_items_by_source(self, source) -> list[Opening]:
        # Queries the source from GSI
        data = self.db.query(
            IndexName="opening_source_index",
            TableName=self.table,
            KeyConditionExpression="opening_source = :attr",
            ExpressionAttributeValues={":attr": {"S": source}},
        )

        # Loads and format the items
        items = json.loads(data["Items"])

        # Converts the json to python objects
        return [Opening(**item) for item in items]
