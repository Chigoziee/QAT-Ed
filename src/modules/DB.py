import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()


class DynamoDBTable:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.client("dynamodb")
        self.table = table_name

    # ---------- Write ----------
    def write(self, item: dict) -> None:
        self.dynamodb.put_item(TableName=self.table, Item=item)

    # ---------- Read ----------
    def read(self, key: dict) -> dict | None:
        try:
            response = self.dynamodb.get_item(TableName=self.table, Key=key)
        except ClientError as exc:
            raise RuntimeError(f"DynamoDB get_item failed: {exc}") from exc

        return response.get("Item")