from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from kink import di


class Opening(Model):
    """
    A DynamoDB Opening Table
    """

    class Meta:
        table_name = di["DB_TABLE_NAME"]
        region = di["AWS_REGION"]

    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    posted_date = UnicodeAttribute()
    recruiter = UnicodeAttribute()
    updated_at = UnicodeAttribute()
