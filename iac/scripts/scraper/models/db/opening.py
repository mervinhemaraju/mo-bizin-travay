import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Opening(Model):
    """
    A DynamoDB Opening Table
    """

    class Meta:
        table_name = os.environ["DB_TABLE_NAME"]
        region = os.environ["AWS_REGION"]

    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    posted_date = UnicodeAttribute()
    closing_date = UnicodeAttribute()
    salary_range = UnicodeAttribute()
    location = UnicodeAttribute()
    recruiter = UnicodeAttribute()
    updated_at = UnicodeAttribute()
    source = UnicodeAttribute()

    def __str__(self) -> str:
        return str(vars(self))
